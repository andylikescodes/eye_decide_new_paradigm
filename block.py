import trial
from psychopy import core, visual, gui, data, event

# Block class
class Block:
	def __init__(self, experiment_type, block_id, n_trials, report, is_practice):
		self.type = experiment_type
		self.n_trials = n_trials
		self.report = report
		self.block_id = block_id
		self.is_practice = is_practice

	def draw_text(self, win, text, pos=[0,0], draw_now=True):
		text = visual.TextStim(win, pos=pos, text=text)
		text.draw()
		if draw_now == True:
			win.flip()

	def run(self, win, mouse, event, tracker=None, exp=None):

		block_txt = 'This block has {} trials, the type of experiment is {}, press space bar to start.'.format(str(self.n_trials), str(self.type))

		self.draw_text(win, block_txt)
		event.waitKeys(keyList=['space'])

		new_trial = trial.Trial(self.type)
		for i in range(self.n_trials):
			new_trial.run(win, mouse, event, report=self.report, exp=exp, block_type=self.type, 
							block_id=self.block_id, trial_number=i, is_practice=self.is_practice)

