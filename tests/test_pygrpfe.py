'''
Tests for pygfe

DATE: Jan 2021
'''

import pytest
import pandas as pd
import pygrpfe as gfe
import numpy as np

ax = np.newaxis

def test_pygfe_group():

    def dgp_simulate(ni,nt,gamma=2.0,eps_sd=1.0):
        """ simulates according to the model """
        alpha = np.random.normal(size=(ni))
        eps   = np.random.normal(size=(ni,nt))
        v     = np.random.normal(size=(ni,nt))
        
        # non-censored outcome
        W = alpha[:,ax] + eps*eps_sd
        
        # utility
        U = (np.exp( alpha * (1-gamma)) - 1)/(1-gamma)
        U = U - U.mean()
        
        # costs
        C1 = -1; C0=0;
        
        # binary decision
        Y = np.ones((ni,nt))
        Y[:,0] = U.squeeze() > C1 + v[:,0]
        for t in range(1,nt): 
            Y[:,t] = U > C1*Y[:,t-1] + C0*(1-Y[:,t-1]) + v[:,t]
        W =  W * Y
            
        return(W,Y)

    ni = 200
    nt = 20
    Y,D = dgp_simulate(ni,nt,2.0)

    M_itm = np.stack([Y,D],axis=2)
    G_i,_ = gfe.group(M_itm)

    assert G_i.max() > 0
