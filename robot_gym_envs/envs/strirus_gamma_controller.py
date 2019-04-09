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
        xposbefore = self.get_body_com("body_1_part")[0]
        self.do_simulation(a, self.frame_skip)
        xposafter = self.get_body_com("body_1_part")[0]
        forward_reward = (xposafter - xposbefore)/self.dt
        ctrl_cost = .5 * np.square(a).sum()
        contact_cost = 0.5 * 1e-3 * np.sum(
            np.square(np.clip(self.sim.data.cfrc_ext, -1, 1)))
        survive_reward = 1.0
        reward = forward_reward - ctrl_cost - contact_cost + survive_reward
        state = self.state_vector()
        notdone = np.isfinite(state).all() \
            and state[2] >= 0.2 and state[2] <= 1.0
        done =  notdone
        ob = self._get_obs()
        return ob, reward, done, dict(
            reward_forward=forward_reward,
            reward_ctrl=-ctrl_cost,
            reward_contact=-contact_cost,
            reward_survive=survive_reward)

    def _get_obs(self):
        return np.concatenate([
            self.sim.data.qpos.flat[2:],
            self.sim.data.qvel.flat,
            np.clip(self.sim.data.cfrc_ext, -1, 1).flat,
        ])

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(size=self.model.nq, low=-.1, high=.1)
        qvel = self.init_qvel + self.np_random.randn(self.model.nv) * .1
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5
