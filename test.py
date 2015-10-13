filename = 'adults.data'
headings = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary']



# A classifier. 
class Classifier:
	def __init__(self):
		self.data = []
		self.rule = None
		self.action = None
		
		
# One environment (a dictionary that maps field names to their values).	
# For example, 
#   {'education': 'HS-grad', 'workclass': 'Local-gov', 'age': '67' ...}
class Environment:
	def __init__(self, data):
		self.dictionary = {headings[h]: data[h] for h in range(len(headings))}
		
		
		
# Returns list of environments
def create_environments():	
	with open("adult.data", "r") as file:		
		data = [f.replace(' ', '').rstrip().split(',') for f in file.readlines()]
	
	return [Environment(d) for d in data]
	

def create_classifiers():
	print('Hi')
	
		

def save_classification:
	file = open('adult_classification.csv', "w" )

environments = create_environments()

for e in environments:
	print(e.dictionary)
	
classifiers = []

for i in range(10):
	c = Classifier()
	classifiers.append(c)

for c in classifiers:
	print(c)