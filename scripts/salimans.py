#!/usr/bin/env pythonimport numpy as npfrom scipy import dot, sqrt, ones, randn, tileimport timefrom scipy import zerosimport sysimport osimport configparserimport gymfrom neuralnetwork import NNimport robot_gym_envs.envsfrom gym import spacesnreplications = 10                      # number of replicationsmaxevaluations = 100000                 # max number of evaluationsprange = 0.1                            # prange range (default set through Xavier initialization)batchSize = 200                         # number of offspring (to be multiplied by 2)stepsize = 0.01                         # step sizenoiseStdDev = 0.02                      # perturbation coefficientepsilon = 1e-8                          # adam parametersbeta1 = 0.9                             # adam beta1beta2 = 0.999                           # adam beta2maxfit = 0                              # maximum achievable fitness (0 = infinite)ninputs = 23                             # number of inputs neuronsnhiddens = 150                           # number of hiddens neuronsnoutputs = 12                            # number of output neuronsbiases = False                          # whether neurons have biasesngenes = 0                              # number of parameters (calculated on the basis of the neural architecture)# Directory of the script .pyscriptdirname = os.path.dirname(os.path.realpath(__file__))# read parameters from the configuration filedef parseConfigFile(filename):    global maxevaluations    global nreplications    global prange    global batchSize    global nhiddens    global ninputs    global noutputs    global biases    global environment    global ntrials    global maxfit    # The configuration file must have the following sections:    # [ALGO]: parameters for the evolutionary strategy    # [NET]: the environment and the parameters of the neural network    config = configparser.ConfigParser()    config.read(filename)    # Section ALGO    maxevaluations = config.getint("ALGO","maxevaluations")    nreplications = config.getint("ALGO","nreplications")    batchSize = config.getint("ALGO","batchSize")    ntrials = config.getint("ALGO", "ntrials")    maxfit = config.getfloat("ALGO", "maxfit")    # Section NET    environment = config.get("NET", "gymEnv")    nhiddens = config.getint("NET","nhiddens")    if (config.has_option("NET","biases")):        biases = config.getboolean("NET","biases")# Sorting functions# Descendent sortingdef descendent_sort(vect):    # Copy of the vector    tmpv = np.copy(vect)    n = len(tmpv)    # Index list    index = np.arange(n, dtype=np.int32)    i = 0    while i < n:        # Look for maximum        maxv = tmpv[0]        maxi = 0        j = 1        while j < n:            if tmpv[j] > maxv:                maxv = tmpv[j]                maxi = j            j += 1        vect[i] = tmpv[maxi]        index[i] = maxi        i += 1        # Set invalid value        tmpv[maxi] = -999999999999.0    return vect, index# Ascendent sortingdef ascendent_sort(vect):    # Copy of the vector    tmpv = np.copy(vect)    n = len(tmpv)    # Index list    index = np.arange(n, dtype=np.int32)    i = 0    while i < n:        # Look for maximum        minv = tmpv[0]        mini = 0        j = 1        while j < n:            if tmpv[j] < minv:                minv = tmpv[j]                mini = j            j += 1        vect[i] = tmpv[mini]        index[i] = mini        i += 1        # Set invalid value        tmpv[mini] = 999999999999.0    return vect, index# average fitness of the samplesdef AverageFit(fitness):    avef = 0.0    for i in range(len(fitness)):        avef = avef + fitness[i]    avef = avef / len(fitness)    return avef# The OpenAI-ES algorithm (from Salimans et al., 2017)def ES(env,net,seed):    global ngenes    global noiseStdDev    global stepsize    global batchSize    global prange    global ninputs    global nhiddens    global noutputs    global biases    global epsilon    global beta1    global beta2    global ntrials    global bestgfit    global maxfit        # Adam parameters    m = zeros(ngenes) # Mean    v = zeros(ngenes) # Variance    epsilon = 1e-8 # Constant required to avoid possible division by 0    beta1 = 0.9    beta2 = 0.999    # weights range (Xavier-2 initialization)    prange = np.sqrt(2.0 / (ninputs + (noutputs + nhiddens)))    # utilities    weights = zeros(batchSize)    # fitness of samples    fitness = zeros(batchSize * 2)    # allocate and initialize the centroid (Xaxier-2' method)    center = np.arange(ngenes, dtype=np.float64)    center = np.random.randn(ngenes) * np.sqrt(2.0 / (ninputs + (noutputs + nhiddens)))    # biases are initialized to 0.0    if biases:        for g in range(noutputs+nhiddens):                center[g] = 0.0    # Allocate utility vector    utilities = zeros(batchSize * 2)    # initialize statitiscs    stat = np.arange(0, dtype=np.float64)    bestfit = -9999.0                       # best fitness achieved so far    bestgfit = -9999.0                      # best generalization fitness achieved so far    ceval = 0                               # current evaluation    cgen = 0                                # current generation    start_time = time.time()                # start time    nsteps = np.arange(1, dtype=np.int32)   # steps consumed    print("ES: seed %d batchSize %d max %d stepsize %.2f noiseStdDev %.2f prange %.2f network %d->%d-%d ngenes %d" % (seed, batchSize, maxevaluations, stepsize, noiseStdDev, prange, ninputs, nhiddens, noutputs, ngenes))    # main loop    while ceval <= maxevaluations:        cgen = cgen + 1        if (maxfit > 0 and bestgfit >= maxfit):            break        # Extract samples from Gaussian distribution with mean 0.0 and standard deviation 1.0        samples = randn(batchSize,ngenes)                # create symmetric samples        symmSamples = zeros((batchSize * 2, ngenes))        for i in range(batchSize):            sampleIdx = 2 * i            symmSamples[sampleIdx,:] = samples[i,:]            symmSamples[sampleIdx + 1,:] = -samples[i,:]        # Generate offspring (i.e. centroid + samples)        offspring = tile(center.reshape(1,ngenes),(batchSize * 2,1)) + noiseStdDev * symmSamples                # evaluate offspring        for o in range(batchSize * 2):            fitness[o], steps = net.rollout(env,offspring[o],ntrials)            ceval += ntrials        # Sort by fitness and compute weighted mean into center        fitness, index = ascendent_sort(fitness)  # maximization        for i in range(batchSize * 2):            utilities[index[i]] = i        utilities /= (batchSize * 2 - 1)        utilities -= 0.5        # The weights is the difference between the utilities of the symmetric perturbation        for i in range(batchSize):            idx = 2 * i            weights[i] = (utilities[idx] - utilities[idx + 1]) # pos - neg        # Compute the gradient        g = dot(weights, samples) # weights * samples        # Normalization over the number of samples        g /= (batchSize * 2)        # Global gradient        globalg = -g        # Apply bias correction        a = stepsize * sqrt(1 - beta2 ** cgen) / (1 - beta1 ** cgen)        # Update momentum vectors        m = beta1 * m + (1 - beta1) * globalg        v = beta2 * v + (1 - beta2) * (globalg * globalg)        # Move the centroid of the population         dCenter = -a * m / (sqrt(v) + epsilon)                # weight decay not implemented. Can be done with: dCenter -= wcoeff * center                # update center        center += dCenter         # Evaluate the fitness of the centroid        centroidfit,steps = net.rollout(env,center,ntrials)        ceval += ntrials        # We measure the generalization of the best offspring/centroid        offfit = fitness[batchSize * 2 - 1]        if (centroidfit > offfit):            f,steps = net.rollout(env,center,ntrials)            ceval += ntrials        else:            f,steps = net.rollout(env,offspring[index[batchSize * 2 - 1]],ntrials)            ceval += ntrials        if (f > bestgfit):            bestgfit = f            bestgsol = np.copy(offspring[index[batchSize * 2 - 1]])        # we update the best fitness        if (centroidfit > offfit and centroidfit > bestfit):                bestfit = centroidfit                bestsol = np.copy(center)        if (offfit > centroidfit and offfit > bestfit):                bestfit = offfit                bestsol = offspring[index[batchSize * 2 - 1]]        stat = np.append(stat,[ceval, bestgfit, bestfit, np.average(fitness), offfit, centroidfit, cgen])        print('Seed %d Evals %d Gen %d Bestfit %.2f Bestgfit %.2f centroid %.2f bestsam %.2f Avg %.2f weights %.2f gradient %.3f a %.3f ' % (seed, ceval, cgen, bestfit, bestgfit, centroidfit, offfit, np.average(fitness), np.average(np.absolute(center)),np.average(np.absolute(globalg)), a))    fname = scriptdirname + "/S" + str(seed) + ".fit"    fp = open(fname, "w")    fp.write('Seed %d Gen %d Eval %d Bestfit %.2f Bestgfit %.2f centroid %.2f bestsam %.2f Avg %.2f weights %.2f gradient %.3f Runtime %d\n' % (seed, cgen, ceval, bestfit, bestgfit, centroidfit, offfit, np.average(fitness), np.average(np.absolute(center)),np.average(np.absolute(globalg)), (time.time() - start_time)))    fp.close()    fname = scriptdirname + "/statS" + str(seed)    stat.resize([int(len(stat)/7), 7])    stat = stat.transpose()    np.save(fname, stat)    fname = scriptdirname + "/bestS" + str(seed)    np.save(fname, bestsol)    fname = scriptdirname + "/bestgS" + str(seed)    np.save(fname, bestgsol)# Main functiondef main(argv):    global nreplications    global verbose    global ngenes    global nhiddens    global ninputs    global noutputs    global biases    global environment    global ntrials    seed = 1    argc = len(argv)    filename = "configuration.ini".encode('utf-8')    i = 1    while (i < argc):        if (argv[i] == "-f"):            i += 1            if (i < argc):                filename = argv[i]                i += 1        elif (argv[i] == "-s"):            i += 1            if (i < argc):                seed = int(argv[i])                i += 1        elif (argv[i] == "-v"):            i += 1            verbose = True        else:            # We simply ignore the argument            i += 1    parseConfigFile(filename)    env = gym.make(environment)    net = NN(gym.spaces.Box(shape=(23,),low=-10000,high=10000,dtype='float32'),env.action_space,nhiddens)    # gym.spaces.Box(shape=(23,),low=-10000,high=10000,dtype='float32')    # env.observation_space    ngenes = net.netParameter()    if biases:        ngenes += nhiddens + noutputs        print("Environment %s, network %d->%d->%d, genes %d, Maxeval %d" % (environment, net.input_size, net.hidden, net.output_size, ngenes, maxevaluations))    # Run the evolutionary algorithm for multiple replications    for i in range(nreplications):        np.random.seed(seed)        ES(env,net,seed)        seed = seed + 1    passif __name__ == "__main__":    main(sys.argv)