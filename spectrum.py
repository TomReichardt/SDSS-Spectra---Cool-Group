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

        self.__dict__.update(dict(self.header))

    def plot(self, ax=None):
        wavelength = 10**self.spectrum_data['loglam']
        flux = self.spectrum_data['flux']
        if isinstance( ax, type(None) ):
            ax = plt.gca()
        ax.plot(wavelength/(1+self.Z), flux)
        
        return ax

fileList = glob( opj( curdir, 'spectra', '*.fits' ) )
c = 299792.458
s = Spectrum( fileList[1] )

ax = s.plot()
plt.savefig('s')
