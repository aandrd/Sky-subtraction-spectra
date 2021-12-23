# Alain Andrade Valenzuela - 1st year PhD in Astrphysics student
# Universidad Andres Bello
# December 2021

# -----------------------------------------------------------------------------
from astropy.io import ascii
from astropy.table import Table, hstack
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import numpy as np
import os

# rute of python script -------------------------------------------------------
ruta = os.getcwd()

# array for the aperture cycle ------------------------------------------------
sky_data = ['giraffe_ancillary_sky']
spectrums = ['girafee_spectrum']

# cycle in the sky datas ------------------------------------------------------
arr = []
count = 0

# 1st for loop iterating in the files of spectres folders
for sky, spectrograph in zip(sky_data, spectrums):
    # set path of files and search spectrum archives --------------------------
    data_route = f'{ruta}/data/{sky}/'
    spec_route = f'{ruta}/data/{spectrograph}/original/'

    # list with files sorted for both folders
    spec_archives = np.sort(os.listdir(spec_route))
    archives = np.sort(os.listdir(data_route))

    # cycle in the spectra archives -----------------------------------------
    for archive, archive_spec in zip(archives, spec_archives):
        spec_sky = f'{ruta}/data/{sky}/{archive}'
        spec_obs = f'{ruta}/data/{spectrograph}/original/{archive_spec}'

        # exclude the non-fits data -------------------------------------------
        if (archive == '.DS_Store') or (archive_spec == 'dat') or (archive_spec == '.DS_Store'):
            continue
        # open fits file of sky
        fits_file = fits.open(spec_sky)  # fits file of sky
        prim_spec = fits_file[0]         # primary header of sky
        spec_spec = fits_file[1]         # secondary header of sky

        refval = prim_spec.header['CRVAL2']  # Value of ref pixel [nm]
        step = prim_spec.header['CDELT2']    # Binning factor

        # open fits file of spectra
        fits_file_spec = fits.open(spec_obs)  # fits file of star specrta
        prim_spec_obs = fits_file_spec[0]  # primary header of star spectra
        spec_spec_obs = fits_file_spec[1]  # secondaty header of stars spectra
        v_helio = prim_spec_obs.header['HELICORR']  # search V_helio in header

        # some prints ---------------------------------------------------------
        print('-------------------------------------------------')
        print(archive_spec)  # name of star spectra fits file
        print(archive)       # name of sky spectra fits file
        print(f'heliocentric velocity : {v_helio} [km/s]')

        if count >= 0:
            # set name of spectra ---------------------------------------------
            name_spec_split = archive_spec.split('.')  # split the string array of name
            name_spec = f'{name_spec_split[0]}.{name_spec_split[1]}.{name_spec_split[2]}'

            # -----------------------------------------------------------------
            data = prim_spec.data           # sky data
            data2 = spec_spec_obs.data[0]   # star spectra data

            wave_spec = data2[0] * 10       # nm to angstrom convertion
            rflux_spec = data2[1]           # flux array of star spectra

            # cycle to create mean/median sky spectra --------------------------
            median_sky = []
            for i in range(len(data[:, 0])):  # for in the bins array
                bin = data[i, :]              # select all fibers for each bin
                if len(data[0, :]) > 3:       # take median if fibers > 3
                    median_sky.append(np.median(bin))
                else:
                    median_sky.append(np.mean(bin))  # take mean if fibers <= 3

            flux_clean = rflux_spec - median_sky  # make the subtraction in [adu]

            # plot of the procedure of sky substraction ---------------------
            plt.plot(wave_spec, rflux_spec, color='k', alpha=0.4, linewidth=0.7)  # star with telluric lines
            plt.plot(wave_spec, rflux_spec - median_sky, color='b')  # clean star spectra
            plt.plot(wave_spec, np.array(median_sky), color='r', alpha=0.6, linewidth=0.7)  # sky spectra

            plt.xlabel(r'$\lambda$[angstrom]')
            plt.ylabel(r'$F$ [adu]')
            plt.grid(color='grey', alpha=0.3, linestyle='--')
            plt.legend(['spectra', 'spectra-sky', 'sky'])
            plt.title(f'GIRAFFE: {name_spec}')
            plt.show()

            # save the star spectra without telluric lines in a .dat file -----
            # cleaned_spectra = Table([wave_spec, flux_clean], names=['wavelength', 'reduced_flux'])
            # ascii.write(cleaned_spectra, f'/Users/hbarra/Desktop/Universidad/Phd/Courses/Practica/data/giraffe_clean/{name_spec}_clean.dat', overwrite=True, format='commented_header')

        count += 1
