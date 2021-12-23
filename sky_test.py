from astropy.io import ascii
from astropy.table import Table, hstack
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import os

# some functions --------------------------------------------------------------


def doppler(v, x_old):
    c = 299792.458  # km/s
    x_new = x_old * np.sqrt((1 + (v / c)) / (1 - (v / c)))  # lambda_new = lamda_old * sqrt((1 + v/c)/(1 - v/c))
    return x_new


# rute of python script -------------------------------------------------------
ruta = os.getcwd()

espectros = ['ADP.2019-05-07T09_34_55.214.fits', 'ADP.2019-05-07T10_03_49.472.fits', 'ADP.2019-05-15T14_29_30.216.fits']
cielos = ['ADP.2019-05-07T09_34_54.902.fits', 'ADP.2019-05-07T10_03_49.010.fits', 'ADP.2019-05-15T14_29_29.706.fits']
dopplers_iraf = ['ADP.2019-05-07T09_34_55.214_sky_dopcor.dat', 'ADP.2019-05-07T10_03_49.472_sky_dopcor.dat', 'ADP.2019-05-15T14_29_30.216_sky_dopcor.dat']

sky_path = f'{ruta}/cielos/'
spec_path = f'{ruta}/espectros/'

for sky, spec, dopcor_spec in zip(cielos, espectros, dopplers_iraf):
    # abrir espectro ----------------------------------------------------------
    spectra = fits.open(f'{spec_path}/{spec}')
    hrd_prim_spec = spectra[0].header
    hdr_sec_spec = spectra[1].header
    data_spec = spectra[1].data[0]

    wave_spec = data_spec[0] * 10
    rflux_spec = data_spec[1]

    # abrir cielo -------------------------------------------------------------
    cielo = fits.open(f'{sky_path}/{sky}')
    hdr_prim_sky = cielo[0].header
    data_sky = cielo[0].data

    # mediana del cielo -------------------------------------------------------
    median_sky = []
    for i in range(len(data_sky[:, 0])):
        bin = data_sky[i, :]
        if len(data_sky[0, :]) > 3:
            median_sky.append(np.median(bin))
        else:
            median_sky.append(np.mean(bin))

    # eje x del cielo ---------------------------------------------------------
    refval = hdr_prim_sky['CRVAL2']  # Value of ref pixel [nm]
    step = hdr_prim_sky['CDELT2']  # Binning factor

    arr = np.arange(0, len(median_sky), 1)
    wave_sky = (refval + arr * step) * 10

    # shifted sky with dopcor(IRAf) --------------------------------------------
    iraf_sky = ascii.read(f'{ruta}/{dopcor_spec}')
    wave_iraf_sky = iraf_sky[0][:]
    median_sky_iraf = iraf_sky[1][:]

    # doppler shift USING PYTHON ----------------------------------------------
    v_helio = hrd_prim_spec['HELICORR']
    wave_sky_doppler = doppler(v_helio, wave_sky)

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # plots para ver la comparacion entre los 3 metodos usados ----------------
    plt.plot(wave_spec, median_sky, alpha=0.6, c='k')
    # plt.plot(wave_sky_doppler, median_sky, alpha=0.6, c='b', linestyle='dotted')
    plt.plot(wave_iraf_sky, median_sky_iraf, alpha=0.6, c='r', linestyle='dashed')
    plt.grid(color='grey', alpha=0.3, linestyle='--')
    plt.title('comparacion entre cielos con doppler shift aplicado')
    plt.xlabel(r'$\lambda$[angstrom]')
    plt.ylabel(r'$F$ [adu]')
    plt.legend(['Alain method', 'dopcor_iraf'])
    plt.show()

    # -------------------------------------------------------------------------
    plt.plot(wave_spec, rflux_spec - median_sky, alpha=0.6, c='k')
    # plt.plot(wave_sky_doppler, rflux_spec - median_sky, alpha=0.6, c='b', linestyle='dotted')
    plt.plot(wave_iraf_sky, rflux_spec - median_sky_iraf, alpha=0.6, c='r', linestyle='dashed')
    plt.title('comparacion de espectros limpios')
    plt.grid(color='grey', alpha=0.3, linestyle='--')
    plt.xlabel(r'$\lambda$[angstrom]')
    plt.ylabel(r'$F$ [adu]')
    plt.legend(['Alain method', 'dopcor_iraf'])
    plt.show()

    # -------------------------------------------------------------------------
    # # doppler shift with python procedure -------------------------------------
    # plt.plot(wave_spec, rflux_spec, color='k', alpha=0.4, linewidth=0.7)
    # plt.plot(wave_sky_doppler, rflux_spec - median_sky, color='b')
    # plt.plot(wave_sky_doppler, np.array(median_sky), color='r', alpha=0.6, linewidth=0.7)
    # plt.xlabel(r'$\lambda$[angstrom]')
    # plt.ylabel(r'$F$ [adu]')
    # plt.title("doppler shift with python")
    # plt.grid(color='grey', alpha=0.3, linestyle='--')
    # plt.legend(['observed', 'spectra-sky', 'sky'])
    # plt.show()

    # # dopcor(iraf) procedure --------------------------------------------------
    # plt.plot(wave_spec, rflux_spec, color='k', alpha=0.4, linewidth=0.7)
    # plt.plot(wave_iraf_sky, rflux_spec - median_sky_iraf, color='b')
    # plt.plot(wave_iraf_sky, np.array(median_sky_iraf), color='r', alpha=0.6, linewidth=0.7)
    # plt.xlabel(r'$\lambda$[angstrom]')
    # plt.ylabel(r'$F$ [adu]')
    # plt.title("doppler shift with dopcor(IRAF)")
    # plt.grid(color='grey', alpha=0.3, linestyle='--')
    # plt.legend(['observed', 'spectra-sky', 'sky'])
    # plt.show()

    # # alain's method procedure ------------------------------------------------
    # plt.plot(wave_spec, rflux_spec, color='k', alpha=0.4, linewidth=0.7)
    # plt.plot(wave_spec, rflux_spec - median_sky, color='b')
    # plt.plot(wave_spec, np.array(median_sky), color='r', alpha=0.6, linewidth=0.7)
    # plt.xlabel(r'$\lambda$[angstrom]')
    # plt.ylabel(r'$F$ [adu]')
    # plt.title("Alain's method")
    # plt.grid(color='grey', alpha=0.3, linestyle='--')
    # plt.legend(['observed', 'spectra-sky', 'sky'])
    # plt.show()
