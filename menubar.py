import rumps
from subprocess import Popen
import os
import sys
import src.windows.pop_up as pop_up
from PyQt5 import QtWidgets
from src.setup_checks import CheckChatdbAccess, CheckConfigExists, CheckOpenaiKey, CheckShortcutExists, CheckTestFail


class RuntimeEnvironment():
    def __init__(self):

        self.WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.RUNNING_IN_INSTALLER = True
            self.CONFIG_PATH = os.path.join(self.WORKING_DIR, 'assets', 'config.json')
            self.MAIN_NAME = 'main'
            # self.MAIN_PATH = self.WORKING_DIR
            self.MAIN_PATH = os.path.abspath(os.path.join(self.WORKING_DIR, '..'))
            self.MAIN_EXE = os.path.join(self.MAIN_PATH, 'MacOS' ,self.MAIN_NAME)
            self.PYTHON_EXE = f'python'
            self.POPEN_CMD = [self.MAIN_EXE, '--config', self.CONFIG_PATH]
            self.ASSET_PATH = os.path.join(self.WORKING_DIR, 'assets', 'instructions.txt')
            self.INSTRUCTION_CMD = ["open", "-e", os.path.join(self.WORKING_DIR, 'assets', 'instructions.txt')]
        else:
            self.RUNNING_IN_INSTALLER = False
            self.CONFIG_PATH = os.path.join(self.WORKING_DIR, 'configs', 'config.json')
            self.MAIN_NAME = 'main.py'
            self.MAIN_PATH = os.path.abspath(self.WORKING_DIR)
            self.MAIN_EXE = os.path.join(self.MAIN_PATH, self.MAIN_NAME)
            self.PYTHON_EXE = f'.venv/bin/python'
            self.POPEN_CMD = [self.PYTHON_EXE, self.MAIN_EXE, '--config', self.CONFIG_PATH]
            self.ASSET_PATH = os.path.join(self.WORKING_DIR, 'assets/instructions.txt')
            self.INSTRUCTION_CMD = ["open", "-e", os.path.join('assets','instructions.txt')]

class MenubarText:
    START = 'Start'
    RESTART = 'Restart'
    STOP = 'Stop'
    EDIT_CONFIG = 'Edit Config'
    QUIT = 'Quit'
    REVEAL_FILES = 'Reveal Files'

debug = True
rumps.debug_mode(debug)
bot_process = None
rte = RuntimeEnvironment()

##################################################
####### SETUP CHECK ##############################
##################################################
checks = [
    CheckConfigExists(config_path=rte.CONFIG_PATH),
    CheckOpenaiKey(config_path=rte.CONFIG_PATH),
    CheckChatdbAccess(),
    CheckShortcutExists(),
    CheckTestFail()
]

if not all(check.success for check in checks):
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("iMessage GPT Bot Setup Window")
    app.setApplicationDisplayName("iMessage GPT Bot Setup Window")
    w = pop_up.MainWindow(checks)
    app.exec()
    app.exit()

# quit()



##################################################
####### PROGRAM START ############################
##################################################
def kill_and_null_proc():
    global bot_process
    if bot_process is not None:
        bot_process.kill()
        bot_process = None



def on_click_stop(_):
    kill_and_null_proc()
    start_button = app.menu[MenubarText.START]
    stop_button = app.menu[MenubarText.STOP]
    restart_button = app.menu[MenubarText.RESTART]

    restart_button.set_callback(None)
    stop_button.set_callback(None)
    start_button.set_callback(on_click_start)


@rumps.clicked(MenubarText.EDIT_CONFIG)
def on_click_edit_config(_):
    Popen(["open", "-e", rte.CONFIG_PATH])

def on_click_restart(_):
    kill_and_null_proc()
    on_click_start(_)

@rumps.clicked(MenubarText.QUIT)
def clean_up_before_quit(_):
    kill_and_null_proc()
    rumps.quit_application()

@rumps.clicked(MenubarText.REVEAL_FILES)
def clean_up_before_quit(_):
    Popen(["open", "-R", rte.ASSET_PATH])
    # kill_and_null_proc()
    # rumps.quit_application()

@rumps.clicked(MenubarText.START)
def on_click_start(_):
    global bot_process
    start_button = app.menu[MenubarText.START]
    stop_button = app.menu[MenubarText.STOP]
    restart_button = app.menu[MenubarText.RESTART]

    restart_button.set_callback(on_click_restart)
    stop_button.set_callback(on_click_stop)
    start_button.set_callback(None)
    bot_process = Popen(rte.POPEN_CMD, cwd=rte.WORKING_DIR)

app = rumps.App('💬', quit_button=None)
app.menu = [
    MenubarText.START,
    MenubarText.STOP,
    MenubarText.RESTART, 
    MenubarText.EDIT_CONFIG,
    MenubarText.REVEAL_FILES,
    MenubarText.QUIT
]

app.run()