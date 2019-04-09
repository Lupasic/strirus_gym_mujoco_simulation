import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Strirus_gamma_controller-v0',
    entry_point='robot_gym_envs.envs:Strirus_gamma_controller',
    max_episode_steps=10000,
    reward_threshold=6000.0,
)
