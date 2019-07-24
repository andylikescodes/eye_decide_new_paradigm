from psychopy import core, visual, gui, data, event, logging
from psychopy.sound.backend_pygame import SoundPygame as Sound
import random, math
import numpy as np

# A clock class to handle the clock animation and user input during clock animation.

class Clock:
	def __init__(self, radius, tick_length=0.5, user_input=True, 
				edges=64):
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
		return circle

	def draw_fixation(self, win):
		# Draw a fixation
		fixation = visual.GratingStim(win, color='white', colorSpace='rgb',
              tex=None, mask='circle', size=0.2)
		return fixation

	def draw_ticks(self, win):
		all_ticks = []
		for i in range(0,12):
			x_start, y_start = self.cal_pos(self.radius, (math.pi/2)-i*math.pi/6)
			x_end, y_end = self.cal_pos((self.radius - self.tick_length), (math.pi/2)-i*math.pi/6)
			line = visual.Line(win, start=(x_start, y_start), end=(x_end, y_end))
			all_ticks.append(line)
		return all_ticks

	def draw_plain_clock(self, win):
		# display instructions and wait
		circle = self.draw_circle(win)
		fixation = self.draw_fixation(win)
		ticks = self.draw_ticks(win)

		return circle, fixation, ticks

	def draw_moving_clock(self, win, event, play_random_sound=False, tracker=None, beep_dist=None, exp=None):
		timer = core.Clock()
		event.clearEvents()
		# Play sound properties
		if play_random_sound == True:
			random.seed() # Set random seed to get random sequence everytime.
			beep_time = np.random.choice(beep_dist, 1)
			beep_rotation = np.floor(beep_time/2.5)
			beep_time_this_clock = beep_time - beep_rotation * 2.5
		
		rotations = 0

		# Initialize all objects
		circle, fixation, ticks = self.draw_plain_clock(win)
		ball = visual.Circle(win, radius=0.2, fillColor='white', pos=[0,0], 
					edges=self.edges, lineWidth=3)
		speaker = Sound(value="F", secs=0.2, stereo=False)

		pressed = -1
		sound_played = -1
		clock_keep_running = 0
		key=[]
		# MSG Eye-tracker - clock display
		tracker.sendMessage('CLOCK ONSET')
		while clock_keep_running < 1:
			if (pressed == 1) | (sound_played == 1):
				clock_keep_running += 1

			rotations = rotations + 1
			timer.add(2.5)

			time_start = timer.getTime()
			clock_where = math.pi/2
			time_now = time_start
			while time_now <= 0:
				# print(rotations)
				dot_x, dot_y = self.cal_pos(self.radius, clock_where)
				circle.draw()
				fixation.draw()
				ball.pos=[dot_x, dot_y]
				ball.draw()
				for tick in ticks:
					tick.draw()
				win.flip()

				if (play_random_sound == True) & (sound_played == -1):
					if (beep_rotation == rotations):
						where_beep_clock = math.pi/2 - beep_time_this_clock/2.5 * 2 * math.pi
						if (where_beep_clock >= clock_where):
							speaker.play()
							tracker.sendMessage('EVENT-TIME RECORDED - SOUND PLAYED.')
							event_time = beep_time[0]
							exp.addData('event_time', event_time)
							sound_played = 1

				if (self.user_input == True) & (rotations > 1) & (pressed==-1) & (play_random_sound == False):
					key = event.getKeys(keyList=['space'])
					if key:
						if key[0] == 'space':
							tracker.sendMessage('EVENT-TIME RECORDED - KEYPRESSED.')
							pressed = 1
							event_time = 2.5 * rotations + (time_now - time_start)
							exp.addData('event_time', event_time)
				elif (rotations <= 1):
					event.clearEvents()

				time_now = timer.getTime()
				clock_where = math.pi/2-(time_now - time_start)/2.5 * 2 * math.pi
				# print(time_now)
				# print(clock_where)
				# print((time_now - time_start)/2.5)

		# MSG Eye-tracker - clock closed
		tracker.sendMessage('CLOCK OFFSET')
		# Add a 0.5 seconds after the clock was played
		core.wait(0.5)
		return event_time







		