#!/bin/bash

if [ $# -lt 2 ]
  then
    echo "No arguments supplied"
    exit 1
fi

cur_path=$(pwd)

cd $HOME/.mujoco/mujoco200/bin

./compile $cur_path/$1 $cur_path/$2

cd $cur_path
