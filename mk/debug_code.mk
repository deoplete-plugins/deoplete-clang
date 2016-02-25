SET_DEBUG_PREFIX := self.tu_data, self.params, self.database = dict(), dict(), dict()
SET_DEBUG := try:\n            from helper import set_debug\n            if self.vim.vars["deoplete\#enable_debug"]:\n                log_file \= self.vim.vars["deoplete\#sources\#clang\#debug\#log_file"]\n                set_debug(logger, os.path.expanduser(log_file))\n        except Exception:\n            pass\n
TIMEIT_PREFIX := @timeit(logger, 
TIMEIT_SUFFIX := )
TIMEIT_GET_COMPLETE_POSITION := ${TIMEIT_PREFIX}"simple", [0.00003000, 0.00015000]${TIMEIT_SUFFIX}
TIMEIT_GATHER_CANDIDATES := ${TIMEIT_PREFIX}"simple", [0.02000000, 0.05000000]${TIMEIT_SUFFIX}
TIMEIT_GET_CURRENT_BUFFER := ${TIMEIT_PREFIX}"simple", [0.20000000, 0.30000000]${TIMEIT_SUFFIX}
TIMEIT_GET_PARAMS := ${TIMEIT_PREFIX}"simple", [0.00000200, 0.00000400]${TIMEIT_SUFFIX}
TIMEIT_GET_COMPILE_PARAMS := ${TIMEIT_PREFIX}"simple", [0.00200000, 0.00300000]${TIMEIT_SUFFIX}
TIMEIT_GET_COMPILATION_DATABASE := ${TIMEIT_PREFIX}"simple", [0.00200000, 0.00300000]${TIMEIT_SUFFIX}
TIMEIT_GET_TRANSLATION_UNIT := ${TIMEIT_PREFIX}"simple", [0.00000200, 0.00000400]${TIMEIT_SUFFIX}
TIMEIT_GET_COMPLETION := ${TIMEIT_PREFIX}"simple", [0.01500000, 0.02500000]${TIMEIT_SUFFIX}
TIMEIT_PARSE_CANDIDATES := ${TIMEIT_PREFIX}"verbose", [0.00000500, 0.00002000]${TIMEIT_SUFFIX}

LOGGER_GET_COMPILE_PARAMS := logger.debug(params)
LOGGER_GET_COMPILE_PARAMS_SUFFIX := self.params\[fname\] = params

LOGGER_GET_COMPILATION_DATABASE_BEFORE := logger.debug(list(self.compilation_database.getCompileCommands(fname)[0].arguments))
LOGGER_GET_COMPILATION_DATABASE_BEFORE_SUFFIX := if self.compilation_database:

LOGGER_GET_COMPILATION_DATABASE_AFTER := logger.debug(params)
LOGGER_GET_COMPILATION_DATABASE_AFTER_SUFFIX := self.database\[fname\] = params
