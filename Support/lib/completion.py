import re
import urllib
import subprocess
import tm
# Import rope modules
try:
    from rope.base.project import Project
    try:
        from rope.contrib import codeassist
    except:
        tm.exit_show_tool_tip('Cannot find rope.contrib.codeassist. Rope may need to be updated.')
    try:
        from rope.contrib.autoimport import AutoImport
    except:
        tm.exit_show_tool_tip('Cannot find rop.contrib.autoimport. Rope may need to be updated.')
except:
    tm.exit_show_tool_tip('Rope module not found!')


class BaseCommand(object):
    """
    Base command. This class should be extended by command classes that
    correspond to completion bundle commands.
    """

    def __init__(self, source):
        self.source = source

    def get_project(self, project_dir = tm.PROJECT_DIRECTORY):
        """
        Returns a rope project for a given directory
        """
        if project_dir is None:
            return None
        else:
            return Project(tm.PROJECT_DIRECTORY)

    def get_auto_import(self, project = None, underlined = True):
        if not project:
            project = self.get_project()

        if project is None:
            return None
        else:
            autoimport = AutoImport(project, False, underlined)
            autoimport.generate_cache()
            return autoimport

    def execute(self):
        raise NotImplemented("%s should override this method!" % self.__class__.__name__)


class CompleteCommand(BaseCommand):
    """
    Provides code completion suggestions.
    """

    def execute(self):
        # TODO: Determine if this is necessary. Can we still provide basic completion in a 'standalone' file?
        if tm.PROJECT_DIRECTORY is None:
            tm.exit_show_tool_tip('No completions.')

        if re.match(r'^(from|import)\s+.*', tm.CURRENT_LINE):
            self._complete_import()
        else:
            self._complete()

    def _complete_import(self):
        autoimport = self.get_auto_import()

        current_word = tm.current_word(r"[a-zA-Z_]*", 'both')

        proposals = autoimport.import_assist(current_word)

        names = []
        name_re = re.compile(r'.*import\s+.*')
        for name, module in proposals:
            if name_re.match(tm.CURRENT_LINE):
                names.append(name)
            else:
                names.append(module)

        tm.ui.complete(names, {'initial_filter': current_word,
            'extra_chars': "_"})

    def _complete(self):
        caret_index = self.source.find(tm.CURRENT_LINE) + tm.LINE_INDEX
        project = self.get_project()
        resource = project.get_resource(tm.FILEPATH.replace(tm.PROJECT_DIRECTORY, '')[1:])


        current_word = tm.current_word(r"[a-zA-Z_]*", 'both')
        proposals = codeassist.code_assist(project, self.source, caret_index, resource)

        try:
            if len(proposals) == 0:
                raise 'no proposals found'
        except:
            tm.exit_show_tool_tip("No completions.")

        if len(proposals) == 1:
            tm.exit_insert_text(proposals[0].name.replace(current_word, '', 1))
        else:
            proposals = codeassist.sorted_proposals(proposals)
            names = [proposal.name for proposal in proposals]
            tm.ui.complete(names, {'initial_filter': current_word, 'extra_chars': "_"})


class InsertImportCommand(BaseCommand):
    """
    Inserts import statements in a document.
    """

    def execute(self):
        if tm.PROJECT_DIRECTORY is None:
            tm.exit_show_tool_tip('No imports found.')

        autoimport = self.get_auto_import()

        current_word = tm.current_word(r"[a-zA-Z_]*", 'both')

        if not current_word:
            tm.exit_show_tool_tip('No imports found.')

        proposals = autoimport.import_assist(current_word)
        result = None

        try:
            if len(proposals) == 0:
                raise 'no proposals found'
        except:
            tm.exit_show_tool_tip("No imports found.")

        if len(proposals) == 1:
            result = 'from %s import %s' % (proposals[0][1], proposals[0][0])
        else:
            names = []
            for name, module in proposals:
                names.append(('%s (%s)' % (name, module),
                    'from %s import %s' % (module, name)))

            result = tm.ui.menu(names)

        if result:
            self._insert_import(result, current_word)
        else:
            tm.exit_discard()

    def _insert_import(self, statement, word):
        line = tm.CURRENT_LINE
        doc = self.source
        line_num = tm.LINE_NUMBER
        line_idx = tm.LINE_INDEX

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
                tm.exit_show_tool_tip('%s already imported (%s)' % (name, line))

        imports.append(statement)

        output = ''
        if post:
            output = '\n'.join(post)
        if imports:
            output = '%s\n%s' % ('\n'.join(imports), output)
        if pre:
            output = '%s\n%s' % ('\n'.join(pre), output)

        print output
        # tm.exit_replace_text(output)

        tm.go_to({"line": line_num + 1, "column": line_idx + 1})


class ScanProjectCommand(BaseCommand):
    """
    Scans a project to get information about its modules.
    """

    def execute(self):
        if tm.PROJECT_DIRECTORY is None:
            tm.exit_show_tool_tip('No project to scan.')

        project = self.get_project()
        project.validate(project.root)
        tm.exit_show_tool_tip('Project scanned.')
        
        

    # def test(self):
    #     cmd = os.path.join(os.path.dirname(__file__), 'test.py')
    #
    #     p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #     while p.poll() is None:
    #         data = p.stdout.readline()
    #         sys.stdout.write("<p>parent read: " + data.strip() + "</p>")
    #         sys.stdout.flush()


        # STDOUT << '<br/><br/><div class="raw_out"><span class="showhide">'
        # STDOUT << "<a href=\"javascript:hideElement('raw_out')\" id='raw_out_h' style='display: none;'>&#x25BC; Hide Raw Output</a>"
        # STDOUT << "<a href=\"javascript:showElement('raw_out')\" id='raw_out_s' style=''>&#x25B6; Show Raw Output</a>"
        # STDOUT << '</span></div>'
        # STDOUT << '<div class="inner" id="raw_out_b" style="display: none;"><br/>'
        # STDOUT << "<code>#{exhaust.input.to_s}</code><br/>"

        # tm.exit_show_html()

class OpenDefinitionCommand(BaseCommand):
    """
    Opens the definition for a given entity.
    """

    def execute(self):
        #TODO: support multiple matches
        if tm.PROJECT_DIRECTORY is None:
            tm.exit_show_tool_tip('You must create a project first!')

        project = self.get_project()
        caret_index = self.source.find(tm.CURRENT_LINE) + tm.LINE_INDEX
        try:
            resource, line = codeassist.get_definition_location(project, self.source, caret_index)
        except:
            resource = None

        if resource is not None:
            subprocess.Popen(['open', 'txmt://open?url=file://%s&line=%d' % (urllib.quote(resource.real_path), line)])
        else:
            tm.exit_show_tool_tip('Definition not found.')
