# Alain Andrade - PhD(c) Universidad andres bello 
from astropy.table import Table, hstack
import numpy as np
import matplotlib.pyplot as plt



# this script was made to rebin an array ( modify the resolution power of a spectra)
# rebin array with dx size ----------------------------------------------------------------
def rebin_wavelength(wavelength, flux, shape):

    table = Table([wavelength, data[0][0]], names=['wavelength', 'flux'])

    wavelength_short = np.arange(wavelength[0], wavelength[len(wavelength) - 1], shape)
    new_flux = []

    for i in range(len(wavelength_short)):
        if i < (len(wavelength_short) - 1):
            left = wavelength_short[i]
            right = wavelength_short[i + 1]

            flux = table['flux'][(wavelength > left) & (wavelength < right)]
            flux_binned = np.mean(flux)
            new_flux.append(flux_binned)

        else:
            last_flux = table['flux'][i]
            new_flux.append(last_flux)

    return wavelength_short, new_flux
