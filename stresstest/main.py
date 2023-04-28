#!/usr/bin/env python
import argparse
import pickle
import random
import time
from dataclasses import dataclass

import wandb


@dataclass
class Runstate:
    step: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Checkpoint:
    run_id: int
    runstate: Runstate


def save_data(filename: str, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load_data(filename: str):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def save_checkpoint(runstate: Runstate, args: argparse.Namespace):
    assert wandb.run is not None

    save_data(
        args.checkpoint_filename,
        Checkpoint(
            run_id=wandb.run.id,
            runstate=runstate,
        ),
    )


def run_program(runstate: Runstate, args: argparse.Namespace):
    sleeptime = args.runtime / args.num_logs

    for _ in range(args.num_logs):
        time.sleep(sleeptime)

        wandb.log(
            {
                'x': runstate.x,
                'y': runstate.y,
                'z': runstate.z,
            },
            step=runstate.step,
            commit=False,
        )

        runstate.step += 1
        runstate.x += random.random() - 0.5
        runstate.y += random.random() - 0.5
        runstate.z += random.random() - 0.5


def load_checkpoint(args: argparse.Namespace) -> tuple[Runstate, dict]:
    try:
        checkpoint = load_data(args.checkpoint_filename)
    except FileNotFoundError:
        runstate = Runstate()
        wandb_kwargs = {}
    else:
        runstate = checkpoint.runstate
        wandb_kwargs = {
            'resume': 'must',
            'id': checkpoint.run_id,
        }

    return runstate, wandb_kwargs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=str)
    parser.add_argument('--runtime', type=int, default=600)
    parser.add_argument('--num-logs', type=int, default=100)

    args = parser.parse_args()
    args.checkpoint_filename = f'{args.path}/checkpoint.pkl'

    return args


def main() -> int:
    args = parse_args()

    runstate, wandb_kwargs = load_checkpoint(args)

    wandb.init(**wandb_kwargs)
    run_program(runstate, args)

    save_checkpoint(runstate, args)

    return 0


if __name__ == '__main__':
    exit(main())
