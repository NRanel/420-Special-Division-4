import mne
import numpy as np
import matplotlib.pyplot as plt
from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci


#print(__doc__)

# #############################################################################
# # Set parameters and read data

# avoid classification of evoked responses by using epochs that start 1s after
# cue onset.
tmin, tmax = -1.0, 4.0
event_id = dict(hands=2, feet=3)
subject = 1
runs = [6, 10, 14]  # motor imagery: hands vs feet

raw_fnames = eegbci.load_data(subject, runs)
raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
eegbci.standardize(raw)  # set channel names
montage = make_standard_montage("standard_1005")
raw.set_montage(montage)

# Apply band-pass filter
raw.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")

events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))

picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")

# Get the infromation of raw
raw.info
raw.info.keys()

# Get the channel names
raw.info['ch_names']

# Plot raw data with default parameters
raw.plot()

# Compute the power spectral density of raw data and plot
spectrum = raw.compute_psd()
spectrum.plot(average=True, picks="data", exclude="bads")

# Plot a power spectral density of raw data for a specific channel(s)
midline = ['Fp1']
spectrum.plot(picks=midline, exclude="bads")

# Plot sensor (electrode) locations on a head
raw.plot_sensors(ch_type="eeg")

montage.plot()

# Plot topomap (heatmap) of power spectral density of raw data 
raw.compute_psd().plot_topomap()

# Apply ICA to Raw data
ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
ica.fit(raw)
ica.exclude = [15]  # ICA components
ica.plot_properties(raw, picks=ica.exclude)

# Find the covariance of channels of raw data and plot
noise_cov = mne.compute_raw_covariance(raw, method="shrunk")
fig_noise_cov = mne.viz.plot_cov(noise_cov, raw.info, show_svd=False)

#Plot ICA components
mne.viz.plot_ica_sources(ica, raw)
ica.plot_components()
ica.plot_overlay(raw)