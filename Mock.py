from nicegui import ui
from nicegui import run
from nicegui import events
import mne
import numpy as np
import matplotlib.pyplot as plt
from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
import easygui
import plotly.graph_objects as go
from mne.datasets import eegbci
import re
import os
from multiprocessing import Process
import sklearn

###Global variables

with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()

###Necessary Functions for buttons

def choose_local_file() -> None:
    container = ui.row()
    with container:
        container.clear()
        try:
            global file 
            file = easygui.fileopenbox()
            localfile_input.value = f"{file}"
            #ui.button('Clear', on_click=container.clear)
            return container
        except:
            print("ERROR WITH choose_local_file")
            return
    #
#

##Bar Graph Generator Function
def generate_Bar_Graph():
    try:
        placement.clear()
        raw = mne.io.read_raw_edf(file)
        fig = go.Figure(go.Bar(x=raw.times, y=raw.get_data()[0]))
        fig.update_layout(
            title='EEG Bar Graph'
        )
        figure = ui.plotly(fig).classes('w-full h-90')
        figure.move(placement)
    except:
        print("ERROR IN generate_Bar_Graph")
        return
    
##Topo Map Generator Fucnction
def generate_Topo_Map():
    print("File name" + file)
    try:
        raw = mne.io.read_raw_edf(file, preload=True)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        raw.compute_psd().plot_topomap()
    except:
        print("ERROR IN generate_Topo_Map")
        return
    

##Raw Plot Generator Function
def raw_plot():
    raw = mne.io.read_raw_edf(file, preload=True)
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    raw = apply_filter(raw)
    raw.plot(block=True)


##Montage Plot Generator Function
def generate_montage_plot():
    raw = mne.io.read_raw_edf(file, preload=True)
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw = apply_filter(raw)
    #raw.plot_sensors(ch_type="eeg")
    montage.plot()
    


##Ica Generator Function
def generate_ICA():
    try:
        raw = mne.io.read_raw_edf(file, preload=True)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        #raw.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")
        events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")
        ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
        ica.fit(raw)
        ica.exclude = [15]  # ICA components
        ica.plot_properties(raw, picks=ica.exclude)

    except:
        print('Failed ICA')
        print("Ensure you have a file selected")
    
##ICA components function
def generate_ica_components():
    try:
        raw = mne.io.read_raw_edf(file, preload=True)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)

        events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")

        ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
        ica.fit(raw)
        ica.exclude = [15]  # ICA components
        

        mne.viz.plot_ica_sources(ica, raw)
        ica.plot_components()
    except:
        print("ICA components failed")
        print("Ensure you have a filed selected")
        
##ICA plot overlay
def generate_ica_plot_overlay():
    try:
        raw = mne.io.read_raw_edf(file, preload=True)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        #raw.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")
        events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")
        ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
        ica.fit(raw)
        ica.exclude = [15]  # ICA components

        #mne.viz.plot_ica_sources(ica, raw)
        ica.plot_overlay(raw)
    except:
        print('Failed ICA plot overlay')
        print("Ensure you have a file selected")
    
##EEG Covariance
def generate_covariance_shrunk():
    try:
        raw = mne.io.read_raw_edf(file, preload=True)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        noise_cov = mne.compute_raw_covariance(raw, method="shrunk")
        fig_noise_cov = mne.viz.plot_cov(noise_cov, raw.info, show_svd=False)
    except:
        print("EEG covariance failed")
        print("Ensure you have a filed selected")

##Covariarance Function
def generate_covariance_diagonal_fixed():
    raw = mne.io.read_raw_edf(file, preload=True)
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    raw = apply_filter(raw)
    noise_cov = mne.compute_raw_covariance(raw, method="diagonal_fixed")
    mne.viz.plot_cov(noise_cov, raw.info, show_svd=False)

#Plot Creation Function
def create_mne_plot(data):

    fig = go.Figure(go.Scatter(x=data.times, y=data.get_data()[0]))

    fig.update_layout(
        title='EEG data plot',
        xaxis=dict(title='time (s)'),
        yaxis=dict(title='Amplitude')
    )
    return fig

# Define the function to process the file
def process_file():
    global file
    if file:
        try:
            placement.clear()
            raw = mne.io.read_raw_edf(file, preload=True)  # Load the EEG data
            raw = apply_filter(raw)
            fig = create_mne_plot(raw)  # Create a Plotly figure
            figure = ui.plotly(fig).classes('w-full h-90')  # Display the figure
            figure.move(placement)
        except Exception as e:
            print(f"Error processing the file: {str(e)}")

def apply_filter(raw):
    if highpass.value == True & lowpass.value == True:
        raw.filter(lowpass_value.value, highpass_value.value, fir_design="firwin", skip_by_annotation="edge")
    elif highpass.value == True & lowpass.value == False:
        raw.filter(None, highpass_value.value, fir_design="firwin", skip_by_annotation="edge")
    elif highpass.value == False & lowpass.value == True:
        raw.filter(lowpass_value.value, None, fir_design="firwin", skip_by_annotation="edge")
    elif highpass.value == False & lowpass.value == False:
        raw.filter(None, highpass_value.value, fir_design="firwin", skip_by_annotation="edge")
    return raw

