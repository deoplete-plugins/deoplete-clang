# Colorable output
include mk/color.mk
# Snippets for debug and profiling
include mk/debug_code.mk

RPLUGIN_PATH := ./rplugin/python3/deoplete/sources/
MODULE_NAME := deoplete_clang.py

DEOPLETE_CLANG := ${RPLUGIN_PATH}${MODULE_NAME}
CLANG_DATA := ${RPLUGIN_PATH}/deoplete_clang/clang_data.py
HELPER := ${RPLUGIN_PATH}/deoplete_clang/helper.py
PROFILER := ${RPLUGIN_PATH}/deoplete_clang/profiler.py

all: autopep8

test: test_modules flake8

test_modules:
	pip3 install -U -r ./test/requirements.txt

flake8:
	@flake8 -v --config=$(PWD)/.flake8 ${DEOPLETE_CLANG} ${HELPER} ${PROFILER} || true

autopep8: clean
	@autopep8 -i ${DEOPLETE_CLANG}

clean:
	@echo "Cleanup debug code in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n        try:.*    def get_complete_position/\n    def get_complete_position/g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i ':a;N;$$!ba;s/from profiler import timeit\n//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i ':a;N;$$!ba;s/from logging import getLogger\nlogger = getLogger(__name__)\n\n//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i 's/^    @timeit.*$$//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i 's/^        logger.*$$//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py

set_debug:
	@sed -i ':a;N;$$!ba;s/${SET_DEBUG_PREFIX}\n\n    def get_complete_position/${SET_DEBUG_PREFIX}\n\n        ${SET_DEBUG}\n    def get_complete_position/g' ./rplugin/python3/deoplete/sources/deoplete_clang.py

import_logger: set_debug
	@sed -i ':a;N;$$!ba;s/from clang_data import index_h\n\n\nclass Source/from clang_data import index_h\n\nfrom logging import getLogger\nlogger = getLogger(__name__)\n\n\nclass Source/g' ${DEOPLETE_CLANG}

import_timeit: set_debug
	@sed -i ':a;N;$$!ba;s/\n\n\nclass Source/\n\nfrom profiler import timeit\n\nclass Source/g' ${DEOPLETE_CLANG}

timeit-get_complete_position: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPLETE_POSITION}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-gather_candidates: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GATHER_CANDIDATES}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-get_current_buffer: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_CURRENT_BUFFER}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-get_params: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_PARAMS}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-get_compile_params: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPILE_PARAMS}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-get_compilation_database: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPILATION_DATABASE}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-get_translation_unit: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_TRANSLATION_UNIT}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-get_completion: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPLETION}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

timeit-parse_candidates: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_PARSE_CANDIDATES}\n    def $(subst timeit-,,$@)/g' ${DEOPLETE_CLANG}

logger-get_compile_params: import_logger
	@echo "Enable $(subst logger-,,$@) debug logger in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n        ${LOGGER_GET_COMPILE_PARAMS_SUFFIX}/\n\n        ${LOGGER_GET_COMPILE_PARAMS}\n        ${LOGGER_GET_COMPILE_PARAMS_SUFFIX}/g' ${DEOPLETE_CLANG}

logger-get_compilation_database: import_logger
	@echo "Enable $(subst logger-,,$@) debug logger in ${CYELLOW}${DEOPLETE_CLANG}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n        ${LOGGER_GET_COMPILATION_DATABASE_BEFORE_SUFFIX}/\n\n        ${LOGGER_GET_COMPILATION_DATABASE_BEFORE}\n        ${LOGGER_GET_COMPILATION_DATABASE_BEFORE_SUFFIX}/g' ${DEOPLETE_CLANG}
	@sed -i ':a;N;$$!ba;s/\n\n        ${LOGGER_GET_COMPILATION_DATABASE_AFTER_SUFFIX}/\n\n        ${LOGGER_GET_COMPILATION_DATABASE_AFTER}\n        ${LOGGER_GET_COMPILATION_DATABASE_AFTER_SUFFIX}/g' ${DEOPLETE_CLANG}

.PHONY: autopep8 flake8 clean set_debug import_timeit
