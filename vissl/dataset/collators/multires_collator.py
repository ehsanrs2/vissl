#!/usr/bin/env python3
#
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import torch


def multires_collator(batch):
    """
    """
    assert "data" in batch[0], "data not found in sample"
    assert "label" in batch[0], "label not found in sample"

    data = [x["data"] for x in batch]
    labels = [torch.tensor(x["label"]) for x in batch]
    data_valid = [torch.tensor(x["data_valid"]) for x in batch]
    data_idx = [torch.tensor(x["data_idx"]) for x in batch]
    num_duplicates, num_images = len(data[0]), len(data)

    output_data, output_label, output_data_valid, output_data_idx = [], [], [], []
    for pos in range(num_duplicates):
        _output_data = []
        for idx in range(num_images):
            _output_data.append(data[idx][pos])
            output_label.append(labels[idx][pos])
            output_data_valid.append(data_valid[idx][pos])
            output_data_idx.append(data_idx[idx][pos])
        output_data.append(torch.stack(_output_data))

    output_batch = {}
    output_batch["data"] = [output_data]
    output_batch["label"] = [torch.stack(output_label)]
    output_batch["data_valid"] = [torch.stack(output_data_valid)]
    output_batch["data_idx"] = [torch.stack(output_data_idx)]
    return output_batch
