import os
import sys

DEBUG: bool = True
WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

RUNNING_AS_EXECUTABLE: bool = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

if RUNNING_AS_EXECUTABLE:
    CONFIG_PATH = os.path.join(WORKING_DIR, 'assets', 'config.json')
    EXE_LOCATION = os.path.join(os.path.abspath(os.path.join(WORKING_DIR, '..')), 'MacOS')
    BOT_EXE = os.path.join(EXE_LOCATION, 'bot')
    ERROR_POPUP_EXE = os.path.join(EXE_LOCATION, 'error_popup')
    PYTHON_EXE = 'python'
    BOT_POPEN_CMD = [BOT_EXE, '--config', CONFIG_PATH]
    POPUP_POPEN_CMD = [ERROR_POPUP_EXE]
    INSTRUCTION_CMD = ["open", "-e", os.path.join(WORKING_DIR, 'assets', 'instructions.txt')]
else:
    CONFIG_PATH = os.path.join(WORKING_DIR, 'configs', 'config.json')
    BOT_EXE = os.path.join(WORKING_DIR, 'bot.py')
    ERROR_POPUP_EXE = os.path.join(WORKING_DIR, 'error_popup.py')
    PYTHON_EXE = os.path.join(WORKING_DIR, '.venv', 'bin', 'python')
    BOT_POPEN_CMD = [PYTHON_EXE, BOT_EXE, '--config', CONFIG_PATH]
    POPUP_POPEN_CMD = [PYTHON_EXE, ERROR_POPUP_EXE]
    INSTRUCTION_CMD = ["open", "-e", os.path.join('assets', 'instructions.txt')]

INSTRUCTIONS_PATH = os.path.join(WORKING_DIR, 'assets', 'instructions.txt')
LOGGER_FILE = os.path.join(WORKING_DIR, 'assets', 'iMessage_GPT_Bot.log')
