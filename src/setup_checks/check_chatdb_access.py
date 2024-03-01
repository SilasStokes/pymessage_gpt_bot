
from ..imessage_reader.fetch_data import FetchData
from .setup_model import SetupCheckBase

class CheckChatdbAccess(SetupCheckBase):

    def _check_setup(self):
        try:
            _ = FetchData().get_most_recent_messages()
            return True, ""
        except Exception as e:
            return False, f"Could not connect to chat.db. Error: {e}"


    def __init__(self):
        self.check_name = "Verifying iMessage Database Access"
        self.instructions = ""
        self.success, self.error_reason = self._check_setup()
