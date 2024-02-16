from src.imessage_reader import fetch_data
import imessage
import time
import openai
import os
import json
import argparse
import logging
from autoresponder.models import AutoRespondConfig
# from generator import EmojipastaGenerator
from emojipasta.generator import EmojipastaGenerator

HOME = os.path.expanduser('~')
DND_STATE_PATH = f'{HOME}/Library/DoNotDisturb/DB/Assertions.json'
DND_READABLE_PATH = f'{HOME}/Library/DoNotDisturb/DB/ModeConfigurations.json'
client = openai.Client()

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='./src/configs/autoresponder.config.json',
                    help='pass the file path to your keyfile')

cl_args = parser.parse_args()

try:
    with open(cl_args.config) as json_file:
        config = AutoRespondConfig(**json.load(json_file))
except Exception as exc:
    print(
        f'ERROR: check config file - something is broken.{Exception=} {exc=}. Exiting...')
    exit(1)


def generate_response(text_message: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'user',
                'content': text_message
            }
        ],
        max_tokens=1000,
        temperature=0
    )
    return resp.choices[0].message.content


def get_focus_mode() -> str:
    try:
        with open(DND_STATE_PATH, 'r') as dnd_state_file, open(DND_READABLE_PATH, 'r') as dnd_readable_file:
            dnd_state = json.load(dnd_state_file)
            modeid = dnd_state['data'][0]['storeAssertionRecords'][0]['assertionDetails']['assertionDetailsModeIdentifier']
            config = json.load(dnd_readable_file)
            focus = config['data'][0]['modeConfigurations'][modeid]['mode']['name']
            return focus
    except:
        return ''



def main():
    logging.debug(f'starting autoresponder with {config=}')
    fd = fetch_data.FetchData()
    emoji_generator = EmojipastaGenerator.of_default_mappings()

    while True:
        focus_mode = get_focus_mode()

        if config.only_respond_during_focus_mode and not focus_mode:
            logging.debug(f'focus mode is off, skipping...')
            time.sleep(config.delay_between_loops)
            continue

        logging.debug(f'starting loop: ')
        
        start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - config.delay_between_loops))
        msgs = fd.get_messages_between_dates(date_start = start_time)
        if not msgs:
            logging.debug(f'\tno messages found')
        
        for msg in msgs:

            logging.debug(f'\tchecking message: {msg.text}')
            if msg.is_from_me == 1:
                logging.debug(f'\t\tis from me, skipping...')
                continue

            gpt_prompt = f'You\'re being used as an autoresponder for Silas. Currently he is in {focus_mode} mode so he\'s not seeing the message and need you to generate the response for him. Please use the message history to tailor a custom response. Include a fun fact based on text history. Also inform the recipient what focous mode he is in. The message history is below:\n\n'
            message_history = fd.get_messages_from(msg.user_id)
            message_history_str = 'Message History:\n'
            for i, text in enumerate(message_history):
                if i > 10:
                    break
                content = text.text
                direction = 'me' if text.is_from_me == 1 else 'friend'
                message_history_str += f'{direction}: {content}\n'

            gpt_prompt += message_history_str
            gpt_prompt += f'\n\nMessage to respond to:\n{msg.text}'

            
            resp = generate_response(gpt_prompt)
            if config.emoji_pasta:
                resp = emoji_generator.generate_emojipasta(resp)
            logging.debug(f'\tResponse Generated: {resp}')
            
            # this is the line that's broken, 
            # need to figure out how to get the proper response
            # currently this wont respond to group chats. 
            # if you wanted to respond to a group chat, you'd need this format. 
            # imessage.send([num1, num2, num3], resp)
            imessage.send([msg.user_id], resp)

        logging.debug(f'\tsleeping for {config.delay_between_loops} seconds...')
        time.sleep(config.delay_between_loops)

if __name__ == "__main__":
    main()