from astropy.io import fits
import matplotlib.pyplot as plt


class Spectrum():
    def __init__(self, filename):
        self.file = filename
        with fits.open(self.file) as file_data:
            self.header = file_data[0].header
            self.spectrum_data = file_data[1].data

        self.ra = self.header['RA']
        self.dec = self.header['DEC']


    def show_spectrum(self):
        wavelength = 10**self.spectrum_data['loglam']
        flux = self.spectrum_data['flux']
        plt.plot(wavelength, flux)
        plt.show()

s = Spectrum(r'C:\Users\thoma_000\Documents\SciCoder\SDSS-Spectra---Cool-Group\spectra\spec-10000-57346-0002.fits')
print(s.ra, s.dec)