########### Functions For MNE Datasets

def EEGBCI_raw_plot():
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    eegbci.standardize(raw)  # set channel names
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    raw.plot(block=True)
#

def EEGBCI_generate_montage_plot():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw = apply_filter(raw)
    #raw.plot_sensors(ch_type="eeg")
    montage.plot()
#

def EEGBCI_generate_Topo_Map():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    try:
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        raw.compute_psd().plot_topomap()
    except:
        print("ERROR IN generate_Topo_Map")
        return
#

def EEGBCI_generate_ICA():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end

    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    raw = apply_filter(raw)
    #raw.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")
    events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")
    ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
    ica.fit(raw)
    ica.exclude = [15]  # ICA components
    ica.plot_properties(raw, picks=ica.exclude)

    print('Failed ICA')
    print("Ensure you have a file selected")
#
def EEGBCI_generate_ICA_components():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    try:
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        #raw.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")
        events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")
        ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
        ica.fit(raw)
        ica.exclude = [15]  # ICA components
        

        mne.viz.plot_ica_sources(ica, raw)
        ica.plot_components()

    except:
        print('Failed ICA')
        print("Ensure you have a file selected")

def EEGBCI_generate_ICA_plot_overlay():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    try:
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        #raw.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")
        events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")
        ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
        ica.fit(raw)
        ica.exclude = [15]  # ICA components

        #mne.viz.plot_ica_sources(ica, raw)
        ica.plot_overlay(raw)
    except:
        print('Failed ICA plot overlay')
        print("Ensure you have a file selected")

def EEGBCI_generate_covariance_shrunk():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    try:
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        noise_cov = mne.compute_raw_covariance(raw, method="shrunk")
        fig_noise_cov = mne.viz.plot_cov(noise_cov, raw.info, show_svd=False)
    except:
        print("EEG covariance failed")
        print("Ensure you have a filed selected")

def EEGBCI_generate_covariance_diagonal():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    try:
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        noise_cov = mne.compute_raw_covariance(raw, method="diagonal_fixed")
        fig_noise_cov = mne.viz.plot_cov(noise_cov, raw.info, show_svd=False)
    except:
        print("EEG covariance failed")
        print("Ensure you have a filed selected")

def EEGBCI_generate_covariance_shrunk():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    try:
        raw = mne.io.read_raw_edf(file, preload=True)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        noise_cov = mne.compute_raw_covariance(raw, method="shrunk")
        fig_noise_cov = mne.viz.plot_cov(noise_cov, raw.info, show_svd=False)
    except:
        print("EEG covariance failed")
        print("Ensure you have a filed selected")

def EEGBCI_generate_covariance_diagonal_fixed():
    #boilerplate start
    #ensure the correct folder exists for mne
    home_directory = os.path.expanduser( '~' )
    home_directory = home_directory + '\mne_data'
    print(home_directory)
    if not os.path.exists(home_directory):
        os.mkdir(home_directory)
    
    #Shows runs for testing
    print(subject_label.text, " Subject")
    print(runs_label.text, ' Runs')
    
    #regular expresions 
    subject = re.findall(r'\d+', subject_label.text)
    runs = re.findall(r'\d+', runs_label.text)
    subject = int(subject[0])
    runs = [int(i) for i in runs]
    print(subject, " Subject")
    print(runs, ' Runs')
    raw_fnames = eegbci.load_data(subject, runs)
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])
    #boilerplate end
    try:
        raw = mne.io.read_raw_edf(file, preload=True)
        eegbci.standardize(raw)
        montage = make_standard_montage("standard_1005")
        raw.set_montage(montage)
        raw = apply_filter(raw)
        noise_cov = mne.compute_raw_covariance(raw, method="diagonal_fixed")
        fig_noise_cov = mne.viz.plot_cov(noise_cov, raw.info, show_svd=False)
    except:
        print("EEG covariance failed")
        print("Ensure you have a filed selected")


def test():
    process = Process(target=EEGBCI_raw_plot)
    process.start()
    process.join()
#

    



#################################


#BEGINNING OF PAGE LAYOUT

#Start of Header-----------------------------------------------------------------------------------------------------------------------------
with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    dark = ui.dark_mode(False)
    with ui.tabs() as tabs:
        ui.image("brainwave_compnay_logo.png").classes("w-16")
        ui.tab('Local Files')
        ui.tab('MNE Datasets')
        #ui.tab('Preprocessing')
    ui.switch('Mode').bind_value(dark)

#End of Header-------------------------------------------------------------------------------------------------------------------------------

#If we want something on the right side of the screen, (A right drawer, similar to the left drawer) then uncomment the 2 lines below this
# with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
#     ui.label('RIGHT DRAWER')


#Here is the start of the Footer-------------------------------------------------------------------------------------------------------------
#with ui.footer().style('background-color: #3874c8'):
#    with ui.row().classes('w-full justify-center'):
#        ui.button('Dark', on_click=dark.enable)
#        ui.button('Light', on_click=dark.disable)    

#End of the Footer---------------------------------------------------------------------------------------------------------------------------

