import numpy as np
from scipy import dot, sqrt, ones, randn, tile
import time
from scipy import zeros
import sys
import os
import configparser
import gym
from neuralnetwork import NN
import robot_gym_envs.envs
from gym import spaces

def parseConfigFile(filename):

    global maxevaluations
    global nreplications
    global prange
    global batchSize
    global nhiddens
    global ninputs
    global noutputs
    global biases
    global environment
    global ntrials
    global maxfit



    # The configuration file must have the following sections:
    # [ALGO]: parameters for the evolutionary strategy
    # [NET]: the environment and the parameters of the neural network

    config = configparser.ConfigParser()
    config.read(filename)


    # Section ALGO
    maxevaluations = config.getint("ALGO","maxevaluations")
    nreplications = config.getint("ALGO","nreplications")
    batchSize = config.getint("ALGO","batchSize")
    ntrials = config.getint("ALGO", "ntrials")
    maxfit = config.getfloat("ALGO", "maxfit")

    # Section NET
    environment = config.get("NET", "gymEnv")
    nhiddens = config.getint("NET","nhiddens")
    if (config.has_option("NET","biases")):
        biases = config.getboolean("NET","biases")


def main(argv):
    global nreplications
    global verbose
    global ngenes
    global nhiddens
    global ninputs
    global noutputs
    global biases
    global environment
    global ntrials

    seed = 1
    argc = len(argv)
    filename = "configuration.ini".encode('utf-8')

    i = 1
    while (i < argc):
        if (argv[i] == "-f"):
            i += 1
            if (i < argc):
                filename = argv[i]
                i += 1
        elif (argv[i] == "-s"):
            i += 1
            if (i < argc):
                seed = int(argv[i])
                i += 1
        elif (argv[i] == "-v"):
            i += 1
            verbose = True
        else:
            # We simply ignore the argument
            i += 1

    parseConfigFile(filename)
    env = gym.make(environment)

    net = NN(gym.spaces.Box(shape=(23,), low=-10000, high=10000, dtype='float32'), env.action_space, nhiddens)
    # gym.spaces.Box(shape=(23,),low=-10000,high=10000,dtype='float32')
    # env.observation_space
    weights = np.load('bestgS1.npy')

    net.rollout(env, genotype=weights, trials=ntrials, render=True)

    pass


if __name__ == "__main__":
    main(sys.argv)