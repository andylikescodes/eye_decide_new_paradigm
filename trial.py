import clock as c
from psychopy import core, visual, gui, data, event
import numpy as np
import math, random
from config import *

# Trial class
class Trial:
	def __init__(self, experiment_type, clock_radius=4):
		self.type = experiment_type
		self.clock = c.Clock(radius=clock_radius)

	def draw_text(self, win, text, pos=[0,0], draw_now=True):
		text = visual.TextStim(win, pos=pos, text=text)
		text.draw()
		if draw_now == True:
			win.flip()

	def draw_fixation(self, win, draw_now=True):
		fixation = visual.GratingStim(win, color='white', colorSpace='rgb',
                      tex=None, mask='circle', size=0.2)
		fixation.draw()
		if draw_now == True:
			win.flip()


	def report(self, win, instr_txt, mouse=None, exp=None, block_type=None, block_id=None, trial_number=None, is_practice=False, is_report=True):
		self.draw_text(win, instr_txt)
		event.waitKeys(keyList=['space'])

		circle = self.clock.draw_circle(win)
		fixation = self.clock.draw_fixation(win)
		ticks = self.clock.draw_ticks(win)
		circle_ball = visual.Circle(win, radius=0.2, fillColor='white', 
				edges=self.clock.edges, lineWidth=3, units='deg')

		while True:
			mouse.setVisible(visible=1)
			circle.draw()
			fixation.draw()
			for tick in ticks:
				tick.draw()

			dot_x, dot_y = mouse.getPos()
			r = np.sqrt(dot_x**2 + dot_y**2)
			theta = math.acos(dot_x/r)

			if dot_y < 0:
				theta = -theta

			dot_x = self.clock.radius * math.cos(theta)
			dot_y = self.clock.radius * math.sin(theta)

			circle_ball.pos = [dot_x, dot_y]
			circle_ball.draw()
			win.flip()

			buttons = mouse.getPressed()
			if buttons[0] == 1:
				circle.draw()
				fixation.draw()
				for tick in ticks:
					tick.draw()

				circle_ball.pos = [dot_x, dot_y]
				circle_ball.draw()
				win.flip()
				keys = event.waitKeys(keyList=['space', 'escape'])
				if keys[0] == 'escape':
					continue

				if keys[0] == 'space':
					break

		# Record report x, y position in a file
		exp.addData('block_type', block_type)
		exp.addData('block_id', block_id)
		exp.addData('is_practice', is_practice)
		exp.addData('is_report', is_report)
		exp.addData('trial_number', trial_number)
		exp.addData('x', dot_x)
		exp.addData('y', dot_y)
		exp.nextEntry()
		core.wait(0.3)
		self.draw_text(win, 'Input Recorded')
		core.wait(1)

	def no_report(self, exp=None, block_type='no_report', block_id=None, trial_number=None, is_practice=False, is_report=False):
		exp.addData('block_type', block_type)
		exp.addData('block_id', block_id)
		exp.addData('is_practice', is_practice)
		exp.addData('is_report', is_report)
		exp.addData('trial_number', trial_number)
		exp.addData('x', 0)
		exp.addData('y', 0)
		exp.nextEntry()
		core.wait(0.3)

	def draw_trial_instr(self, win, trial_number, task_instr):
		trial_number_text = 'Trial #' + str(trial_number)
		# Trial discription
		self.draw_text(win, trial_number_text, pos=[0, +3], draw_now=False)
		self.draw_text(win, task_instr, pos=[0, -3], draw_now=False)
		self.draw_fixation(win, draw_now=False)

	def run(self, win, mouse, event, tracker=None, report=True, exp=None, block_type=None, block_id=None, trial_number=None, is_practice=False, beep_dist=None):
		# MSG eye-tracker: Trial starts
		tracker.sendMessage('TRIAL {} STARTS'.format(str(trial_number)))
		event_time = 0
		if self.type =='w':
			if report == False:
				self.draw_trial_instr(win, trial_number, NO_REPORT_PER_TRIAL_INSTR)
			else:
				self.draw_trial_instr(win, trial_number, W_TIME_PER_TRIAL_INSTR)
			win.flip()
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			event_time = self.clock.draw_moving_clock(win, event, exp=exp, tracker=tracker)
			# Report 
			if report == True:
				report_text = W_TIME_PER_REPORT_INSTR
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		if self.type =='m':
		# Trial discription
			self.draw_trial_instr(win, trial_number, M_TIME_PER_TRIAL_INSTR)
			win.flip()
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			event_time = self.clock.draw_moving_clock(win, event, exp=exp, tracker=tracker)

			# Report 
			if report == True:
				report_text = M_TIME_PER_REPORT_INSTR
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		if self.type == 'i':
			# Trial discription
			self.draw_trial_instr(win, trial_number, I_TIME_PER_TRIAL_INSTR)
			win.flip()
			# Draw a fixation point
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			event_time = self.clock.draw_moving_clock(win, event, exp=exp, tracker=tracker)

			# Report 
			if report == True:
				report_text = I_TIME_PER_REPORT_INSTR
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		if self.type == 's':
			# Trial discription
			self.draw_trial_instr(win, trial_number, S_TIME_PER_TRIAL_INSTR)
			win.flip()
			# Draw a fixation point
			event.waitKeys(keyList=['space'])
			event_time = self.clock.draw_moving_clock(win, event, play_random_sound=True, exp=exp, beep_dist=beep_dist, tracker=tracker)

			# Report 
			if report == True:
				report_text = S_TIME_PER_REPORT_INSTR
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		## MSG eye-tracker: trial ends
		tracker.sendMessage('TRIAL {} ENDS'.format(str(trial_number)))
		return event_time