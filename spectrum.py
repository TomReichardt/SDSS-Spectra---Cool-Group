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

class Attributes:
    pass

class Spectrum():
    def __init__(self, filename):
        self.file = filename
        with fits.open(self.file) as file_data:
            try:
                setattr(self, 'headers', Attributes()) # Set `headers` attribute as an Attribute object
                for exten in file_data: #loop over the extensions
                    head = exten.header
                    setattr(self.headers, exten.name.lower(), head)
                # use as Spectrum.headers.coadd['<key>']

                # self.primary = file_data['PRIMARY'].header # primary already added above
                self.coadd   = file_data[  'COADD'].data
                self.spall   = file_data[  'SPALL'].data
                self.spzline = file_data['SPZLINE'].data

            except KeyError:
                raise IOError('The provided `.fits` file is not from SDSS.')

        self.unit = uts.Unit( self.headers.primary['BUNIT'].replace('Ang', 'angstrom') )
        self.class = self.spall["CLASS"]

    def __repr__(self):
        return "{}({})".format(self.__class_.__name__, self.file)

    def __str__(self):
        return "<Spectrum object of a {}: produced from {}>".format(self.class, self.file)

    @property
    def spectral_lines(self):
        return sorted(set(zip(self.spzline['LINEWAVE'], self.spzline['LINENAME'])))


    def plot_spectrum(self, lines=True, ax=None):
        wavelength = 10**self.coadd['loglam']
        flux = self.coadd['flux']

        if ax is None:
            fig, ax = plt.subplots()
            ax.set_xlabel( r"Wavelength $[{}]$".format(uts.Unit('angstrom').to_string('latex_inline').strip('$')) )
            ax.set_ylabel(r"Flux $[{}]$".format( self.unit.to_string('latex_inline').strip('$') ))

        ax.plot(wavelength / (1 + np.squeeze(self.spall['Z'])), flux, '-', alpha=0.7)

        if lines:
            for i, (line_w, line_n) in enumerate(self.spectral_lines):
                j = i % 11
                ax.axvline(x=line_w, color='k', linestyle='-.', linewidth=1.0, alpha=0.5)
                ax.text(line_w, -30-j*2.5, line_n, horizontalalignment='center')

            y_max = np.max(ax.get_ylim())
            y_range = np.ptp(flux) * 1.9
            ax.set_ylim(bottom=y_max-y_range, top=y_max)

        return ax

    def plot_on_sky(self, ax=None):
        ra = coord.Angle(self.headers.primary["RA"] * uts.degree)
        ra = ra.wrap_at(180 * uts.degree)
        dec = coord.Angle(self.headers.primary["DEC"] * uts.degree)

        if ax is None:
            ax = plt.subplot(111, projection='mollweide')
            ax.grid(True)

        ax.scatter(ra.radian, dec.radian, s=75, edgecolor='k', zorder=10)

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
SPEC = Spectrum( fileList[1] )
spectra = [Spectrum(f) for f in fileList[:]]

ax = plt.subplot(projection='mollweide')
ax.grid(True)

for s in spectra:
    ax = s.plot_on_sky(ax=ax)
plt.show()

# fig = plot_spec(random.sample(spectra, 7), plot_types)
# fig.savefig(opj( curdir, 'test' ))
