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
import EegFunc
###Global variables

with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()

###Necessary Functions for buttons
EegFunc.generate_Bar_Graph

EegFunc.generate_Topo_Map

EegFunc.raw_plot

EegFunc.generate_montage_plot

EegFunc.generate_ICA




#BEGINNING OF PAGE LAYOUT

#Start of Header-----------------------------------------------------------------------------------------------------------------------------
with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    dark = ui.dark_mode()
    with ui.tabs() as tabs:
        ui.tab('Local Files')
        ui.tab('MNE Datasets')
        ui.tab('Preprocessing')

#End of Header-------------------------------------------------------------------------------------------------------------------------------

#If we want something on the right side of the screen, (A right drawer, similar to the left drawer) then uncomment the 2 lines below this
# with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
#     ui.label('RIGHT DRAWER')


#Here is the start of the Footer-------------------------------------------------------------------------------------------------------------
with ui.footer().style('background-color: #3874c8'):
    with ui.row():
        ui.button('Dark', on_click=dark.enable)
        ui.button('Light', on_click=dark.disable)    

#End of the Footer---------------------------------------------------------------------------------------------------------------------------

#EVERYTHING AFTER THIS LINE WILL GO INSIDE OF THE MAIN VIEW



with ui.tab_panels(tabs, value='Local Files').classes('w-full'):
    with ui.tab_panel('Local Files'):
        
                with ui.stepper().props('vertical').classes('w-full') as stepper:
                    with ui.step('Choose File'):
                        ui.button('Choose Local File', on_click=EegFunc.choose_local_file)
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
           
                with ui.column():
                        ui.button('Raw Plot', on_click=EegFunc.raw_plot)
                        ui.button('Generate Montage Plot', on_click=EegFunc.generate_montage_plot)
                        ui.button('Generate Bar Graph')
                        ui.button('Generate Topographic Map', on_click=EegFunc.generate_Topo_Map)
                        ui.button('Generate Heat Map')
                        ui.button('Generate ICA', on_click=EegFunc.generate_ICA)
                        ui.button('Generate Covariance chart')
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


ui.run()