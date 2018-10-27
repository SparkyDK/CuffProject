# Files
PRESSURE_READER_FILE_NAME = 'TEST_Pressure_Values.txt'
PRESSURE_TYPES = ["PMAX", "PAINVALUE", "PAINTOLERANCE", "PATM"]
SCHEDULE_TYPES = ["PAIN", "NILL"]

# Atmospheric ressure tolerance
#ATM_TOLERANCE = 10
ATM_TOLERANCE_HIGH = 10
ATM_TOLERANCE_LOW = 5

# Debug
DEBUG = True
HISTORY_LENGTH = 5
airtank_stub = False

# Parameters
MAX_NUM_PHASES = 8
MAX_NUM_SCHEDULES = 4
MAX_NUM_PARAMETERS = 4

refresh_period = 0.1
relay_settling_time = 0.04
pressure_settling_time = 0.3
venting_timeout = 15
cuff_charging_time = 0.005

transparency_level = 0.35
