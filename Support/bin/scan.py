#!/usr/bin/env python
# encoding: utf-8
import sys
import textmate
from textmate import ui
from utils import get_project

# Import rope modules
try:
    from rope.base.project import Project
    try:
        from rope.contrib import codeassist
    except:
        textmate.exit_show_tool_tip('Cannot find rope.contrib.codeassist. Rope may need to be updated.')
except:
    textmate.exit_show_tool_tip('Rope module not found!')

def main():

    if textmate.PROJECT_DIRECTORY is None:
        textmate.exit_show_tool_tip('No project to scan.')
    
    project = get_project()
    project.validate(project.root)
    textmate.exit_show_tool_tip('project scanned.')

if __name__ == "__main__":
    main()


