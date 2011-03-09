#!/usr/bin/env python
# encoding: utf-8
import os, sys

# Add bundle lib path.
LIB_PATH = os.path.join(os.environ["TM_BUNDLE_SUPPORT"], "lib")
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

import tm

if __name__ == "__main__":
    if tm.PROJECT_DIRECTORY is None:
        tm.exit_show_tool_tip('You must create a project first!')

    arg = sys.argv[1]
    source = sys.stdin.read()
    
    if arg == 'complete':
        from completion import CompleteCommand
        command = CompleteCommand(source)
    elif arg == 'import':
        from completion import InsertImportCommand
        command = InsertImportCommand(source)
    elif arg == 'scan':
        from completion import ScanProjectCommand
        command = ScanProjectCommand(source)
    elif arg == 'open':
        from completion import OpenDefinitionCommand
        command = OpenDefinitionCommand(source)
    else:
        raise ValueError("Command not found. Acceptable commands are: complete, import, scan, open")

    command.execute()