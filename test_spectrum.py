import  os, pdb
from    os.path             import  join    as      opj
from    os.path             import  isfile  as      opif
from    os.path             import  isdir   as      opid
from    astropy.io          import  fits
from    glob                import  glob
import  matplotlib.pyplot   as      plt
import  numpy               as      np
#import  spectrum
from    spectrum            import Spectrum
#from spectrum import show_spectrum

curdir = os.path.split(os.path.realpath(__file__))[0]

test_file = opj(curdir, 'spectra', 'spec-6055-56102-0008.fits')

def test_fits_exist():
    s = Spectrum(test_file)
    assert opif(s.file), 'File does not exist'

def test_ra():
    s = Spectrum(test_file)
    np.testing.assert_almost_equal(s.ra, 212.641274)

def test_dec():
    s = Spectrum(test_file)
    np.testing.assert_almost_equal(s.dec, 44.621874)

def test_headers_read():
    s = Spectrum(test_file)
    assert len(s.headers) == 4, 'Unexpected number of headers: len(headers) != 4'

def test_coadd():
    s = Spectrum(test_file)
    assert type(s.coadd) == fits.fitsrec.FITS_rec, 'COADD is the wrong object type or does not exist'

def test_spall():
    s = Spectrum(test_file)
    assert type(s.spall) == fits.fitsrec.FITS_rec, 'SPALL is the wrong object type or does not exist'

def test_spall():
    s = Spectrum(test_file)
    assert type(s.spzline) == fits.fitsrec.FITS_rec, 'SPALL is the wrong object type or does not exist'

s = Spectrum(test_file)
print(type(s.spzline))
