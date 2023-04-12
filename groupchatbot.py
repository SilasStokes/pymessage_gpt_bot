from imessage_reader import fetch_data
import imessage
import time
import openai
import argparse
import json
import logging
from src.models import GroupchatConfig

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='./src/configs/groupchat.config.json',
                    help='pass the file path to your groupchat config file.')

cl_args = parser.parse_args()

try:
    with open(cl_args.config) as json_file:
        config = GroupchatConfig(**json.load(json_file))
except Exception as exc:
    print(
        f'ERROR: check config file - something is broken.{Exception=} {exc=}. Exiting...')
    exit(1)

def get_gpt_response(command: str) -> str:
    resp = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'{config.gptprompt}\n{command}',
        max_tokens=1000,
        temperature=0
    )
    return f'{resp.choices[0].text.strip()}'


def main():
    fd = fetch_data.FetchData()
    while True:
        logging.debug(f'starting loop: ')
        start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - config.delay_between_loops))
        msgs = fd.get_messages_between_dates(date_start = start_time)

        if not msgs:
            logging.debug(f'\tno messages found')
        for msg in msgs:
            logging.debug(f'\tchecking message {msg.text}')
            if '!bot' not in msg.text or msg.user_id != config.groupchat_name:
                logging.debug(f'\t\tis not a command for the bot, skipping...')
                continue

            msg.text = msg.text.replace('!bot', '').strip()
            logging.debug(f'command received for bot: {msg.text}')

            resp = get_gpt_response(msg.text)
            resp = f'bot: {resp}'

            imessage.send(config.groupchat_recipients, resp)

        logging.debug(f'\tsleeping for {config.delay_between_loops} seconds...')
        time.sleep(config.delay_between_loops)

if __name__ == "__main__":
    main()
