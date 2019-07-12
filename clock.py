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

				self.draw_plain_clock(win, draw_now=False)
				dot_x = self.radius * math.cos(clock_where)
				dot_y = self.radius * math.sin(clock_where)
				circle = visual.Circle(win, radius=0.2, fillColor='white', pos=(dot_x, dot_y), 
					edges=self.edges, lineWidth=3)
				circle.draw()

				clock_where = clock_where - clock_step
				win.flip()
				pressed = -1
			if (self.user_input == True) & (i == 1) & (pressed==-1):
				key = event.getKeys(keyList=['space'])
				if key:
					if key[0] == 'space':
						#tracker.sendMessage('M-TIME RECORDED.')
						pressed = 1
						continue







		