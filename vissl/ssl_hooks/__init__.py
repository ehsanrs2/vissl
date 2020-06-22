#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from enum import Enum, auto
from typing import List

from classy_vision.hooks.classy_hook import ClassyHook
from vissl.ssl_hooks.deepclusterv2_hooks import (  # noqa
    ClusterMemoryHook,
    InitMemoryHook,
)
from vissl.ssl_hooks.log_hooks import (  # noqa
    LogGpuStatsHook,
    LogLossLrEtaHook,
    LogLossMetricsCheckpointHook,
    LogPerfTimeMetricsHook,
)
from vissl.ssl_hooks.state_update_hooks import (  # noqa
    CheckNanLossHook,
    FreezeParametersHook,
    SetDataSamplerEpochHook,
    SSLModelComplexityHook,
    UpdateBatchesSeenHook,
    UpdateTestBatchTimeHook,
    UpdateTrainBatchTimeHook,
    UpdateTrainIterationNumHook,
)
from vissl.ssl_hooks.swav_hooks import NormalizePrototypesHook  # noqa
from vissl.ssl_hooks.swav_hooks import SwAVUpdateQueueScoresHook  # noqa
from vissl.ssl_hooks.tensorboard_hook import SSLTensorboardHook  # noqa
from vissl.utils.hydra_config import AttrDict


class SSLClassyHookFunctions(Enum):
    """
    Enumeration of all the hook functions in the ClassyHook class.
    """

    on_start = auto()
    on_phase_start = auto()
    on_forward = auto()
    on_loss_and_meter = auto()
    on_backward = auto()
    on_update = auto()
    on_step = auto()
    on_phase_end = auto()
    on_end = auto()


def default_hook_generator(cfg: AttrDict) -> List[ClassyHook]:
    hooks = []

    # conditionally add hooks based on use-case
    if cfg.MONITOR_PERF_STATS:
        perf_stat_freq = (
            cfg.PERF_STAT_FREQUENCY if cfg.PERF_STAT_FREQUENCY > 0 else None
        )
        hooks.append(LogPerfTimeMetricsHook(perf_stat_freq))
    if cfg.CRITERION.name == "swav_loss":
        hooks.extend([SwAVUpdateQueueScoresHook(), NormalizePrototypesHook()])
    if cfg.CRITERION.name == "deepclusterv2_loss":
        hooks.extend([InitMemoryHook(), ClusterMemoryHook()])
    if cfg.MODEL.MODEL_COMPLEXITY.COMPUTE_COMPLEXITY:
        hooks.extend([SSLModelComplexityHook()])

    # hooks that are used irrespective of workflow type
    rolling_btime_freq = cfg.ROLLING_BTIME_FREQ if cfg.ROLLING_BTIME_FREQ > 0 else None
    hooks.extend(
        [
            CheckNanLossHook(),
            SetDataSamplerEpochHook(),
            FreezeParametersHook(),
            UpdateBatchesSeenHook(),
            UpdateTrainBatchTimeHook(),
            UpdateTestBatchTimeHook(),
            UpdateTrainIterationNumHook(),
            LogLossMetricsCheckpointHook(),
            LogLossLrEtaHook(rolling_btime_freq),
            LogGpuStatsHook(),
        ]
    )
    return hooks
