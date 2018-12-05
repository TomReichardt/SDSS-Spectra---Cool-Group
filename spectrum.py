from astropy.io import fits
import matplotlib.pyplot as plt


class Spectrum():
    def __init__(self, filename):
        self.file = filename
        self.data = fits.open(self.file)
        self.spectrum_data = self.data[1].data

    def show_spectrum(self):
        wavelength = 10**self.spectrum_data['loglam']
        flux = self.spectrum_data['flux']
        plt.plot(wavelength, flux)
        plt.show()


s = Spectrum(r'C:\Users\thoma_000\Documents\SciCoder\SDSS-Spectra---Cool-Group\spectra\spec-10000-57346-0002.fits')
s.show_spectrum()
