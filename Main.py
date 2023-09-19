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


###Global variables

with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()

###Necessary Functions for buttons

#handles opening file explorer
def handle_upload(e: events.UploadEventArguments):
    
    
    print('\n\nCHECK THIS' + file)
    raw = mne.io.read_raw_edf(file)

    eegbci.standardize(raw)  # set channel names
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)

    raw.plot()
#


def generate_Bar_Graph(e: events.UploadEventArguments):
    try:
        raw = mne.io.read_raw_edf(file)
    except:
        print("ERROR IN generate_Bar_Graph")
        return
#


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
#


def raw_plot():
    raw = mne.io.read_raw_edf(file)
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    y = raw.plot()
    print(type(y))
#


def generate_montage_plot():
    raw = mne.io.read_raw_edf(file)
    eegbci.standardize(raw)
    montage = make_standard_montage("standard_1005")
    raw.set_montage(montage)
    mne.viz.plot_montage(montage)
    return
#
    

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



###File Selection

def choose_local_file() -> None:
    try:
        global file 
        file = easygui.fileopenbox()
        ui.input(label="Local File Path", value=f"{file}", placeholder='Local File Path', validation={'Input too long': lambda value: len(value) < 20})
        return
    except:
        print("ERROR WITH choose_local_file")
        return
#


###Header

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('Local Files')
        ui.tab('MNE Datasets')
        ui.tab('Preprocessing')
    #
#

with ui.tab_panels(tabs, value='Local Files').classes('w-full'):
    with ui.tab_panel('Local Files'):
        with ui.splitter() as splitter:
            with splitter.before:
                with ui.stepper().props('vertical').classes('w-full') as stepper:
                    with ui.step('Choose File'):
                        ui.button('Choose Local File', on_click=choose_local_file)
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
                                
                                highpass = ui.checkbox('Highpass Filter', value=True)
                                lowpass = ui.checkbox('Lowpass filter', value=True)
                            #
                            with ui.row():
                                with ui.column().bind_visibility_from(highpass, 'value'):
                                    ui.number(label='Highpass Filter', value=7, format='%.1f')
                                #
                                with ui.column().bind_visibility_from(lowpass, 'value'):
                                    ui.number(label='Highpass Filter', value=30, format='%.1f')
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
            with splitter.after:
                with ui.column():
                        ui.button('Raw Plot', on_click=raw_plot)
                        ui.button('Generate Montage Plot', on_click=generate_montage_plot)
                        ui.button('Generate Bar Graph', on_click=handle_upload)
                        ui.button('Generate Topographic Map', on_click=generate_Topo_Map)
                        ui.button('Generate Heat Map', on_click=handle_upload)
                        ui.button('Generate ICA', on_click=generate_ICA)
                        ui.button('Generate Covariance chart', on_click=handle_upload)
                    #
                #
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
            ui.select(['Library 1', 'BCIEEG Data', 3], value=1)
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

dark = ui.dark_mode()
ui.label('Switch mode:')
ui.button('Dark', on_click=dark.enable)
ui.button('Light', on_click=dark.disable)

ui.run()