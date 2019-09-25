from psychopy import core, visual, gui, data, event, logging, parallel
import numpy, random
import block
from config import *
from psychopy.iohub import launchHubServer
from psychopy.data import ExperimentHandler
import utils
import experiment_handler


# Get user input for experiment parameters
myDlg = gui.Dlg(title="Experiment")
myDlg.addText('Subject info')
myDlg.addField('subject_id:', 000)
myDlg.addText('Experiment Info')
myDlg.addField('number of trials for the no report practice block:', 10)
myDlg.addField('number of trials for the no report  block:', 25)
myDlg.addField('number of trials for each of the practice block', 10)
myDlg.addField('number of blocks for each experiment type:', 5)
myDlg.addField('number of trials for each experiment block:', 10)
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    print(ok_data)
else:
    print('user cancelled')

#====== Global setting of the experiment
# Create window to show stimuli
win = visual.Window([1920,1080],allowGUI=True,
                    monitor='testMonitor', units='deg', fullscr=True)
# Create mouse
mouse = event.Mouse(win=win)
mouse.setVisible(visible=0)

# Testing block before the actual experiment:
testing_block = block.Block(experiment_type='test', block_id=0, n_trials=1, report=False, is_practice=False, is_testing=True)
testing_block.run(win, mouse, event, block_which=1, total_blocks=1)

win.close()

# add global event key to terminate the program
event.globalKeys.add(key='q', modifiers=['ctrl'], func=core.quit)

# Create experiment handler (data input) to record user inputs
exp = ExperimentHandler()

# Grab information from user input:
subject_id = ok_data[0]
n_practice_trials_no_report = ok_data[1]
n_trials_no_report_start = ok_data[2]
n_trials_no_report_end = n_trials_no_report_start
n_practice_trials_each_type = ok_data[3]
n_blocks_each_type = ok_data[4]
n_trials_per_block = ok_data[5]

#====== Eye tracking setup
edf_filename = './'+str(subject_id)

iohub_config = {'eyetracker.hw.sr_research.eyelink.EyeTracker':
           {'name': 'tracker',
            'model_name': 'EYELINK 1000 DESKTOP',
            'runtime_settings': {'sampling_rate': 500,
                                 'track_eyes': 'RIGHT'},
            'default_native_data_file_name': str(subject_id)
           }
           }

io = launchHubServer(**iohub_config)

# Get the eye tracker device.
tracker = io.devices.tracker

# run eyetracker calibration
r = tracker.runSetupProcedure()
win = visual.Window([1920,1080],allowGUI=True,
                    monitor='testMonitor', units='deg', fullscr=True)
mouse = event.Mouse(win=win)
mouse.setVisible(visible=0)

# ====== EEG Event Markers Set-up

# Initialize EEG trigger
utils.sendEEGtrigger()




# ===== Experiment
# Start experiment
experiment_handler.run(win, mouse, event, exp=exp, tracker=tracker,
                      n_trials_no_report_start=n_trials_no_report_start, 
                      n_trials_no_report_end=n_trials_no_report_end, 
                      n_practice_trials_no_report=n_practice_trials_no_report, 
                      n_practice_trials_each_type=n_practice_trials_each_type,
                      n_blocks_each_type=n_blocks_each_type,
                      n_trials_per_block=n_trials_per_block)

# Save the output files
exp.saveAsWideText(fileName=str(subject_id) + '.csv', delim=',')


#====== Exit Program
utils.draw_instructions(win, END_EXPERIMENT_TEXT_1, END_EXPERIMENT_TEXT_2)
# pause until there's a keypress
event.waitKeys()

# Window close and program termination

core.quit()
