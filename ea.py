N_GENOME_CTS_ATTRIBUTES = 12
LEARNING_RATE = 1/sqrt(N_GENOME_CTS_ATTRIBUTES)
DONT_CARE_VALUE = -1

class WORKCLASS(Enum):
    DONT_CARE = -1
    PRIVATE = 0
    SELF_EMP_NOT_INC = 1
    SELF_EMP_INC = 2
    FEDERAL_GOV = 3
    LOCAL_GOV = 4
    STATE_GOV = 5
    WITHOUT_PAY = 6
    NEVER_WORKED = 7

class EDUCATION(Enum):
    DONT_CARE = -1
    BACHELORS = 0
    SOME_COLLEGE = 1
    11TH = 2
    HS_GRAD = 3
    PROF_SCHOOL = 4
    ASSOC_ACDM = 5
    ASSOC_VOC = 6
    9TH = 7
    7TH_8TH = 8
    12TH = 9
    MASTERS = 10
    1ST_4TH = 11
    10TH = 12
    DOCTORATE = 13
    5TH_6TH = 14
    PRESCHOOL = 15

class MARITAL_STATUS(Enum):
    DONT_CARE = -1
    MARRIED_CIV_SPOUSE = 0
    DIVORCED = 1
    NEVER_MARRIED = 2
    SEPARATED = 3
    WIDOWED = 4
    MARRIED_SPOUSE_ABSENT = 5
    MARRIED_AF_SPOUSE = 6

class OCCUPATION(Enum):
    DONT_CARE = -1
    TECH_SUPPORT = 0
    CRAFT_REPAIR = 1
    OTHER_SERVICE = 3
    SALES = 4
    EXEC_MANAGERIAL = 5
    PROF_SPECIALTY = 6
    HANDLERS_CLEANERS = 7
    MACHINE_OP_INSPCT = 8
    ADM_CLERICAL = 9
    FARMING_FISHING = 10
    TRANSPORT_MOVING = 11
    PRIV_HOUSE_SERV = 12
    PROTECTIVE_SERV = 13
    ARMED_FORCES = 14

class RELATIONSHIP(Enum):
    DONT_CARE = -1
    WIFE = 0
    OWN_CHILD = 1
    HUSBAND = 2
    NOT_IN_FAMILY = 3
    OTHER_RELATIVE = 4
    UNMARRIED = 5

class RACE(Enum):
    DONT_CARE = -1
    WHITE = 0
    ASIAN_PAC_ISLANDER = 1
    AMER_INDIAN_ESKIMO = 2
    OTHER = 3
    BLACK = 4

class SEX(Enum):
    DONT_CARE = -1
    FEMALE = 0
    MALE = 1

class NATIVE_COUNTRY(Enum):
    DONT_CARE = -1
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

class Rule(object):
    def __init__(self, minage, maxage):
        self.minage = minage
        self.sigmaminage = sigmaminage
        self.maxage = maxage
        self.sigmamaxage
        self.workclass
        self.minfnlwgt
        self.sigmaminfnlwgt
        self.maxfnlwgt
        self.sigmamaxfnlwgt
        self.education
        self.mineducationnum
        self.sigmamineducationnum
        self.maxeducationnum
        self.sigmamaxeducationnum
        self.maritalstatus
        sef.occupation
        self.relationship
        self.race
        sef.sex
        self.mincapitalgain
        self.sigmamincapitalgain
        self.maxcapitalgain
        self.sigmamaxcapitalgain
        self.mincapitalloss
        self.sigmamincapitalloss
        self.maxcapitalloss
        self.sigmamaxcapitalloss
        self.minhoursperweek
        self.sigmaminhoursperweek
        self.maxhoursperweek
        self.sigmamaxhoursperweek
        self.nativecountry
        self.classification


    
