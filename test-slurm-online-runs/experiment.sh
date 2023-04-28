#!/bin/bash

num_tasks=100
num_tasks_per_job=20

# create unique experiment id
experiment_id="experiment=test-slurm-online-runs"

sbatch_args=(
  --job-name $experiment_id
  job.sbatch
)

for i in $(seq $num_tasks); do
  i=$(printf "%04d" $i)

  # create unique task id
  task_id="task=$i"

  # create task command
  task_command="$PWD/main.py $((20 * 60 * 60)) --num-logs 10"

  # echo task path and command
  echo $experiment_id $task_id $task_command

done | filter_tasks.sh | group_tasks.sh $experiment_id $num_tasks_per_job "${sbatch_args[@]}"
