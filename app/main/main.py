from app.constants.CONSTANTS import MAX_NUM_SCHEDULES

DEBUG = True
Global_cnt = 0

# GUI limitations will determine this constant
Max_num_schedules = MAX_NUM_SCHEDULES

# pain schedule to be read (i.e. Pain or Nill)
pain_schedule = []
# Amount of time for each pain schedule entry
time_schedule = []

#default pressure values
Pmax = 0 #max pressure
Pup = 0 #upper pressure limit
Plow = 0 #lower pressure limit
Patm = 0 #atmospheric pressure
P = 0 #current pressure
Pnew = 0 #new pressure value)

# Only the following parameter labels are supported and these are defined in this dictionary
d = dict(PATM=0, PAINH=0, PAINL=0, PMAX=0)
Max_num_Parameters = len(d)