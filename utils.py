from psychopy import core, visual, gui, data, event, logging
import numpy, random
from config import *

def draw_instructions(win, text1, text2):
	fixation = visual.GratingStim(win, color='white', colorSpace='rgb',
                              tex=None, mask='circle', size=0.2)
	message1 = visual.TextStim(win, pos=[0,+3], text=text1)
	message2 = visual.TextStim(win, pos=[0,-3], text=text2)
	message1.draw()
	message2.draw()
	fixation.draw()
	win.flip()