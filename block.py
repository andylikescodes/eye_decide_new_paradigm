import trial
from config import *
from psychopy import core, visual, gui, data, event
import numpy as np

# Block class
class Block:
	def __init__(self, experiment_type, block_id, n_trials, report, is_practice):
		self.type = experiment_type
		self.n_trials = n_trials
		self.report = report
		self.block_id = block_id
		self.is_practice = is_practice
		self.event_time_dist = []

	def draw_text(self, win, text, pos=[0,0], draw_now=True):
		text = visual.TextStim(win, pos=pos, text=text, wrapWidth=30, alignHoriz='center')
		text.draw()
		if draw_now == True:
			win.flip()

	def run(self, win, mouse, event, tracker=None, exp=None, beep_dist=None):
		if self.report == False:
			block_txt = GENERAL_INSTR + NO_REPORT_INSTR
		if self.type == 'w':
			block_txt = GENERAL_INSTR + W_TIME_INSTR
		if self.type == 'm':
			block_txt = GENERAL_INSTR + M_TIME_INSTR
		if self.type == 's':
			block_txt = GENERAL_INSTR + S_TIME_INSTR
		if self.type == 'i':
			block_txt = GENERAL_INSTR + I_TIME_INSTR

		self.draw_text(win, block_txt)
		event.waitKeys(keyList=['space'])

		new_trial = trial.Trial(self.type)
		# MSG - block starts
		tracker.sendMessage('BLOCK {} STARTS'.format(str(self.block_id)))
		for i in range(self.n_trials):
			event_time = new_trial.run(win, mouse, event, report=self.report, exp=exp, block_type=self.type, 
							block_id=self.block_id, trial_number=i+1, is_practice=self.is_practice, beep_dist=beep_dist)
			self.event_time_dist.append(event_time)
		# MSG - block ends
		tracker.sendMessage('BLOCK {} ENDS'.format(str(self.block_id)))
