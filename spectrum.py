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
            try:
                self.primary = file_data['PRIMARY'].data
                self.coadd   = file_data[  'COADD'].data
                self.spall   = file_data[  'SPALL'].data
                self.spzline = file_data['SPZLINE'].data
            except KeyError:
                raise IOError('The provided `.fits` file is not from SDSS.')
        

    def plot(self, ax=None):
        wavelength = 10**self.coadd['loglam']
        flux = self.coadd['flux']
        if isinstance( ax, type(None) ):
            ax = plt.gca()
        ax.plot(wavelength/(1+np.squeeze(self.spall['Z'])), flux)
        
        return ax
        
    def plot_indices(self):
        lineWV    = self.spzline[  'LINEWAVE']
        lineNames = self.spzline[  'LINENAME']
        lineEW    = self.spzline[    'LINEEW']
        lineEWErr = self.spzline['LINEEW_ERR']

fileList = glob( opj( curdir, 'spectra', '*.fits' ) )
c = 299792.458
SPEC = Spectrum( fileList[1] )
pdb.set_trace()
plt.clf()
ax = SPEC.plot()
plt.savefig('s')

pdb.set_trace()
