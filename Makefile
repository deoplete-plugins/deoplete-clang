# Colorable output
include mk/color.mk
# Snippets for debug and profiling
include mk/debug_code.mk

RPLUGIN_PATH := ./rplugin/python3/deoplete/sources/
MODULE_NAME := deoplete_clang.py
MODULE_PATH := ${RPLUGIN_PATH}${MODULE_NAME}

all: clean

clean:
	@echo "Cleanup debug code in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n        try:.*    def get_complete_position/\n    def get_complete_position/g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i ':a;N;$$!ba;s/from profiler import timeit\n//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i ':a;N;$$!ba;s/logger = getLogger(__name__)\n\n//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i 's/^    @timeit.*$$//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i 's/^        logger.*$$//g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i ':a;N;$$!ba;s/\n\n        self.database\[fname\] = params/\n        self.database\[fname\] = params/g' ./rplugin/python3/deoplete/sources/deoplete_clang.py
	@sed -i ':a;N;$$!ba;s/params = self.completion_flags\n\n\n/params = self.completion_flags\n\n/g' ./rplugin/python3/deoplete/sources/deoplete_clang.py

set_debug:
	@sed -i ':a;N;$$!ba;s/${SET_DEBUG_PREFIX}\n\n    def get_complete_position/${SET_DEBUG_PREFIX}\n\n        ${SET_DEBUG}\n    def get_complete_position/g' ./rplugin/python3/deoplete/sources/deoplete_clang.py

import_logger: set_debug
	@sed -i ':a;N;$$!ba;s/from clang_data import index_h\n\n\nclass Source/from clang_data import index_h\n\nlogger = getLogger(__name__)\n\n\nclass Source/g' ${MODULE_PATH}

import_timeit: set_debug
	@sed -i ':a;N;$$!ba;s/\n\n\nclass Source/\n\nfrom profiler import timeit\n\nclass Source/g' ${MODULE_PATH}

timeit-get_complete_position: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPLETE_POSITION}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-gather_candidates: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GATHER_CANDIDATES}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-get_current_buffer: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_CURRENT_BUFFER}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-get_params: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_PARAMS}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-get_compile_params: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPILE_PARAMS}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-get_compilation_database: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPILATION_DATABASE}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-get_translation_unit: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_TRANSLATION_UNIT}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-get_completion: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_GET_COMPLETION}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

timeit-parse_candidates: import_timeit
	@echo "Enable $(subst timeit-,,$@) @timeit decorator in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n    def $(subst timeit-,,$@)/\n\n    ${TIMEIT_PARSE_CANDIDATES}\n    def $(subst timeit-,,$@)/g' ${MODULE_PATH}

logger-get_compile_params: import_logger
	@echo "Enable $(subst logger-,,$@) debug logger in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n        self.params\[fname\] = params/\n\n        ${LOGGER_GET_COMPILE_PARAMS}\n        self.params\[fname\] = params/g' ${MODULE_PATH}

logger-get_compilation_database: import_logger
	@echo "Enable $(subst logger-,,$@) debug logger in ${CYELLOW}${MODULE_PATH}${CRESET}..."
	@sed -i ':a;N;$$!ba;s/\n\n        if self.compilation_database:/\n\n        ${LOGGER_GET_COMPILATION_DATABASE_BEFORE}\n        if self.compilation_database:/g' ${MODULE_PATH}
	@sed -i ':a;N;$$!ba;s/\n\n        self.database\[fname\] = params/\n\n        ${LOGGER_GET_COMPILATION_DATABASE_AFTER}\n        self.database\[fname\] = params/g' ${MODULE_PATH}

.PHONY: clean set_debug import_timeit
