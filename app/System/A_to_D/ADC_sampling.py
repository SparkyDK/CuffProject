# from app.System.A_to_D.pyads1256 import ADS1256

from app.GUI import g
from app.constants.CONSTANTS import DEBUG
from app.filereaders.quick_read_test import quick_read

class ADC_sampling:
    def get_current_pressure(self):
        # Using code taken from: https://github.com/SeanDHeath/PyADS1256
        #ads = ADS1256()
        if (DEBUG == True):
            pass
            # Do a test read of the A/D ID register
            #myid = ads.ReadID()
            #print("A/D ID:", myid)

        #g.digital_pressure_value = ads.ReadADC()
        #print ("Pressure value read at:", localtime, " =", g.digital_pressure_value)

        g.digital_pressure_value = quick_read().read(filename="./app/input_files/Test_Value.txt")
        #g.digital_pressure_value = g.digital_pressure_value - 100000
        #digital_pressure_value = g.digital_pressure_value
        #print ("Global_cnt:", g.Global_cnt, "digital_pressure_value now", g.digital_pressure_value)
        return (g.digital_pressure_value)

