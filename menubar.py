import rumps
from subprocess import Popen
from src.setup_checks import CheckChatdbAccess, CheckConfigExists, CheckOpenaiKey, CheckShortcutExists
from src.runtime_environment import CONFIG_PATH, BOT_POPEN_CMD, INSTRUCTIONS_PATH, WORKING_DIR, DEBUG, POPUP_POPEN_CMD
from src.autoresponder.logger import logger

logger.debug('menubar loading')


class Menubar:
    START = 'Start'
    RESTART = 'Restart'
    STOP = 'Stop'
    EDIT_CONFIG = 'Edit Config'
    QUIT = 'Quit'
    REVEAL_FILES = 'Reveal Files'


rumps.debug_mode(DEBUG)
bot_process = None

# SETUP CHECK
checks = [
    CheckConfigExists(config_path=CONFIG_PATH),
    CheckOpenaiKey(config_path=CONFIG_PATH),
    CheckChatdbAccess(),
    CheckShortcutExists()
]

if not all(check.success for check in checks):
    logger.debug('Some check(s?) failed... running error_popup')
    Popen(POPUP_POPEN_CMD)


# PROGRAM START
def kill_and_null_proc():
    global bot_process
    if bot_process is not None:
        bot_process.kill()
        bot_process = None


def on_click_stop(_):
    kill_and_null_proc()
    start_button = app.menu[Menubar.START]
    stop_button = app.menu[Menubar.STOP]
    restart_button = app.menu[Menubar.RESTART]

    restart_button.set_callback(None)
    stop_button.set_callback(None)
    start_button.set_callback(on_click_start)


@rumps.clicked(Menubar.EDIT_CONFIG)
def on_click_edit_config(_):
    logger.debug(f'{Menubar.EDIT_CONFIG} clicked')
    Popen(["open", "-e", CONFIG_PATH])


def on_click_restart(_):
    kill_and_null_proc()
    on_click_start(_)


@rumps.clicked(Menubar.QUIT)
def clean_up_before_quit(_):
    logger.debug(f'{Menubar.QUIT} clicked')
    kill_and_null_proc()
    rumps.quit_application()


@rumps.clicked(Menubar.REVEAL_FILES)
def clean_reveal_files(_):
    logger.debug(f'{Menubar.REVEAL_FILES} clicked')
    Popen(["open", "-R", INSTRUCTIONS_PATH])


@rumps.clicked(Menubar.START)
def on_click_start(_):
    global bot_process
    logger.debug('start clicked')
    start_button = app.menu[Menubar.START]
    stop_button = app.menu[Menubar.STOP]
    restart_button = app.menu[Menubar.RESTART]

    restart_button.set_callback(on_click_restart)
    stop_button.set_callback(on_click_stop)
    start_button.set_callback(None)
    bot_process = Popen(BOT_POPEN_CMD, cwd=WORKING_DIR)


app = rumps.App('💬', quit_button=None)
app.menu = [
    Menubar.START,
    Menubar.STOP,
    Menubar.RESTART,
    Menubar.EDIT_CONFIG,
    Menubar.REVEAL_FILES,
    Menubar.QUIT
]

app.run()
