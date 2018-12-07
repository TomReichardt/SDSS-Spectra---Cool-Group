import  os, pdb
from    os.path             import  join    as      opj
from    os.path             import  isfile  as      opif
from    os.path             import  isdir   as      opid
from    astropy.io          import  fits
from    glob                import  glob
import  matplotlib.pyplot   as      plt
import  numpy               as      np
#import  spectrum
from spectrum import Spectrum
#from spectrum import show_spectrum

test_spec1='./spectra/spec-6055-56102-0008.fits'

def test_fits_exist():
    s = Spectrum(test_spec1)
    assert opif(s.file), 'File does not exist'



def test_coordinate():
    s = Spectrum(test_spec1)
    assert s.plot_on_sky





