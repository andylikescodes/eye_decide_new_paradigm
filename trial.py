import clock as c
from psychopy import core, visual, gui, data, event

# 

class Trial:
	def __init__(self, experiment_type, clock_radius=8):
		self.type = experiment_type
		self.clock = c.Clock(radius=clock_radius)

	def report(self, win, mouse=None, exp=None, block_type=None, block_id=None, trial_number=None):
		while True:
			self.clock.draw_circle(win)
			self.clock.draw_ticks(win)


			mouse.setVisible(visible=1)
			print(mouse.getPos())

			# dot_x, dot_y = self.cal_pos(self.radius, clock_where)
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

		exp.addData('block_type', block_type)
		exp.addData('block_id', block_id)
		exp.addData('trial_number', trial_number)
		exp.addData('x', dot_x)
		exp.addData('y', dot_y)
		exp.nextEntry()
		core.wait(0.5)

	#def run(self, win, mouse, event, tracker, report=True, exp=None, block_type=None, block_id=None, trial_number=None):
	# Test without eyetracker
	def run(self, win, mouse, event, tracker=None, report=True, exp=None, block_type=None, block_id=None, trial_number=None):
		if self.type =='w':
		# Trial discription
			text = visual.TextStim(win, pos=[0,0], text="Text discription for w task")
			text.draw()
			win.flip()

			# Draw a fixation point
			fixation = visual.GratingStim(win, color=-1, colorSpace='rgb',
	                              tex=None, mask='circle', size=0.2)
			fixation.draw()
			win.flip()
			core.wait(1)

			clock = c.Clock(user_input=True, radius=8)
			# clock.draw_moving_clock(win, event, tracker) # Draw a moving clock

			# Test without eyetracker
			clock.draw_moving_clock(win, event)

			# Instruction to ask for user input
			text = visual.TextStim(win, pos=[0,0], text="Click on the clock when you feel the urge to move")
			text.draw()
			win.flip()
			# Report by taking user mouse input

			if report == True:
				self.report(win, mouse=mouse, exp=exp, block_type=block_type, block_id=block_id, trial_number=trial_number)

			
