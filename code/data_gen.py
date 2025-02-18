import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from gwpy.timeseries import TimeSeries

# from gw_generator import signal_export

def signal_export(*args, **kwargs):
    return None

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
signal_export(h_series - h_template_series, join(FILE_DIR, 'noise.txt'), normalize_amplitude=False, normalize_times=False)

# -- Resampling
target_srate = 4096.*u.Hz  # Looks best, by far
# target_srate = 2048.*u.Hz
h_series = h_series.resample(target_srate)
h_template_series = h_template_series.resample(target_srate)


plt.figure(figsize=(12, 6))
plt.plot(h_series)
plt.plot(h_template_series)
plt.show()


# -- We NEED the maximum of both to be 1, but want to retain relative
# -- amplitudes. Thus we normalize both by maximum of maxima.
normalize = max(h_series.abs().max(), h_template_series.abs().max())

h_series /= normalize
h_template_series /= normalize

signal_export(h_series, join(FILE_DIR, 'generic_template_w_noise.txt'), normalize_amplitude=False)
signal_export(h_template_series, join(FILE_DIR, 'generic_template_no_noise.txt'), normalize_amplitude=False)


# -- Eccentric Case -----------------------------------------------------------
nr_file = np.loadtxt(join(FILE_DIR, 'eccentric_template.txt'))
nr_series = TimeSeries(nr_file[:, 1], times=nr_file[:, 0])

noise_file = np.loadtxt(join(FILE_DIR, 'noise.txt'))
noise_series = TimeSeries(noise_file[:, 1], times=noise_file[:, 0])


reweight = nr_series.abs().max()
inject_noise = reweight * TimeSeries(
    noise_series.value[::-1],
    times=np.linspace(nr_series.times[0], nr_series.times[-1], num=len(noise_series))
)
inject_noise = inject_noise.resample(1./nr_series.dt)
# -- For some reason, reverse makes things look much more realistic

nr_series = nr_series[1:]  # Do here, after resampling of noise


# inject_noise = inject_noise.resample(4096*u.Hz)
noisy_nr_series = nr_series + inject_noise
taper_window_3 = windows.tukey(len(nr_series), alpha=.25)
noisy_nr_series_tapered = noisy_nr_series * taper_window_3

plt.plot(inject_noise)
plt.plot(nr_series)
plt.plot(noisy_nr_series_tapered)
plt.show()


normalize = noisy_nr_series_tapered.abs().max()

signal_export(noisy_nr_series_tapered/normalize, join(FILE_DIR, 'eccentric_template_w_noise.txt'), normalize_amplitude=False)
signal_export(nr_series/normalize, join(FILE_DIR, 'eccentric_template_no_noise.txt'), normalize_amplitude=False)
