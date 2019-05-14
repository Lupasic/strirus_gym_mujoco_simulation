# strirus_gym_mujoco_simulation
Robot should move straight in all directions, forward and side. It can be done due the reason that the robot structure is holonomic./home/lupasic/Programs/catkin_ws/src/strirus_full/strirus_gym_mujoco_simulation/README.md

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
sudo apt install libosmesa6-dev libgl1-mesa-glx libglfw3 patchelf libglew2.0
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

if doesnt work, in addition -- make an alias (should check the precise path by your own) in ~/.profile
```
sudo ln -s /usr/lib/x86_64-linux-gnu/libGLEW.so.2.0 /usr/lib/x86_64-linux-gnu/libGLEW.so
```

5. **Install tensor flow** (It's for main algorithm)
```
pip3 install tensorflow
```

6. **Test it**
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
It's already works fine, but firstly, I'd like to explain some steps of generation from XACRO(URDF) to MJCF.

In xacro file you can see these lines:
```
<mujoco>
    <!-- if it doesn't work, try this and put the value by your own $(find strirus_cad_design)/stl/collision-->
    <compiler balanceinertia="true" convexhull="false" 
    fusestatic="false" inertiafromgeom="false" 
    meshdir="../../../../strirus_cad_design/stl/collision"/>
</mujoco>
```

It is needed for make our xml file applicable for our tasks. _fusestatic_ - is the most important part here, others can be different. It is needed to create our file in the same manner as urdf, in this case you can simply modify it for our purposes.

Next step is following:
1. go to src/assets folder
2. ``` ./create_urdf_file output_name.urdf ```
if you want to change the parameters of the model
``` roscd strirus_robot_description/launch/ && nano robot_description_gen.xml ```
3. ```./convert_from_urdf_to_mjcf.sh output_name.urdf new_name.xml```
4. Now we are starting to modify xml file (mjcf) to make it applicable. All needed lines are in _file_with_needed_text.txt_ . It also contains all necessary information about reasons.

## Prepare gym enviroment
**How to make your own env** https://github.com/openai/gym/blob/master/docs/creating-environments.md
```
from root of module (strirus_gym_mujoco_simulation)
sudo pip3 install -e .
```

You can create an instance of the environment with 
```
import robot_gym_envs.envs 
gym.make('Strirus_gamma_controller-v0')
```

## Code structure
- Env
- Neural network
- 

## FAQ
1. If you have problem with os.link part (can be found using debugger (code doesn't run)).
This problem appears when you activate your code in console with import error.

    delete .lock file here```/usr/local/lib/python3.6/dist-packages/mujoco_py/generated```

2. If Pycharm doesn't see your files, choose your folder -> Mark Directory as -> source root
