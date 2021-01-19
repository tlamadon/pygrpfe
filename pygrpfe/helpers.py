""" 
 help functions to run BLM2
"""

import torch
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from statsmodels.discrete.discrete_model import Probit
import patsy as patsy
import matplotlib.pylab as plt
from scipy.optimize import minimize
from scipy import sparse
from scipy.stats import norm

ax = np.newaxis

def group(M_itm, max_k=100,whitening=True,scale=True ):
    """ function that returns the groups
    inputs are the micro moments, the function expect a (N,T,M) matrix.
    
    for example: M_itm = np.stack([Y,X],axis=2)
    """

    ni,nt,nm = M_itm.shape

    if ( scale==True ):
        M_itm = (M_itm - M_itm.mean((0,1)))/ M_itm.std((0,1))

    # following the document on weighting moments
    H_im = M_itm.mean(axis=1)

    # computing the within noise
    R = (M_itm - H_im[:,ax,:]).reshape((nt*ni,nm))
    Vw = np.matmul(R.transpose(),R)/(ni*nt**2)
    Vb = np.matmul( H_im.transpose(), H_im)/ni - Vw
    G = np.matmul(Vb, np.linalg.inv( Vb+ Vw))

    if whitening==False:
        G = np.eye(nm)

    Mw = np.matmul(G,H_im.transpose()).transpose()
    noise_level = np.matmul(G,np.matmul(Vw,G.transpose())).sum()
    
    # finding number of groups
    for k_i in range(2,max_k):
        #km = KMeans(init='k-means++', n_clusters=k_i, n_init=100)
        km = KMeans(algorithm='full',init='random', n_clusters=k_i, n_init=100, max_iter=1000)
        res = km.fit(Mw)
        sum_sqr = ((Mw - res.cluster_centers_[res.labels_,:])**2).sum()
        if sum_sqr/ni < noise_level:
            break
    ID_i = res.labels_.reshape((ni,1))
    # print("k_i = {}".format(k_i))
    # print(G)
    
    return(ID_i.flatten(),G)          

def train(model, maxiter=1000):
    
    optimizer = torch.optim.Adam(model.params, lr=0.1)

    maxiter = 10000
    loss_vec = np.zeros(maxiter)
    loss_last = 1e5
    
    for i in range(maxiter):
        optimizer.zero_grad()
        loss = model.loss()
        
        # gradient descent
        loss.backward(retain_graph=True)
        optimizer.step()          
        
        # check loss change
        loss2 = loss.item()
        dloss = np.abs(loss_last - loss2)/np.abs(loss_last)
        if (dloss< 1e-8):
            break
        
        loss_last = loss2        
        loss_vec[i] = loss2

    return(loss_vec)
    
      