#!/bin/bash


cur_path=$(pwd)

cd $HOME/.mujoco/mujoco200/bin

if [ $# -lt 1 ]
  then
    echo "No arguments supplied, just activate the simulator"
    ./simulate
  else
    ./simulate $cur_path/$1
fi

exit 0