#EVERYTHING AFTER THIS LINE WILL GO INSIDE OF THE MAIN VIEW
container = ui.row()

with ui.tab_panels(tabs, value='Local Files').classes('w-full'):
    with ui.tab_panel('Local Files'):
        with ui.stepper().props('vertical').classes('w-full') as stepper:
            with ui.step('Choose File'):
                container
                ui.button('Choose Local File', on_click= choose_local_file)
                localfile_input = ui.input(label="Local File Path", placeholder='Local File Path').props('clearable')
                with ui.stepper_navigation():
                    ui.button('Next', on_click=stepper.next)
            #
            with ui.step('Choose Filters'):
                with ui.row():
                    band_filter = ui.checkbox('Band Filter', value=False)
                    other_filter = ui.checkbox('Other Filter', value = False)
                #
                ui.separator()
                with ui.column().bind_visibility_from(band_filter, 'value'):
                    
                    with ui.row():
                        highpass = ui.checkbox('Highpass filter', value=True)
                        lowpass = ui.checkbox('Lowpass Filter', value=True)
                        
                    #
                    with ui.row():
                        with ui.column().bind_visibility_from(highpass, 'value'):
                            lowpass_value = ui.number(label='Highpass Filter', value=7, format='%.1f')
                        #
                        with ui.column().bind_visibility_from(lowpass, 'value'):
                            highpass_value = ui.number(label='Lowpass Filter', value=30, format='%.1f')
                        #
                    #
                #
                ui.separator()
                with ui.column().bind_visibility_from(other_filter, 'value'):
                    
                    ui.label('options here')
                #
                with ui.stepper_navigation():
                    ui.button('Next', on_click=stepper.next)
                    ui.button('Back', on_click=stepper.previous).props('flat')
            #
        #
        #place plot here
        with ui.row().classes('w-full justify-center m-3'):
                ui.button('Process File', on_click=process_file)
                ui.button('Raw Plot', on_click= raw_plot)
                ui.button('Generate Montage Plot', on_click= generate_montage_plot)
                #ui.button('Generate Bar Graph', on_click=generate_Bar_Graph)
                ui.button('Generate Topographic Map', on_click= generate_Topo_Map)
                #This literally did nothing, so im commenting it out
                #ui.button('Generate Heat Map')
                ui.button('Generate ICA', on_click= generate_ICA)
                ui.button('Generate ICA Components', on_click= generate_ica_components)
                ui.button('Generate ICA plot overlay', on_click= generate_ica_plot_overlay)
                ui.button('Generate Covariance Chart Shrunk', on_click= generate_covariance_shrunk)
                ui.button('Generate Covariance Chart Diagonal-Fixed', on_click= generate_covariance_diagonal_fixed)
            #
        #
        with ui.row():
            placement = ui.row().classes('w-full justify-center')  
               
    #
        #

    #
#
    #
    with ui.tab_panel('Preprocessing'):
        ui.label('Preprocessing Options to com')
    #
    with ui.tab_panel('MNE Datasets'):
        with ui.row():
            ui.label('Sample Data from the MNE Library')

            
        with ui.row().classes('w-full justify-center m-3'):
            dataset = ui.toggle(['EEGBCI', 'Eyelink'], value=1)
        with ui.row().classes('w-full justify-center m-3'):
            ui.label(' ')
        with ui.row().classes('w-full justify-center m-3').bind_visibility_from(dataset, 'value'):
            ui.input('Subjects', placeholder='4',
                     on_change=lambda e:subject_label.set_text('Subjects selected: ' + e.value)
                     )
            subject_label = ui.label()
        with ui.row().classes('w-full justify-center m-3').bind_visibility_from(dataset, 'value'):
            ui.input('Runs', placeholder='1,2,3,4',
                     on_change=lambda e:runs_label.set_text('Runs selected: ' + e.value))
            runs_label = ui.label()
        with ui.row().classes('w-full justify-center m-3').bind_visibility_from(dataset, 'value'):
            ui.button('Raw Plot', on_click=EEGBCI_raw_plot)
            ui.button('Generate Montage Plot', on_click= EEGBCI_generate_montage_plot)
            #ui.button('Generate Bar Graph', on_click=EEGBCI_generate_Bar_Graph)
            ui.button('Generate Topographic Map', on_click= EEGBCI_generate_Topo_Map)
            #ui.button('Generate Heat Map')
            ui.button('Generate ICA', on_click= EEGBCI_generate_ICA)
            ui.button('Generate ICA Components', on_click= EEGBCI_generate_ICA_components)
            ui.button('Generate ICA Plot Overlay', on_click= EEGBCI_generate_ICA_plot_overlay)
            ui.button('Generate Covariance Chart Shrunk', on_click=EEGBCI_generate_covariance_shrunk)
            ui.button('Generate Covariance Chart Diagonal-Fixed', on_click=EEGBCI_generate_covariance_diagonal_fixed)
        #
    #
#







###Footer that is displayed when clicking sticky button
with ui.footer(value=False) as footer:
    ui.label('This is a Visual Interface for working with the Python MNE library')
#


with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')
#
ui.run()

