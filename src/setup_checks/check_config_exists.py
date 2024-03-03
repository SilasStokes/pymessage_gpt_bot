
from .setup_model import SetupCheckBase

class CheckConfigExists(SetupCheckBase):
    def _check_setup(self):
        try:
            with open(self.config_path, 'r') as config_file:
                _ = config_file.read()
                return True, ""
        except FileNotFoundError:
            return False, f"Configuration at {self.config_path} not found..."

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.check_name = "Verifying config exists"
        self.success, self.error_reason = self._check_setup()
        self.instructions = [
            "We could not find the config.txt, did you rename it? Please add it back...",
            "You can find the folder two ways:",
            "Click okay, use the iMessage GPT Bot menubar drop down to reveal files, add it there",
            "Go to Applications/iMessage GPT Bot, right click to reveal files, and navigate to the assets folder"
        ]