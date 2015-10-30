import math
import random
import lcs_enums
from global_variables import *
import copy

N_GENOME_CTS_ATTRIBUTES = 12
LEARNING_RATE = 1.5/math.sqrt(N_GENOME_CTS_ATTRIBUTES)
EPSILON = 0.5

AGEMIN = 20
AGEMAX = 60
AGEDEV = 2

FNLMIN = 100000 
FNLMAX = 400000
FNLDEV = 20000

EDUMIN = 6
EDUMAX = 15
EDUDEV = 1

CAPITALMIN = 10000
CAPITALMAX = 24000
CAPITALDEV = 1000

HOURSMIN = 8
HOURSMAX = 40
HOURSDEV = 0.5

# Takes a child, in the form of a dictionary (conditions) and mutates it.
def getMutantChild(child):
	#iterate over the values in the dictionary
	
	for key, value in child.items():
		#mutate a continous value
		if (key in CTS_ATTRIBUTES):
			value[0] = max(int(value[0] + value[3] * random.normalvariate(0, 1)), 0)					# min bound
			value[1] = max(int(value[1] + value[3] * random.normalvariate(0, 1)), value[0])				# max bound
			value[2] = max(value[2] * math.exp(LEARNING_RATE * random.normalvariate(0, 1)), EPSILON)	# sigma min
			value[3] = max(value[3] * math.exp(LEARNING_RATE * random.normalvariate(0, 1)), EPSILON)	# sigma max
		else:
			'''
			
			I realised it's not very ideal to generate new options for one key...
			For example, if you had a classifier with race = 0, and one with race = [0, 1], the one with [0, 1] would
			have a higher accuracy because it accommodates more environments.
			
			'''
			'''
			#if not continuous, check probability and maybe add new entry		
			vl = 1 if isinstance(value, int) else len(value)
			if(random.random() < LEARNING_RATE/vl and vl < ENUM_ATTRIBUTES[key]):
				new_value = value
				if isinstance(value, int):
					new_value = [value]	# Turns it into a list if it's an integer
				newEntry = random.randint(0, ENUM_ATTRIBUTES[key])				
				while(newEntry in new_value): #make sure it's not a duplicate
					newEntry = random.randint(0, ENUM_ATTRIBUTES[key])
				
				new_value.append(newEntry)
				
				child[key] = new_value
				#if we didnt add one, maybe we should remove one
			elif(random.random() < LEARNING_RATE/vl and vl > 1):
				value.remove(value[random.randrange(vl)])
				child[key] = value
			'''
			'''
			So instead, I just modify one of the keys instead. This should make it explore more.
			
			'''			
			if(random.random() < LEARNING_RATE/len(child)):
				changedKey = ALL_ATTRIBUTES[random.randint(0, len(ALL_ATTRIBUTES) - 1)]
				while (changedKey in child):
					changedKey = ALL_ATTRIBUTES[random.randint(0, len(ALL_ATTRIBUTES) - 1)]
				if (changedKey in CTS_ATTRIBUTES):
					newValue = generateCtsInitial(changedKey)
				else:
					newValue = random.randint(0, ENUM_ATTRIBUTES[changedKey])
				child.pop(key, None)
				child[changedKey] = newValue
			
	if (random.random() < LEARNING_RATE/len(child) and len(child) < len(ALL_ATTRIBUTES)):
		newKey = ALL_ATTRIBUTES[random.randint(0, len(ALL_ATTRIBUTES) - 1)]
		while (newKey in child):
			newKey = ALL_ATTRIBUTES[random.randint(0, len(ALL_ATTRIBUTES) - 1)]
		if (newKey in CTS_ATTRIBUTES):
			newValue = generateCtsInitial(newKey)
		else:
			newValue = random.randint(0, ENUM_ATTRIBUTES[newKey])
		child[newKey] = newValue


	return child
	


def generateCtsInitial(key):
    minBound = 0
    maxBound = 0
    sigmamax = 0
    sigmamin = 0
    if (key == 'AGE'):
        sigmamax = AGEDEV
        sigmamin = AGEDEV
        minBound = random.normalvariate(AGEMIN, AGEDEV)
        maxBound = random.normalvariate(AGEMAX, AGEDEV)
    elif (key == 'FNLWGT'):
        sigmamax = FNLDEV
        sigmamin = FNLDEV
        minBound = random.normalvariate(FNLMIN, FNLDEV)
        maxBound = random.normalvariate(FNLMAX, FNLDEV)
    elif (key == 'EDUCATION_NUM'):
        sigmamax = EDUDEV
        sigmamin = EDUDEV
        minBound = random.normalvariate(EDUMIN, EDUDEV)
        maxBound = random.normalvariate(EDUMAX, EDUDEV)
    elif ((key == 'CAPITAL_GAIN') or (key == 'CAPITAL_LOSS')):
        sigmamax = CAPITALDEV
        sigmamin = CAPITALDEV
        minBound = random.normalvariate(CAPITALMIN, CAPITALDEV)
        maxBound = random.normalvariate(CAPITALMAX, CAPITALDEV)
    elif (key == 'HOURS_PER_WEEK'):
        sigmamax = HOURSDEV
        sigmamin = HOURSDEV
        minBound = random.normalvariate(HOURSMIN, HOURSDEV)
        maxBound = random.normalvariate(HOURSMAX, HOURSDEV)

    if (maxBound < minBound):
        temp = maxBound
        maxBound = minBound
        minBound = temp

    
        
        
    return [minBound, maxBound, sigmamin, sigmamax]
