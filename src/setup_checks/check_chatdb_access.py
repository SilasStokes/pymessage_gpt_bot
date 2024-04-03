
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
        self.success, self.error_reason = self._check_setup()

        self.instructions = [
            "iMessage Bot needs full disk access in order to be able to read messages ",
            "Go to System Settings -> Security -> Full Disk Access",
            "If you don't see iMessage GPT Bot, click the + icon and manually add from your Application folder",
            "Click the slider to give access"
        ]
