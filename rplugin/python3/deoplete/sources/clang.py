from .base import Base

from deoplete.util import charpos2bytepos
from deoplete.util import debug
from deoplete.util import error

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'clang'
        self.mark = '[clang]'
        self.filetypes = ['c', 'cpp', 'objc', 'objcpp']
        self.input_pattern = r''
        self.rank = 500

    def get_complete_position(self, context):
        return

    def gather_candidates(self, context):
        return
