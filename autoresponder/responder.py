from .models import Configuration, SingleChat, GroupChat, DefaultSingleChat
from imessage_reader.fetch_data import FetchData
from imessage_reader.data_container import MessageData
from emojipasta import Emojipasta


import imessage

import openai

import json
import os
import logging
import sched
import time

_home = os.path.expanduser('~')
_dnd_state_path = f'{_home}/Library/DoNotDisturb/DB/Assertions.json'
_dnd_readable_path = f'{_home}/Library/DoNotDisturb/DB/ModeConfigurations.json'

class AutoResponder:
    def __init__(self, config: Configuration, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.fetch_data = FetchData()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.client = openai.Client(api_key=self.config.openai_api_key)
        self.emojipasta_generator = Emojipasta.of_default_mappings()
        
    def _get_focus_mode(self) -> str | None:
        try:
            with open(_dnd_state_path, 'r') as dnd_state_file, open(_dnd_readable_path, 'r') as dnd_readable_file:
                dnd_state = json.load(dnd_state_file)
                mode_id = dnd_state['data'][0]['storeAssertionRecords'][0]['assertionDetails']['assertionDetailsModeIdentifier']
                config = json.load(dnd_readable_file)
                focus = config['data'][0]['modeConfigurations'][mode_id]['mode']['name']
                return focus
        except:
            return None
        
    def _build_text_chain_single_chat(self, message: MessageData, single_chat: SingleChat) -> str:
        previous_messages = 0 if not single_chat.context else single_chat.number_previous_messages
        history = self.fetch_data.get_messages_from(single_chat.phone_number, previous_messages + 1)
        prompt = f'{single_chat.prompt}\n'
        for text in reversed(history):
            person = self.config.personal_info.name if text.is_from_me else single_chat.name
            prompt += f'{person}: {text.text}\n'
        self.logger.debug(f'Request generated for {single_chat.name}: {prompt}')
        return prompt
    
    def _build_text_chain_group_chat(self, message: MessageData, group_chat: GroupChat) -> str:
        previous_messages = 0 if not group_chat.context else group_chat.number_previous_messages
        history = self.fetch_data.get_messages_from(message.user_id, previous_messages + 1)
        prompt = f'{group_chat.prompt}\n'
        phone_number_to_name = { contact.phone_number: contact.name for contact in group_chat.recipients }
        for text in reversed(history):
            if text.is_from_me:
                person = self.config.personal_info.name
            elif text.phone_number in phone_number_to_name:
                person = phone_number_to_name[text.phone_number]
            else:
                person = 'N/A'
            prompt += f'{person}: {text.text}\n'
        self.logger.debug(f'Request generated for {group_chat.name}: {prompt}')
        return prompt
    
    def _build_text_chain_default_single_chat(self, message: MessageData, chat: DefaultSingleChat) -> str:
        previous_messages = 0 if not chat.context else chat.number_previous_messages
        history = self.fetch_data.get_messages_from(message.user_id, previous_messages + 1)
        prompt = f'{chat.prompt}\n'
        for text in reversed(history):
            person = self.config.personal_info.name if text.is_from_me else 'Them'
            prompt += f'{person}: {text.text}'
        self.logger.debug(f'Request generated for {message.user_id}: {prompt}')
        return prompt
    
    def _generate_response(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model='gpt-4',
            messages=[{
                'role': 'user',
                'content': message
            }],
            max_tokens=self.config.max_tokens,
            temperature=0,
        )
        return response.choices[0].message.content
    
    def _handle_response(self) -> None:
        focus_mode = self._get_focus_mode()
        messages = self.fetch_data.get_messages_between_dates(
            time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - self.config.delay_between_loops)))
        messages_from_me = filter(lambda message: message.is_from_me == 1, messages)
        messages_from_others = filter(lambda message: message.is_from_me != 1, messages)
        
        # Messages from me
        for message in messages_from_me:
            single_chat = [ chat for chat in self.config.single_chats if message.user_id == chat.phone_number ]
            group_chat = [ chat for chat in self.config.group_chats if message.user_id == chat.name ]
            if single_chat and single_chat[0].enabled and single_chat[0].bot_trigger_command != '' and single_chat[0].bot_trigger_command in message.text:
                message.text = message.text.replace(single_chat[0].bot_trigger_command, '')
                prompt = self._build_text_chain_single_chat(message, single_chat[0])
                response = self._generate_response(prompt)
                if single_chat[0].emoji_pasta:
                    response = self.emojipasta_generator.generate_emojipasta(response)
                
                self.logger.debug(f'Response generated for {single_chat[0].name}: {response}')
                imessage.send([message.user_id], response)
            elif group_chat and group_chat[0].enabled and group_chat[0].bot_trigger_command != '' and group_chat[0].bot_trigger_command in message.text:
                message.text = message.text.replace(group_chat[0].bot_trigger_command, '')
                prompt = self._build_text_chain_group_chat(message, group_chat[0])
                response = self._generate_response(prompt)
                if group_chat[0].emoji_pasta:
                    response = self.emojipasta_generator.generate_emojipasta(response)
                
                self.logger.debug(f'Response generated for {group_chat[0].name}: {response}')
                recipients = [recipient.phone_number for recipient in group_chat[0].recipients]
                imessage.send(recipients, response)
            elif not single_chat and not group_chat and self.config.default_single_chat.enabled and self.config.default_single_chat.bot_trigger_command in message.text:
                message.text = message.text.replace(self.config.default_single_chat.bot_trigger_command, '')
                prompt = self._build_text_chain_default_single_chat(message, self.config.default_single_chat)
                response = self._generate_response(prompt)
                if self.config.default_single_chat.emoji_pasta:
                    response = self.emojipasta_generator.generate_emojipasta(response)
                self.logger.debug(f'Response generated for {message.user_id}: {response}')
                imessage.send([message.user_id], response)

        # Messages from others
        for message in messages_from_others:
            self.logger.debug(f'Message: {message}')
            # IMPORTANT:
            # Single chats are identified by phone number. Group chats are identified by the group name
            single_chat = [ chat for chat in self.config.single_chats if message.user_id == chat.phone_number ]
            group_chat = [ chat for chat in self.config.group_chats if message.user_id == chat.name ]
            if single_chat and single_chat[0].enabled and single_chat[0].bot_trigger_command in message.text:
                message.text = message.text.replace(single_chat[0].bot_trigger_command, '')
                prompt = self._build_text_chain_single_chat(message, single_chat[0])
                response = self._generate_response(prompt)
                if single_chat[0].emoji_pasta:
                    response = self.emojipasta_generator.generate_emojipasta(response)

                self.logger.debug(f'Response generated for {single_chat[0].name}: {response}')
                imessage.send([message.user_id], response) 
            elif group_chat and group_chat[0].enabled and group_chat[0].bot_trigger_command in message.text:
                message.text = message.text.replace(group_chat[0].bot_trigger_command, '')
                prompt = self._build_text_chain_group_chat(message, group_chat[0])
                response = self._generate_response(prompt)
                if group_chat[0].emoji_pasta:
                    response = self.emojipasta_generator.generate_emojipasta(response)
                self.logger.debug(f'Response generated for {group_chat[0].name}: {response}')
                recipients = [recipient.phone_number for recipient in group_chat[0].recipients]
                imessage.send(recipients, response)
            elif not single_chat and not group_chat and self.config.default_single_chat.enabled and self.config.default_single_chat.bot_trigger_command in message.text:
                message.text = message.text.replace(self.config.default_single_chat.bot_trigger_command, '')
                prompt = self._build_text_chain_default_single_chat(message, self.config.default_single_chat)
                response = self._generate_response(prompt)
                if self.config.default_single_chat.emoji_pasta:
                    response = self.emojipasta_generator.generate_emojipasta(response)
                self.logger.debug(f'Response generated for {message.user_id}: {response}')
                imessage.send([message.user_id], response)
        
        self.scheduler.enter(self.config.delay_between_loops, 1, self._handle_response, ())
    
    def run(self):
        self.scheduler.enter(self.config.delay_between_loops, 1, self._handle_response, ())
        self.scheduler.run()
        