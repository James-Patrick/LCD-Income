# -*- coding: utf-8 -*-

# Note: You must run 'pip install enum34' before this will work on Python versions < 3.4.
# Note: You must also run 'pip install colorama'.
# By Michael Stewart, James Patrick and Brandon Papalia.

from global_variables import *
import random_rules, lcs_enums, ea

import time, sys, getopt, ast, random, copy, math, os

# Colorama (for nicer output)
from colorama import init, Fore
init()


''' Notes '''
# After a while, we need to choose a number where the classifier is sufficiently experienced enough to be deleted if it's fitness is too low


''' (Not used, but it's useful for reference)
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
NUM_CLASSIFIERS = 1000	# Initial classifier population
LEARN_MODE    = 0
CLASSIFY_MODE = 1
RESULTS_MODE = 2
CLASSIFIERS_FILE = "classifiers"

IMBALANCE_RATIO = 3846.0 / 16281.0			# Ratio of min/maj

COUNT = 0
USING_EA = True
USING_DUPLICATION = True

LEARNING_TIMES = 1			# Number of times the learning dataset is scanned

ACCURACY_CUTOFF = 0.75		# Accuracy required to mutate/be deleted (if unsufficient)
EXPERIENCE_CUTOFF = 100		# Amount of experience required to mutate

classifiers = []
total_deleted = 0
total_classifiers = 0

verbose = False

RESULTS_FILE = "results"
learning_time = None		# In results mode, time taken for learning to complete

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
			
		# Duplicate this classifier, creating the same classifier but for the inverse rule
		if duplicate:
			
			def flipped_action(action):
				if action == '<=50K':
					return '>50K'
				else:
					return '<=50K'
				
			if USING_DUPLICATION:
				dc = copy.deepcopy(self)
				dc.action = flipped_action(self.action)

			#dc = Classifier(self.condition, flipped_action(self.action), False)
		
		self.__class__.__all__.add(self)

	# Checks if condition is met in environment
	def check_condition(self, environment):
		for k, v in self.condition.items():
			
			# If continuous, check whether the value is not within minBound and maxBound.
			# If discrete, check whether the classifier's field do not match the environment's field.
			if k in CTS_ATTRIBUTES:
				if environment.dictionary[k] < v[0] or environment.dictionary[k] > v[1]:
					return False
			else:
				if environment.dictionary[k] != v:
					return False	
				#if isinstance(v, int):
				#	if environment.dictionary[k] != v:
				#		return False	
				#else:
				#	if environment.dictionary[k] not in v:
				#		return False
		return True	

	def mutate(self):
	
		def create_child():
			new_condition = ea.getMutantChild(copy.deepcopy(self.condition))
			new_action	  = copy.deepcopy(self.action)
			c = Classifier(new_condition, new_action)
		
		if (self.experience > EXPERIENCE_CUTOFF and self.accuracy > ACCURACY_CUTOFF):
		
			if not self.has_mutated:
		
				create_child()
				self.has_mutated = True					

			#Give it a second chance to mutate if it's >50K!
			#r = random.random()
			#if r < (5.0/math.pow(len(classifiers), 3)) and self.action == ">50K":
			#	create_child()
			#if r < (5.0/math.pow(len(classifiers), 3)) and self.action == "<=50K":
			#	create_child()		
	
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
	
	
	def classify(self, environment):
		if self.check_condition(environment):
			return [self.accuracy, self.action]

	# Prints the details of the classifier in a nice, easy-to-read manner.
	def print_details(self):
		if verbose:
			print("{0:<15s} : {1}".format("Condition:", self.condition))
			print("{0:<15s} : {1}".format("Action:", self.action))
			print("{0:<15s} : {1}".format("Fitness:", self.fitness))
			print("{0:<15s} : {1}".format("Experience:", self.experience))
			print("{0:<15s} : {1}".format("Times Correct:", self.times_correct))
			print("{0:<15s} : {1}".format("Times Wrong:", self.times_wrong))			
			print("{0:<15s} : {1}".format("Accuracy:", self.accuracy * 100))
			print()
	
	# Outputs the classifier's info as a dictionary
	def to_dictionary(self):
		to_dict = {}
		to_dict["id"] = self.id
		to_dict["condition"] = self.condition
		to_dict["action"] = self.action
		to_dict["accuracy"] = self.accuracy
		to_dict["experience"] = self.experience	  
		to_dict["lifetime"] = self.lifetime		
		return to_dict

	# Inputs the classifiers info from a dictionary
	def read_from_dictionary(self, from_dict):
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
		if verbose:
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
		print('-r Results mode')

	mode = LEARN_MODE

	try:
		opts, args = getopt.getopt(argv, "hvlcr")
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
		elif opt == '-r':
			mode = RESULTS_MODE			


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

		# Writes all classifiers to a file, in dictionary format
		def write_classifiers(output_file, new_classifiers):
			for c in new_classifiers:
				output_file.write(str(c.to_dictionary()))
				output_file.write('\n')

		# One timestep. Returns the updated list of classifiers
		def step(environment):
			global classifiers			
			for c in classifiers:
				c.learn(environment)
			
		time_start = time.time()
	
		global classifiers
		
		create_classifiers()
		count = 0
		
		for x in xrange(LEARNING_TIMES):
			count = 0
			print "\n----------------------------------"
			print "Learning", x + 1, "/", LEARNING_TIMES
			print "----------------------------------"
			for x in range(len(environments)):		
				step(environments[x])
				count += 1
				if count % 500 == 0:
					if verbose: print "\n\n"
					print "Step:", count, "\tClassifiers:", len(classifiers)
					if verbose: print "\n"
		
		print "\n----------------------------------"
		"Num classifiers:", len(classifiers)
		"Total deleted:", total_deleted
		time_end = time.time()
		total_time = time_end - time_start
		print "Total time:", total_time, "seconds"
		
		output_file = open(CLASSIFIERS_FILE, "w")
		print"Tidying up...", len(classifiers), ">>",
		final_classifiers = list()
		for c in classifiers:
			if not (c.experience < EXPERIENCE_CUTOFF or c.accuracy < ACCURACY_CUTOFF):
				final_classifiers.append(c)
		print len(final_classifiers)
		write_classifiers(output_file, final_classifiers)
		print "----------------------------------\n"
		
		if RESULTS_MODE:
			global learning_time
			learning_time = total_time

		
	def do_classify_mode():		
	
		def read_classifiers():
			print("Reading classifiers...")			
			with open(CLASSIFIERS_FILE, "r") as file:
				classifier_dict = [ast.literal_eval(l) for l in file.readlines()]
			return [Classifier(from_dict = k) for k in classifier_dict]

		
		# One timestep. 
		def step(environment, classifiers, total_seen, total_correct, total_incorrect, total_missed, maj_missed, min_missed):
			match_set = []
			for c in classifiers:
				cl = c.classify(environment)			# [classifier, action, accuracy]
				if cl:
					match_set.append(cl)
			
			
			# Assign more weighting to the minority class if using IR
			if USING_IR:
				if len(match_set) > 0:
					for c in match_set:
						if c[1] == ">50K":
							c[0] *= (1 + IMBALANCE_RATIO)
						else:
							c[0] *= (1 - IMBALANCE_RATIO)

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
					if environment.correct_class == ">50K":
						min_missed += 1
					else:
						maj_missed +=1
					if verbose:
						sys.stdout.write(Fore.RED + print_char + Fore.WHITE)
			else:
				if verbose:	
					sys.stdout.write(" ")
				total_missed += 1
				total_incorrect += 1
				if environment.correct_class == ">50K":
					min_missed += 1
				else:
					maj_missed +=1
			return [total_correct, total_incorrect, total_missed, maj_missed, min_missed]


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
		maj_missed = 0
		min_missed = 0
		for x in range(len(environments)):		
			total_seen += 1
			cim = step(environments[x], classifiers, total_seen, total_correct, total_incorrect, total_missed, maj_missed, min_missed);		
			total_correct = cim[0]
			total_incorrect = cim[1]
			total_missed = cim[2]
			maj_missed = cim[3]
			min_missed = cim[4]
			
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
		
		if RESULTS_MODE:
			acc = total_correct * 1.0 / total_seen * 1.0
			err = 1.0 - acc
			majm = maj_missed * 1.0 / total_incorrect * 1.0
			minm = min_missed * 1.0 / total_incorrect * 1.0			
			global average_results
			average_results.append([len(classifiers), err, acc, learning_time, total_time, majm, minm, total_missed])

			#acc = "{0:.3f}".format(acc)			
			#err = "{0:.3f}".format(err)
			#lt = "{0:.3f}".format(learning_time)
			#tt = "{0:.3f}".format(total_time)
			#majm = "{0:.3f}".format(majm)	
			#minm = "{0:.3f}".format(minm)
			#results_string = str(NUM_CLASSIFIERS * 2) + "\t\t" + str(len(classifiers)) + "\t\t" + err + "\t" + acc + "\t" + lt + "\t" + tt + "\t" + majm + "\t" + minm + "\t" + str(total_missed) + "\n"
			#rf.write(results_string)
		
		print "Total time:", total_time, "seconds"		
		
	
	# For getting results. Runs a series of tests and logs the performance in a file.
	def do_results_mode():
		global rf
		global NUM_CLASSIFIERS
		global ACCURACY_CUTOFF
		rf = open(RESULTS_FILE, "w")
		rf.write("# ini: The initial number of classifiers\n")
		rf.write("# fin: The final number of classifiers\n")
		rf.write("% err: The error percentage (1 - acc)\n")
		rf.write("% acc: The accuracy percentage\n")
		rf.write("l time: The time taken to learn from the training dataset\n")
		rf.write("l time: The time taken to classify the test dataset\n")
		rf.write("% majm: The percentages of misses that were meant to be the majority class\n")
		rf.write("% minm: The percentages of misses that were meant to be the minority class\n")
		rf.write("t missed: The number of environments that could not be classified (no relevant classifier available)\n")
		rf.write("\nThe top line is without IR, and bottom with IR.\n")
		rf.write("================================================================================\n")
		rf.write("# ini\t# fin\t\t% err\t% acc\tl time\tc time\tmaj m\tmin m\tt missed\n")
		rf.write("================================================================================\n")

		LEARNING_TIMES = 1
		trial_runs = 3

		global USING_DUPLICATION
		USING_DUPLICATION = True

		def run_test(test_number, test_information):
			print Fore.CYAN + "\n\n=================================================================================", Fore.WHITE
			print "Running test", test_number
			print test_information
			#print "Initial classifiers:", NUM_CLASSIFIERS * 2, Fore.GREEN
			#if USING_DUPLICATION:
			#	print Fore.GREEN + "Using duplication"
			#else:
			#	print Fore.RED + "Not using duplication"
			print Fore.CYAN + "=================================================================================", Fore.WHITE	
			rf.write("\n" + test_information)
			rf.write("\n--------------------------------------------------------------------------------\n")
			global USING_IR
			global average_results
			global rf
			global classifiers
			for x in [False, True]:
				USING_IR = x
				print "Using IR:", USING_IR	
				print Fore.CYAN + "=================================================================================", Fore.WHITE	
				average_results = []
				for y in range(0, trial_runs):
					classifiers = []
					print Fore.YELLOW + "Trial", y + 1, Fore.WHITE
					do_learn_mode()
					do_classify_mode()
				avgs = ["{0:.4f}".format(float(sum(col))/len(col)) for col in zip(*average_results)]
				avgs_string = str(NUM_CLASSIFIERS * 2) + "\t\t" + avgs[0] + "\t\t" + avgs[1] + "\t" + avgs[2] + "\t" + avgs[3] + "\t" + avgs[4] + "\t" + avgs[5] + "\t" + avgs[6] + "\t" + avgs[7] + "\n"
				rf.write(avgs_string)
			

		NUM_CLASSIFIERS = 500 # duplicated to 500

		''' Tests: '''
		# Accuracy cutoff : 0.15
		# Accuracy cutoff : 0.30
		# Accuracy cutoff : 0.45
		# Accuracy cutoff : 0.60
		# Accuracy cutoff : 0.75

		test_number = 0

		# Accuracy cutoff tests (no IR)
		for x in range(0, 5):
			ACCURACY_CUTOFF = (x + 1) * 0.15
			test_number += 1			
			test_information = "Accuracy cutoff: " + str(ACCURACY_CUTOFF)
			run_test(test_number, test_information)		
	
		rf.close()	
	
	
	if mode == LEARN_MODE:
		do_learn_mode()
	elif mode == CLASSIFY_MODE:
		do_classify_mode()
	elif mode == RESULTS_MODE:
		do_results_mode()
	

if __name__ == "__main__":
    main(sys.argv[1:])