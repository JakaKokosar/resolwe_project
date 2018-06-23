""" t-SNE """
import argparse

from json import dump, loads

from Orange.data import Table
from Orange.projection import PCA

import numpy as np
from MulticoreTSNE import MulticoreTSNE


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('data_table',
                        help="data:table object")

    parser.add_argument('pca_components',
                        help="Number of PCA components")

    parser.add_argument('perplexity',
                        help="float, optional (default: 30)")

    parser.add_argument('iterations',
                        help="int, optional (default: 300)")

    parser.add_argument('init',
                        help="string or numpy array, optional (default: 'random')")

    parser.add_argument('n_jobs',
                        help="Number of jobs")

    parser.add_argument('embedding_json',
                        help='Embedding JSON')

    parser.add_argument('class_var_json',
                        help='Class variable JSON')

    return parser.parse_args()


def pca_preprocessing(data, pca_components):
    """
    :param data:
    :param pca_components:

    :return:
    """

    pca = PCA(n_components=pca_components, random_state=0)
    model = pca(data)
    pca_data = model(data)
    return pca_data


def tsne(X, perplexity, iterations, init, n_jobs):
    """
    :param X:
    :param perplexity:
    :param iterations:
    :param init:
    :param n_jobs:

    :return:
    """

    t_sne = MulticoreTSNE(perplexity=perplexity,
                          n_iter=iterations,
                          init=init,
                          early_exaggeration=1,
                          angle=.8,
                          random_state=0,
                          n_jobs=n_jobs)

    return t_sne.fit_transform(X).astype(np.float32)


def main():
    """Run the program."""
    args = parse_arguments()

    # TODO: catch exceptions, validate input arguments
    data = Table(args.data_table)
    pca_components = int(args.pca_components)
    perplexity = float(args.perplexity)
    iterations = int(args.iterations)
    n_jobs = int(args.n_jobs)

    if not args.init:
        init = 'random'
    else:
        init = np.array(loads(args.init))

    # run PCA pre-processing
    pca_result = pca_preprocessing(data, pca_components)

    # compute t_sne embedding
    embedding = tsne(pca_result.X, perplexity, iterations, init, n_jobs)

    with open(args.embedding_json, 'w') as json_f:
        dump({'embedding': embedding.tolist()}, json_f, separators=(',', ':'))

    with open(args.class_var_json, 'w') as json_f:
        name = data.domain.class_var.name
        values = data.domain.class_var.values
        y_data = data.Y

        dump({'name': name, 'values': values, 'y_data': y_data.tolist()},
             json_f, separators=(',', ':'))


if __name__ == "__main__":
    main()
