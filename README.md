```vim
" deoplete-clang
" libclang shared library path
let g:deoplete#sources#clang#libclang_path = '/opt/llvm/lib/libclang.dylib'
" or
let g:deoplete#sources#clang#libclang_path = '/opt/llvm/lib/libclang.so'

" clang builtin header path
let g:deoplete#sources#clang#clang_header = '/opt/llvm/lib/clang'

" libclang default compile flags
let g:deoplete#sources#clang#flags = ['-x', 'c', '-std=c11']
" or c++
let g:deoplete#sources#clang#flags = ['-x', 'c++', '-std=c++11']

" libclang complete result sort algorism
" Default: '' -> deoplete.nvim delault sort order
" libclang priority sort order
let g:deoplete#sources#clang#sort_algo = 'priority'
" alphabetical sort order
let g:deoplete#sources#clang#sort_algo = 'alphabetical'

" compile_commands.json directory path
" Not file path. Need build directory path
let g:deoplete#sources#clang#clang_complete_database = '/path/to/neovim/build'

" debug
let g:deoplete#enable_debug = 1
let g:deoplete#sources#clang#debug#log_file = '~/.log/nvim/python/deoplete-clang.log'
```
