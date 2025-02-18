import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from gwpy.timeseries import TimeSeries
from scipy.signal import windows


# gen = gwsignal_get_waveform_generator('SEOBNRv4EHM')
# gen = gwsignal_get_waveform_generator('NR_hdf5')
# PATH = '.'
# import lal
# params = lal.CreateDict()
# import lalsimulation as lalsim
# lalsim.SimInspiralWaveformParamsInsertNumRelData(params, '~/Documents')

import sxs
nr_sim = sxs.load('SXS:BBH:0324').h
nr_sim_22 = nr_sim[:, nr_sim.index(2, 2)]


equally_spaced_times = np.arange(nr_sim.t[0], nr_sim.t[-1], step=2)

nr_sim_22 = nr_sim_22.interpolate(equally_spaced_times)

nr_series = TimeSeries(
    np.real(nr_sim_22),
    times=equally_spaced_times,
)

# nr_series_cropped = nr_series[len(nr_series)//4:]  # Corresponds to about half of signal, due to finer sampling at end
nr_series_cropped = nr_series[len(nr_series)//2:]  # Corresponds to about half of signal
taper_window = windows.tukey(len(nr_series_cropped), alpha=.25)
nr_series_tapered = nr_series_cropped * taper_window

# nr_series.interpolate(
#     np.arange(nr_series.times[0], nr_series.times[-1], step=wf_params['deltaT'])
# )
# nr_series.resample(wf_params['deltaT'])

# plt.plot(nr_sim.t, nr_sim.data.view(float))
# plt.plot(nr_sim.t, nr_sim_22)
plt.plot(nr_series)
plt.plot(nr_series_tapered)
plt.show()


from gw_generator import signal_export
signal_export(nr_series_tapered, 'eccentric_template.txt')


noise_file = np.loadtxt('/home/user/Documents/GitHub/gwbar/noise.txt')
noise_times = noise_file[:, 0]
noise_data = noise_file[:, 1]

noise_series = TimeSeries(noise_data, times=noise_times)

# noise_series = noise_series.resample(nr_series_tapered.sample_rate)

# # noisy_nr_series = nr_series_cropped.inject(noise_series)
# # offset=len(noise_series)//8
# noise_series = noise_series.resample(4096*u.Hz)
# offset = 10
# # reweight = noise_series.abs().max()
# reweight = nr_series_tapered.abs().max()
# # reweight = noise_series.abs().max() / nr_series_tapered.abs().max()
# inject_noise = reweight*TimeSeries(noise_series[offset:offset+len(nr_series_cropped)], times=nr_series_cropped.times)
# -- Maximum of eccentric is at 0.3, we have to reduce for nice looking output

reweight = nr_series_tapered.abs().max()
inject_noise = reweight * TimeSeries(noise_series.value[::-1], times=np.linspace(nr_series_cropped.times[0], nr_series_cropped.times[-1], num=len(noise_series)))
inject_noise = inject_noise.resample(1./nr_series_cropped.dt)
# -- For some reason, reverse makes things look much more realistic


# inject_noise = inject_noise.resample(4096*u.Hz)
noisy_nr_series = nr_series_cropped[1:] + inject_noise
noisy_nr_series_tapered = noisy_nr_series * taper_window[1:]

plt.plot(inject_noise)
plt.plot(nr_series_tapered)
plt.plot(noisy_nr_series_tapered)

plt.show()


normalize = noisy_nr_series_tapered.abs().max()

signal_export(noisy_nr_series_tapered/normalize, '/home/user/Documents/GitHub/gwbar/eccentric_template_w_noise.txt', normalize_amplitude=False)
signal_export(nr_series_tapered/normalize, '/home/user/Documents/GitHub/gwbar/eccentric_template_as_data.txt', normalize_amplitude=False)
