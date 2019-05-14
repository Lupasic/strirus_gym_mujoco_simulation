import gym
env = gym.make('Ant-v2')
env.reset()
for _ in range(1000):
#    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()

#import gym
#import robot_gym_envs.envs

# env = gym.make('Strirus_gamma_controller-v0')
#env = gym.make('Ant-v2')
#for i_episode in range(20):
#    observation = env.reset()
#    for t in range(1000):
#        env.render()
#        print(observation)
#        action = env.action_space.sample()
#        observation, reward, done, info = env.step(action)
#        if done:
#            print("Episode finished after {} timesteps".format(t + 1))
#            break
#env.close()
