#!/usr/bin/env python
# encoding: utf-8
import sys
import textmate
from textmate import ui

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
    # TODO: Determine if this is necessary. Can we still provide basic completion in a 'standalone' file?
    if textmate.PROJECT_DIRECTORY is None:
        textmate.exit_show_tool_tip('No completions.')

    source = sys.stdin.read()

    #from rope.contrib import autoimport
    project = Project(textmate.PROJECT_DIRECTORY)
    #autoimport = autoimport.AutoImport(project)
    resource = project.get_resource(textmate.FILEPATH.replace(textmate.PROJECT_DIRECTORY, '')[1:])
    #project.validate(self.project_path)
    caret_index = source.find(textmate.CURRENT_LINE) + textmate.LINE_INDEX

    current_word = textmate.current_word(r"[a-zA-Z_]*", 'both')

    proposals = codeassist.code_assist(project, source, caret_index, resource)
    
    try:
        if len(proposals) == 0:
            raise 'no proposals found'
    except:
        textmate.exit_show_tool_tip("No completions.")
    
    if len(proposals) == 1:
        textmate.exit_insert_text(proposals[0].name.replace(current_word, '', 1))
    else:
        proposals = codeassist.sorted_proposals(proposals)
        #autoimport.generate_cache()
        #autoimport.generate_modules_cache(modules)
        #project.pycore.analyze_module(resource)
        names = [proposal.name for proposal in proposals]
        #if self.starting.strip() and '.' not in self.expression:
        #        import_assists = self.autoimport.import_assist(self.starting)
        #        names.extend(x[0] + ' : ' + x[1] for x in import_assists)

        #plist = "{ menuItems=(%s);}"
        ui.complete(names, {'initial_filter': current_word, 'extra_chars': "_"})



# def goto_definition(self):
#     """
#     Tries to find the definition for the currently selected scope;
# 
#         * if the definition is found, returns a tuple containing the file path and the line number (e.g. ``('/Users/fabiocorneti/src/def.py', 23))``
#         * if no definition is found, returns None
# 
#     """
#     #TODO: support multiple matches
#     if TM_PROJECT_DIRECTORY is None:
#         return None
#     project = Project(TM_PROJECT_DIRECTORY)
#     caret_index = self.source.find(TM_CURRENT_LINE) + TM_LINE_INDEX
#     resource, line = codeassist.get_definition_location(project, self.source, caret_index)
#     if resource is not None:
#         return 'txmt://open?url=file://%s&line=%d' % (urllib.quote(resource.real_path), line)
#     else:
#         return ''

if __name__ == "__main__":
    main()


