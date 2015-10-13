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



# A classifier. 
# Contains a condition, an action, a fitness value
class Classifier:
	def __init__(self):
		self.data = []
		self.condition = None
		self.action = None
		self.prediction = 0.0
		self.fitness = 0.0
		self.error = 0.0
		self.rule = [self.condition, self.action]
	
	def generate_random_rule():
		print('hi')
		
		
# One environment (a dictionary that maps field names to their values).	
# For example, 
#   {'education': 'HS-grad', 'workclass': 'Local-gov', 'age': 67 ...}
# self.correct_class = The correct class label for this particular environment.
class Environment:
	def __init__(self, data):
		# Note: make continuous stuff
		self.dictionary = {}
		for h in range(len(HEADINGS) - 1):
			# Convert field to integer if it is numeric, otherwise keep it as a string (so it may handle discrete/continuous variables)
			self.dictionary[HEADINGS[h]] = int(data[h]) if data[h].isnumeric() else data[h]
		self.correct_class = data[len(HEADINGS) - 1]
	
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
	print('')
	

	
# One timestep. 
def step():
	print('')
	
	

def main():
	environments = create_environments()
	classifiers = create_classifiers()	
	
	match_set  = []
	action_set = []
	
	environments[0].print_details()

if __name__ == "__main__":
    main()	

