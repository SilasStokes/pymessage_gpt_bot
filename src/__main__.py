import argparse
import json

from autoresponder.logger import logger
from autoresponder.models import Configuration
from autoresponder.responder import AutoResponder

_parser = argparse.ArgumentParser(description='Configuration details for the autoresponder')
_parser.add_argument('--config', '-C', required=True, help='Path to the configuration file (JSON format)')
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