FILENAME = 'adult.data'
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

HEADINGS = [


# A classifier. 
class Classifier:
	def __init__(self):
		self.data = []
		self.condition = None
		self.action = None
		self.rule = [self.condition, self.action]
	
	def generate_random_rule():
		print('hi')
		
		
# One environment (a dictionary that maps field names to their values).	
# For example, 
#   {'education': 'HS-grad', 'workclass': 'Local-gov', 'age': '67' ...}
class Environment:
	def __init__(self, data):
		# Note: make continuous stuff
		
		self.dictionary = {}

		self.dictionary = {HEADINGS[h]: data[h] for h in range(len(HEADINGS))}
		
	
	
		
# Returns list of environments
def create_environments():	
	with open(FILENAME, "r") as file:		
		data = [f.replace(' ', '').rstrip().split(',') for f in file.readlines()]
	
	return [Environment(d) for d in data]
	
	
	

# Creates the initial population of classifiers, in the form of a list.
def create_classifiers():
	print('Hi')
	
		

def main():

	environments = create_environments()
	classifiers = create_classifiers()	

if __name__ == "__main__":
    main()	
	
'''
for e in environments:
	print(e.dictionary)
'''
	

	
'''	
classifiers = []

for i in range(10):
	c = Classifier()
	classifiers.append(c)

for c in classifiers:
	print(c)
'''