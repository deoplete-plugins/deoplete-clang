import os
import re

from .base import Base
from deoplete.util import load_external_module

current = __file__

load_external_module(current, 'clang')
import clang.cindex as clang

load_external_module(current, 'sources/deoplete_clang')
from clang_data import index_h


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'clang'
        self.mark = '[clang]'
        self.filetypes = ['c', 'cpp', 'objc', 'objcpp', 'cuda']
        self.rank = 500
        # TODO(zchee): not need "r'[a-zA-Z_]\w*::\w*'" in C language
        self.input_pattern = (r'[^. \t0-9]\.\w*|'
                              r'[^. \t0-9]->\w*|'
                              r'[a-zA-Z_]\w*::\w*')

    def on_init(self, context):
        vars = context['vars']

        self.debug_enabled = vars.get(
            'deoplete#sources#clang#debug',
            False
        )
        self.library_path = vars.get(
            'deoplete#sources#clang#libclang_path',
            ''
        )
        self.clang_header = vars.get(
            'deoplete#sources#clang#clang_header',
            ''
        )
        self.completion_flags = vars.get(
            'deoplete#sources#clang#flags',
            []
        )
        self.sort_algo = vars.get(
            'deoplete#sources#clang#sort_algo',
            ''
        )
        self.std = vars.get(
            'deoplete#sources#clang#std',
            {
                'c': 'c11',
                'cpp': 'c++1z',
                'objc': 'c11',
                'objcpp': 'c++1z'
            }
        )
        self.default_filename = vars.get(
            'deoplete#sources#clang#default_file',
            ''
        )
        self.test_extensions = vars.get(
            'deoplete#sources#clang#test_extensions',
            {'.h': ['.c', '.cpp', '.m', '.mm'], '.hpp': ['.cpp']}
        )

        self.std_c = self.std.get('c', 'c11')
        self.std_cpp = self.std.get('cpp', 'c++1z')
        self.std_objc = self.std.get('objc', 'c11')
        self.std_objcpp = self.std.get('objcpp', 'c++1z')

        clang_complete_database = vars.get(
            'deoplete#sources#clang#clang_complete_database',
            ''
       )

        if not clang.Config.loaded or \
                clang.Config.library_path != self.library_path:
            clang.Config.loaded = False
            clang.Config.set_library_file(self.library_path)
            clang.Config.set_compatibility_check(False)

        # search for .clang file
        path = os.path.dirname(self.vim.current.buffer.name)
        while not os.path.isfile(path + "/.clang"):
            if path == "/":
                break
            path = os.path.realpath(path + "/..")

        path2 = path + "/.clang"
        if os.path.isfile(path2):
            flags_file = open(path2)
            flags = flags_file.read().rstrip()
            m = re.match(r'^flags\s*=\s*', flags)
            if m is not None:
                self.completion_flags = flags[m.end():].split()
            else:
                m = re.match(r'^compilation_database\s*=\s*', flags)
                if m is not None:
                    path3 = flags[m.end():]
                    if path3[0] == '"' and path3[-1] == '"':
                        path3 = path3[1:-1]
                    if os.path.isabs(path3):
                        clang_complete_database = path3
                    else:
                        clang_complete_database = path+"/"+path3

        if clang_complete_database and os.path.isdir(clang_complete_database):
            self.compilation_database = \
                clang.CompilationDatabase.fromDirectory(
                    clang_complete_database)
        else:
            self.compilation_database = None

        self.index = clang.Index.create()
        # TODO(zchee): More elegant way
        self.tu_data, self.params, self.database = dict(), dict(), dict()

    def on_event(self, context):
        # Note: Dummy call to make cache
        try:
            self.gather_candidates(context)
        except:
            # Ignore the error
            pass

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        line = context['position'][1]
        col = (context['complete_position']
               if 'complete_position' in context
               else context['position'][2]) + 1
        buf = self.vim.current.buffer
        if self.compilation_database:
            params = self.get_params(buf.name)
        else:
            params = self.completion_flags + \
                self.get_minimum_flags(context['filetype'])
            params.append('-I' + self.get_builtin_clang_header())

        complete = self.get_completion(
            buf.name, line, col,
            self.get_current_buffer(buf),
            params)
        if complete is None:
            return []

        if self.sort_algo == 'priority':
            def get_priority(x):
                return x.string.priority
            results = sorted(complete.results, key=get_priority)
        elif self.sort_algo == 'alphabetical':
            def get_abbrevation(x):
                return self.get_abbr(x.string).lower()
            results = sorted(complete.results, key=get_abbrevation)
        else:
            results = complete.results

        return list(map(self.parse_candidates, results))

    def get_current_buffer(self, b):
        return [(b.name, '\n'.join(b[:]))]

    def get_abbr(self, strings):
        for chunks in strings:
            if chunks.isKindTypedText():
                return chunks.spelling
        return ""

    def get_minimum_flags(self, filetype):
        flags = ['-x']

        if filetype == 'c':
            flags += ['c', '-std=' + self.std_c]
        elif filetype == 'cpp':
            flags += ['c++', '-std=' + self.std_cpp]
        elif filetype == 'objc':
            flags += ['objective-c', '-std=' + self.std_objc]
        elif filetype == 'objcpp':
            flags += ['objective-c++', '-std=' + self.std_objcpp]

        return flags

    def get_builtin_clang_header(self):
        include_dir = self.clang_header
        if not include_dir:
            return ''
        versions = sorted([d for d in os.listdir(include_dir)
                           if os.path.isdir(os.path.join(include_dir, d))])

        # Use latest clang version
        latest = versions[-1]

        return os.path.join(include_dir, latest, 'include')

    def get_params(self, fname):
        if fname in self.params:
            return self.params[fname]
        else:
            return self.get_compile_params(fname)

    def get_compile_params(self, fname):
        if fname in self.database:
            params = self.database[fname]
        else:
            params = self.get_compilation_database(os.path.abspath(fname))

        header = self.get_builtin_clang_header()
        if header:
            param = '-I' + header

            if param not in params:
                params.append(param)

        self.params[fname] = params
        return params

    def get_commands_for_file(self, fname):
        assert bool(self.compilation_database)

        get_cmds = self.compilation_database.getCompileCommands
        commands = get_cmds(fname)

        if commands is not None:
            return (fname, commands)

        noext_name, extension = os.path.splitext(fname)

        test_for = self.test_extensions.get(extension, None)

        if test_for is not None:
            for test_ext in test_for:
                test_fname = noext_name + test_ext
                commands = get_cmds(test_fname)

                if commands is not None:
                    return (test_fname, commands)

        if self.default_filename:
            test_fname = self.default_filename

            commands = get_cmds(test_fname)
            if commands is not None:
                return (test_fname, commands)

        return (None, None)

    def get_compilation_database(self, fname):
        params = self.completion_flags

        if self.compilation_database:
            used_fname, cmds = self.get_commands_for_file(fname)

            if cmds is not None and cmds[0] is not None:
                cmds = cmds[0]
                cwd = cmds.directory
                skip = 1
                for arg in cmds.arguments:
                    full_path = ''
                    if not os.path.isabs(arg[0]):
                        full_path = os.path.realpath(os.path.join(cwd, arg))
                    if skip or full_path == used_fname or arg in \
                            ['-c', used_fname,
                             os.path.basename(used_fname),
                             full_path]:
                        skip = 0
                        continue
                    elif arg == '-o':
                        skip = 1
                        continue
                    elif arg.startswith('-I'):
                        include_path = arg[2:]
                        if not os.path.isabs(include_path):
                            include_path = os.path.normpath(
                                os.path.join(cwd, include_path))
                        params.append('-I' + include_path)
                        continue
                    params.append(arg)

        self.database[fname] = params
        return params

    def get_translation_unit(self, fname, args, buf):
        # clang.TranslationUnit
        # PARSE_NONE = 0
        # PARSE_DETAILED_PROCESSING_RECORD = 1
        # PARSE_INCOMPLETE = 2
        # PARSE_PRECOMPILED_PREAMBLE = 4
        # PARSE_CACHE_COMPLETION_RESULTS = 8
        # PARSE_SKIP_FUNCTION_BODIES = 64
        # PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION = 128
        flags = 15

        ast_file = fname + ".tu"
        if os.path.exists(ast_file):
            tu = self.index.read(ast_file)
        else:
            tu = self.index.parse(fname, args, buf, flags)
            tu.save(ast_file)
        tu.reparse(buf)
        os.remove(ast_file)

        self.tu_data[fname] = tu

        return tu

    def get_completion(self, fname, line, column, buf, args):
        if fname in self.tu_data:
            tu = self.tu_data[fname]
        else:
            tu = self.get_translation_unit(fname, args, buf)

        return tu.codeComplete(fname, line, column, buf,
                               include_macros=True,
                               include_code_patterns=True,
                               include_brief_comments=False)

    def parse_candidates(self, result):
        completion = {'dup': 1}
        _type = ""
        word = ""
        placeholder = ""

        for chunk in [x for x in result.string if x.spelling]:
            chunk_spelling = chunk.spelling

            if chunk.isKindTypedText():
                word += chunk_spelling
                placeholder += chunk_spelling
                continue

            elif chunk.isKindResultType():
                _type += chunk_spelling
            else:
                placeholder += chunk_spelling

        completion['word'] = word
        completion['abbr'] = completion['info'] = placeholder

        completion['kind'] = ' '.join(
            [(index_h.kinds[result.cursorKind]
              if (result.cursorKind in index_h.kinds)
              else str(result.cursorKind)), _type])

        return completion
