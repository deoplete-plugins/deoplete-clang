if exists('g:loaded_deoplete_clang')
  finish
endif
let g:loaded_deoplete_clang = 1

let g:deoplete#sources#clang#libclang_path =
      \ get(g:, 'deoplete#sources#clang#libclang_path', '')

let g:deoplete#sources#clang#clang_header =
      \ get(g:, 'deoplete#sources#clang#clang_header', '')

let g:deoplete#sources#clang#std#c =
      \ get(g:, 'deoplete#sources#clang#std#c', 'c11')

let g:deoplete#sources#clang#std#cpp =
      \ get(g:, 'deoplete#sources#clang#std#cpp', 'c++1z')

let g:deoplete#sources#clang#std#objc =
      \ get(g:, 'deoplete#sources#clang#std#objc', 'c11')

let g:deoplete#sources#clang#std#objcpp =
      \ get(g:, 'deoplete#sources#clang#std#objcpp', 'c++1z')

let g:deoplete#sources#clang#flags =
      \ get(g:, 'deoplete#sources#clang#flags', [])

let g:deoplete#sources#clang#sort_algo =
      \ get(g:, 'deoplete#sources#clang#sort_algo', '')

let g:deoplete#sources#clang#clang_complete_database =
      \ get(g:, 'deoplete#sources#clang#clang_complete_database', '')
