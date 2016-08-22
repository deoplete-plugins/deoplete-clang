import re
import subprocess
from .base import Base

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'cmake'
        self.mark = '[cmake]'
        self.filetypes = ['cmake']
        self.rank = 600
        self.debug_enabled = False
        self._commands = {}
        self._variables = []
        self._identifiers = []

        self._gather_commands()
        self._gather_variables()


    def _get_command_help_text(self, command):
        p = subprocess.Popen(command, shell=True,
                stdout=subprocess.PIPE)
        return str(p.stdout.read()).replace('\\n', '\n')


    def _gather_commands(self):
        help_text= self._get_command_help_text('cmake --help-commands')
        regex = re.compile(r'\s([\w\d]+\s*\([^)]*?\))')
        commands = regex.findall(help_text)
        for command in commands:
            name = command.split('(')[0]
            if name not in self._commands:
                regex = re.compile(r'\(([^)]*?)\)')
                args = regex.findall(command)[0]
                self._commands[name] = ' '.join(args.replace('\n', ' ').split())


    def _gather_variables(self):
        help_text = self._get_command_help_text('cmake --help-variable-list')
        language_keyword = ['C', 'CXX', 'FORTRAN', 'JAVA', 'PYTHON']
        for variable in help_text.split('\n'):
            if variable.find('<LANG>') >= 0:
                variables = [variable.replace('<LANG>', v)
                             for v in language_keyword]
                self._variables += variables
            elif variable not in self._variables:
                self._variables.append(variable)


    def _gather_identifier(self):
        regex = re.compile(r'\s*set\(([\w\d]+)[\w\d\s./]*\)')
        self._identifiers = regex.findall('\n'.join(self.vim.current.buffer))


    def on_event(self, context):
        self._gather_identifier()


    def gather_candidates(self, context):
        self._gather_identifier()

        commands = [{'word': c, 'kind': 'command', 'menu': self._commands[c]}
                for c in self._commands]
        variables = [{'word': v, 'kind': 'variable'}
                for v in self._variables]
        identifiers = [{'word': i, 'kind': 'identifier'}
                for i in self._identifiers]
        return commands + variables + identifiers
