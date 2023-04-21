#!/usr/bin/env python

# thanks to some weirdness, this program requires a linked in binary file
# but also thanks to weirdness with generating that binary file, ld 
# needs to be run from the working directory of the input
# or else it gets extra underscores in the symbols. This mess of 
# python makes sure we execute in the correct working directory
# and works out the absolute path of the output
#
# this can then be called from within a meson generator

import sys
import pathlib
import subprocess

try:
    i = sys.argv[2]
    o = sys.argv[1]
    ld = sys.argv[3]
    arch = sys.argv[4]
except:
    sys.exit(-1)


# generate absolute paths and raw filenames from our arguments
infile = str(pathlib.Path(i).parts[-1])
indir = pathlib.Path(i).resolve().parent
outfile = str(pathlib.Path(o).parts[-1])
outdir = pathlib.Path(o).resolve().parent

if ld.endswith("cc"):
    import re
    ld = str(re.sub("g?cc$", "ld", ld))

if not ld.startswith("/"): # if we've been given an absolute path, don't look it up on $PATH
    import shutil
    ld = shutil.which(ld)

print("Linker: {}".format(ld))
if not pathlib.Path(ld).exists():
    print("ld doesn't exist!")
    exit(-1)

print("Generating {}/{} from {}/{} for arch:{}".format(outdir, outfile, indir, infile, arch))

subprocess.run(
        [ld, "-r", "-b", "binary", "-o", str(outdir.joinpath(outfile)), infile],
        cwd=str(indir))

