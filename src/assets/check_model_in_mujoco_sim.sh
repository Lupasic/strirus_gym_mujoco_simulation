#!/bin/bash

if [ $# -lt 1 ]
  then
    echo "No arguments supplied"
    exit 1
fi

cur_path=$(pwd)

cd $HOME/.mujoco/mujoco200/bin

./simulate $cur_path/$1
cd $cur_path
