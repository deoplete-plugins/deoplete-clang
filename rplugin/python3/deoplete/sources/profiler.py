class bcolors:
    RED = '\033[1;41m'
    GREEN = '\033[1;42m'
    YELLOW = '\033[1;43m'
    BLUE = '\033[1;44m'
    MAGENTA = '\033[1;45m'
    CYAN = '\033[1;46m'
    ENDC = '\033[0m'


def timeit(fmt, threshold, logger):
    from json import dumps
    import time
    import os.path

    def is_json(json_data):
        try:
            json_object = dumps(json_data, indent=4)
        except ValueError:
            return False
        else:
            return json_object

    def timereald(method):
        def timed(*args, **kw):

            start = time.clock()
            result = method(*args, **kw)
            end = time.clock()

            obj, value = args
            data = is_json(value) if False else value

            sec = (end - start)
            sec_color = bcolors.RED
            if sec <= threshold[0]:
                sec_color = bcolors.BLUE
            elif sec <= threshold[1]:
                sec_color = bcolors.GREEN

            if fmt == 'simple':
                logger.debug("\nName: %r\nClock: %s%2.8f%s sec" %
                             (method.__name__,
                              sec_color,
                              sec,
                              bcolors.ENDC,
                              ))
            else:
                logger.debug("\nName: %r\nClock: %s%2.8f%s sec\nObj: %s\nkw: %s\n%s" %
                             (method.__name__,
                              sec_color,
                              sec,
                              bcolors.ENDC,
                              obj,
                              kw,
                              data,
                              ))
            return result
        return timed
    return timereald


def profile(sort='cumulative', lines=50, strip_dirs=False):
    import cProfile
    import tempfile
    import pstats

    def outer(fun):
        def inner(*args, **kwargs):
            file = tempfile.NamedTemporaryFile()
            prof = cProfile.Profile()
            try:
                ret = prof.runcall(fun, *args, **kwargs)
            except:
                file.close()
                raise

            prof.dump_stats(file.name)
            stats = pstats.Stats(file.name)
            if strip_dirs:
                stats.strip_dirs()
            if isinstance(sort, (tuple, list)):
                stats.sort_stats(*sort)
            else:
                stats.sort_stats(sort)
            stats.print_stats(lines)

            file.close()
            return ret
        return inner

    # in case this is defined as "@profile" instead of "@profile()"
    if hasattr(sort, '__call__'):
        fun = sort
        sort = 'cumulative'
        outer = outer(fun)
    return outer

# fp=open(os.path.expanduser('~/.log/nvim/python/deoplete-clang.log'), 'w+')
# @profile(stream=fp)
# @cProfiler(gather_candidates)
# @timecall(immediate=True)
# @profile(filename=os.path.expanduser('~/.log/nvim/python/deoplete-clang.log'), immediate=False, stdout=False)
# @profile_this

def cProfiler():
    import cProfile
    import pstats

    def _f(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        logger.debug("\n<<<---")
        # res = func(*args, **kwargs)
        p = pstats.Stats.dump_stats(self, os.path.expanduser(
            '~/.log/nvim/python/deoplete-clang.log'))
        logger.debug(p.strip_dirs().sort_stats('cumtime').print_stats(20))
        logger.debug("\n--->>>")
        logger.debug(str(_f))
        # return res
    return _f


def profile(func):
    def _f(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        print("\n<<<---")
        res = func(*args, **kwargs)
        p = pstats.Stats(pr)
        p.strip_dirs().sort_stats('cumtime').print_stats(20)
        print("\n--->>>")
        return res
    return _f


def profile_this(fn):
    import cProfile
    import pstats

    def profiled_fn(*args, **kwargs):
        # name for profile dump
        fpath = os.path.expanduser('~/.log/nvim/python/deoplete-clang.log')
        prof = cProfile.Profile()
        logger.debug("\n<<<---")
        ret = prof.runcall(fn, *args, **kwargs)
        p = pstats.Stats(prof)
        logger.debug(str(p.print_stats(20)))
        logger.debug("\n--->>>")
        return ret
    return profiled_fn
