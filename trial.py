import clock as c
from psychopy import core, visual, gui, data, event
import numpy as np
import math, random

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
		return fixation

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
			
			circle_ball.pos = [dot_x, dot_y]
			circle_ball.draw()
			win.flip()
			buttons = mouse.getPressed()

			if buttons[0] == 1:
				circle.draw()
				fixation.draw()
				for tick in ticks:
					tick.draw()

				xx = dot_x
				yy = dot_y
				r = np.sqrt(xx**2 + yy**2)
				theta = math.acos(xx/r)

				# Flip the radian while yy is negative. Sign loses during arccosin operation
				if yy < 0:
					theta = -theta
				
				dot_x = self.clock.radius * math.cos(theta)
				dot_y = self.clock.radius * math.sin(theta)
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

	def run(self, win, mouse, event, tracker=None, report=True, exp=None, block_type=None, block_id=None, trial_number=None, is_practice=False, beep_dist=None):
		# MSG eye-tracker: Trial starts
		tracker.sendMessage('TRIAL {} STARTS'.format(str(trial_number)))
		event_time = 0
		if self.type =='w':
			w_text = "Trial#{}, Text discription for w task, click space bar to start".format(str(trial_number)) # TODO: Change this later for stuff
			# Trial discription
			self.draw_text(win, w_text)
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			event_time = self.clock.draw_moving_clock(win, event, exp=exp, tracker=tracker)
			# Report 
			if report == True:
				report_text = "Click on the clock when you feel the urge to move, press esc to reset" # TODO: Change the txt
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		if self.type =='m':
		# Trial discription
			m_text = "Trial#{}, Text discription for m task, click space bar to start".format(str(trial_number))
			self.draw_text(win, m_text)
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			event_time = self.clock.draw_moving_clock(win, event, exp=exp, tracker=tracker)

			# Report 
			if report == True:
				report_text = "Click on the clock when you feel the urge to move, press esc to reset" # TODO: Change the txt
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		if self.type == 'i':
			# Trial discription
			i_text = "Trial#{}, Text discription for i task, click space bar to start".format(str(trial_number))
			self.draw_text(win, i_text)
			# Draw a fixation point
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			event_time = self.clock.draw_moving_clock(win, event, exp=exp, tracker=tracker)

			# Report 
			if report == True:
				report_text = "Click on the clock when you feel the urge to move, press esc to reset"
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		if self.type == 's':
			# Trial discription
			s_text = "Trial#{}, Text discription for s task, click space bar to start".format(str(trial_number))
			self.draw_text(win, s_text)
			# Draw a fixation point
			event.waitKeys(keyList=['space'])
			event_time = self.clock.draw_moving_clock(win, event, play_random_sound=True, exp=exp, beep_dist=beep_dist, tracker=tracker)

			# Report 
			if report == True:
				report_text = "Click on the clock where you feel the sound was played, press esc to reset"
				# MSG - report starts
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
				# MSG - report ends
			elif report == False:
				self.no_report(exp=exp, block_type='no_report', block_id=block_id, trial_number=trial_number, is_practice=is_practice, is_report=report)

		## MSG eye-tracker: trial ends
		tracker.sendMessage('TRIAL {} ENDS'.format(str(trial_number)))
		return event_time