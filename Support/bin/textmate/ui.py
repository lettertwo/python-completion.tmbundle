import re
import tempfile
import plistlib
import subprocess
import textmate
from dialog import get_string
from dialog import menu

# TODO: rewrite this as pydoc
# Interactive Code Completion Selector
# Displays the pop-up completion menu with the list of +choices+ provided.
# 
# +choices+ should be an array of dictionaries with the following keys:
# 
# * +display+ -- The title to display in the suggestions list
# * +insert+  -- Snippet to insert after selection
# * +image+   -- An image name, see the <tt>:images</tt> option
# * +match+   -- Typed text to filter on (defaults to +display+)
# 
# All options except +display+ are optional.
# 
# +options+ is a hash which can accept the following keys:
#
# * <tt>:extra_chars</tt>       -- by default only alphanumeric characters will be accepted,
#   you can add additional characters to the list with this option.
# 	This string is escaped for regex. List each character in a simple string EG: '{<#^'
# * <tt>:case_insensitive</tt>  -- ignore case when filtering
# * <tt>:static_prefix</tt>     -- a prefix which is used when filtering suggestions.
# * <tt>:initial_filter</tt>    -- defaults to the current word
# TODO: implement support for images
# * <tt>:images</tt>            -- a +Hash+ of image names to paths
# 
def complete(choices, options = {}):
    
    if '2' not in textmate.DIALOG:
        raise 'Dialog2 not found.'
    
    if 'initial_filter' not in options:
        characters = 'a-zA-Z0-9'
        if 'extra_chars' in options:
            characters += re.escape(options['extra_chars'])

        options['initial_filter'] = textmate.current_word(characters, "left")

    command = [textmate.DIALOG, "popup", "--returnChoice"]
    if "initial_filter" in options and options['initial_filter']:
        command.append("--alreadyTyped %s" % textmate.sh_escape(options["initial_filter"]))
    if "static_prefix" in options and options['static_prefix']:
        command.append("--staticPrefix %s" % textmate.sh_escape(options["static_prefix"]))
    if "extra_chars" in options and options['extra_chars']:
        command.append("--additionalWordCharacters %s" % textmate.sh_escape(options['extra_chars']))
    if "case_insensitive" in options and options['case_insensitive']:
        command.append("--caseInsensitive")

    def formalize(choice):
        try:
            choice['display']
            return choice
        except (KeyError, IndexError, TypeError):
            return {'display': choice}

    choices = [formalize(choice) for choice in choices]
    
    plist = {'suggestions': choices}

    try:
        f = tempfile.NamedTemporaryFile()
        plistlib.writePlist(plist, f)
        f.seek(0)
        
        command = ' '.join(command).strip()
        
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        process.stdin.write(f.read())
        process.stdin.close()
        f.close()

    except Exception as e:
        textmate.exit_show_tool_tip('ERROR: %s' % e)
    finally:
        f.close()
