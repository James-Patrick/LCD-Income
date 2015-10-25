# -*- coding: utf-8 -*-
import random
import ea



def generate_condition():

	PROBABILITY = 0.2		# The chance that a field will be included in the condition

	ADULT_FIELDS = {
		"AGE": [19, 80],
		"WORKCLASS": ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"],
		"FNLWGT": [100000, 300000],
		"EDUCATION": ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"],
		"EDUCATION_NUM": [7, 13],
		"MARITAL_STATUS": ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"],
		"OCCUPATION": ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"],
		"RELATIONSHIP": ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"],
		"RACE": ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"],
		"SEX": ["Female", "Male"],
		"CAPITAL_GAIN": [0, 10000],
		"CAPITAL_LOSS": [0, 10000],
		"HOURS_PER_WEEK": [0, 60],
		"NATIVE_COUNTRY": ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]
	}
	
	#CONTINUOUS_FIELDS = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
	
	condition = {}
	
	def make_condition():
		
		for k, v in ADULT_FIELDS.items():	
			r = random.random()
			if r < PROBABILITY:	
				if k in CTS_ATTRIBUTES:
					condition[k] = generateCtsInitial(k)		# Select randomly between min-max if it's a continuous field such as "age"
				else:
					condition[k] = enumVal(k, random.randint(0, len(v)))			# Select a random value if it's a discrete field such as "workclass"
		return condition

	
                
	
	while(len(condition.keys()) == 0):
		condition = make_condition()
	
	return Rule(condition)

def enumVal(name, index):
        if (name == 'WORKCLASS'):
                return WORKCLASS(index)
        elif (name == 'EDUCATION'):
                return EDUCATION(index)
        elif (name == 'MARITAL_STATUS'):
                return MARITAL_STATUS(index)
        elif (name == 'OCCUPATION'):
                return OCCUPATION(index)
        elif (name == 'RELATIONSHIP'):
                return RELATIONSHIP(index)
        elif (name == 'RACE'):
                return RACE(index)
        elif (name == 'SEX'):
                return SEX(index)
        elif (name == 'NATIVE_COUNTRY'):
                return NATIVE_COUNTRY(index)                                                      


def generateCtsInitial(newKey):
    return

def sourceTexttoEnum(category, name):
	
def generate_action(class_labels):
	return random.choice(class_labels)
