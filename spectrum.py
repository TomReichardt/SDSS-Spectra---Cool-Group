import  os, pdb
from    os.path             import  join    as      opj
from    os.path             import  isfile  as      opif
from    os.path             import  isdir   as      opid
from    astropy.io          import  fits
from    glob                import  glob
import  astropy.coordinates as      coord
import  astropy.units       as      uts
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
        ax.plot(wavelength/(1+np.squeeze(self.spall['Z'])), flux, '-', alpha=0.7)
        ax.set_xlabel(r'Wavelength $\AA$')
        ax.set_ylabel('Flux')

        i = 0
        line_name = [x[0] for x in self.spzline['LINENAME'].split(" ")]
        for x, linename in sorted(set(zip(self.spzline['LINEWAVE'], self.spzline['LINENAME']))):
            j = i % 11
            ax.axvline(x=x, color='k', linestyle='-.', linewidth=1.0, alpha=0.5)
            ax.text(x, -30-j*2.5, linename, horizontalalignment='center') 
            i = i+1        
        
        ylim = ax.get_ylim()
        yRange = np.ptp(ylim)*2.
        ax.set_ylim( bottom=np.max(ylim)-yRange )
        
        
        return ax

    def plot_on_sky(self, ax=None):
        ra = coord.Angle(self.primary["RA"] * uts.degree)
        ra = ra.wrap_at(180 * uts.degree)
        dec = coord.Angle(self.primary["DEC"] * uts.degree)

        if ax is None:
            ax = plt.gca()
        ax.scatter(ra.radian, dec.radian)

        return ax

    def plot_indices(self, ax=None):
        lineWV    = self.spzline[  'LINEWAVE']
        lineNames = self.spzline[  'LINENAME']
        lineEW    = self.spzline[    'LINEEW']
        lineEWErr = self.spzline['LINEEW_ERR']
        
        sore = np.argsort( lineWV )
        lineWV    =    lineWV[sore]
        lineNames = lineNames[sore]
        lineEW    =    lineEW[sore]
        lineEWErr = lineEWErr[sore]
        
        if ax is None:
            ax = plt.gca()
        ax.errorbar( lineWV, lineEW, yerr=lineEWErr, fmt='o' )
        ax.set_xlabel( r"Wavelength $[{}]$".format(uts.Unit('angstrom').to_string('latex_inline').strip('$')) )
        ax.set_ylabel( r"${{\rm EW}}\ [{}]$".format(uts.Unit('angstrom').to_string('latex_inline').strip('$')) )
        
        return ax

fileList = glob( opj( curdir, 'spectra', '*.fits' ) )
c = 299792.458
SPEC = Spectrum( fileList[1] )

plt.clf()
ax = SPEC.plot_indices()
plt.savefig( 'test' )
plt.clf()
ax = SPEC.plot_spectrum()
plt.savefig('spec')
pdb.set_trace()

# fig = plt.figure(figsize=(8,6))
# gs = gridspec.GridSpec(1,2)
# ax = plt.subplot(gs[0,1], projection="mollweide")
# ax.grid(True)
# ax = SPEC.plot_on_sky(ax=ax)
# ax = plt.subplot(gs[0,0])
# ax = SPEC.plot_spectrum(ax=ax)
plt.show()
