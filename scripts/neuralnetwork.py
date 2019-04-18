import numpy as np
import gym
import math

def sigmoid(x):
    return 1/(1+np.exp(-x))

class NN:
    def __init__(self,inputs,outputs,hiddens):

        self.inputs = inputs.shape[0]
        if list(outputs.shape)==[]:
            self.outputs = 1
        else:
            self.outputs = outputs.shape[0]

        self.hidden = hiddens #hidden neurons number
        self.input_size = self.inputs#len(inputs)
        self.output_size = self.outputs
        #value to split the genotype into matrix
        self.first_layer = self.input_size * self.hidden
        self.recurrent_layer = self.first_layer + self.hidden * self.hidden
        #weight matrix initialization
        self.input_weight = np.zeros((self.input_size, self.hidden))
        self.recurrent_weight = np.zeros((self.hidden, self.hidden))
        self.output_weight = np.zeros((self.hidden, self.output_size))
        #store the state of hidden neurons
        self.hiddenState = np.zeros(self.hidden)

    def toPrint(self,inp):
        lfirst = np.dot(inp, self.input_weight)
        lrecurrent = sigmoid(np.dot(lfirst, self.recurrent_weight))
        lout = sigmoid(np.dot(lrecurrent, self.output_weight))
        return lout

    def netParameter(self):
        return self.input_size * self.hidden + self.hidden * self.hidden + self.hidden * self.output_size

    def setInput(self, inp):
        self.inputs = inp

    def rollout(self, env, genotype, trials, render=False, seed=None):
        self.reset_net()
        step_total = 0

        rew_total = 0
        for j in range(trials):
            # To ensure replicability (we always pass a valid seed, even if fully-random evaluation is going to be run)
            if seed is not None:
                env.seed(seed)
            for task in range(4):
                ob = env.reset()
                dist_variance = 0
                cur_task_step = 0
                cur_rew = 0
                for t in range(2000):
                    # prepare input var
                    if task == 0:
                        ob[20] = 1
                    if task == 1:
                        ob[20] = -1
                    if task == 2:
                        ob[21] = 1
                    if task == 3:
                        ob[21] = -1

                    cur_ob = ob[:23]
                    # cur_ob[:11] = cur_ob[:11] % (2*math.pi)
                    ac = self.updateNet(cur_ob,genotype)
                    # post processing
                    # if task == 0:
                    #     pass
                    # if task == 1:
                    #     ac *= -1
                    # if task == 2:
                    #     ac[3:5] *= -1
                    #     ac[6:8] *= -1
                    # if task == 3:
                    #     ac[0:2] *= -1
                    #     ac[9:11] *= -1
                    # ac += ob[:12]

                    # Perform a step
                    ob, rew, done, _ = env.step(ac) # mujoco internally scales actions in the proper ranges!!!
                    # Append the reward
                    if task == 0:
                        dist_variance += abs(ob[24])
                    if task == 1:
                        dist_variance += abs(ob[24])
                    if task == 2:
                        dist_variance += abs(ob[23])
                    if task == 3:
                        dist_variance += abs(ob[23])

                    cur_task_step += 1
                    if cur_task_step == 1000:
                        if task == 0:
                            cur_rew = 10*(abs(ob[23]) / dist_variance)
                        if task == 1:
                            if ob[23] > 0:
                                ob[23] = 0
                            cur_rew = (abs(ob[23]) / dist_variance)
                        if task == 2:
                            cur_rew = 10*(abs(ob[24]) / dist_variance)
                        if task == 3:
                            if ob[24] > 0:
                                ob[24] = 0
                            cur_rew = (abs(ob[24]) / dist_variance)
                        rew_total += cur_rew/4
                        step_total += cur_task_step
                    if render:
                        env.render()
            # Transform the list of rewards into an array

        return rew_total/trials, step_total

    def updateNet(self,observation, genotype):
        self.inputs = observation

        self.input_weight = genotype[:self.first_layer].reshape(self.input_size, self.hidden)

        self.recurrent_weight = genotype[self.first_layer:self.recurrent_layer].reshape(self.hidden, self.hidden)

        self.output_weight = genotype[self.recurrent_layer:].reshape(self.hidden, self.output_size)
        lfirst = np.dot(self.inputs, self.input_weight)
        lrecurrent = np.dot(self.hiddenState, self.recurrent_weight)

        lhidden = np.tanh(lfirst+lrecurrent)
        #store the hidden state
        self.hiddenState = lhidden
        #output calculation
        lout = np.tanh(np.dot(lhidden, self.output_weight))

        return lout

    def evaluateNet(self,genotype):
        netOut = self.updateNet(genotype)
        return netOut
        #print self.outputs
        #print netOut
        #fitness = np.linalg.norm(self.outputs-netOut)
        #print fitness
        #text = raw_input("prompt")
        #return 1- fitness

    def reset_net(self):
        self.input_weight = np.zeros((self.input_size, self.hidden))
        self.recurrent_weight = np.zeros((self.hidden, self.hidden))
        self.output_weight = np.zeros((self.hidden, self.output_size))
        self.hiddenState = np.zeros(self.hidden)
