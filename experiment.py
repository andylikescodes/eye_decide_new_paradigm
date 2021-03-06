from psychopy import core, visual, gui, data, event, logging
import numpy, random
import block
from config import *
from psychopy.iohub import launchHubServer
from psychopy.data import ExperimentHandler

# Get user input for saving the data

myDlg = gui.Dlg(title="Experiment")
myDlg.addText('Subject info')
myDlg.addField('subject_id:', 000)
myDlg.addText('Experiment Info')
myDlg.addField('number of trials for the no report  block:', 30)
myDlg.addField('number of trials for each of the practic block', 10)
myDlg.addField('number of blocks for each experiment type:', 4)
myDlg.addField('number of trials for each block:', 10)
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    print(ok_data)
else:
    print('user cancelled')

# Grab information from user input:
subject_id = ok_data[0]
n_no_report = ok_data[1]
n_practice_each_block = ok_data[2]
n_blocks_each_type = ok_data[3]
n_trials_per_block = ok_data[4]

# Create experiment handler (data input) to record user inputs
exp = ExperimentHandler()

# Create window to show stimuli
win = visual.Window([1920,1080],allowGUI=True,
                    monitor='testMonitor', units='deg', fullscr=True)

# win = visual.Window([800,600],allowGUI=True,
#                     monitor='testMonitor', units='deg')
# Create mouse
mouse = event.Mouse(win=win)
mouse.setVisible(visible=0)

# display instructions to start the experiment
fixation = visual.GratingStim(win, color='white', colorSpace='rgb',
                              tex=None, mask='circle', size=0.2)
message1 = visual.TextStim(win, pos=[0,+3], text=GENERAL_INSTR)
message2 = visual.TextStim(win, pos=[0,-3], text="The experiment is about to start! Hit a key when ready.")
message1.draw()
message2.draw()
fixation.draw()
win.flip()
#pause until there's a keypress
event.waitKeys()

#Create no report blcok
w_block_no_report_start = block.Block(experiment_type='w', block_id=1, n_trials=n_no_report, report=False, is_practice=False)

#Create practice blocks
practice_block_w = block.Block(experiment_type='w', block_id=1, n_trials=n_practice_each_block, report=True, is_practice=True)
practice_block_m = block.Block(experiment_type='m', block_id=2, n_trials=n_practice_each_block, report=True, is_practice=True)
practice_block_i = block.Block(experiment_type='s', block_id=3, n_trials=n_practice_each_block, report=True, is_practice=True)
practice_block_s = block.Block(experiment_type='i', block_id=4, n_trials=n_practice_each_block, report=True, is_practice=True)

#Create no report blcok at the end
w_block_no_report_end = block.Block(experiment_type='w', block_id=2, n_trials=n_no_report, report=False, is_practice=False)

# Create experiment blocks
experiment_block_list = []
for i in range(n_blocks_each_type):
    experiment_block_list.append(block.Block(experiment_type='w', block_id=i+1, n_trials=n_trials_per_block, report=True, is_practice=False))
    experiment_block_list.append(block.Block(experiment_type='m', block_id=i+1, n_trials=n_trials_per_block, report=True, is_practice=False))
    experiment_block_list.append(block.Block(experiment_type='i', block_id=i+1, n_trials=n_trials_per_block, report=True, is_practice=False))
    experiment_block_list.append(block.Block(experiment_type='s', block_id=i+1, n_trials=n_trials_per_block, report=True, is_practice=False))

# randomly shuffle the experimant blocks
random.shuffle(experiment_block_list)

practice_block_list = [practice_block_w, practice_block_m, practice_block_s, practice_block_i]
random.shuffle(practice_block_list)

# block sequence
w_block_no_report_start.run(win, mouse, event, exp=exp) # Start with a no report w block

s_beep_dist = w_block_no_report_start.event_time_dist

for block in practice_block_list:
    block.run(win, mouse, event, exp=exp, beep_dist=s_beep_dist) # Run practice blocks

for block in experiment_block_list:
    block.run(win, mouse, event, exp=exp, beep_dist=s_beep_dist) # Run experiment blocks

w_block_no_report_end.run(win, mouse, event, exp=exp) # End with a no report w block

# Save the output files
exp.saveAsWideText(fileName=str(subject_id) + '.csv', delim=',')

# Display experiment end txt
message1 = visual.TextStim(win, pos=[0,+3], text='Thank you for your participation.')
message2 = visual.TextStim(win, pos=[0,-3], text="The experiment is ended, press any key to exit the experiment!")
message1.draw()
message2.draw()
win.flip()
#pause until there's a keypress
event.waitKeys()

# Window close and program termination
win.close()
core.quit()
