#!/bin/bash

num_tasks=1000
num_tasks_per_job=20

sbatch_args=(
  --job-name $experiment_id
  job.sbatch
)

export WANDB_DIR=$PWD
export WANDB_PROJECT=wandb-stresstest
export WANDB_MODE=offline

# create unique experiment id
experiment_id="experiment=test-slurm-online-runs"

for i in $(seq $num_tasks); do
  i=$(printf "%04d" $i)

  # create unique task id
  task_id="task=$i"

  # create task command
  task_path=$(make_task_path.sh $experiment_id $task_id)
  task_command="$PWD/main.py $task_path --runtime 60 --num-logs 100"

  # echo task path and command
  echo $experiment_id $task_id $task_command

done | filter_tasks.sh | group_tasks.sh $experiment_id $num_tasks_per_job "${sbatch_args[@]}"
