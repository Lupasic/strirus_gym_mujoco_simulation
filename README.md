# strirus_gym_mujoco_simulation
Robot should move straight in all directions, forward and side. It can be done due the reason that the robot structure is holonomic.

## Installation
1. **Install gym** https://gym.openai.com
```
pip3 install gym
```
2. **Receive MuJoCo License and activate it** https://www.roboti.us/license.html
3. **Install MuJoCo binary** https://www.roboti.us/index.html

Unzip the downloaded mjpro200 directory into ~/.mujoco/mjpro200, and place your license key (the mjkey.txt file from your email) at ~/.mujoco/mjkey.txt. Also, put it in ~/.mujoco/mjpro200/bin
4. **Install MuJoCo package**
```
pip3 install gym[mujoco]
```
If you have any problems, https://github.com/openai/mujoco-py

I had problem with LD_LIBRARY_PATH, solution is to install it 
```
sudo LD_LIBRARY_PATH=$HOME/.mujoco/mujoco200/bin pip3 install mujoco-py
```
also add 
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lupasic/.mujoco/mujoco200/bin
```

If you use PyCharm and it doesn't see LD_LIBRARY_PATH, then run->edit cofigurations->enviroment variables, put it there

If you see GLEW initialization error: Missing GL version, then
```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so
```

if doesnt work, in addition -- make an alias (should check the precise path by your own)
```
sudo ln -s /usr/lib/x86_64-linux-gnu/libGLEW.so.2.0 /usr/lib/x86_64-linux-gnu/libGLEW.so
```

in ~/.profile
5. **Test it**
```
import gym
env = gym.make('Ant-v2')
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()
```

## Steps for generation a model from URDF
1. go to src/assets folder
2. ``` ./create_urdf_file output_name.urdf ```
if you want to change the parameters of the model 
``` roscd strirus_robot_description/launch/ && nano robot_description_gen.xml ```
3. ```./convert_from_urdf_to_mjcf.sh output_name.urdf new_name.xml
4. Now we are starting to modify to make it applicable.
- Add in the beginning <include file="terrain.xml"/>

