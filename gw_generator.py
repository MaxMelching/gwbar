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
def signal_export(signal: TimeSeries, name: str) -> None:
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

    np.savetxt(name, np.transpose([signal_export.times, signal_export.data]))

# signal_export(h, 'generic_template.txt')
signal_export(h_tapered, 'generic_template.txt')
