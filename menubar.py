import rumps
from subprocess import Popen
import os
import sys

rumps.debug_mode(True)

class RuntimeEnvironment():

    def __init__(self):
        self.WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.RUNNING_IN_INSTALLER = True
            self.CONFIG_PATH = os.path.join(self.WORKING_DIR, 'config.json')
            self.MAIN_NAME = 'main'
            self.MAIN_PATH = os.path.abspath(os.path.join(self.WORKING_DIR, '..'))
            self.PYTHON_EXE = f'python'
            self.MAIN_EXE = os.path.join(self.MAIN_PATH, self.MAIN_NAME)
            self.POPEN_CMD = [self.MAIN_EXE, '--config', self.CONFIG_PATH]
        else:
            self.RUNNING_IN_INSTALLER = False
            self.CONFIG_PATH = os.path.join(self.WORKING_DIR, 'configs', 'config.json')
            self.MAIN_NAME = 'main.py'
            self.MAIN_PATH = os.path.abspath(self.WORKING_DIR)
            self.PYTHON_EXE = f'.venv/bin/python'
            self.MAIN_EXE = os.path.join(self.MAIN_PATH, self.MAIN_NAME)
            self.POPEN_CMD = [self.PYTHON_EXE, self.MAIN_EXE, '--config', self.CONFIG_PATH]

rte = RuntimeEnvironment()

class MenubarText:
    START = 'Start'
    RESTART = 'Restart'
    STOP = 'Stop'
    EDIT_CONFIG = 'Edit Config'
    QUIT = 'Quit'

bot_process = None

def kill_and_null_proc():
    global bot_process
    if bot_process is not None:
        bot_process.kill()
        bot_process = None


@rumps.clicked(MenubarText.START)
def on_click_start(_):
    global bot_process
    kill_and_null_proc()
    bot_process = Popen(rte.POPEN_CMD, cwd=rte.WORKING_DIR)

@rumps.clicked(MenubarText.STOP)
def on_click_stop(_):
    kill_and_null_proc()

@rumps.clicked(MenubarText.EDIT_CONFIG)
def on_click_edit_config(_):
    Popen(["open", "-e", rte.CONFIG_PATH])

app = rumps.App('💬', quit_button=rumps.MenuItem(MenubarText.QUIT))
app.menu = [
    (MenubarText.START),
    (MenubarText.STOP),
    (MenubarText.RESTART), # update this to be stateful based on if process is not null
    (MenubarText.EDIT_CONFIG)
]
app.run()