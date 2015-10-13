#import ea.py
import random_rules
import random

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




# A classifier. 
# Contains a condition, an action, a fitness value
class Classifier:
	def __init__(self, id):
		self.id = id
		# self.condition = None
		# self.action = None
		self.condition = random_rules.generate_condition()
		self.action = random.choice(CLASS_LABELS)
		self.prediction = 0.0
		self.fitness = 0.0
		self.error = 0.0
		self.experience = 0
		self.times_correct = 0
		self.times_wrong = 0
		self.accuracy = 0.0
		self.rule = [self.condition, self.action]
		
		
		#self.test = random_rules.generate_condition()
		
		
	


		
	def classify(self, environment):
		def check_condition(environment):
			for k, v in self.condition.items():
				if environment.dictionary[k] != v:
					return False			# One condition of this classifier was not met				
			return True		

		def update_classifier(was_correct):
			self.experience += 1
			if was_correct:
				self.times_correct += 1 
				self.accuracy = self.times_correct/self.experience
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
		print("{0:<15s} : {1}".format("Classifier #", self.id))
		print("{0:<15s} : {1}".format("Condition:", self.condition))
		print("{0:<15s} : {1}".format("Action:", self.action))
		#print("{0:<15s} : {1}".format("Prediction:", self.prediction))
		print("{0:<15s} : {1}".format("Fitness:", self.fitness))
		print("{0:<15s} : {1}".format("Experience:", self.experience))
		print("{0:<15s} : {1}".format("Times Correct:", self.times_correct))
		print("{0:<15s} : {1}".format("Times Wrong:", self.times_wrong))
		print("{0:<15s} : {1}".format("Accuracy:", self.accuracy * 100))
		#print("{0:<15s} : {1}".format("Error:", self.error))		
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
			self.dictionary[HEADINGS[h]] = int(data[h]) if data[h].isnumeric() else data[h]
		self.correct_class = data[len(HEADINGS) - 1]
	
	# Prints the details of the environment in a nice, easy-to-read manner.
	def print_details(self):
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
	return [Classifier(x) for x in range(10)]	
	

	
# One timestep. 
def step(environment, classifiers):
	match_set  = []		# The classifiers who have their conditions met in this timestep's environment
	action_set = []		# The classifiers from the Match Set with the highest fitness
	for c in classifiers:
		c.classify(environment)
	#print([c.classify(environment) for c in classifiers])

	

def main():
	environments = create_environments()
	classifiers  = create_classifiers()	
	
	for c in classifiers:
		c.print_details()
		
	print('------------------------------------')
	
	match_set  = []
	action_set = []
	
	#environments[0].print_details()
	

	for x in range(25000):		
		step(environments[x], classifiers);


if __name__ == "__main__":
    main()	

