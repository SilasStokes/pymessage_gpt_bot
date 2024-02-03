from .models import Configuration, SingleChat
from imessage_reader.fetch_data import FetchData
from imessage_reader.data_container import MessageData
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
        
    def _build_text_chain_single_chat(self, message: MessageData, single_chat: SingleChat):
        history = self.fetch_data.get_messages_from(single_chat.phone_number, single_chat.number_previous_messages)
        prompt = single_chat.prompt
        newest_message = message.text
        prompt += '\n'
        for text in reversed(history):
            if not single_chat.context:
                break
            person = self.config.personal_info.name if text.is_from_me else single_chat.name
            prompt += f'{person}: {text.text}\n'
                
        prompt += f'Reply to this: {newest_message}'
        self.logger.debug(f'Request generated for {single_chat.name}: {prompt}')
        return prompt
    
    def _generate_response(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role': 'user',
                'content': message
            }],
            max_tokens=self.config.max_tokens,
            temperature=0,
        )
        return response.choices[0].message.content
    
    def _handle_response(self):
        focus_mode = self._get_focus_mode()
        messages = self.fetch_data.get_messages_between_dates(
            time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - self.config.delay_between_loops)))
        messages = filter(lambda message: message.is_from_me != 1, messages)

        for message in messages:
            self.logger.debug(f'Message: {message}')
            
            # IMPORTANT:
            # Single chats are identified by phone number. Group chats are identified by the group name
            single_chat = [ chat for chat in self.config.single_chats if message.user_id == chat.phone_number ]
            group_chat = [ chat for chat in self.config.group_chats if message.user_id == chat.name ]
            if single_chat:
                prompt = self._build_text_chain_single_chat(message, single_chat[0])
                response = self._generate_response(prompt)
                self.logger.debug(f'Response generated for {single_chat[0].name}: {response}')
                imessage.send([message.user_id], response) 
            elif group_chat:
                pass
            elif self.config.default_single_chat:
                pass
         
        self.scheduler.enter(self.config.delay_between_loops, 1, self._handle_response, ())
    
    def run(self):
        self.scheduler.enter(self.config.delay_between_loops, 1, self._handle_response, ())
        self.scheduler.run()
        