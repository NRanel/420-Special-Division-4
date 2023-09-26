from nicegui import ui
from nicegui import events
import mne
import numpy as nppip
import matplotlib.pyplot as plt
from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
import easygui


###File SelectionS

def choose_local_file() -> None:
    container = ui.row()
    with container:
        container.clear()
        try:
            global file 
            file = easygui.fileopenbox()
            ui.input(label="Local File Path", value=f"{file}", placeholder='Local File Path', validation={'Input too long': lambda value: len(value) < 20})
            ui.button('Clear', on_click=container.clear)
            return container
        except:
            print("ERROR WITH choose_local_file")
            return
    #
#   
    

##Bar Graph Generator Function
def generate_Bar_Graph(e: events.UploadEventArguments):
    try:
        raw = mne.io.read_raw_edf(file)
    except:
        print("ERROR IN generate_Bar_Graph")
        return
    
##Topo Map Generator Fucnction
def generate_Topo_Map():
    print("File name" + file)
    try:
        raw = mne.io.read_raw_edf(file)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw.compute_psd().plot_topomap()
    except:
        print("ERROR IN generate_Topo_Map")
        return
    raw.plot_topomap()

##Raw Plot Generator Function
def raw_plot():
    raw = mne.io.read_raw_edf(file)
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    y = raw.plot()
    print(type(y))


##Montage Plot Generator Function
def generate_montage_plot():
    raw = mne.io.read_raw_edf(file)
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    mne.viz.plot_montage(montage)
    return


##Ica Generator Function
def generate_ICA():
    try:
        raw = mne.io.read_raw_edf(file)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)

        ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
        ica.fit(raw)
        ica.exclude = [15]  # ICA components
        ica.plot_properties(raw, picks=ica.exclude)

        mne.viz.plot_ica_sources(ica, raw)
        ica.plot_components()
        ica.plot_overlay(raw)
    except:
        return