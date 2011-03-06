"""
Many of these methods are ported or adopted from the TextMate support bundle's
(Ruby) TextMate module.
"""
import sys
import os

# Add TM supoprt path.
SUPPORT_PATH = os.path.join(os.environ["TM_SUPPORT_PATH"], "lib")
if not SUPPORT_PATH in sys.path:
    sys.path.insert(0, SUPPORT_PATH)

# from dialog import menu, get_string
from tm_helpers import current_word, env_python, sh, sh_escape


# TextMate environment vars
PROJECT_DIRECTORY = os.environ.get('TM_PROJECT_DIRECTORY', None)
FILEPATH = os.environ.get('TM_FILEPATH')
LINE_INDEX = int(os.environ.get('TM_LINE_INDEX', -1))
CURRENT_LINE = os.environ.get('TM_CURRENT_LINE', None)
LINE_NUMBER = int(os.environ.get('TM_LINE_NUMBER', -1))
SCOPE = os.environ.get('TM_SCOPE', None)
CURRENT_WORD = os.environ.get('TM_CURRENT_WORD', None)
DIALOG = os.environ.get('DIALOG', None)
PYTHONPATH = os.environ.get('PYTHONPATH', None)

def exit_discard():
    sys.exit(200)


def exit_replace_text(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(201)


def exit_replace_document(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(202)


def exit_insert_text(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(203)


def exit_insert_snippet(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(204)


def exit_show_html(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(205)


def exit_show_tool_tip(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(206)


def exit_create_new_document(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(207)


def go_to(options = {}):
    if 'file' in options:
        default_line = 1
    else:
        default_line = LINE_NUMBER
    
    defaults = {
        'file': FILEPATH,
        'line': default_line,
        'column': 1
    }
    defaults.update(options)
    options = defaults
    
    command = "txmt://open?"
    if 'file' in options:
        command = "%surl=file://%s&" % (command, options['file'])
    command = "%sline=%s&column=%s" % (command, options['line'], options['column'])
    command = 'open %s' % sh_escape(command)

    import subprocess
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    process.wait()

