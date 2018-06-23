""" filter selection script """
import argparse

from json import loads
from Orange.data import Table, Domain, ContinuousVariable

import numpy as np


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('data_table',
                        help="data:table object")

    parser.add_argument('embedding',
                        help="data:tsne object")

    parser.add_argument('selection',
                        help="List of indexes")

    parser.add_argument('x_tsne_var',
                        help="Table variable to store data")

    parser.add_argument('y_tsne_var',
                        help="Table variable to store data")

    parser.add_argument('output_data',
                        help='Output Data Table (.pickle)')

    return parser.parse_args()


def main():
    """Run the program."""
    args = parse_arguments()

    # TODO: catch exceptions, validate input arguments
    data = Table(args.data_table)                   # type: Table
    embedding = np.array(loads(args.embedding))     # type: np.ndarray
    selection = list(loads(args.selection))         # type: list
    output_data = args.output_data                  # type: str
    x_tsne_var = args.x_tsne_var                    # type: str
    y_tsne_var = args.y_tsne_var                    # type: str

    domain = data.domain
    domain = Domain(domain.attributes,
                    domain.class_vars,
                    domain.metas + (ContinuousVariable(x_tsne_var), ContinuousVariable(y_tsne_var)))

    output = data.transform(domain)
    output.metas[:, -2:] = embedding
    selected = output[selection]

    if output:
        selected.save(output_data)


if __name__ == "__main__":
    main()
