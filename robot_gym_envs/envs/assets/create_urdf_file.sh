#!/bin/bash

#if you want to change parameters, change data robot_description_gen.xml
# roscd strirus_robot_description/launch/ && nano robot_description_gen.xml

roslaunch strirus_robot_description robot_description_gen.xml &
#wait while rosmaster become active
sleep 5;

if [ $# -eq 0 ]
  then
    echo "No arguments supplied, name of the file created automaticaly"
    rosparam get -p /robot_description > strirus_gamma.urdf;
  else
    rosparam get -p /robot_description > $1;
fi

killall rosmaster

exit 0


