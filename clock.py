from psychopy import core, visual, gui, data, event
import random, math
import numpy as np

# A clock class to handle the clock animation.

class Clock:
	def __init__(self, radius, tick_length=0.5, user_input=True, edges=128):
		self.radius = radius
		self.edges = edges
		self.user_input = user_input
		self.tick_length = tick_length

	def cal_pos(self, radius, radians):
		dot_x = radius * math.cos(radians)
		dot_y = radius * math.sin(radians)

		return dot_x, dot_y

	def draw_circle(self, win):
		circle = visual.Circle(win, radius=self.radius, edges=self.edges, lineWidth=3)
		circle.draw()

	def draw_ticks(self, win):
		for i in range(0,12):
			x_start = self.radius * math.cos((math.pi/2)-i*math.pi/6)
			y_start = self.radius * math.sin((math.pi/2)-i*math.pi/6)

			x_end = (self.radius - self.tick_length) * math.cos((math.pi/2)-i*math.pi/6)
			y_end = (self.radius - self.tick_length) * math.sin((math.pi/2)-i*math.pi/6)

			line = visual.Line(win, start=(x_start, y_start), end=(x_end, y_end))
			line.draw()

	def draw_plain_clock(self, win, draw_now=True):
		# display instructions and wait
		self.draw_circle(win)

		# TODO1: Draw ticks - calculated by Jake
		self.draw_ticks(win)
		
		if draw_now == True:
			win.flip()

		# if report == True:
		# 	while True:

		# 		self.draw_circle(win)
		# 		self.draw_ticks(win, tick_length)


		# 		mouse.setVisible(visible=1)
		# 		print(mouse.getPos())

		# 		# dot_x, dot_y = self.cal_pos(self.radius, clock_where)
		# 		dot_x, dot_y = mouse.getPos()
		# 		circle_ball = visual.Circle(win, radius=0.2, fillColor='white', pos=(dot_x/2, dot_y/2), 
		# 			edges=self.edges, lineWidth=3, units='deg')
		# 		circle_ball.draw()
		# 		win.flip()
		# 		buttons = mouse.getPressed()
		# 		if buttons[0] == 1:
		# 			self.draw_circle(win)
		# 			self.draw_ticks(win, tick_length)
		# 			xx = dot_x
		# 			yy = dot_y
		# 			r = np.sqrt(xx**2 + yy**2)
		# 			theta = math.acos(xx/r)

		# 			if yy < 0:
		# 				theta = -theta
					
		# 			dot_x = self.radius * math.cos(theta)
		# 			dot_y = self.radius * math.sin(theta)
		# 			circle = visual.Circle(win, radius=0.2, fillColor='white', pos=(dot_x, dot_y), 
		# 			edges=self.edges, lineWidth=3)
		# 			circle.draw()
		# 			win.flip()
		# 			keys = event.waitKeys(keyList=['space', 'escape'])
		# 			if keys[0] == 'escape':
		# 				continue

		# 			if keys[0] == 'space':
		# 				break

		# 	exp.addData('block_type', block_type)
		# 	exp.addData('block_id', block_id)
		# 	exp.addData('trial_number', trial_number)
		# 	exp.addData('x', dot_x)
		# 	exp.addData('y', dot_y)
		# 	exp.nextEntry()
		# 	core.wait(0.5)
				


	def draw_moving_clock(self, win, event, tracker=None):
		'''
			define termination condition (2 rotations)
			While < defined T-condition:
				# iterate each frame
				Draw Tick
				if user_input == True:
					save user input time
					log user input key
					send message to eyetracker (Still need to figure out how to do this)
		'''

		for i in range(2):
			clock_end = math.pi/2
			clock_start = math.pi/2 + 2*math.pi
			clock_where = clock_start

			clock_step = 2*math.pi/240 # TODO: Need to figure out how to set the time of the clock
			while clock_where >= clock_end:

				self.draw_plain_clock(win)
				dot_x = self.radius * math.cos(clock_where)
				dot_y = self.radius * math.sin(clock_where)
				circle = visual.Circle(win, radius=0.2, fillColor='white', pos=(dot_x, dot_y), 
					edges=self.edges, lineWidth=3)
				circle.draw()

				clock_where = clock_where - clock_step
				win.flip()

			if (self.user_input == True) & (i == 1):
				key = event.getKeys(keyList=['space'])
				if key[0] == 'space':
					tracker.sendMessage('M-TIME RECORDED.')






		