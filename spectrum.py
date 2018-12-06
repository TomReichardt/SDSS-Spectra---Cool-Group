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
import  argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--lines",
                    default=['Ly_alpha', 'H_alpha'],
                    required=False,
                    help="a list of optional lines: 'Ly_alpha', 'N_V', 'C_IV', 'He_II', \
                    'C_III]', 'Mg_II', '[O_II]', '[O_II]', '[Ne_III]', 'H_zeta', '[Ne_III]', \
                    'H_epsilon', 'H_delta', 'H_gamma', '[O_III]', 'He_II', 'H_beta', \
                    '[O_III]', '[O_III]', 'He_II', '[O_I]', '[N_II]', 'He_I', '[O_I]', \
                    '[S_III]', '[O_I]', '[N_II]', 'H_alpha', '[N_II]', '[S_II]', \
                    '[S_II]', '[Ar_III]'")
args = parser.parse_args()

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

    def plot_spectrum(self, ax=None, *args):
        wavelength = 10**self.coadd['loglam']
        flux = self.coadd['flux']
        if isinstance( ax, type(None) ):
            ax = plt.gca()
        ax.plot(wavelength/(1+np.squeeze(self.spall['Z'])), flux, '-', alpha=0.7)
        ax.set_xlabel(r'Wavelength $\AA$')
        ax.set_ylabel('Flux')

        i = 0
        line_list = [x[0] for x in self.spzline['LINENAME'].split(" ")]
        if args.lines == 'all':
            line_name = line_list
        else:
            line_name = args.linelist
        
        for k in range(len(line_list)):
            j = i % 11
            if line_list[k] in line_name:
                line_wave = self.spzline['LINEWAVE'][k]
                ax.axvline(x=line_wave, color='k', linestyle='-.', linewidth=1.0, alpha=0.5)
                ax.text(line_wave, -30-j*2.5, linename, horizontalalignment='center')
            i = i+1

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
spectra = [Spectrum(f) for f in fileList[:]]
plot_types = {'spectrum' : True,
              'on_sky'   : True,
              'indices'  : True}


def plot_spec(spectra, plot_types):
    fig = plt.figure(figsize=(8,8))
    n_plot_types = sum(plot_types.values())
    gs = gridspec.GridSpec(n_plot_types, 1)
    current_sp = 0
    axs = []
    if plot_types['spectrum']:
        ax = plt.subplot(gs[current_sp, 0])
        for s in spectra:
            ax = s.plot_spectrum(ax=ax)
        current_sp += 1

    if plot_types['on_sky']:
        ax = plt.subplot(gs[current_sp, 0], projection="mollweide")
        ax.grid(True)
        for s in spectra:
            ax = s.plot_on_sky(ax=ax)
        current_sp += 1

    if plot_types['indices']:
        ax = plt.subplot(gs[current_sp, 0])
        for s in spectra:
            ax = s.plot_indices(ax=ax)
        current_sp += 1

    plt.show()

plot_spec(spectra, plot_types)
