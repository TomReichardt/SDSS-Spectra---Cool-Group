import  os, pdb
from    os.path             import  join    as      opj
from    os.path             import  isfile  as      opif
from    os.path             import  isdir   as      opid
from    astropy.io          import  fits
from    glob                import  glob
import  matplotlib.pyplot   as      plt
import  numpy               as      np


curdir = os.path.split(os.path.realpath(__file__))[0]


class Spectrum():
    def __init__(self, filename):
        self.file = filename
        with fits.open(self.file) as file_data:
            self.header = file_data[0].header
            self.spectrum_data = file_data[1].data
        exStr = "self.{key:s} = self.header['{key:s}']"
        for key in self.header.keys():
            exec( exStr.format( key=key ) )

    def show_spectrum(self):
        wavelength = 10**self.spectrum_data['loglam']
        flux = self.spectrum_data['flux']
        plt.plot(wavelength, flux)
        plt.show()

fileList = glob( opj( curdir, 'spectra', '*.fits' ) )
c = 299792.458
s = Spectrum( fileList[1] )
print(s.ra, s.dec)
