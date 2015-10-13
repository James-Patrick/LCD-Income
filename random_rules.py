import random

def generate_condition():

	PROBABILITY = 0.2		# The chance that a field will be included in the condition

	ADULT_FIELDS = {
		"age": [19, 80],
		"workclass": ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"],
		"fnlwgt": [100000, 300000],
		"education": ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"],
		"education-num": [7, 13],
		"marital-status": ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"],
		"occupation": ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"],
		"relationship": ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"],
		"race": ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"],
		"sex": ["Female", "Male"],
		"capital-gain": [0, 10000],
		"capital-loss": [0, 10000],
		"hours-per-week": [0, 60],
		"native-country": ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]
	}
	
	CONTINUOUS_FIELDS = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
	
	condition = {}
	
	def make_condition():
		
		for k, v in ADULT_FIELDS.items():	
			r = random.random()
			if r < PROBABILITY:	
				if k in CONTINUOUS_FIELDS:
					condition[k] = random.randrange(v[0], v[1])		# Select randomly between min-max if it's a continuous field such as "age"
				else:
					condition[k] = random.choice(v)					# Select a random value if it's a discrete field such as "workclass"
		return condition
		
	
	while(len(condition.keys()) == 0):
		condition = make_condition()
	
	return condition
	
	

