"""
Results generator.

@author: Panagiotis Anagnostou
"""

import __utilities as util
import gc
import numpy as np
import pandas as pd
import pickle
import re
import warnings

warnings.filterwarnings("ignore")


def evaluate(X, y, name):
    print(X.shape)

    results = util.execute_evaluation(X=X, y=y)

    with open("result_dict.dump", "rb") as ind:
        all_results = pickle.load(ind)

    all_results[name + str(X.shape)] = results
    del X, y

    with open("result_dict.dump", "wb") as out:
        pickle.dump(all_results, out)

    gc.collect()


if __name__ == "__main__":
    # %% Analyze Baron dataset
    name = "DRComparison-Baron"
    X, y = util.h5file("data/", name)

    evaluate(X, y, name)

    # %% Analyze Deng dataset
    name = "mat-Deng"
    X, y = util.h5file("data/", name)

    evaluate(X, y, name)

    # %% Analyze Chen dataset
    name = "scRNAseq-ChenBrainData"
    X, y = util.h5file("data/", name)

    evaluate(X, y, name)

    # %% Analyze Cancer dataset
    X = pd.read_csv("./data/cancer/data.csv", index_col=0, header=0)
    X = np.asarray(X, dtype="float64")
    y = pd.read_csv("./data/cancer/labels.csv", index_col=0, header=0)
    y["Class"] = pd.Categorical(y["Class"])
    y["Class"] = y.Class.cat.codes
    y = np.asarray(y).transpose()[0]

    print("\nCancer")

    evaluate(X, y, name)

    # %% Analyze USPS dataset
    X = np.array(pd.read_csv("data/USPS-data", sep=";").applymap(lambda x: re.sub(",", ".", x))).astype(dtype="float32")
    y = np.array(pd.read_csv("data/USPS-class")).transpose()[0]

    print("\nUSPS")

    evaluate(X, y, name)

    # %% Analyze BBC dataset
    X = np.array(pd.read_csv("data/bbc_data.csv", header=None))
    y = np.array(pd.read_csv("data/bbc_class.csv")).transpose()[0]

    print("\nBBC")

    evaluate(X, y, name)
