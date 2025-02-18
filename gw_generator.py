import lalsimulation.gwsignal.core.waveform as wfm
from lalsimulation.gwsignal.models import gwsignal_get_waveform_generator
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from gwpy.timeseries import TimeSeries


gen = gwsignal_get_waveform_generator('IMRPhenomXPHM')

# -- We choose GW150914-like intrinsic parameters
wf_params = {
    # -- Binary Parameters
    'mass1': 36*u.Msun,
    'mass2': 29*u.Msun,
    'distance': 420*u.Mpc,
    'inclination': 0.2*u.rad,
    # -- Technical Parameters
    # 'deltaT': 1/512*u.s,
    'deltaT': 1/1024*u.s,  # Slower evaluation of TeX file, but looks smoother.
                             # -> also needed for higher fmax in case FT is performed
    'f22_start': 20.*u.Hz,  # Optional
    'f22_ref': 20.*u.Hz,  # Optional
    'f_max': 1024.*u.Hz,  # Optional
    # 'deltaF': 2**-4*u.Hz,  # Optional
    'condition': 1,
}

hpols = wfm.GenerateTDWaveform(wf_params, gen)

ext_params = {
    'det': 'H1',
    'ra': 0.*u.rad,
    'dec': 0.*u.rad,
    'psi': 0.*u.rad,
    'tgps': 0.*u.s,
}  # TODO: find GW150914 values

# h = hpols.strain(**ext_params)
h = hpols[0]


# -- Tapering to make waveform shorter, as it tends to be too long a priori
from scipy.signal import windows
# h_cut = h.crop(start=-0.42*u.s)
h_cut = h.crop(start=-0.2*u.s, end=0.04*u.s)
taper_window = windows.tukey(len(h_cut), alpha=.25)
h_tapered = h_cut * taper_window


# -- Plot for verification
plt.plot(h)
plt.plot(h_tapered, '--')
plt.xlim(-0.5, 0.1)
plt.show()

print(h.data)
print(h.times)

# -- Before exporting: rescale signal to have maximum amplitude of 1
# -- and times between 0 and 1. This is assumed in plotting routine.
def signal_export(signal: TimeSeries, name: str, normalize_amplitude: bool=True, normalize_times=True) -> None:
    """
    Export GW signal in time domain for format required by gwbar.

    Parameters
    ----------
    signal : ~gwpy.timeseries.TimeSeries
        The signal to export.
    """
    signal_export = signal.copy()
    if normalize_amplitude:
        signal_export /= signal_export.abs().max()
    if normalize_times:
        signal_export.times = np.linspace(0, 1, num=signal_export.size, endpoint=True)

    np.savetxt(name, np.transpose([signal_export.times, signal_export.data]))

# signal_export(h, 'generic_template.txt')
signal_export(h_tapered, 'generic_template.txt')


data = np.loadtxt('/home/user/Documents/GitHub/gwbar/fig1-observed-H.txt')
times_data = data[:, 0]
h_data = data[:, 1]


h_series = TimeSeries(h_data, times=times_data)
h_series_peak = np.argmax(h_series)



data = np.loadtxt('/home/user/Documents/GitHub/gwbar/fig2-unfiltered-waveform-H.txt')
times_template = data[:, 0]
h_template = data[:, 1]

h_template_series = TimeSeries(
    h_template,
    times=times_template
    # t0=h_series.t0,
    # dt=h_series.dt,
)

from scipy.signal import windows
taper_window = windows.tukey(len(h_template_series), alpha=.25)
h_template_series = h_template_series * taper_window


taper_window_2 = windows.tukey(len(h_series), alpha=.25)
h_series = h_series * taper_window_2



# -- Store noise realization (with high sampling rate)
signal_export(h_series[1:] - h_template_series, '/home/user/Documents/GitHub/gwbar/noise.txt', normalize_amplitude=False, normalize_times=False)


# print(h_series.dt, h_template_series.dt)
# print(h_series.sample_rate, h_template_series.sample_rate)

# h_series = h_series.resample(4096*u.Hz)
# h_template_series = h_template_series.resample(4096*u.Hz)

# print(h_series)
# # TODO: resample

# plt.figure(figsize=(12, 6))
# plt.plot(h_series)
# # plt.vlines(h_series.times.value[h_series_peak], -1, 1, color='red')
# plt.plot(h_template_series)
# plt.show()




normalize = max(h_series.abs().max(), h_template_series.abs().max())

h_series /= normalize
h_template_series /= normalize


signal_export(h_series, '/home/user/Documents/GitHub/gwbar/h_data.txt', normalize_amplitude=False)
signal_export(h_template_series, '/home/user/Documents/GitHub/gwbar/h_template.txt', normalize_amplitude=False)
