" Tiny init.vim for deoplete-clang
set runtimepath+=$HOME/src/github.com/Shougo/deoplete.nvim
set runtimepath+=$HOME/src/github.com/zchee/deoplete-clang

let g:deoplete#enable_at_startup = 1
let g:deoplete#enable_smart_case = 1
let g:deoplete#file#enable_buffer_path = 1

let g:deoplete#sources#clang#libclang_path = "/opt/llvm/lib/libclang.dylib"
let g:deoplete#sources#clang#clang_header = '/opt/llvm/lib/clang'
" let g:deoplete#sources#clang#sort_algo = 'priority' " alphabetical

" clang default include flags for OS X
"   - echo | clang -v -E -x c -
let g:deoplete#sources#clang#flags = [
      \ "-cc1",
      \ "-triple", "x86_64-apple-macosx10.11.0",
      \ "-emit-obj",
      \ "-mrelax-all",
      \ "-disable-free",
      \ "-disable-llvm-verifier",
      \ "-mrelocation-model", "pic",
      \ "-pic-level", "2",
      \ "-mthread-model", "posix",
      \ "-mdisable-fp-elim",
      \ "-munwind-tables",
      \ "-target-cpu", "core2",
      \ "-target-linker-version", "264.3",
      \ "-dwarf-column-info",
      \ "-debugger-tuning=lldb",
      \ "-resource-dir", "/opt/llvm/lib/clang/3.9.0",
      \ "-isysroot", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk",
      \ "-ferror-limit", "19",
      \ "-fmessage-length", "213",
      \ "-stack-protector", "1",
      \ "-fblocks",
      \ "-fobjc-runtime=macosx-10.11.0",
      \ "-fencode-extended-block-signature",
      \ "-fmax-type-align=16",
      \ ]

filetype plugin indent on
syntax on
