import os
import sys

from .base import Base

from deoplete.util import charpos2bytepos
from deoplete.util import debug
from deoplete.util import error

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    clang_dir = os.path.join(os.path.dirname(current_dir), 'clang')
    sys.path.insert(0, clang_dir)
    import clang.cindex as clang
except ImportError:
    # TODO(zchee) Not use 'import neovim'. instead of deoplete.error
    import neovim
    neovim.Nvim.command("echoerr 'cant find clang-python3 module'")


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'clang'
        self.mark = '[clang]'
        self.filetypes = ['c', 'cpp', 'objc', 'objcpp']
        # TODO(zchee): not need "r'[a-zA-Z_]\w*::\w*'" in C
        self.input_pattern = (r'[^. \t0-9]\.\w*|'
                              r'[^. \t0-9]->\w*|'
                              r'[a-zA-Z_]\w*::\w*')
        self.rank = 500

        # Load libclang shared library
        library_path = self.vim.vars['deoplete#sources#clang#libclang_path']
        clang.Config.set_library_path(library_path)
        clang.Config.set_compatibility_check(False)
        self.clang_header = self.vim.vars[
            'deoplete#sources#clang#clang_header']

    def get_complete_position(self, context):
        return -1

    def gather_candidates(self, context):
        return []
