#!/usr/bin/env python
# encoding: utf-8

import sys, os, re
import textmate
from textmate import ui
from utils import get_project
from utils import get_auto_import

def main():
    if textmate.PROJECT_DIRECTORY is None:
        textmate.exit_show_tool_tip('No imports found.')

    project = get_project()
    autoimport = get_auto_import(project)
    
    current_word = textmate.current_word(r"[a-zA-Z_]*", 'both')
    
    if not current_word:
        textmate.exit_show_tool_tip('No imports found.')
    
    proposals = autoimport.import_assist(current_word)
    result = None

    try:
        if len(proposals) == 0:
            raise 'no proposals found'
    except:
        textmate.exit_show_tool_tip("No imports found.")

    if len(proposals) == 1:
        result = 'from %s import %s' % (proposals[0][1], proposals[0][0])
    else:
        names = []
        for name, module in proposals:
            names.append(('%s (%s)' % (name, module),
                'from %s import %s' % (module, name)))
        
        result = ui.menu(names)
        
    if result:
        insert_import(result, current_word)
    else:
        textmate.exit_discard()


def insert_import(statement, word):
    line = textmate.CURRENT_LINE
    doc = sys.stdin.read()
    line_num = textmate.LINE_NUMBER
    line_idx = textmate.LINE_INDEX
    
    pre, imports, post = [], [], []
    import_re = re.compile(r'^\s*from|import .+')
    def_re = re.compile(r'^\s*class|def .+')

    for line in doc.split('\n'):
        if post:
            post.append(line)
        elif imports:
            if def_re.match(line):
                post.append(line)
            else:
                imports.append(line)
        else:
            if import_re.match(line):
                imports.append(line)
            elif def_re.match(line):
                post.append(line)
            else:
                pre.append(line)
    
    # Move any empty lines at the end of the imports list to the post list.
    tmp = list(imports)
    for i in reversed(range(len(tmp))):
        if import_re.match(tmp[i]):
            break
        else:
            post.insert(0, imports.pop(i))

    # Check to see if the import already exists.
    name = re.split(r'\s+', statement).pop()
    for line in imports:
        if re.match(r'.*import.+%s.*' % name, line):
            textmate.exit_show_tool_tip('%s already imported (%s)' % (name, line))

    imports.append(statement)
    
    output = ''
    if post:
        output = '\n'.join(post)
    if imports:
        output = '%s\n%s' % ('\n'.join(imports), output)
    if pre:
        output = '%s\n%s' % ('\n'.join(pre), output)

    print output

    textmate.go_to({"line": line_num + 1, "column": line_idx + 1})

if __name__ == "__main__":
    main()

