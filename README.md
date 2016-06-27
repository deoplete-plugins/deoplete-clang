# deoplete-clang
|| **Status** |
|---|---|
|**Ubuntu 14.04** |[![Build Status](https://travis-ci.org/zchee/deoplete-clang.svg?branch=master)](https://travis-ci.org/zchee/deoplete-clang)|

C/C++/Objective-C/Objective-C++ source for [deoplete.nvim](https://github.com/Shougo/deoplete.nvim)


## Overview
Asynchronous C/C++/Objective-C/Objective-C++ completion for Neovim.  
Using,

### deoplete.nvim
[Shougo/deoplete.nvim](https://github.com/Shougo/deoplete.nvim)

Dark powered asynchronous completion framework for neovim.  
Fastetst, Fully asynchronous, Nonblocking user interface, Customizable source for each languages, and more.  
The Nextgen word completion.

### libclang-python3
[zchee/libclang-python3](https://github.com/zchee/libclang-python3)

Clang compiler bindings for python.  
but llvm official bindings are Python2 only. It was ported to Python3.  
Original author is @Anteru. I was fork it, and follow the latest of llvm clang.


## Required

### Neovim and neovim/python-client
https://github.com/neovim/neovim  
https://github.com/neovim/python-client

### deoplete.nvim
https://github.com/Shougo/deoplete.nvim

### libclang shared object (dynamic library)
http://llvm.org  
https://github.com/apple/swift-clang


## How to install

### 1. Install Neovim
See Neovim wiki.

- [Installing Neovim](https://github.com/neovim/neovim/wiki/Installing-Neovim)
- [Following HEAD](https://github.com/neovim/neovim/wiki/Following-HEAD)
- [Building](https://github.com/neovim/neovim/wiki/Building-Neovim)

### 2. Install neovim/python-client
Neovim remonte client for python.  
See https://github.com/neovim/python-client

```bash
pip2 install --upgrade neovim
pip3 install --upgrade neovim
```

### 3. Install libclang and clang headers
for linux, e.g. apt family,

```bash
apt-get install clang
```

for OS X, Homebrew way
```bash
brew install llvm --with-clang
```
but not tested. recommend is build from source.  
See http://clang.llvm.org/get_started.html  
or try build-llvm script. Need `cmake`, `ninja` or `Xcode`  

[Build llvm for OS X](https://gist.github.com/zchee/740e99acd893afeeae6d)

### 4. Install deoplete and deoplete-clang
```vim
" dein.vim (fastest)
call dein#add('Shougo/deoplete.nvim')
call dein#add('zchee/deoplete-clang')
" NeoBundle
NeoBundle 'Shougo/deoplete.nvim'
NeoBundle 'zchee/deoplete-clang'
" vim-plug
Plug 'Shougo/deoplete.nvim'
Plug 'zchee/deoplete-clang'
```


## Available Settings

| Setting value | Default | Required |
|:-------------:|:-------:|:--------:|
`g:deoplete#sources#clang#libclang_path` | `''` | **Yes**
`g:deoplete#sources#clang#clang_header` | `''` | **Yes**
`g:deoplete#sources#clang#std` | See this section | No
`g:deoplete#sources#clang#flags` | See this section | No
`g:deoplete#sources#clang#sort_algo` | `''` | No
`g:deoplete#sources#clang#clang_complete_database` | `''` | No

### `g:deoplete#sources#clang#libclang_path`
|||
|---|---|
| **Required** | Yes |
| **Type** | string |
| **Default** | - |
| **Example** | `path/to/lib/libclang.so` |

libclang shared object (dynamic library) file path.  
In linux, `libclang.so`. In OS X, `libclang.dylib`.

Find commands,
```bash
# In linux
(sudo) find / -name libclang.so
# In OS X
mdfind -name libclang.dylib
```

### `g:deoplete#sources#clang#clang_header`
|||
|---|---|
| **Required** | Yes |
| **Type** | string |
| **Default** | - |
| **Example** | `path/to/lib/clang` |

clang built-in include header directory path.  
**Not `clang-c`**. and **not required clang version**.  
deoplete-clang always use latest clang version.

e.g.,

```bash
/opt/llvm/lib/clang
└── 3.9.0
    ├── include
    │   ├── Intrin.h
    │   ├── __clang_cuda_cmath.h
    │   ├── __clang_cuda_runtime_wrapper.h
    │   ├── __stddef_max_align_t.h
    │   ├── __wmmintrin_aes.h
    │   ├── __wmmintrin_pclmul.h
    │   ├── adxintrin.h
    │   ├── altivec.h
    │   ├── ammintrin.h
    │   ├── arm_acle.h
    │   ├── arm_neon.h
    .
    .
    .
    │   ├── stdalign.h
    │   ├── stdarg.h
    │   ├── stdatomic.h
    │   ├── stdbool.h
    │   ├── stddef.h
    │   ├── stdint.h
    .
    .
    .
    │   ├── xsavecintrin.h
    │   ├── xsaveintrin.h
    │   ├── xsaveoptintrin.h
    │   ├── xsavesintrin.h
    │   └── xtestintrin.h
    ├── lib
    │   └── darwin
    └── vtables_blacklist.txt
```

### `g:deoplete#sources#clang#std`
|||
|---|---|
| **Required** | No |
| **Type** | dict |
| **C Default** | `c11` |
| **C++ Default** | `c++1z` |
| **Objective-C Default** | `c11` |
| **Objective-C++ Default** | `c++1z` |
| **Example** | `{'c': 'c11', 'cpp': 'c++1z', 'objc': 'c11', 'objcpp': 'c++1z'}` |

Each C family language standard version.  
By default, use clang supported latest version.

### `g:deoplete#sources#clang#flags`
|||
|---|---|
| **Required** | No |
| **Type** | list |
| **C Default** | `['-x', 'c']` |
| **C++ Default** | `['-x', 'c++']` |
| **Objective-C Default** | `['-x', 'objective-c']` |
| **Objective-C++ Default** | `['-x', 'objective-c++']` |
| **Example** | `["-fblocks",]` |

`C(XX)FLAGS` for generate completion word.  
Setting value **other than default**. Not needs `-x c` or etc.

If you want to know default clang build flags, try

```bash
# C
echo | clang -v -E -x c -
# C++
echo | clang -v -E -x c++ -
# Objective-C
echo | clang -v -E -x objective-c -
# Objective-C++
echo | clang -v -E -x objective-c++ -
```

e.g. In OS X,

```vim
let g:deoplete#sources#clang#flags = [
      \ "-cc1",
      \ "-triple", "x86_64-apple-macosx10.11.0",
      \ "-isysroot", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk",
      .
      .
      .
      \ "-fmax-type-align=16",
      \ ]
```

### `g:deoplete#sources#clang#sort_algo`
|||
|---|---|
| **Required** | No |
| **Type** | string |
| **Default** | `''` |
| **Example** | `priority` or `alphabetical` |

libclang completion result sort algorism. Available value are `priority` or `alphabetical`.  

By defalut(`''`), use deoplete.nvim sort algorism.  
`priority`, Sort by libclang determine priority.  
`alphabetical`, Sort by alphabetical order.


### `g:deoplete#sources#clang#clang_complete_database`
|||
|---|---|
| **Required** | No |
| **Type** | string |
| **Default** | `''` |
| **Example** | `/path/to/neovim/build` |

Support Clang JSON Compilation Database Format Specification.  
See http://clang.llvm.org/docs/JSONCompilationDatabase.html.

Setting value are **must be exists `compile_commands.json` directory**.  
This setting is **optional**.

If set it, use instead of `g:deoplete#sources#clang#flags`.  
but, Currently parse `compile_commands.json` will take time.  
Please set only if you really need support compilation database.

I'm planning more parse speed rewrite in Go.  
Just moments.

## FAQ

### deoplete-clang does not support header names completion?

It is not supported.  You should use neoinclude plugin instead.
https://github.com/Shougo/neoinclude.vim
