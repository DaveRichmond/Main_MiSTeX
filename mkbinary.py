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
except:
    sys.exit(-1)

# generate absolute paths and raw filenames from our arguments
infile = str(pathlib.Path(i).parts[-1])
indir = pathlib.Path(i).resolve().parent
outfile = str(pathlib.Path(o).parts[-1])
outdir = pathlib.Path(o).resolve().parent

subprocess.run(
        ["ld", "-r", "-b", "binary", "-o", str(outdir.joinpath(outfile)), infile],
        cwd=str(indir))

print("Generating {}/{} from {}/{}".format(outdir, outfile, indir, infile))
