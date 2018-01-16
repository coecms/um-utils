#!/bin/bash
module purge
module use /g/data3/hh5/public/modules
module load conda

/usr/bin/env python - $* << EOF
import iris
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description=
                        "Extract 10m wind and concatenate to file")
    parser.add_argument("--output", "-o",
                        help="output file",
                        default='wind10m.nc')
    parser.add_argument("--verbose", "-v", help="Verbose output",
                        action="store_true")
    parser.add_argument("file", help="input file(s)", nargs="+")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        print(args)

    # Wind constraint
    Wind10m = iris.AttributeConstraint(
        STASH=lambda stash: stash in ['m01s03i225', 'm01s03i226'])
    cubes=iris.load(args.file, Wind10m)
    if args.verbose:
        print(cubes)
        print("===============================")
        print(cubes.concatenate())
    iris.fileformats.netcdf.save(cubes.concatenate(), args.output, zlib=False)

if __name__ == '__main__':
    main()
EOF
