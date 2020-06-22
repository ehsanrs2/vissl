#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import logging
import os


def set_env_vars(local_rank, node_id, cfg):
    os.environ["WORLD_SIZE"] = str(
        cfg.DISTRIBUTED.NUM_NODES * cfg.DISTRIBUTED.NUM_PROC_PER_NODE
    )
    dist_rank = cfg.DISTRIBUTED.NUM_PROC_PER_NODE * node_id + local_rank
    os.environ["RANK"] = str(dist_rank)
    os.environ["LOCAL_RANK"] = str(local_rank)
    if cfg.DISTRIBUTED.NCCL_DEBUG:
        os.environ["NCCL_DEBUG"] = "INFO"


def print_system_env_info(current_env):
    keys = list(current_env.keys())
    keys.sort()
    for key in keys:
        logging.info("{}:\t{}".format(key, current_env[key]))
