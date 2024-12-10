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
