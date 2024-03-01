import openai
import json
from src.autoresponder import Configuration
from .setup_model import SetupCheckBase

class CheckOpenaiKey(SetupCheckBase):

    def _check_setup(self):
        try:
            with open(self.config_path, 'r') as config_file:
                config_data = config_file.read()
                config = Configuration.from_json(config_data)
        except FileNotFoundError:
            return False, f"Configuration at {self.config_path} not found..."
        except json.JSONDecodeError as e:
            return False, f"Could not properly parse {self.config_path}: {e}"

        if len(config.openai_api_key) == 0:
            return False, "no openai api key supplied"

        client = openai.OpenAI(api_key=config.openai_api_key)
        try:
            client.models.list()
        except openai.AuthenticationError:
            return False, "could not authenticate with supplied openai key"
        except Exception as e:
            return False, f"Failed doing test connection to openai. Error: {e}"
        return True, ""


    def __init__(self, config_path: str):
        self.config_path = config_path
        self.check_name = "Verifying iMessage Database Access"
        self.instructions = ""
        self.success, self.error_reason = self._check_setup()

