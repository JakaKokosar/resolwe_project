""" filter selection script """
import argparse
import json
import numpy as np


from Orange.data import Table, Domain


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Filter cells (rows) by total counts"
        "(library size) or number of expressed genes.")

    parser.add_argument('data_table',
                        help="data:table object")

    parser.add_argument('counts',
                        help="Filter counts (list)")

    parser.add_argument('axis',
                        help="Table axis (int)")

    parser.add_argument('upper_limit',
                        help='Upper limit selection (float)')

    parser.add_argument('lower_limit',
                        help='Lower limit selection (float)')

    parser.add_argument('output_data',
                        help='Output Data Table (.pickle)')

    return parser.parse_args()


def main():
    """Run the program."""
    args = parse_arguments()

    # TODO: catch exceptions, validate input arguments
    data = Table(args.data_table)               # type: Table
    counts = np.array(json.loads(args.counts))  # type: np.ndarray
    axis = int(args.axis)                       # type: int
    output_data = args.output_data              # type: str
    upper_limit = float(args.upper_limit) if args.upper_limit else None
    lower_limit = float(args.lower_limit) if args.lower_limit else None

    mask = np.ones(counts.shape, dtype=bool)

    if lower_limit:
        mask &= lower_limit <= counts
    if upper_limit:
        mask &= counts <= upper_limit

    selection = np.count_nonzero(mask)

    if axis:  # 0 for columns, 1 for rows
        assert counts.size == len(data)
        data = data[mask]
    else:
        assert counts.size == len(data.domain.attributes)
        atts = [v for v, m in zip(data.domain.attributes, mask) if m]
        data = data.from_table(
            Domain(atts, data.domain.class_vars, data.domain.metas),
            data
        )

    if len(data) == 0 or len(data.domain) + len(data.domain.metas) == 0:
        data = None

    if data:
        data.save(output_data)
        print(selection)


if __name__ == "__main__":
    main()
