import argparse
import json
import os
import sys

from autoresponder import logger
from autoresponder import Configuration
from autoresponder import AutoResponder

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    DEFAULT_CONFIG_LOCATION = f'{os.path.dirname(os.path.realpath(__file__))}/config.json'
else:
    DEFAULT_CONFIG_LOCATION = f'{os.path.dirname(os.path.realpath(__file__))}/configs/config.json'

_parser = argparse.ArgumentParser(
    description='Configuration details for the autoresponder')
_parser.add_argument(
    '--config', '-C', help='Path to the configuration file (JSON format)', default=DEFAULT_CONFIG_LOCATION)
_args = _parser.parse_args()

try:
    with open(_args.config, 'r') as config_file:
        logger.info(f'Loading configuration from {_args.config}')
        config_data = config_file.read()
        config = Configuration.from_json(config_data)
except FileNotFoundError:
    logger.error(f'Configuration file not found at: {_args.config}')
except json.JSONDecodeError as e:
    logger.error(f'Could not properly parse {_args.config}: {e}')

autoresponder = AutoResponder(config=config, logger=logger)
autoresponder.run()
