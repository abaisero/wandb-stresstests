#!/usr/bin/env python

import argparse
import random
import time

import wandb


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('runtime', type=int)
    parser.add_argument('--num-logs', type=int, default=100)

    return parser.parse_args()


def main():
    args = parse_args()

    wandb.init(config=vars(args))
    assert wandb.run is not None

    sleeptime = args.runtime / args.num_logs

    y = 0.0

    for x in range(args.num_logs):
        time.sleep(sleeptime)

        y += random.random() - 0.5

        wandb.log(
            {
                'x': x,
                'y': y,
            },
            step=x,
            commit=False,
        )


if __name__ == '__main__':
    main()
