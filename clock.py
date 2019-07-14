from psychopy import core, visual, gui, data, event
from psychopy.sound.backend_pygame import SoundPygame as Sound
import random, math
import numpy as np

# A clock class to handle the clock animation and user input during clock animation.

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
		# Draw the circle
		circle = visual.Circle(win, radius=self.radius, edges=self.edges, lineWidth=3)
		circle.draw()

	def draw_fixation(self, win):
		# Draw a fixation
		fixation = visual.GratingStim(win, color='white', colorSpace='rgb',
              tex=None, mask='circle', size=0.2)
		fixation.draw()

	def draw_ticks(self, win):
		for i in range(0,12):
			x_start, y_start = self.cal_pos(self.radius, (math.pi/2)-i*math.pi/6)
			x_end, y_end = self.cal_pos((self.radius - self.tick_length), (math.pi/2)-i*math.pi/6)
			line = visual.Line(win, start=(x_start, y_start), end=(x_end, y_end))
			line.draw()

	def draw_plain_clock(self, win, draw_now=True):
		# display instructions and wait
		self.draw_circle(win)
		self.draw_fixation(win)
		self.draw_ticks(win)

		if draw_now == True:
			win.flip()

	def draw_moving_clock(self, win, event, play_random_sound=False, tracker=None):
		# Clock speed definition TODO: Need to figure out the time representation of each step.
		n_steps = 240

		# Play sound properties
		random.seed() # Set random seed to get random sequence everytime.
		rn_sound_frame = random.randint(np.floor(n_steps/5), n_steps-np.floor(n_steps/5)) # Play a sound between 1/5 and 3/5 in the clock
		rn_sound_tracker = 0 # Track the frame that the sound should be played
		
		for i in range(2):
			clock_end = math.pi/2
			clock_start = math.pi/2 + 2*math.pi
			clock_where = clock_start
			clock_step = 2*math.pi/n_steps # TODO: Need to figure out how to set the time of the clock

			while clock_where >= clock_end:

				self.draw_plain_clock(win, draw_now=False)
				dot_x, dot_y = self.cal_pos(self.radius, clock_where)
				circle = visual.Circle(win, radius=0.2, fillColor='white', pos=(dot_x, dot_y), 
					edges=self.edges, lineWidth=3)
				circle.draw()

				clock_where = clock_where - clock_step
				win.flip()
				
				if (i == 1) & (play_random_sound == True):
					rn_sound_tracker = rn_sound_tracker + 1
					
					if rn_sound_frame == rn_sound_tracker:
						speaker = Sound(value="F", secs=0.2, stereo=False)
						speaker.play()
						#tracker.sendMessage('Sound Played RECORDED.')
						continue

				pressed = -1
				if (self.user_input == True) & (i == 1) & (pressed==-1):
					key = event.getKeys(keyList=['space'])
					if key:
						if key[0] == 'space':
							#tracker.sendMessage('M-TIME RECORDED.')
							pressed = 1
							continue
		# Add a 0.5 seconds after the clock was played
		core.wait(0.5)







		