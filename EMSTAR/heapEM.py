# @Hasan Kurban, 2016
import numpy as np ,sys, time
from EMSTAR.heaping import *
import EMSTAR.heapEM
from scipy.stats import multivariate_normal
import warnings
warnings.filterwarnings("ignore")

# E-step: Given P(x_i|C_j), calculate P(C_j|x_i)
def e_step(data, mu, sigma,prior,nclust):

    n, d= data.shape

    # P(C|x)
    W  = np.zeros((nclust,n),dtype=float)
    for k in range(nclust):
        W[k] = (multivariate_normal.pdf(data, mean=mu[k], cov=sigma[k],allow_singular=True)) * prior[k]
    temp2= W.sum(axis=0)
    W = W / temp2

    # Adjust for numeric underflow
    W[np.where(np.isnan(W))] = np.finfo(np.float).eps
    W[np.where(W<0)] = np.finfo(np.float).eps

    return W

# M-step: Updata mu, sigma, prior for each cluster
def m_step(data, W, mu, sigma,nclust):

    n = data.shape[0]
    for t in range(nclust):
        temp3 = (data -mu[t])*  W.T[:, t][:, np.newaxis]
        temp4 = (data-mu[t]).T
        sigma[t] = np.dot(temp4,temp3) / W.sum(axis=1)[t]

        # Handle singularity
        if np.isfinite(np.linalg.cond(sigma)) is False:
            sigma = np.fill_diagonal(sigma, 0.000000000001)

        mu[t] = (data *  W.T[:,t][:,np.newaxis]).sum(axis=0)/ W.sum(axis=1)[t]
    prior = W.sum(axis=1)/n
    return mu, sigma, prior


def em_clustering(data, nclust, maxiter, epsilon, mu_indices):

    # Initialization of mean, covariance, and prior
    n,d = data.shape
    mu = np.zeros((nclust,d),dtype=float)  # mu.shape(nclust,d)
    sigma = np.zeros((nclust,d,d),dtype=float) # sigma.shape(k, d, d)

    if len(mu_indices) != 0:
        for t in range(len(mu_indices)):  # assigning the first nclust points to the mu
            mu[t] = data[mu_indices[t]]
            sigma[t] = np.identity(d)
    else:
        for t in range(nclust):  # assigning the first nclust points to the mu
            mu[t] = data[t]
            sigma[t] = np.identity(d)

    prior = np.asarray(np.repeat(1.0/nclust,nclust),dtype=float) # for each cluster one prior:

    # buildHeap heaps
    W= e_step(data,mu, sigma,prior,nclust) # calling E-step funct.
    mu, sigma, prior = m_step(data, W, mu, sigma,nclust) # calling M-step funct. 

    heaps,badDataIndex,badData,temp1 = buildHeap(data,W,n,d,nclust)

    # Updating Heap
    for i in range(maxiter):   
        W1 = e_step(badData,mu, sigma,prior,nclust)

        # Updating weight for bad data points:
        for k in range(len(badDataIndex)):
            for c in range(nclust):
                 W[c,badDataIndex[k][1]]= W1[c,k]
        mu, sigma, prior = m_step(data, W, mu, sigma,nclust)#M-step
        heaps,badDataIndex,badData,temp2= newHeap(data,heaps,W1,badDataIndex,d,nclust)  # Updating heaps:
        s = set(temp1)
        temp3 = [y for y in temp2 if y not in s]
        dissimilarity = round(float(len(temp3))/len(temp2),4)

        if dissimilarity <= epsilon:
            print("Convergence at iteration: ", i+1)
            break
        temp1 = 1* temp2 
    return mu, sigma, prior, i+1