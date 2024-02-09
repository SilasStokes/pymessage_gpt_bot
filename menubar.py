import rumps
from subprocess import Popen
import os

rumps.debug_mode(True)

class MenubarText:
    START = 'Start'
    RESTART = 'Restart'
    STOP = 'Stop'
    EDIT_CONFIG = 'Edit Config'
    QUIT = 'Quit'

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = 'configs/example-config.json'
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
    bot_process = Popen(['.venv/bin/python', 'src', '--config', CONFIG_PATH], cwd=WORKING_DIR)

@rumps.clicked(MenubarText.STOP)
def on_click_stop(_):
    kill_and_null_proc()

@rumps.clicked(MenubarText.EDIT_CONFIG)
def on_click_edit_config(_):
    Popen(["open", "-e", f'{WORKING_DIR}/{CONFIG_PATH}'])

app = rumps.App('💬', quit_button=rumps.MenuItem(MenubarText.QUIT))
app.menu = [
    (MenubarText.START),
    (MenubarText.STOP),
    (MenubarText.RESTART), # update this to be stateful based on if process is not null
    (MenubarText.EDIT_CONFIG)
]
app.run()