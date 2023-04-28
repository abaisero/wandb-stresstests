#!/usr/bin/env python

import argparse
import time

import wandb


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('n', type=int)
    parser.add_argument('--sleep', type=int, default=None)

    return parser.parse_args()


def main():
    args = parse_args()

    wandb.init(config=vars(args))
    assert wandb.run is not None

    for i in range(args.n):
        wandb.log(
            {
                'i': i,
            },
            step=i,
            commit=False,
        )

        wandb.log(
            {
                'time': time.time(),
            },
            step=i,
            commit=False,
        )

        if args.sleep is not None:
            time.sleep(args.sleep)


if __name__ == '__main__':
    main()
