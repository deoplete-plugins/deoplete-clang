#!/usr/bin/env python3

import clang.cindex
import sys
import os.path

if len(sys.argv) != 3:
    print("Usage: complete.py [libclang.(so|dylib)] [cpp file]")
    sys.exit()

clang.cindex.Config.set_library_file(sys.argv[1])
index = clang.cindex.Index.create()

translation_unit = index.parse(
    os.path.abspath(sys.argv[2]),
    ['-x', 'c++', '-std=c++11'])

complete = translation_unit.codeComplete(sys.argv[2], 6, 11)
print(list(complete.results))
