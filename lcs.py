# -*- coding: utf-8 -*-

# Note: You must run 'pip install enum34' before this will work on Python versions < 3.4.
# By Michael Stewart, James Patrick and Brandon Papalia.

from global_variables import *
import random_rules
import lcs_enums
import ea


import time, sys, getopt, ast, random, copy, math



''' Colorama (for nicer output) '''
from colorama import init, Fore
init()




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

LEARNING_FILENAME = 'adult.data'
TESTING_FILENAME  = 'adult.test.txt' #'adult.data'# 'adult.test.txt'
HEADINGS = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',	'marital-status', 'occupation', 'relationship', 'race',	'sex', 'capital-gain', 'capital-loss',	'hours-per-week', 'native-country', 'salary']
CLASS_LABELS = ['<=50K', '>50K']
NUM_CLASSIFIERS = 1000
LEARN_MODE    = 0
CLASSIFY_MODE = 1
CLASSIFIERS_FILE = "classifiers"
MAX_CLASSIFIERS = 999999
COUNT = 0
USING_EA = False

LEARNING_TIMES = 3

ACCURACY_CUTOFF = 0.40		# Accuracy required to mutate/be deleted (if unsufficient)
EXPERIENCE_CUTOFF = 120		# Amount of experience required to mutate

classifiers = []
total_deleted = 0
total_classifiers = 0

verbose = False

def make_verbose():
	global verbose
	verbose = True


# A classifier. 
# Contains a condition, an action, a fitness value
class Classifier:
	__all__ = set()
	def __init__(self, condition = None, action = None, duplicate = True, from_dict = False):


		if from_dict:
			self.read_from_dictionary(from_dict)
		else:

			if condition:
				self.condition = condition
			else:
				self.condition = random_rules.generate_condition()
			if action:
				self.action = action
			else:
				self.action = random_rules.generate_action(CLASS_LABELS)

			self.prediction 	= 0.0
			self.fitness 		= 0.0
			self.error			= 0.0
			self.experience 	= 0
			self.times_correct 	= 0
			self.times_wrong 	= 0
			self.accuracy		= 0.0
			self.lifetime		= 0
			self.has_mutated 	= False
			
			global total_classifiers
			self.id = total_classifiers
			total_classifiers += 1
			
			global classifiers
			classifiers.append(self)
			
			if verbose:
				if self.action == ">50K":
					sys.stdout.write(Fore.CYAN + '.')
				else:
					sys.stdout.write(Fore.YELLOW + '.')
				sys.stdout.write(Fore.WHITE)
			
			
			#ea.getMutantChild(self.condition)

		# Duplicate this classifier, creating the same classifier but for the inverse rule
		if duplicate:
			
			def flipped_action(action):
				if action == '<=50K':
					return '>50K'
				else:
					return '<=50K'
				
			dc = copy.deepcopy(self)
			dc.action = flipped_action(self.action)

			#dc = Classifier(self.condition, flipped_action(self.action), False)
		
		self.__class__.__all__.add(self)

	# Checks if condition is met in environment
	def check_condition(self, environment):
		for k, v in self.condition.items():
			
			# If continuous, check whether the value is within minBound and maxBound.
			# If discrete, check whether the classifier's field matches the environment's field.
			if k in CTS_ATTRIBUTES:
				if environment.dictionary[k] < v[0] or environment.dictionary[k] > v[1]:
					return False
			else:
				if environment.dictionary[k] != v:
					return False
		return True	

	def mutate(self):
	
		def create_child():
			new_condition = ea.getMutantChild(copy.deepcopy(self.condition))
			new_action	  = copy.deepcopy(self.action)
			c = Classifier(new_condition, new_action)
		
		global classifiers		
		if len(classifiers) < MAX_CLASSIFIERS:			
			if (self.experience > EXPERIENCE_CUTOFF and self.accuracy > ACCURACY_CUTOFF):
			
				if not self.has_mutated:
			
					create_child()
					self.has_mutated = True					

				# Give it a second chance to mutate (more if it's >50K)!
				r = random.random()
				if r < (750.0/math.pow(len(classifiers), 2)) and self.action == ">50K":
					create_child()
				if r < (50.0/math.pow(len(classifiers), 2)) and self.action == "<=50K":
					create_child()		
						
							
							
					

	
	def check_delete(self):
		global total_deleted
		global classifiers
		if (self.experience > (EXPERIENCE_CUTOFF * 2) and self.accuracy < ACCURACY_CUTOFF) or (self.lifetime > 1000 and self.experience < 5):
			total_deleted += 1
			classifiers.remove(self)	
			if verbose:
				sys.stdout.write(Fore.RED + '.')
				sys.stdout.write(Fore.WHITE)		

		
	# Learns from the environment. Checks whether the rule held by the classifier is correct or not, depending on whether its conditions are met in the environment
	def learn(self, environment):

		# Updates the classifier's parameters based on whether it was correct or incorrect.
		def update_classifier(was_correct):
			self.experience += 1
			if was_correct:
				self.times_correct += 1 
				self.accuracy = self.times_correct * 1.0 / self.experience * 1.0
				# Mutate!
				#if(random.random() < MUTATE_CHANCE):
				#	ch = Classifier(ea.getMutantChild(self.condition), self.action)
				if USING_EA:
					self.mutate()
			else:
				self.times_wrong += 1

			
		# If this classifier has met all its conditions on the environment, add +1 experience points and return the classifier's action
		# (which in this case is either <= 50K or > 50K)
		
		if self.check_condition(environment):
			was_correct = (self.action == environment.correct_class)	
			update_classifier(was_correct)
		
		self.check_delete()
		self.lifetime = self.lifetime + 1
		
			#self.print_details()
