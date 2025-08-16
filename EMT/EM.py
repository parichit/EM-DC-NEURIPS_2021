# @Hasan Kurban, 2016, IUB, Computer Scince Department
import numpy as np
from scipy.stats import multivariate_normal

# E-step: Given P(x_i|C_j), calculate P(C_j|x_i)
def e_step(data, mu, sigma,prior,nclust):
    n= data.shape[0]
    W  = np.zeros((nclust,n),dtype=float) # P(C|x)
    for k in range(nclust):
        W[k] = (multivariate_normal.pdf(data, mean=mu[k], cov=sigma[k],allow_singular=True)) * prior[k]
    temp2= W.sum(axis=0)
    W = W / temp2
    W[np.where(np.isnan(W))] = np.finfo(np.float32).eps
    W[np.where(W < 0)] = np.finfo(np.float32).eps

    return W

# M-step: Updata mu , sigma, prior for each cluster
def m_step(data, W, mu, sigma,nclust):
    n= data.shape[0]
    for t in range(nclust):
        temp3 = (data -mu[t])*  W.T[:,t][:,np.newaxis]
        temp4 = (data-mu[t]).T
        sigma[t] = np.dot(temp4,temp3)  / W.sum(axis=1)[t]

        if np.isfinite(np.linalg.cond(sigma)) is False:
            sigma = np.fill_diagonal(sigma, 0.000001)

        mu[t] = (data *  W.T[:,t][:,np.newaxis]).sum(axis=0)/ W.sum(axis=1)[t]
    prior =W.sum(axis=1)/n 
    return mu, sigma, prior


def em_clustering(data,nclust,maxiter,epsilon, mu_indices):
    #Initialization of mean, covariance, and prior
    n,d = data.shape
    mu = np.zeros((nclust,d),dtype=float)  
    sigma = np.zeros((nclust,d,d),dtype=float)

    if len(mu_indices) != 0:
        for t in range(len(mu_indices)):  # assigning the first nclust points to the mu
            mu[t] = data[mu_indices[t]]
            sigma[t] = np.identity(d)
    else:
        for t in range(nclust):  # assigning the first nclust points to the mu
            mu[t] = data[t]
            sigma[t] = np.identity(d)

    prior =  np.asarray(np.repeat(1.0/nclust,nclust),dtype=float) #for each cluster one prior:

    for i in range(maxiter): 
        mu_old = 1 * mu
        W = e_step(data,mu, sigma,prior,nclust) #calling E-step funct.
        mu, sigma, prior = m_step(data, W, mu, sigma,nclust) # calling M-step funct.
        #checking stopping criterion
        temp =0
        for j in range(nclust):
            temp = temp + np.sqrt(np.power((mu[j] - mu_old[j]),2).sum()) 
        temp = round(temp,4)     
        if temp <= epsilon:
            break  
        #print  "Iteration number = %d, stopping criterion = %.4f" %(i+1,temp)
    return mu,sigma,prior,i