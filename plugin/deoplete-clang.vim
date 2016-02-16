if exists('g:loaded_deoplete_clang')
  finish
endif
let g:loaded_deoplete_clang = 1

if !exists("g:deoplete#sources#clang#libclang_path")
  let g:deoplete#sources#clang#libclang_path = get(g:, 'deoplete#sources#clang#libclang_path', '')
endif

if !exists("g:deoplete#sources#clang#clang_header")
  let g:deoplete#sources#clang#clang_header = get(g:, 'deoplete#sources#clang#clang_header', '')
endif

if !exists("g:deoplete#sources#clang#debug_log")
  let g:deoplete#sources#clang#debug_log = get(g:, 'deoplete#sources#clang#debug_log', '')
endif
