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

if !exists("g:deoplete#sources#clang#flags")
  let g:deoplete#sources#clang#flags = get(g:, 'deoplete#sources#clang#flags', '')
endif

if !exists("g:deoplete#sources#clang#sort_algo")
  let g:deoplete#sources#clang#sort_algo = get(g:, 'deoplete#sources#clang#sort_algo', '')
endif

if !exists("g:deoplete#sources#clang#clang_complete_database")
  let g:deoplete#sources#clang#clang_complete_database = get(g:, 'deoplete#sources#clang#clang_complete_database', '')
endif
