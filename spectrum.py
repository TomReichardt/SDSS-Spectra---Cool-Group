import  os, pdb
from    os.path             import  join    as      opj
from    os.path             import  isfile  as      opif
from    os.path             import  isdir   as      opid
from    astropy.io          import  fits
from    glob                import  glob
import  astropy.coordinates as      coord
import  astropy.units       as      u
import  matplotlib.pyplot   as      plt
import  matplotlib.gridspec as      gridspec
import  numpy               as      np


curdir = os.path.split(os.path.realpath(__file__))[0]

class Spectrum():
    def __init__(self, filename):
        self.file = filename
        with fits.open(self.file) as file_data:
            try:
                self.primary = file_data['PRIMARY'].header
                self.coadd   = file_data[  'COADD'].data
                self.spall   = file_data[  'SPALL'].data
                self.spzline = file_data['SPZLINE'].data
            except KeyError:
                raise IOError('The provided `.fits` file is not from SDSS.')


    def plot_spectrum(self, ax=None):
        wavelength = 10**self.coadd['loglam']
        flux = self.coadd['flux']
        if isinstance( ax, type(None) ):
            ax = plt.gca()
        ax.plot(wavelength/(1+np.squeeze(self.spall['Z'])), flux)


    def plot_on_sky(self, ax=None):
        ra = coord.Angle(self.primary["RA"] * u.degree)
        ra = ra.wrap_at(180 * u.degree)
        dec = coord.Angle(self.primary["DEC"] * u.degree)

        if ax is None:
            ax = plt.gca()
        ax.scatter(ra.radian, dec.radian)

        return ax

    def plot_indices(self):
        lineWV    = self.spzline[  'LINEWAVE']
        lineNames = self.spzline[  'LINENAME']
        lineEW    = self.spzline[    'LINEEW']
        lineEWErr = self.spzline['LINEEW_ERR']

fileList = glob( opj( curdir, 'spectra', '*.fits' ) )
c = 299792.458
s = Spectrum( fileList[1] )

fig = plt.figure(figsize=(8,6))
gs = gridspec.GridSpec(1,2)
ax = plt.subplot(gs[0,1], projection="mollweide")
ax.grid(True)
ax = s.plot_on_sky(ax=ax)
ax = plt.subplot(gs[0,0])
ax = s.plot_spectrum(ax=ax)
plt.show()
