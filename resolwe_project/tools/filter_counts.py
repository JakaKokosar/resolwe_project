#!/usr/bin/env python3
""" filter count script """
import argparse
import numpy as np


from json import dump
from Orange.data import Table


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Filter cells(rows) by total counts"
        "(library size) or number of expressed genes.")

    parser.add_argument('data_table',
                        help="data:table object")
    parser.add_argument('axis',
                        help="Table axis")
    parser.add_argument('measure',
                        help="Quality control measure descriptions")
    parser.add_argument('output_json',
                        help='Output JSON')

    return parser.parse_args()


def main():
    """Run the program."""
    args = parse_arguments()

    # TODO: catch exceptions, validate input arguments
    data = Table(args.data_table)

    # if 0: number of genes/features with non-zero expression level
    # if 1: total counts by cell/gene
    measure = int(args.measure)

    # 0 for columns, 1 for rows
    axis = int(args.axis)

    out_data = {}

    if measure:
        counts = np.nansum(data.X, axis=axis)
    else:
        mask = (data.X != 0) & (np.isfinite(data.X))
        counts = np.count_nonzero(mask, axis=axis)

    out_data['counts'] = counts.tolist()

    with open(args.output_json, 'w') as out_file:
        dump(out_data, out_file, separators=(',', ':'))


if __name__ == "__main__":
    main()
