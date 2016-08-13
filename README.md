# deoplete-clang
|| **Status** |
|---|---|
|**Ubuntu 14.04** |[![Build Status](https://travis-ci.org/zchee/deoplete-clang.svg?branch=master)](https://travis-ci.org/zchee/deoplete-clang)|

C/C++/Objective-C/Objective-C++ source for [deoplete.nvim](https://github.com/Shougo/deoplete.nvim)


## Overview
Deoplete-clag offers asynchronous completion of code written in C, C++,
Objective-C and Objective-C++ inside of Neovim. It is built upon the following
tools:

### deoplete.nvim
[Shougo/deoplete.nvim](https://github.com/Shougo/deoplete.nvim)

The *dark powered asynchronous completion framework* for neovim.  It offers a
fast, fully asynchronous, nonblocking user interface, customizable sources for
each languages, and more.  The Next generation of word completion.

### libclang-python3
[zchee/libclang-python3](https://github.com/zchee/libclang-python3)

A Python 3 port of the official clang compiler bindings for Python. The
original author is @Anteru, I forked it and follow the latest of llvm clang.


## Requirements

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
See the Neovim wiki.

- [Installing Neovim](https://github.com/neovim/neovim/wiki/Installing-Neovim)
- [Following HEAD](https://github.com/neovim/neovim/wiki/Following-HEAD)
- [Building](https://github.com/neovim/neovim/wiki/Building-Neovim)

### 2. Install the neovim/python-client
Neovim remonte client for python.  
See https://github.com/neovim/python-client

```bash
pip2 install --upgrade neovim
pip3 install --upgrade neovim
```

### 3. Install libclang and clang headers
For GNU/Linux, e.g. apt family,

```bash
apt-get install clang
```

for macOS, Homebrew way
```bash
brew install llvm --with-clang
```
This has not been tested, it is recommended to build from source.  See
http://clang.llvm.org/get_started.html  or try the build-llvm script. You will
need `cmake`, `ninja` or `Xcode`  

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

The libclang shared object (dynamic library) file path. On GNU/Linux the file
name is `libclang.so`. On macOS it is `libclang.dylib`.

If you have trouble locating the library you can use the `find` command,
```bash
# On GNU/Linux
[sudo] find / -name libclang.so
# On macOS
mdfind -name libclang.dylib
```

### `g:deoplete#sources#clang#clang_header`
|||
|---|---|
| **Required** | Yes |
| **Type** | string |
| **Default** | - |
| **Example** | `path/to/lib/clang` |

The clang built-in include header directory path; **not `clang-c`**, and **not
the required clang version**. Deoplete-clang always use the latest clang
version.

Example:

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

The standard version for each of the C family languages. By default, use the
lastest version supported by clang.

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

`C(XX)FLAGS` for generating completions. Setting value **other than default**.
Does not need `-x c` or similar.

If you want to know the default clang build flags your of your installation you
can try

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

For example, on macOS the settings would correspond to:

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

The sorting algorithm for libclang completion results. Available values are
`priority` or `alphabetical`.  

By defalut (`''`) use the deoplete.nvim sort algorithm.  `priority` sorts the
way libclang determines priority, `alphabetical` sorts by alphabetical order.


### `g:deoplete#sources#clang#clang_complete_database`
|||
|---|---|
| **Required** | No |
| **Type** | string |
| **Default** | `''` |
| **Example** | `/path/to/neovim/build` |

Support a clang JSON compilation database format specification; see
http://clang.llvm.org/docs/JSONCompilationDatabase.html for more information.

The setting value **must be an existing `compile_commands.json` directory**.
This setting is **optional**.

When this setting is used the compilation database file will take precedence
over the `g:deoplete#sources#clang#flags` setting. Parsing the compilation
database file will take some time, so please on use this setting if you really
need to support a compilation database.

I'm planning the rewrite the parser in Go for faster parsing in the future.


## FAQ

### deoplete-clang does not support header names completion?

This is not supported. You should use the neoinclude plugin instead:
https://github.com/Shougo/neoinclude.vim
