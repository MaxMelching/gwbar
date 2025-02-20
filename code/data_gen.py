import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from gwpy.timeseries import TimeSeries

from gw_generator import signal_export

from os.path import join, dirname
FILE_DIR = dirname(__file__)


# -- GW150914 -----------------------------------------------------------------
data = np.loadtxt(join(FILE_DIR, 'fig1-observed-H.txt'))
h_series = TimeSeries(data[:, 1], times=data[:, 0])
h_series = h_series[1:]
h_series_peak = np.argmax(h_series)

data = np.loadtxt(join(FILE_DIR, 'fig2-unfiltered-waveform-H.txt'))
h_template_series = TimeSeries(data[:, 1], times=data[:, 0])
# h_template_series = h_template_series.append(
#     TimeSeries(np.array([0]), times=np.array([h_template_series.times.value[-1] + 0*h_template_series.dt.value])*u.s)
# )


from scipy.signal import windows
taper_window_1 = windows.tukey(len(h_template_series), alpha=.25)
h_template_series *= taper_window_1

taper_window_2 = windows.tukey(len(h_series), alpha=.25)
h_series *= taper_window_2


# -- Store noise realization (with high sampling rate)
# signal_export(h_series[1:] - h_template_series, join(FILE_DIR, 'noise.txt'), normalize_amplitude=False, normalize_times=False)
# signal_export(h_series - h_template_series, join(FILE_DIR, 'noise.txt'), normalize_amplitude=False, normalize_times=False)


# from gw_signal_tools.PSDs import psd_gw150914
from gw_signal_tools.waveform import get_signal_at_target_frequs, fd_to_td, td_to_fd, fill_f_range

data = np.loadtxt(join(FILE_DIR, 'psd-H.txt'))
from gwpy.frequencyseries import FrequencySeries
psd_gw150914 = np.sqrt(FrequencySeries(data[:, 1], frequencies=data[:, 0]))


h_template_fd = td_to_fd(h_template_series)
print(h_template_series.epoch, h_template_fd.epoch)

h_template_series_whiten_fd = h_template_fd / get_signal_at_target_frequs(psd_gw150914, h_template_fd.frequencies)
h_template_series_whiten_fd = fill_f_range(
    h_template_series_whiten_fd,
    fill_val=0.,
    # fill_bounds=[20*u.Hz, 1023*u.Hz]
    fill_bounds=[10*u.Hz, 1023*u.Hz]
    # fill_bounds=[20*u.Hz, 420*u.Hz]
)


h_template_series_whiten = fd_to_td(h_template_series_whiten_fd)
h_template_series_whiten /= h_template_series_whiten.abs().max()

taper_window_3 = windows.tukey(len(h_template_series_whiten), alpha=.25)
h_template_series_whiten *= taper_window_3


# -- Resampling
target_srate = 4096.*u.Hz  # Looks best, by far
# target_srate = 2048.*u.Hz
h_series = h_series.resample(target_srate)
h_template_series = h_template_series.resample(target_srate)


# -- We NEED the maximum of both to be 1, but want to retain relative
# -- amplitudes. Thus we normalize both by maximum of maxima.
normalize = max(h_series.abs().max(), h_template_series.abs().max())

h_series /= normalize
h_template_series /= normalize

signal_export(h_series, join(FILE_DIR, 'generic_template_w_noise.txt'), normalize_amplitude=False)
signal_export(h_template_series, join(FILE_DIR, 'generic_template_no_noise.txt'), normalize_amplitude=False)

h_template_series_whiten = h_template_series_whiten.resample(target_srate) #/ normalize
signal_export(h_template_series_whiten, join(FILE_DIR, 'generic_template_no_noise_whitened.txt'), normalize_amplitude=False)
# -- I think storing noise with whitened template is better
signal_export(h_series - h_template_series_whiten, join(FILE_DIR, 'noise.txt'), normalize_amplitude=False, normalize_times=False)


plt.figure(figsize=(12, 6))
plt.plot(h_series)
plt.plot(h_template_series)
plt.plot(h_template_series_whiten)
plt.plot(h_series - h_template_series_whiten)
plt.show()


# -- Eccentric Case -----------------------------------------------------------
nr_file = np.loadtxt(join(FILE_DIR, 'eccentric_template.txt'))
nr_series = TimeSeries(nr_file[:, 1], times=nr_file[:, 0])

noise_file = np.loadtxt(join(FILE_DIR, 'noise.txt'))
noise_series = TimeSeries(noise_file[:, 1], times=noise_file[:, 0])


reweight = nr_series.abs().max()
inject_noise = TimeSeries(
    # reweight * noise_series.value[::-1],
    1.2 * reweight * noise_series.value,
    times=np.linspace(nr_series.times[0], nr_series.times[-1], num=len(noise_series))
)
inject_noise = inject_noise.resample(1./nr_series.dt)
# -- For some reason, reverse makes things look much more realistic -> for previous noise that was true

nr_series = nr_series[1:]  # Do here, after resampling of noise


# inject_noise = inject_noise.resample(4096*u.Hz)
noisy_nr_series = nr_series + inject_noise
taper_window_4 = windows.tukey(len(nr_series), alpha=.25)
noisy_nr_series_tapered = noisy_nr_series * taper_window_4

plt.plot(inject_noise)
plt.plot(nr_series)
plt.plot(noisy_nr_series_tapered)
plt.show()


normalize = noisy_nr_series_tapered.abs().max()

signal_export(noisy_nr_series_tapered/normalize, join(FILE_DIR, 'eccentric_template_w_noise.txt'), normalize_amplitude=False)
signal_export(nr_series/normalize, join(FILE_DIR, 'eccentric_template_no_noise.txt'), normalize_amplitude=False)
