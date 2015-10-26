from enum import Enum
from global_variables import *




workclassText = ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"]
educationText = ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"]
maritalText = ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"]
occupationText = ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"]
relationshipText = ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"]
raceText = ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"]
sexText = ["Female", "Male"]
nativeCountryText = ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]


class WORKCLASS(Enum):
    PRIVATE = 0
    SELF_EMP_NOT_INC = 1
    SELF_EMP_INC = 2
    FEDERAL_GOV = 3
    LOCAL_GOV = 4
    STATE_GOV = 5
    WITHOUT_PAY = 6
    NEVER_WORKED = 7

class EDUCATION(Enum):
    BACHELORS = 0
    SOME_COLLEGE = 1
    _11TH = 2
    HS_GRAD = 3
    PROF_SCHOOL = 4
    ASSOC_ACDM = 5
    ASSOC_VOC = 6
    _9TH = 7
    _7TH_8TH = 8
    _12TH = 9
    MASTERS = 10
    _1ST_4TH = 11
    _10TH = 12
    DOCTORATE = 13
    _5TH_6TH = 14
    PRESCHOOL = 15

class MARITAL_STATUS(Enum):
    MARRIED_CIV_SPOUSE = 0
    DIVORCED = 1
    NEVER_MARRIED = 2
    SEPARATED = 3
    WIDOWED = 4
    MARRIED_SPOUSE_ABSENT = 5
    MARRIED_AF_SPOUSE = 6

class OCCUPATION(Enum):
    TECH_SUPPORT = 0
    CRAFT_REPAIR = 1
    OTHER_SERVICE = 2
    SALES = 3
    EXEC_MANAGERIAL = 4
    PROF_SPECIALTY = 5
    HANDLERS_CLEANERS = 6
    MACHINE_OP_INSPCT = 7
    ADM_CLERICAL = 8
    FARMING_FISHING = 9
    TRANSPORT_MOVING = 10
    PRIV_HOUSE_SERV = 11
    PROTECTIVE_SERV = 12
    ARMED_FORCES = 13

class RELATIONSHIP(Enum):
    WIFE = 0
    OWN_CHILD = 1
    HUSBAND = 2
    NOT_IN_FAMILY = 3
    OTHER_RELATIVE = 4
    UNMARRIED = 5

class RACE(Enum):
    WHITE = 0
    ASIAN_PAC_ISLANDER = 1
    AMER_INDIAN_ESKIMO = 2
    OTHER = 3
    BLACK = 4

class SEX(Enum):
    FEMALE = 0
    MALE = 1

class NATIVE_COUNTRY(Enum):
    UNITED_STATES = 0
    CAMBODIA = 1
    ENGLAND = 2
    PUERTO_RICO = 3
    CANADA = 4
    GERMANY = 5
    OUTLYING_US = 6
    INDIA = 7
    JAPAN = 8
    GREECE = 9
    SOUTH = 10
    CHINA = 11
    CUBA = 12
    IRAN = 13
    HONDURAS = 14
    PHILIPPINES = 15
    ITALY = 16
    POLAND = 17
    JAMAICA = 18
    VIETNAM = 19
    MEXICO = 20
    PORTUGAL = 21
    IRELAND = 22
    FRANCE = 23
    DOMINICAN_REPUBLIC = 24
    LOAS = 25
    ECUADOR = 26
    TAIWAN = 27
    HAITI = 28
    COLOMBIA = 29
    HUNGARY = 30
    GUATEMALA = 31
    NICARAGUE = 32
    SCOTLAND = 33
    THAILAND = 34
    YUGOSLAVIA = 35
    EL_SALVADOR = 36
    TRINIDAD_TOBAGO = 37
    PERU = 38
    HONG = 39
    HOLAND_NETHERLANDS = 40

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

def sourceTexttoEnum(category, name):
	if (category == 'WORKCLASS'):
		return WORKCLASS(workclassText.index(name))
	elif (category == 'EDUCATION'):
		return EDUCATION(educationText.index(name))
	elif (category == 'MARITAL_STATUS'):
		return MARITAL_STATUS(maritalText.index(name))
	elif (category == 'OCCUPATION'):
		return OCCUPATION(occupationText.index(name))
	elif (category == 'RELATIONSHIP'):
		return RELATIONSHIP(relationshipText.index(name))
	elif (category == 'RACE'):
		return RACE(raceText.index(name))
	elif (category == 'SEX'):
		return SEX(sexText.index(name))
	elif (category == 'NATIVE_COUNTRY'):
		return NATIVE_COUNTRY(nativeCountryText.index(name))
		

# Turns out we have a global variable for this, oops
'''
def maxEnumValue(category):
	if (category == 'WORKCLASS'):
		return len(workclassText) - 1
	elif (category == 'EDUCATION'):
		return len(educationText) - 1
	elif (category == 'MARITAL_STATUS'):
		return len(maritalText) - 1
	elif (category == 'OCCUPATION'):
		returnlen(occupationText) - 1
	elif (category == 'RELATIONSHIP'):
		return len(relationshipText) - 1
	elif (category == 'RACE'):
		return len(raceText) - 1
	elif (category == 'SEX'):
		return len(sexText) - 1
	elif (category == 'NATIVE_COUNTRY'):
		return len(nativeCountryText) - 1
'''