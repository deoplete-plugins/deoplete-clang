import sys
import clang.cindex

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
        self.input_pattern = r''
        self.rank = 500

    def get_complete_position(self, context):
        return -1

    def gather_candidates(self, context):
        return []
