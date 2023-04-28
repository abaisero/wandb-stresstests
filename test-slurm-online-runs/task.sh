#!/bin/bash

export WANDB_DIR=$PWD
export WANDB_PROJECT=wandb-stresstest

python main.py "$@"
