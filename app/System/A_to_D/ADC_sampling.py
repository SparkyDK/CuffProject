# from app.System.A_to_D.pyads1256 import ADS1256

# import sys
# from ADS1256_definitions import *
# from pipyadc import ADS1256


# Code from: https://github.com/ul-gh/PiPyADC/blob/master/example.py
# Set up the A/D
#ads = ADS1256()
### STEP 2: Gain and offset self-calibration:
#ads.cal_self()

# Using code taken from: https://github.com/SeanDHeath/PyADS1256
#ads = ADS1256()
# Do a test read of the A/D ID register
#myid = ads.ReadID()
#if (DEBUG == True):
#    print("A/D ID:", myid)

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
# CH_SEQUENCE = (POTI, LDR, EXT2, EXT3, EXT4, EXT7, POTI_INVERTED, SHORT_CIRCUIT)
# CH_SEQUENCE = (EXT2)


# Use the code example in: https://github.com/ul-gh/PiPyADC/blob/master/example.py
### STEP 3: Get data:
# raw_channels = ads.read_sequence(CH_SEQUENCE)
# voltages = [i * ads.v_per_digit for i in raw_channels]
# print raw_channels, voltages

# pressure_value = ads.ReadADC()
# print ("Pressure value read at:", localtime, " =", pressure_value)

from app.GUI import g
from app.constants.CONSTANTS import DEBUG
from app.filereaders.quick_read_test import quick_read

class ADC_sampling:
    pass

    def get_current_pressure(self):
        pass
        if (DEBUG == False):
            pass
            digital_pressure_value = 0
            # digital_pressure_value = read_the_value_from_ADC_conversion
        else:
            # 160000000
            g.digital_pressure_value = quick_read().read(filename="./app/input_files/Test_Value.txt")
            g.digital_pressure_value = g.digital_pressure_value - 100000
            digital_pressure_value = g.digital_pressure_value
            #print ("Global_cnt:", g.Global_cnt, "digital_pressure_value now", digital_pressure_value)

        return (digital_pressure_value)

