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
import  random

plt.ioff()

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

# plt.clf()
# ax = SPEC.plot_indices()
# plt.savefig( 'test' )
# plt.clf()
# ax = SPEC.plot_spectrum()
# plt.savefig('spec')
# pdb.set_trace()

spectra = [Spectrum(f) for f in fileList[:]]
plot_types = {'spectrum' : True,
              'on_sky'   : True,
              'indices'  : True}


def plot_spec(spectra, plot_types):
    fig = plt.figure(figsize=(8,8))
    n_plot_types = sum(plot_types.values())
    nRC = round(np.sqrt(n_plot_types)).astype(int)
    gs = gridspec.GridSpec( nRC, nRC, hspace=0.3, wspace=0.3 )
    current_sp = 0
    col = 0
    if plot_types['spectrum']:
        ax = plt.subplot(gs[col,current_sp])
        for s in spectra:
            ax = s.plot_spectrum(ax=ax)
        current_sp += 1
    if current_sp == nRC:
        col+=1

    if plot_types['indices']:
        ax = plt.subplot(gs[col,current_sp])
        for s in spectra:
            ax = s.plot_indices(ax=ax)
        current_sp += 1
    if current_sp == nRC:
        col+=1

    if plot_types['on_sky']:
        ax = plt.subplot(gs[col,:], projection="mollweide")
        ax.grid(True)
        for s in spectra:
            ax = s.plot_on_sky(ax=ax)
        current_sp += 1

    return fig

fig = plot_spec(random.sample(spectra, 7), plot_types)
fig.savefig('test')