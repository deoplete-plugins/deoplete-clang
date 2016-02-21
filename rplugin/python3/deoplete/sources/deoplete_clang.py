import os
import re
import sys

from deoplete.sources.base import Base

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from clang_data import ClangData
from helper import get_var
from helper import load_external_module
from helper import set_debug

load_external_module('clang')
import clang.cindex as cl

from logging import getLogger
logger = getLogger(__name__)

# Profiler
from profiler import timeit
# PyVmMonitor_dir = '/Applications/PyVmMonitor.app/Contents/MacOS/public_api'
# sys.path.append(PyVmMonitor_dir)
# import pyvmmonitor
# @pyvmmonitor.profile_method()


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'clang'
        self.mark = '[clang]'
        self.filetypes = ['c', 'cpp', 'objc', 'objcpp']
        self.rank = 500
        # TODO(zchee): not need "r'[a-zA-Z_]\w*::\w*'" in C language
        self.input_pattern = (r'[^. \t0-9]\.\w*|'
                              r'[^. \t0-9]->\w*|'
                              r'[a-zA-Z_]\w*::\w*')

        self.library_path = \
            self.vim.vars['deoplete#sources#clang#libclang_path']
        self.clang_header = \
            self.vim.vars['deoplete#sources#clang#clang_header']
        self.completion_flags = \
            self.vim.vars["deoplete#sources#clang#flags"]
        self.sort_algo = \
            self.vim.vars["deoplete#sources#clang#sort_algo"]

        cl.Config.set_library_file(str(self.library_path))
        cl.Config.set_compatibility_check(False)

        clang_complete_database = \
            self.vim.vars['deoplete#sources#clang#clang_complete_database']
        if clang_complete_database != '':
            self.compilation_database = \
                cl.CompilationDatabase.fromDirectory(clang_complete_database)
        else:
            self.compilation_database = None

        self.index = cl.Index.create()
        # TODO(zchee): More elegant way
        self.tu_data, self.params, self.database = dict(), dict(), dict()

        # debug
        if get_var(self.vim, 'deoplete#enable_debug'):
            log_file = get_var(
                self.vim, 'deoplete#sources#clang#debug#log_file')
            set_debug(logger, os.path.expanduser(log_file))

    # @timeit(logger, 'simple', [0.00003000, 0.00015000])
    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    @timeit(logger, 'simple', [0.02000000, 0.05000000])
    def gather_candidates(self, context):
        # faster than self.vim.current.window.cursor[0]
        line = self.vim.eval("line('.')")
        col = (context['complete_position'] + 1)
        buf = self.vim.current.buffer
        if self.compilation_database:
            args = self.get_params(buf.name)
        else:
            args = dict().fromkeys(['args'], [])
            args['args'] = self.completion_flags

        complete = \
            self.get_completion(
                buf.name, line, col,
                self.get_current_buffer(buf),
                args)
        if complete is None:
            return []

        if self.sort_algo == 'priority':
            getPriority = lambda x: x.string.priority
            results = sorted(complete.results, key=getPriority)
        elif self.sort_algo == 'alphabetical':
            getAbbrevation = lambda x: self.get_abbr(x.string).lower()
            results = sorted(complete.results, key=getAbbrevation)
        else:
            results = complete.results

        return list(map(self.parse_candidates, results))

    # @timeit(logger, 'simple', [0.20000000, 0.30000000])
    def get_current_buffer(self, b):
        return [(b.name, '\n'.join(b[:]))]

    def get_abbr(self, strings):
        for chunks in strings:
            if chunks.isKindTypedText():
                return chunks.spelling
        return ""

    # @timeit(logger, 'simple', [0.00000200, 0.00000400])
    def get_params(self, fname):
        if self.params.get(fname) != None:
            return self.params.get(fname)
        else:
            return self.get_compile_params(fname)

    # @timeit(logger, 'simple', [0.00200000, 0.00300000])
    def get_compile_params(self, fname):
        if self.database.get(fname) != None:
            params = self.database.get(fname)
        else:
            params = self.get_compilation_database(os.path.abspath(fname))

        args = [params]

        versions = os.listdir(self.clang_header)
        sorted(versions)
        version = versions[-1]

        headers = os.path.join(self.clang_header, version, 'include')
        for path in os.listdir(headers):
            args.append('-I' + os.path.join(self.clang_header + version + path))

        self.params[fname] = {'args': args}
        return {'args': args}

    # @timeit(logger, 'simple', [0.00200000, 0.00300000])
    def get_compilation_database(self, fname):
        query = dict(args=self.completion_flags)

        # logger.debug(list(self.compilation_database.getCompileCommands(fname)[0].arguments))
        if self.compilation_database:
            cmds = self.compilation_database.getCompileCommands(fname)[0]
            if cmds != None:
                cwd = cmds.directory
                args = []
                skip = 1
                for arg in cmds.arguments:
                    if skip or arg in \
                            ['-c', fname,
                             os.path.realpath(os.path.join(cwd, arg))]:
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
                        args.append('-I' + include_path)
                        continue
                    else:
                        args.append(arg)

        directory = fname.rsplit('/', 1)
        args.append('-I' + directory[0])
        args.append('-I' + os.path.join(directory[0], 'include'))
        # logger.debug(args)

        self.database[fname] = {'args': args}
        return {'args': args}

    # @timeit(logger, 'simple', [0.00000200, 0.00000400])
    def get_translation_unit(self, fname, args, buf_data):
        # cl.TranslationUnit
        # PARSE_NONE = 0
        # PARSE_DETAILED_PROCESSING_RECORD = 1
        # PARSE_INCOMPLETE = 2
        # PARSE_PRECOMPILED_PREAMBLE = 4
        # PARSE_CACHE_COMPLETION_RESULTS = 8
        # PARSE_SKIP_FUNCTION_BODIES = 64
        # PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION = 128
        flags = 15
        tu = self.index.parse(fname, args, buf_data, flags)

        self.tu_data[fname] = tu
        tu.reparse(buf_data)

        return tu

    # @timeit(logger, 'simple', [0.01500000, 0.02500000])
    def get_completion(self, fname, line, column, buf_data, args):
        if self.tu_data.get(fname) != None:
            tu = self.tu_data.get(fname)
        else:
            tu = self.get_translation_unit(fname, args, buf_data)

        return tu.codeComplete(fname, line, column, buf_data,
                               include_macros=False,
                               include_code_patterns=False,
                               include_brief_comments=False)

    # @timeit(logger, 'verbose', [0.00000500, 0.00002000])
    def parse_candidates(self, result):
        completion = dict().fromkeys(['word', 'abbr', 'kind', 'info'], "")
        completion['dup'] = 1
        _type = ""
        word = ""
        abbr = ""
        info = ""

        for chunk in result.string:
            chunk_spelling = chunk.spelling

            if chunk.isKindInformative() or chunk.isKindPlaceHolder() or \
                    str(chunk.kind) == 'Comma' or \
                    chunk_spelling == None:
                continue

            elif chunk.isKindResultType():
                _type += chunk_spelling
                continue

            elif chunk.isKindTypedText():
                abbr += chunk_spelling
                word += chunk_spelling
                info += chunk_spelling
                continue
            else:
                word += chunk_spelling
                info += chunk_spelling

        completion['word'] = word
        completion['abbr'] = abbr
        completion['info'] = info

        if result.cursorKind in ClangData.kinds:
            completion['kind'] = ' '.join(
                [ClangData.kinds[result.cursorKind], _type])
        else:
            completion['kind'] = ' '.join(
                [str(result.cursorKind), _type])

        return completion
