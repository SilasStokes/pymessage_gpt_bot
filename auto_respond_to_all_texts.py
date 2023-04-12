from imessage_reader import fetch_data
import imessage
import time
import openai
import os
import json
import argparse
import logging
from src.models import AutoRespondConfig
# from generator import EmojipastaGenerator
from emojipasta.generator import EmojipastaGenerator

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
    resp = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'{config.gptprompt}\n{text_message}',
        max_tokens=1000,
        temperature=0
    )
    return f'{resp.choices[0].text.strip()}'


def main():
    logging.debug(f'starting autoresponder with {config=}')
    fd = fetch_data.FetchData()
    emoji_generator = EmojipastaGenerator.of_default_mappings()

    while True:
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

            
            resp = generate_response(msg.text)
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