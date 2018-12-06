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
import  seaborn

plt.ioff()

curdir = os.path.split(os.path.realpath(__file__))[0]

class Spectrum():
    def __init__(self, filename):
        self.file = filename
        webbrowser.open_new('https://i.kym-cdn.com/photos/images/newsfeed/001/323/085/7fd.jpg')
        # I see you.
        with fits.open(self.file) as file_data:
            try:
                self.primary = file_data['PRIMARY'].header
                self.coadd   = file_data[  'COADD'].data
                self.spall   = file_data[  'SPALL'].data
                self.spzline = file_data['SPZLINE'].data
            except KeyError:
                raise IOError('The provided `.fits` file is not from SDSS.')

    def __repr__(self):
        return "<Spectrum Object: produced from {}>".format(self.file)

    @property
    def spectral_lines(self):
        return sorted(set(zip(self.spzline['LINEWAVE'], self.spzline['LINENAME'])))

    def plot_spectrum(self, lines=True, ax=None):
        wavelength = 10**self.coadd['loglam']
        flux = self.coadd['flux']

        if ax is None:
            fig, ax = plt.subplots()
            ax.set_xlabel(r'Wavelength $\AA$')
            ax.set_ylabel('Flux')

        ax.plot(wavelength / (1 + np.squeeze(self.spall['Z'])), flux, '-', alpha=0.7)

        if lines:
            for i, (line_w, line_n) in enumerate(self.spectral_lines):
                j = i % 11
                ax.axvline(x=line_w, color='k', linestyle='-.', linewidth=1.0, alpha=0.5)
                ax.text(line_w, -30-j*2.5, line_n, horizontalalignment='center')

            y_max = np.max(ax.get_ylim())
            y_range = np.ptp(flux) * 1.9
            ax.set_ylim(bottom=y_max-y_range, top=y_max)

        # The `top` never changes, and the `bottom` is relative to the spectrum, not the plot axis.
        return ax

    def plot_on_sky(self, ax=None):
        ra = coord.Angle(self.primary["RA"] * uts.degree)
        ra = ra.wrap_at(180 * uts.degree)
        dec = coord.Angle(self.primary["DEC"] * uts.degree)

        if ax is None:
            fig, ax = plt.subplots(projection='mollweide')
            ax.grid(True)
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
            fig, ax = plt.subplots()
            ax.set_xlabel( r"Wavelength $[{}]$".format(uts.Unit('angstrom').to_string('latex_inline').strip('$')) )
            ax.set_ylabel( r"${{\rm EW}}\ [{}]$".format(uts.Unit('angstrom').to_string('latex_inline').strip('$')) )

        ax.errorbar( lineWV, lineEW, yerr=lineEWErr, fmt='o' )

        return ax

fileList = glob( opj( curdir, 'spectra', '*.fits' ) )
c = 299792.458
SPEC = Spectrum( fileList[1] )
print(SPEC.spectral_lines)

spectra = [Spectrum(f) for f in fileList[:]]

ax = spectra[0].plot_spectrum()
ax = spectra[1].plot_spectrum(lines=False, ax=ax)

# fig = plot_spec(random.sample(spectra, 7), plot_types)
# fig.savefig(opj( curdir, 'test' ))
