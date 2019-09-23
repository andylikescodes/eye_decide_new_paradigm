import trial
from config import *
from psychopy import core, visual, gui, data, event
import numpy as np
import utils

# Block class
class Block:
	def __init__(self, experiment_type, block_id, n_trials, report, is_practice, is_testing=False):
		self.type = experiment_type
		self.n_trials = n_trials
		self.report = report
		self.block_id = block_id
		self.is_practice = is_practice
		self.is_testing = is_testing
		self.event_time_dist = []

	def draw_text(self, win, text, pos=[0,0], draw_now=True):
		text = visual.TextStim(win, pos=pos, text=text, wrapWidth=30, alignHoriz='center')
		text.draw()
		if draw_now == True:
			win.flip()

	def run(self, win, mouse, event, tracker=None, exp=None, beep_dist=None, block_which=None, total_blocks=None):
		if self.is_testing == True:
			block_txt_1 = 'This is a testing block before the experiment to make sure everything runs fine.'
			block_txt_2 = 'you don\'t have to do anything. Wait until the next block.'
			new_trial = trial.Trial(self.type)
			utils.draw_instructions(win, block_txt_1, block_txt_2)
			event.waitKeys(keyList=['space'])
			new_trial.run(win, mouse, event, total_block_trials=self.n_trials)

		else:
			if self.is_practice == True:
				temp = 'PRACTICE. '
			else:
				temp = ''
			if self.type == 'w':
				block_txt = '{}W-Time. Press spacebar to continue.'.format(temp)
			if self.type == 'm':
				block_txt = '{}M-Time. Press spacebar to continue.'.format(temp)
			if self.type == 's':
				block_txt = '{}S-Time. Press spacebar to continue.'.format(temp)
			if self.type == 'i':
				block_txt = '{}I-Time. Press spacebar to continue.'.format(temp)
			if self.report == False:
				block_txt = '{}No-Report. Press spacebar to continue.'.format(temp)

			progress_tracker = 'Block {}, {}'.format(str(block_which) + '/' + str(total_blocks), str(self.n_trials) + ' trials')

			utils.draw_instructions(win, block_txt, progress_tracker)
			event.waitKeys(keyList=['space'])

			new_trial = trial.Trial(self.type)
			# MSG - block starts
			tracker.sendMessage('BLOCK {} STARTS'.format(str(self.block_id)))
            
            # EEG triggers to parallel port
            port.sendData(1)
            port.sendData(0)
            
			for i in range(self.n_trials):
				event_time = new_trial.run(win, mouse, event, total_block_trials=self.n_trials, report=self.report, exp=exp, block_type=self.type, 
								block_id=self.block_id, trial_number=i+1, is_practice=self.is_practice, beep_dist=beep_dist, tracker=tracker)
				self.event_time_dist.append(event_time)
			# MSG - block ends
			tracker.sendMessage('BLOCK {} ENDS'.format(str(self.block_id)))
            
            # EEG triggers to parallel port
            port.sendData(2)
            port.sendData(0)
