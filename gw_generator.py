import lalsimulation.gwsignal.core.waveform as wfm
from lalsimulation.gwsignal.models import gwsignal_get_waveform_generator
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from gwpy.timeseries import TimeSeries


gen = gwsignal_get_waveform_generator('IMRPhenomXPHM')

wf_params = {
    # -- Binary Parameters
    'mass1': 36*u.Msun,
    'mass2': 29*u.Msun,
    'distance': 420*u.Mpc,
    # -- Technical Parameters
    # 'deltaT': 1/512*u.s,
    'deltaT': 1/1024*u.s,  # Makes evaluation of TeX file really slow -> but needed for better fmax in FT
    'f22_start': 20.*u.Hz,  # Optional
    'f22_ref': 20.*u.Hz,  # Optional
    'f_max': 1024.*u.Hz,  # Optional
    # # 'deltaF': 2**-4*u.Hz,  # Optional
    'condition': 1,
}

hpols = wfm.GenerateTDWaveform(wf_params, gen)

ext_params = {
    'det': 'H1',
    'ra': 0.*u.rad,
    'dec': 0.*u.rad,
    'psi': 0.*u.rad,
    'tgps': 0.*u.s,
}

h = hpols.strain(**ext_params)


# -- Potentially whiten waveform?
# from gw_signal_tools.PSDs import psd_gw150914, psd_sim
# from gw_signal_tools.waveform import fd_to_td, td_to_fd, get_signal_at_target_frequs, fill_f_range

# hf = td_to_fd(h)

# # hf = wfm.GenerateFDWaveform(wf_params, gen)[0]
# # hf.epoch = hf.epoch - 1/hf.df
# # # print(hf.epoch)


# psd = get_signal_at_target_frequs(
#     # psd_gw150914,
#     psd_sim,
#     hf.frequencies,
#     fill_val=1.*u.strain**2/u.Hz,
#     fill_bounds=[wf_params.get('f22_start', 20.*u.Hz), None],
# )
# asd = psd**0.5
# h_whitened = fd_to_td(hf/asd)
# # h_whitened = fd_to_td(fill_f_range(hf, fill_val=0., fill_bounds=[None, 128*u.Hz])/asd)


# -- Tapering to make waveform shorter, as it tends to be too long a priori
from scipy.signal import windows
# h_cut = h.crop(start=-0.42*u.s)
h_cut = h.crop(start=-0.2*u.s, end=0.01*u.s)
taper_window = windows.tukey(len(h_cut), alpha=.25)
h_tapered = h_cut * taper_window


# -- Potentially plot for verification
plt.plot(h)
plt.plot(h_tapered, '--')
# plt.plot(h_whitened*(h.abs().max()/h_whitened.abs().max()), '-.')  # Rescale
# plt.xlim(-1, 0.1)
# plt.xlim(-0.5, 0.1)
plt.show()

print(h.data)
print(h.times)

# -- Before exporting: rescale signal to have maximum amplitude of 1
# -- and times between 0 and 1. This is assumed in plotting routine.
def signal_export(signal: TimeSeries) -> None:
    """
    Export GW signal in time domain for format required by gwbar.

    Parameters
    ----------
    signal : ~gwpy.timeseries.TimeSeries
        The signal to export.
    """
    signal_export = signal.copy()
    signal_export /= signal_export.abs().max()
    signal_export.times = np.linspace(0, 1, num=signal_export.size, endpoint=True)

    np.savetxt(f'exported_template.txt', np.transpose([signal_export.times, signal_export.data]))

# signal_export(h)
signal_export(h_tapered)
