import wiringpi as wiringpi
import re
import math

def air_tank():
    atmospheric_pressure = 14000000
    pressure_increment = 3000000

    setup = wiringpi.wiringPiSetupGpio()
    if (setup == -1):
        print("setup failed... for wiringpi")
        exit(-1)
    #wiringpi.pinMode(18, 0) # sets GPIO 1 ...urrr... 18 ... to input 
    #wiringpi.pinMode(2, 0) # sets GPIO 2 to input 
    #wiringpi.pinMode(3, 0) # sets GPIO 3 to input

    # Read the states of the relays
    relay1 = wiringpi.digitalRead(2)
    relay2 = wiringpi.digitalRead(3)
    relay3 = wiringpi.digitalRead(4)
#    print ("airtank: s1=", relay1, " s2=", relay2, " s3=", relay3)

    # Get the current pressure values (stored in files for now)
    reservoir_pressure = int(tank_read(filename="./app/input_files/Reservoir_Value.txt"))
    cuff_pressure = int(tank_read(filename="./app/input_files/Cuff_Value.txt"))

    all_cases_handled=False

    if (relay1 == 1 and relay3==0):
    # the vent is open and the air tank relay is closed
        reservoir_pressure = atmospheric_pressure 
        all_cases_handled=True
    
    if (relay1==0 and relay3==1 and relay2==1):
    # the valve to the air tank is open,
    # the vent relay is closed
    # and the connection to the cuff is closed,
    # so set reservoir pressure to cuff pressure plus a bit 
        reservoir_pressure = cuff_pressure + pressure_increment 
        all_cases_handled=True

    if (relay1==0 and relay2==0):
    # the valve to the air tank is open,
    # the vent relay is closed or open (might not vent fast enough, anyway)
    # but the connection to the cuff is open,
    # so flag this as an error and exit
        print ("The air tank is directly connected to the cuff!!!")
        exit(0) 

    if (relay1==1 and relay3==1 and relay2==0 ):
    # the reservoir is connected to the cuff
    # and the vent relay is closed and the airtank relay is closed
    # so make the cuff pressure the weighted sum of the two
        new_value = (10*cuff_pressure + reservoir_pressure)/11
        cuff_pressure = new_value 
        reservoir_pressure = new_value 
        all_cases_handled=True

    if ( relay1==1 and relay3==0 and relay2==0 ):
    # the reservoir is connected to the cuff
    # and the vent relay is open and the airtank relay is closed 
    # so make cuff and reservoir pressure equal to atsmospheric 
        cuff_pressure = atmospheric_pressure 
        reservoir_pressure = atmospheric_pressure 
        all_cases_handled=True

    if ( relay1==1 and relay3==1 and relay2==1 ):
    # Idle case where all relays are closed
        all_cases_handled=True
    
    if (all_cases_handled == False):
        print ("Didn't handle a relay case s1=", relay1, " s2=", relay2, "s3=", relay3)
        exit(0) 

    #print ("res=", reservoir_pressure, " cuff=", cuff_pressure)

    tank_code = tank_write(filename="./app/input_files/Reservoir_Value.txt", value=str(reservoir_pressure))
    cuff_code = tank_write(filename="./app/input_files/Cuff_Value.txt", value=str(cuff_pressure))
    final_code = tank_write(filename="./app/input_files/Test_Value.txt", value=str(cuff_pressure))

def tank_read(filename):
    # read the lookup file values
    f = open(filename, 'r')
    pressure = 0
    lines = f.readlines()
    for line in lines:
        line = re.sub(r'\s*([\S*|\.]*)\s*', r'\1', line, flags=re.UNICODE)
        if (line != ""):
            pressure = float(line)
            pressure = math.ceil(pressure) 
        #print ("quick read of a value of:", pressure)
    f.close()
    #print ("Read file ", filename, " and obtained a value of", pressure)
    return(pressure)

def tank_write(filename, value):
    f = open(filename, 'w')
    operation = f.write(value)
    f.close()
    return (operation)
