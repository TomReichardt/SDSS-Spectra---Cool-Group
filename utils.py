#!/bin/bash

"""
    Cool Group, SciCoder 2018
    
    This script contains test functions for the Spectrum class

"""


import  os, pdb
from    os.path             import  join    as      opj
from    os.path             import  isfile  as      opif
from    os.path             import  isdir   as      opid
from    astropy.io          import  fits
from    glob                import  glob
import  matplotlib.pyplot   as      plt
import  numpy               as      np


curdir = os.path.split(os.path.realpath(__file__))[0]

sList = glob( opj( curdir, 'spectra', '*.fits' ) )
c = 299792.458

test = fits.open( sList[3] ) # open one test spectrum

# print(test.info())
spec = test['COADD'].data
SPAll = test['SPALL'].data
SP = test['SPZLINE'].data
redshift = np.squeeze(SPAll.Z)
vShift = np.log(redshift+1)*c
lShift = vShift*c
# pdb.set_trace()
plt.clf()
plt.plot( 10**(spec['loglam']), spec['flux'] )
plt.plot( 10**(spec['loglam']), spec['model'] )
for line in SP:
    plt.axvline( line['LINEWAVE'], c='r', zorder=0, alpha=0.5 )
plt.savefig('t')
pdb.set_trace()