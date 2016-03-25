" Tiny init.vim for deoplete-clang
set runtimepath+=$HOME/src/github.com/Shougo/deoplete.nvim
set runtimepath+=$HOME/src/github.com/zchee/deoplete-clang

let g:deoplete#enable_at_startup = 1
let g:deoplete#enable_smart_case = 1
let g:deoplete#file#enable_buffer_path = 1

let g:deoplete#sources#clang#libclang_path = "/opt/llvm/lib/libclang.dylib"
let g:deoplete#sources#clang#clang_header = '/opt/llvm/lib/clang'
" let g:deoplete#sources#clang#sort_algo = 'priority' " alphabetical

filetype plugin indent on
syntax on
