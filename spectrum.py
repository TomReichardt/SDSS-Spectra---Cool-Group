import  os, pdb, re
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

    def __repr__(self):
        return "<Spectrum Object: produced from {}>".format(self.file)

    @property
    def spectral_lines(self):
        return sorted(set(zip(self.spzline['LINEWAVE'], self.spzline['LINENAME'])))

    def plot_spectrum(self, lines=['H', 'Lyman', 'He'], ax=None):
        wavelength = 10**self.coadd['loglam']
        flux = self.coadd['flux']
        self.restframe = wavelength / (1 + np.squeeze(self.spall['Z']))
        wMin, wMax = np.min(self.restframe), np.max(self.restframe)

        if ax is None:
            fig, ax = plt.subplots()
            ax.set_xlabel( r"Wavelength $[{}]$".format(uts.Unit('angstrom').to_string('latex_inline').strip('$')) )
            ax.set_ylabel(r"Flux $[{}]$".format( self.unit.to_string('latex_inline').strip('$') ))

        ax.plot(self.restframe, flux, '-', alpha=0.7)

        lineNames = [line[1] for line in self.spectral_lines]
        xMin, xMax = ax.get_xlim()
        yMin, yMax = ax.get_ylim()
        if 'all' in lines:
            lines = set([LL.split('_')[0].lstrip('[') for LL in lineNames])
            print(lines)
        for i, (line) in enumerate(lines):
            found = [self.spectral_lines[lineNames.index(XX)] for XX in lineNames if "{}_".format(line) in XX and (wMin <= self.spectral_lines[lineNames.index(XX)][0] <= wMax)]
            for q, (line_w, line_n) in enumerate(found):
                j = q % 11
                ax.plot([line_w, line_w], [-30-j*2.5, yMax*1.5], color='k', linestyle='-.', linewidth=1.0, alpha=0.5)
                ax.text(line_w, -30-j*2.5, line_n, horizontalalignment='left')

        y_range = np.ptp(flux) * 1.9
        ax.set_ylim(bottom=yMax-y_range, top=yMax)

        # The `top` never changes, and the `bottom` is relative to the spectrum, not the plot axis.
        return ax

    def plot_on_sky(self, ax=None):
        ra = coord.Angle(self.primary["RA"] * uts.degree)
        ra = ra.wrap_at(180 * uts.degree)
        dec = coord.Angle(self.primary["DEC"] * uts.degree)

        if ax is None:
            ax = plt.subplot(111, projection='mollweide')
            ax.grid(True)
        ax.scatter(ra.radian, dec.radian, s=50, zorder=10)
        ax.scatter(ra.radian, dec.radian, s=75, c='k', zorder=0)

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
SPEC = Spectrum( opj(curdir, 'spectra', 'spec-4055-55359-0006.fits') )
# SPEC = Spectrum( fileList[0] )
# print(SPEC.spectral_lines)

# plt.clf()
# ax = SPEC.plot_indices()
# plt.savefig( 'test' )
# plt.clf()
ax = SPEC.plot_spectrum()
plt.savefig('spec')
pdb.set_trace()

spectra = [Spectrum(f) for f in fileList[:]]

ax = spectra[0].plot_spectrum()
plt.savefig('withLines')
plt.clf()
ax = spectra[1].plot_spectrum(lines=False)
plt.savefig('withoutLines')

# fig = plot_spec(random.sample(spectra, 7), plot_types)
# fig.savefig(opj( curdir, 'test' ))
