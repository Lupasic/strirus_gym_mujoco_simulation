import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env
from os import path

class Strirus_gamma_controller(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        startPath = path.dirname(__file__)
        mujoco_env.MujocoEnv.__init__(self, path.join(startPath, "assets", "strirus_gamma_30deg_120btw.xml"), 1)
        utils.EzPickle.__init__(self)

    def step(self, a):
        self.do_simulation(a, self.frame_skip)
        reward = 0
        done =  False
        ob = self._get_obs()
        return ob, reward, done, dict()


    def _get_obs(self):
        return np.concatenate([
            self.sim.data.sensordata.flat,
            [0,0,0],
            self.data.get_body_xpos("body_1_part").flat,
            self.sim.data.get_body_xquat("body_1_part").flat,
            self.sim.data.get_body_xquat("body_2_part").flat
        ])

    def reset_model(self):
        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5
