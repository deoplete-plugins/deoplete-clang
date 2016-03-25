## Problems summary


## Expected


## Environment Information

 - OS:
 - Neovim version:


## Provide a minimal init.vim with less than 50 lines and not plugin manager (Required!)

```vim
" Your minimal init.vim
set runtimepath+=~/path/to/deoplete.nvim/
set runtimepath+=~/path/to/deoplete-clang/
let g:deoplete#enable_at_startup = 1
```

or, try use it [tests/deoplete-clang.vim](../tests/deoplete-clang.vim)


## The reproduce ways from neovim starting (Required!)

 1. foo
 2. bar
 3. baz


## Generate a logfile if appropriate

1. Set environment variables for neovim Python remote plugin

        export NVIM_PYTHON_LOG_FILE=/tmp/log
        export NVIM_PYTHON_LOG_LEVEL=DEBUG

2. Run nvim

        nvim -u minimal.vimrc

3. some works
3. cat /tmp/log_{PID}


## Screen shot (if possible)


## Upload the log file
 - `NVIM_PYTHON_LOG_FILE`
 - `$HOME`/.nvimlog

