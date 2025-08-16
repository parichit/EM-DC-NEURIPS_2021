# @Hasan Kurban, 2016, IUB, Computer Scince Department
# main file for EM clustering algorithm
from EMSTAR.heapEM import *
from EMSTAR.testing import *
import time
from sklearn.metrics.cluster import adjusted_rand_score, adjusted_mutual_info_score


def model_eval(X, y, nclust, maxiter, epsilon, mu_indices):

    # training
    start_time = time.time()
    mu, sigma, prior, iters = em_clustering(X, nclust, maxiter, epsilon, mu_indices)
    TraningTime = time.time() - start_time

    # testing
    W = e_step(X, mu, sigma, prior, nclust)
    
    accuracy, pred = test(y, W, X)
    # pred= W.argmax(axis=0)
    
    ari = adjusted_rand_score(y, pred)
    accuracy = int(round(accuracy*100))
    
    # accuracy = 0
    
    TraningTime = round(TraningTime, 3)
    print("ARI: ", ari)
    
    # print(" Traning running time :%s seconds " % TraningTime)
    # print( "accuracy:%s%%" % accuracy)
    return ari, accuracy, TraningTime, iters
