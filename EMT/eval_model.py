# @Hasan Kurban, 2016, IUB, Computer Scince Department
# main file for EM clustering algorithm
# @Parichit, 2017, IUB, Computer Scince Department
# Edited for BST implementation - @Parichit Sharma, 2021, IUB, Computer Science Department

from EMT.EM import *
from EMT.testing import *
import time
from sklearn.metrics.cluster import adjusted_rand_score


def model_eval(X, y, nclust, maxiter, epsilon, mu_indices):

    # training
    start_time = time.time()
    mu, sigma, prior, iters = em_clustering(X, nclust, maxiter, epsilon, mu_indices)
    averageTraningTime = time.time() - start_time

    # testing
    W = e_step(X, mu, sigma, prior, nclust)
    accuracy, pred = test(y, W, X)

    ari = adjusted_rand_score(y, pred)
    accuracy = int(round(accuracy * 100))
    averageTraningTime = round(averageTraningTime,3)

    # print(" Traning running time :%s seconds " % averageTraningTime)
    # print( "accuracy:%s%%" % accuracy)
    return ari, accuracy, averageTraningTime, iters