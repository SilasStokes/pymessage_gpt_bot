
from .setup_model import SetupCheckBase
import os


SHORTCUTS_DB_PATH = os.path.join(os.path.expanduser('~'), 
                                'Library', 'Shortcuts', "Shortcuts.sqlite")
SHORTCUT_NAME = 'send-imessage'
SQL_CMD = f'SELECT ZNAME FROM ZSHORTCUT WHERE ZNAME LIKE "{SHORTCUT_NAME}";'

class CheckShortcutExists(SetupCheckBase):

    def _check_setup(self):
        import sqlite3
        try:
            conn = sqlite3.connect(SHORTCUTS_DB_PATH)
            cur = conn.cursor()
            cur.execute(SQL_CMD)
            shortcuts = cur.fetchall()
            
            if len(shortcuts) > 0:
                return True, ""
            else:
                return False, "send-imessage shortcut not found in shortcut database"
        except Exception as e:
            return False, f"Could not access shortcut database at {SHORTCUTS_DB_PATH} to check if send-imessage exists, error: {e}"


    def __init__(self):
        self.check_name = "Verifying the send message shortcut works"
        self.success, self.error_reason = self._check_setup()
        self.instructions = [
            "Click okay below and in the iMessage GPT Bot menubar dropdown select \"reveal files\" which will open the apps assets folder",
            "Double click on the \"send-imessage.shortcut\" file and follow the prompts to install it"
        ]