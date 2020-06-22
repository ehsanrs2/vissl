#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""
This script is used to create the low-shot data for VOC svm trainings.
"""
import argparse
import logging
import os
import random
import sys

import numpy as np


# create the logger
FORMAT = "[%(levelname)s: %(filename)s: %(lineno)4d]: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stdout)
logger = logging.getLogger(__name__)


def sample_symbol(input_targets, output_target, symbol, num):
    logger.info(f"Sampling symbol: {symbol} for num: {num}")
    num_classes = input_targets.shape[1]
    for idx in range(num_classes):
        symbol_data = np.where(input_targets[:, idx] == symbol)[0]
        sampled = random.sample(list(symbol_data), num)
        for index in sampled:
            output_target[index, idx] = symbol
    return output_target


def generate_voc07_low_shot_samples(
    targets, k_values, sample_inds, output_path, layername
):
    k_values = [int(val) for val in k_values]
    # the way sample works is: for each independent sample, and a given k value
    # we create a matrix of the same shape as given targets file. We initialize
    # this matrix with -1 (ignore label). We then sample k positive and
    # (num_classes-1) * k negatives.
    num_classes = targets.shape[1]  # N x 20 shape
    for idx in sample_inds:
        for k in k_values:
            logger.info(f"Sampling: {idx} time for k-value: {k}")
            output = np.ones(targets.shape, dtype=np.int32) * -1
            output = sample_symbol(targets, output, 1, k)
            output = sample_symbol(targets, output, 0, (num_classes - 1) * k)
            output_file = os.path.join(output_path, f"{layername}_sample{idx}_k{k}.npy")
            logger.info(f"Saving file: {output_file}")
            np.save(output_file, output)
    logger.info("Done!!")


def main():
    parser = argparse.ArgumentParser(description="Sample Low shot data for VOC")
    parser.add_argument(
        "--targets_data_file",
        type=str,
        default=None,
        help="Numpy file containing image labels",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="path where low-shot samples should be saved",
    )
    parser.add_argument(
        "--k_values",
        type=str,
        default="1,2,4,8,16,32,64,96",
        help="Low-shot k-values for svm testing.",
    )
    parser.add_argument(
        "--num_samples", type=int, default=5, help="Number of independent samples."
    )
    opts = parser.parse_args()

    assert os.path.exists(opts.targets_data_file), "Target file not found. Abort"
    targets = np.load(opts.targets_data_file, encoding="latin1")
    sample_ids = list(range(1, 1 + opts.num_samples))
    generate_voc07_low_shot_samples(
        targets, opts.k_values, sample_ids, opts.output_path, opts.layername
    )


if __name__ == "__main__":
    main()
