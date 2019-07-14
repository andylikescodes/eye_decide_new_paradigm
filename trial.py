import clock as c
from psychopy import core, visual, gui, data, event
import numpy as np
import math, random

# Trial class
class Trial:
	def __init__(self, experiment_type, clock_radius=8):
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

	def report(self, win, instr_txt, mouse=None, exp=None, block_type=None, block_id=None, trial_number=None, is_practice=False):
		self.draw_text(win, instr_txt)
		core.wait(3)

		while True:
			self.clock.draw_circle(win)
			self.clock.draw_ticks(win)

			mouse.setVisible(visible=1)

			dot_x, dot_y = mouse.getPos()
			circle_ball = visual.Circle(win, radius=0.2, fillColor='white', pos=(dot_x/2, dot_y/2), 
				edges=self.clock.edges, lineWidth=3, units='deg')
			circle_ball.draw()
			win.flip()
			buttons = mouse.getPressed()

			if buttons[0] == 1:
				self.clock.draw_circle(win)
				self.clock.draw_ticks(win)
				xx = dot_x
				yy = dot_y
				r = np.sqrt(xx**2 + yy**2)
				theta = math.acos(xx/r)

				# Flip the radian while yy is negative. Sign loses during arccosin operation
				if yy < 0:
					theta = -theta
				
				dot_x = self.clock.radius * math.cos(theta)
				dot_y = self.clock.radius * math.sin(theta)
				circle = visual.Circle(win, radius=0.2, fillColor='white', pos=(dot_x, dot_y), 
				edges=self.clock.edges, lineWidth=3)
				circle.draw()
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
		exp.addData('trial_number', trial_number)
		exp.addData('x', dot_x)
		exp.addData('y', dot_y)
		exp.nextEntry()
		core.wait(0.3)
		self.draw_text(win, 'Input Recorded')
		core.wait(1)

	def run(self, win, mouse, event, tracker=None, report=True, exp=None, block_type=None, block_id=None, trial_number=None, is_practice=False):
		if self.type =='w':
			w_text = "Trial#{}, Text discription for w task, click space bar to start".format(str(trial_number)) # TODO: Change this later for stuff
			# Trial discription
			self.draw_text(win, w_text)
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			self.clock.draw_moving_clock(win, event)
			# Report 
			if report == True:
				report_text = "Click on the clock when you feel the urge to move, press esc to reset" # TODO: Change the txt
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)

		if self.type =='m':
		# Trial discription
			m_text = "Trial#{}, Text discription for m task, click space bar to start".format(str(trial_number))
			self.draw_text(win, m_text)
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			self.clock.draw_moving_clock(win, event)

			# Report 
			if report == True:
				report_text = "Click on the clock when you feel the urge to move, press esc to reset" # TODO: Change the txt
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)


		if self.type == 'i':
			# Trial discription
			i_text = "Trial#{}, Text discription for i task, click space bar to start".format(str(trial_number))
			self.draw_text(win, i_text)
			# Draw a fixation point
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			self.clock.draw_moving_clock(win, event)

			# Report 
			if report == True:
				report_text = "Click on the clock when you feel the urge to move, press esc to reset"
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)

		if self.type == 's':
			# Trial discription
			s_text = "Trial#{}, Text discription for s task, click space bar to start".format(str(trial_number))
			self.draw_text(win, s_text)
			# Draw a fixation point
			event.waitKeys(keyList=['space'])
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock
			# Test without eyetracker
			self.clock.draw_moving_clock(win, event, play_random_sound=True)

			# Report 
			if report == True:
				report_text = "Click on the clock where you feel the sound was played, press esc to reset"
				self.report(win, instr_txt=report_text, mouse=mouse, exp=exp, 
							block_type=block_type, block_id=block_id, trial_number=trial_number, is_practice=is_practice)