#			return self.action
#		else:
#			return None
	
	
	def classify(self, environment):
		if self.check_condition(environment):
			return (self.accuracy, self.action)

	# Prints the details of the classifier in a nice, easy-to-read manner.
	def print_details(self):
		if verbose:
		#	print("{0:<15s} : {1}".format("Classifier #", self.id))
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
	
	# Outputs the classifier's info as a dictionary
	def to_dictionary(self):
		to_dict = {}
	#	to_dict["id"] = self.id
		to_dict["id"] = self.id
		to_dict["condition"] = self.condition
		to_dict["action"] = self.action
		to_dict["accuracy"] = self.accuracy
		to_dict["experience"] = self.experience	  
		to_dict["lifetime"] = self.lifetime		
		return to_dict

	# Inputs the classifiers info from a dictionary
	def read_from_dictionary(self, from_dict):
	#	self.id = from_dict["id"]

		self.condition = from_dict["condition"]
		self.action = from_dict["action"]
		self.accuracy = from_dict["accuracy"]
		self.experience	= from_dict["experience"]
		
		
		
# One environment (a dictionary that maps field names to their values).	
# For example, 
#   {'education': 'HS-grad', 'workclass': 'Local-gov', 'age': 67 ...}
# self.correct_class = The correct class label for this particular environment.
class Environment:
	def __init__(self, data):	
		self.dictionary = {}
		
		for h in range(len(HEADINGS) - 1):
			# Convert field to integer if it is numeric, otherwise keep it as a string (so it may handle discrete/continuous variables).
			h_uppercase = HEADINGS[h].upper().replace('-', '_')
			if data[h] == "?":
				self.dictionary[h_uppercase] = "?"
			else:				
				if h_uppercase in CTS_ATTRIBUTES:
					self.dictionary[h_uppercase] = int(data[h])
				else:
					self.dictionary[h_uppercase] = 	lcs_enums.sourceTexttoEnum(h_uppercase, data[h]).value
			
			
		self.correct_class = data[len(HEADINGS) - 1]
		#self.print_details()
	
	# Prints the details of the environment in a nice, easy-to-read manner.
	def print_details(self):
		if verbose:			#match_set  = []
			#action_set = []
			for k, v in self.dictionary.items():
				print("{0:<20s} : {1}".format(k, v))
			print("----------------------------")
			print("{0:<20s} : {1}".format("Correct class", self.correct_class))


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
	except getopt.GetoptError:			#match_set  = []
			#action_set = []
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


	# Creates a list of environments.
	# Environments are stored as objects, which contain a dictionary, and a correct_class.
	def create_environments(file):	
		with open(file, "r") as file:		
			data = [f.replace(' ', '').rstrip().split(',') for f in file.readlines()]

		return [Environment(d) for d in data]

	

	def do_learn_mode():
	
		
		environments = create_environments(LEARNING_FILENAME)

		# Creates the initial population of classifiers, in the form of a list.
		def create_classifiers():
			for x in range(NUM_CLASSIFIERS):
			  Classifier()
			#return Classifier.__all__

		# Writes all classifiers to a file, in dictionary format
		def write_classifiers(output_file, new_classifiers):
			#global classifiers
			for c in new_classifiers:
				output_file.write(str(c.to_dictionary()))
				output_file.write('\n')

		# One timestep. Returns the updated list of classifiers
		def step(environment):
			global classifiers			
			for c in classifiers:
				c.learn(environment)
			
			#classifiers = Classifier.__all__
			#return classifiers		# Have to refresh the list every step
			
		time_start = time.time()
	
		global classifiers
		
		create_classifiers()
		count = 0
		
		#if verbose:
		#	for c in classifiers:
		#		c.print_details()
		#	print('------------------------------------') 

		
		for x in xrange(LEARNING_TIMES):
			count = 0
			print "\n\n------------------------------"
			print "Learning", x + 1, "/", LEARNING_TIMES
			print "------------------------------"
			for x in range(len(environments)):		
				#new_classifiers = step(environments[x], classifiers);
				#classifiers = copy.deepcopy(new_classifiers)
		
				#sys.stdout.write("X")
				step(environments[x])
				count += 1
				#sys.stdout.write(Fore.WHITE + "X")
				if count % 500 == 0:
					print "\n"
					print "\nStep:", count, "\tClassifiers:", len(classifiers)
					print "\n"
		

		print("Num classifiers: ", len(classifiers))
		print("Total deleted: ", total_deleted)
		time_end = time.time()
		total_time = time_end - time_start
		print(total_time, "seconds")

		output_file = open(CLASSIFIERS_FILE, "w")
		print("Tidying up...")
		print(len(classifiers))
		final_classifiers = list()
		for c in classifiers:
			if not (c.experience < EXPERIENCE_CUTOFF or c.accuracy < ACCURACY_CUTOFF):
				final_classifiers.append(c)
		print(len(final_classifiers))
		write_classifiers(output_file, final_classifiers)		

		
	def do_classify_mode():		
	
		def read_classifiers():
			print("Reading classifiers...")			
			with open(CLASSIFIERS_FILE, "r") as file:
				classifier_dict = [ast.literal_eval(l) for l in file.readlines()]
			return [Classifier(from_dict = k) for k in classifier_dict]

		
		# One timestep. 
		def step(environment, classifiers, total_seen, total_correct, total_incorrect, total_missed):
			match_set = []
			for c in classifiers:
				cl = c.classify(environment)			# [classifier, action, accuracy]
				if cl:
					match_set.append(cl)
			
			
			sorted_set = sorted(match_set, key=lambda tup: tup[0], reverse = True)
			if len(sorted_set) > 0:
				print_char = '.'
				if environment.correct_class == ">50K":
					print_char = '!'

				action = sorted_set[0][1]
				if action == environment.correct_class:
					correct = True
					total_correct += 1
					if verbose:
						sys.stdout.write(Fore.GREEN + print_char + Fore.WHITE)
				else:
					correct = False
					total_incorrect += 1
					if verbose:
						sys.stdout.write(Fore.RED + print_char + Fore.WHITE)
			else:
				sys.stdout.write(" ")
				total_missed += 1
			return [total_correct, total_incorrect, total_missed]


		environments = create_environments(TESTING_FILENAME)	
			
		classifiers = read_classifiers()
		
		if verbose:
			g50 = 0
			l50 = 0
			for c in classifiers:
				if c.action == ">50K":
					g50 += 1
				else:
					l50 += 1
			print ">50K:\t", g50
			print "<=50K:\t", l50
			print "-------------------------"
			time.sleep(3)

		time_start = time.time()
	
		total_correct = 0
		total_incorrect = 0
		total_missed = 0
		total_seen = 0
		for x in range(len(environments)):		
			total_seen += 1
			cim = step(environments[x], classifiers, total_seen, total_correct, total_incorrect, total_missed);		
			total_correct = cim[0]
			total_incorrect = cim[1]
			total_missed = cim[2]
			
		print("\n\n")
		sys.stdout.write("Total:\t\t" + str(total_seen) + "\n")
		sys.stdout.write("Correct:\t" + Fore.GREEN + str(total_correct) + Fore.WHITE + "\n")
		sys.stdout.write("Incorrect:\t" + Fore.RED + str(total_incorrect) + Fore.WHITE + "\n")
		sys.stdout.write("Missed:\t\t" + Fore.YELLOW + str(total_missed) + Fore.WHITE + "\n")		
		print("-------------------------------------------------------")
		print("Accuracy: %.5f" % (total_correct * 1.0 / total_seen * 1.0 * 100))
		print("\n")
		time_end = time.time()
		total_time = time_end - time_start
		print(total_time, "seconds")			
		
	
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
