#import ea.py
import random_rules

import time, sys, getopt

''' Notes '''
# After a while, we need to choose a number where the classifier is sufficiently experienced enough to be deleted if it's fitness is too low


''' (Not used)
HEADINGS_DICT = {'age': 'continuous', 
			'workclass': 'discrete',
			'fnlwgt': 'continuous',
			'education':'discrete',
			'education-num': 'continuous',
			'marital-status': 'discrete',
			'occupation':'discrete',
			'relationship':'discrete',
			'race':'discrete',
			'sex':'discrete',
			'capital-gain':'continuous',
			'capital-loss':'continuous',
			'hours-per-week':'continuous',
			'native-country':'discrete',
			'salary':'class-label'}
'''

FILENAME = 'adult.data'
HEADINGS = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',	'marital-status', 'occupation', 'relationship', 'race',	'sex', 'capital-gain', 'capital-loss',	'hours-per-week', 'native-country', 'salary']
CLASS_LABELS = ['<=50K', '>50K']
NUM_CLASSIFIERS = 20
LEARN_MODE    = 0
CLASSIFY_MODE = 1

verbose = False

def make_verbose():
	global verbose
	verbose = True


# A classifier. 
# Contains a condition, an action, a fitness value
class Classifier:
	def __init__(self, id):
		self.id = id
		# self.condition = None
		# self.action = None
		self.condition = random_rules.generate_condition()
		self.action = random_rules.generate_action(CLASS_LABELS)
		self.prediction 	= 0.0
		self.fitness 		= 0.0
		self.error			= 0.0
		self.experience 	= 0
		self.times_correct 	= 0
		self.times_wrong 	= 0
		self.accuracy		= 0.0
		self.rule = [self.condition, self.action]
		
		
		#self.test = random_rules.generate_condition()

		
	def classify(self, environment):
		def check_condition(environment):
			for k, v in self.condition.items():
				if environment.dictionary[k] != v:
					return False			# One condition of this classifier was not met				
			return True		

		# Updates the classifier's parameters based on whether it was correct or incorrect.
		def update_classifier(was_correct):
			self.experience += 1
			if was_correct:
				self.times_correct += 1 
				self.accuracy = self.times_correct * 1.0 / self.experience * 1.0
			else:
				self.times_wrong += 1
			#self.accuracy =
			
		# If this classifier has met all its conditions on the environment, add +1 experience points and return the classifier's action
		# (which in this case is either <= 50K or > 50K)
		
		if check_condition(environment):
			# Check if correct or not
			was_correct = (self.action == environment.correct_class)	
			update_classifier(was_correct)
			
			self.print_details()
			
			#
			return self.action
		else:
			return None
	
	# Prints the details of the classifier in a nice, easy-to-read manner.
	def print_details(self):
		if verbose:
			print("{0:<15s} : {1}".format("Classifier #", self.id))
			print("{0:<15s} : {1}".format("Condition:", self.condition))
			print("{0:<15s} : {1}".format("Action:", self.action))
		#	print("{0:<15s} : {1}".format("Prediction:", self.prediction))
			print("{0:<15s} : {1}".format("Fitness:", self.fitness))
			print("{0:<15s} : {1}".format("Experience:", self.experience))
			print("{0:<15s} : {1}".format("Times Correct:", self.times_correct))
			print("{0:<15s} : {1}".format("Times Wrong:", self.times_wrong))
			print("{0:<15s} : {1}".format("Accuracy:", self.accuracy * 100))
		#	print("{0:<15s} : {1}".format("Error:", self.error))		
			print()
		
		

		
		
# One environment (a dictionary that maps field names to their values).	
# For example, 
#   {'education': 'HS-grad', 'workclass': 'Local-gov', 'age': 67 ...}
# self.correct_class = The correct class label for this particular environment.
class Environment:
	def __init__(self, data):
		self.dictionary = {}
		for h in range(len(HEADINGS) - 1):
			# Convert field to integer if it is numeric, otherwise keep it as a string (so it may handle discrete/continuous variables).
			self.dictionary[HEADINGS[h]] = int(data[h]) if unicode(data[h]).isnumeric() else data[h]
		self.correct_class = data[len(HEADINGS) - 1]
	
	# Prints the details of the environment in a nice, easy-to-read manner.
	def print_details(self):
		if verbose:
			for k, v in self.dictionary.items():
				print("{0:<20s} : {1}".format(k, v))
			print("----------------------------")
			print("{0:<20s} : {1}".format("Correct class", self.correct_class))
		
		
# Creates a list of environments.
# Environments are stored as objects, which contain a dictionary, and a correct_class.
def create_environments():	
	with open(FILENAME, "r") as file:		
		data = [f.replace(' ', '').rstrip().split(',') for f in file.readlines()]
	
	return [Environment(d) for d in data]
	
	
	

# Creates the initial population of classifiers, in the form of a list.
def create_classifiers():
	return [Classifier(x) for x in range(NUM_CLASSIFIERS)]	
	

	


	



def main(argv):

	def print_usage():
		print('--------------------------')
		print('lcs.py usage')
		print('--------------------------')
		print('Options:')
		print('-v verbose (print output)')
		print('-l Learn mode (default)')
		print('-c Classify mode')

	mode = LEARN_MODE

	try:
		opts, args = getopt.getopt(argv, "hvlc")
	except getopt.GetoptError:
		print_usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print_usage()
			sys.exit()
		elif opt == '-v':
			make_verbose()
		elif opt == '-l':
			mode = LEARN_MODE
		elif opt == '-c':
			mode = CLASSIFY_MODE


	def do_learn_mode():
	
		# One timestep. 
		def step(environment, classifiers):
			match_set  = []
			action_set = []
			for c in classifiers:
				c.classify(environment)
				
				
	
		time_start = time.time()

		environments = create_environments()
		classifiers  = create_classifiers()	
		
		if verbose:
			for c in classifiers:
				c.print_details()
			print('------------------------------------') 

		for x in range(len(environments)):		
			step(environments[x], classifiers);

		time_end = time.time()
		total_time = time_end - time_start
		print(total_time, "seconds")
	
	
	def do_classify_mode():
		# Classify stuff.
		print("This hasn't been made yet.")
		
	
	if mode == LEARN_MODE:
		do_learn_mode()
	else:
		do_classify_mode()
	

if __name__ == "__main__":
    main(sys.argv[1:])	






''' Notes '''
# Look at all classifiers in the match set
# Look at the classifier in M with highest accuracy
# Action set = all classifiers with that same class label as action
# Reward = given when it is part of the action set

# Prediction p , estimate payoff when rule is seen
# Accuracy relative to others
