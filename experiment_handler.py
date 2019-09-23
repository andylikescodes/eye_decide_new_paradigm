from psychopy import core, visual, gui, data, event, logging
import numpy, random
import block
from config import *
from psychopy.iohub import launchHubServer
from psychopy.data import ExperimentHandler
import utils

def run(win, mouse, event, exp, tracker, n_trials_no_report_start, n_trials_no_report_end, n_practice_trials_no_report, n_practice_trials_each_type, n_blocks_each_type, n_trials_per_block):
	
	#Create no report blcok
	no_report_start_practice = block.Block(experiment_type='w', block_id=0, n_trials=n_practice_trials_no_report, report=False, is_practice=True)
	no_report_start = block.Block(experiment_type='w', block_id=1, n_trials=n_trials_no_report_start, report=False, is_practice=False)
	no_report_end = block.Block(experiment_type='w', block_id=2, n_trials=n_trials_no_report_end, report=False, is_practice=False)

	#Create practice blocks
	types = ['w', 'm', 's', 'i']
	n_practice_blocks = len(types)
	practice_block_list = []
	for i in range(n_practice_blocks):
		practice_block= block.Block(experiment_type=types[i], block_id=i, n_trials=n_practice_trials_each_type, report=True, is_practice=True)
		practice_block_list.append(practice_block)
	
	# Create experiment blocks
	experiment_block_list = []
	for i in range(n_blocks_each_type):
		for type_name in types:
			experiment_block_list.append(block.Block(experiment_type=type_name, block_id=i+1, n_trials=n_trials_per_block, report=True, is_practice=False))


	# randomly shuffle the experimant blocks
	random.shuffle(experiment_block_list)
	random.shuffle(practice_block_list)

	# block sequence
	# Experiment Starts
	# ===> Starting with no report blocks
	no_report_start_practice.run(win, mouse, event, block_which=1, total_blocks=1, exp=exp, tracker=tracker) # Start with a no report w block
	no_report_start.run(win, mouse, event, block_which=1, total_blocks=1, exp=exp, tracker=tracker) # Start with a no report w block

	s_beep_dist = no_report_start.event_time_dist # Get distribution of the w time from the no report to generate beep sound

	# ===> Practice blocks
	for i in range(n_practice_blocks):
		practice_block_list[i].run(win, mouse, event, block_which=i+1, total_blocks=n_practice_blocks, exp=exp, beep_dist=s_beep_dist, tracker=tracker) # Run practice blocks

	# ===> Experiment blocks\
	utils.draw_instructions(win, PRACTICE_OVER_1, PRACTICE_OVER_2)
	event.waitKeys()
	n_experiment_blocks = len(experiment_block_list)
	for i in range(n_experiment_blocks):
		experiment_block_list[i].run(win, mouse, event, block_which=i+1, total_blocks=n_experiment_blocks, exp=exp, beep_dist=s_beep_dist, tracker=tracker) # Run experiment blocks

	# ===> Ending with no report blocks
	utils.draw_instructions(win, END_NO_REPORT_1, END_NO_REPORT_2)
	event.waitKeys()
	no_report_end.run(win, mouse, event, block_which=1, total_blocks=1, exp=exp, tracker=tracker) # End with a no report w block
