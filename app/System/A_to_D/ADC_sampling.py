#from app.System.A_to_D.pyads1256 import ADS1256

from app.GUI import g
# from app.constants.CONSTANTS import DEBUG
from app.filereaders.quick_read_test import quick_read

import numpy as np
# import itertools
from app.System.A_to_D.ADS1256_definitions import *
from app.System.A_to_D.PiPyADC import ADS1256
import app.System.A_to_D.ADS1256_default_config as myconfig

#  STEP 0: CONFIGURE CHANNELS AND USE DEFAULT OPTIONS FROM CONFIG FILE:
# For channel code values (bitmask) definitions, see ADS1256_definitions.py.
# The values representing the negative and positive input pins connected to
# the ADS1256 hardware multiplexer must be bitwise OR-ed to form eight-bit
# values, which will later be sent to the ADS1256 MUX register. The register
# can be explicitly read and set via ADS1256.mux property, which is probably
# what we want.  For now, we define a list of differential channels to be input to
# the ADS1256.read_sequence() method which reads all of them one after another.
#
# Single-ended measurement can use AINCOM as the negative input.
# AINCOM does not have to be connected to AGND (0V), but we assume the jumper
# on the Waveshare board is set, so it will be.

# Input pin from the pressure transducer (jumper should *not* be installed between AD0 and ADJ)
# Otherwise potentiometer will be connected to AD0... "potentially" damaging pressure transducer :-)
PRESSURE = POS_AIN0 | NEG_AINCOM
PRESSURE_INVERTED = POS_AINCOM | NEG_AIN0
# Light dependant resistor from the Waveshare high-precision A/D board (if jumper installed between AD1 and LDR):
LDR = POS_AIN1 | NEG_AINCOM
# The other external input screw terminals of the Waveshare board:
EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM

# PRESSURE = POS_AIN0 | NEG_AINCOM

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
#CH_SEQUENCE = (POTI, LDR, EXT2, EXT3, EXT4, EXT7, POTI_INVERTED, SHORT_CIRCUIT)
CH_SEQUENCE = (PRESSURE, LDR, EXT2, EXT3, EXT4, EXT5, EXT6, PRESSURE_INVERTED)

# We only have one input, but we will use the sequential read anyway!
# CH_SEQUENCE = (PRESSURE)

#  CALIBRATION  CONSTANTS
# The ADS1256 has internal gain and offset calibration registers, but these are
# applied to all channels without making any difference.
# For individual calibration values, e.g. to compensate external
# circuitry parasitics, we can compensate in software.
# The following values are dummy ones for now.
CH_OFFSET = np.array((0, 0, -85, 10, 750, 0, 0, 0), dtype=np.int)
GAIN_CAL = np.array((1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), dtype=np.float)

#Even though we only have one input, we still use an array construct
#CH_OFFSET = np.array( (0), dtype=np.int)
#GAIN_CAL = np.array( (1.0), dtype=np.float)

# We will use a simple moving average of 32 samples, as a simple de-noising filter
# This will represent about 16ms of samples (at 2kHz sampling rate)
# We can reduce this number, later, if there isn't much noise
FILTER_SIZE = 32

class ADC_sampling:
    def get_current_pressure(self):
        print ("ADC_sampling 1")

        # Using code taken from: https://github.com/SeanDHeath/PyADS1256
        # ads = ADS1256()

        # Using code taken from: https://github.com/ul-gh/PiPyADC/blob/master/pipyadc.py
        ads2 = ADS1256(myconfig)

        print ("ADC_sampling 1.1")
        # Change the default sample rate of the ADS1256 to 2000 samples per second
        # Correct value will depend on how long the conversion process takes and the frequency
        # content that we expect, vis a vis aliasing noise... We assume pressure values will be stable
        # (i.e. have no frequency content higher than 1kHz... period of 1ms in the time domain ....)
        # Relay settling times are specified at about 20ms and code is configured with this latency.
        # Not sure about the penalty for doing this (power, noise, ...?) but this value
        # can be increased up to 30,000 (pick DRATE_30000).  This is fine, according
        # to the TI data sheet for the ADS1256 (http://www.ti.com/product/ADS1256)
        data_rate = ads2.drate = DRATE_2000
        #print ("Data rate now set to:", data_rate)
        print ("ADC_sampling 1.2")
        # Gain and offset self-calibration:
        ads2.cal_self()
        print ("ADC_sampling 1.2")
        # Get ADC chip ID and check if chip is connected correctly.
        chip_ID = ads2.chip_ID
        print ("ADC_sampling 1.3")
        print("\nADC reported a numeric ID value of: {}.".format(chip_ID))
        if chip_ID != 0:
            # When the value is not correct, user code should exit here.
            print("\nRead incorrect chip ID for ADS1256 (assuming should be 0). Is the hardware connected properly?")
            exit(0)
        else:
            print ("Worked!  Let's go on and add/execute the rest of the A/D code...")
            exit(0) # For now, remove this later....

        # Channel gain must be multiplied by LSB weight in volts per digit to
        # display each channels input voltage. The result is a np.array again here:
        CH_GAIN = ads2.v_per_digit * GAIN_CAL

        # Numpy 2D array as buffer for raw input samples. Each row is one complete
        # sequence of samples for eight input channel pin pairs. Each column stores
        # the number of FILTER_SIZE samples for each channel.
        rows, columns = FILTER_SIZE, len(CH_SEQUENCE)
        filter_buffer = np.zeros((rows, columns), dtype=np.int)

        # Fill the buffer first once before displaying continuously updated results
        print("Channels configured: {}\n"
              "Initializing filter (this can take a while)...".format(
            len(CH_SEQUENCE)))
        for row_number, data_row in enumerate(filter_buffer):
            # Do the data acquisition of the multiplexed input channels.
            # The ADS1256 read_sequence() method automatically fills into
            # the buffer specified as the second argument:
            ads2.read_sequence(CH_SEQUENCE, data_row)

        # Calculate moving average of all (axis defines the starting point) input samples, subtracting the offset
        print ("ADC_sampling 1.4")
        ch_unscaled = np.average(filter_buffer, axis=0) - CH_OFFSET
        ch_volts = ch_unscaled * CH_GAIN

        #g.digital_pressure_value = ch_unscaled
        #print ("Global_cnt:", g.Global_cnt, "digital_pressure_value now", g.digital_pressure_value)

        print ("raw values:", filter_buffer)
        print ("averaged values=", ch_unscaled, " and equivalent voltage=", ch_volts)

        # # Next, update filter_buffer cyclically with new ADC samples and
        # # calculate the averaged results.
        # print("\n\nOutput values averaged over {} ADC samples:".format(FILTER_SIZE))
        # # The following is an endless loop!
        # timestamp = time.time()  # Limit output data rate to fixed time interval
        # for data_row in itertools.cycle(filter_buffer):
        #     # Do the data acquisition of eight multiplexed input channels
        #     # The result channel values are directly read into the array specified
        #     # as the second argument, which must be of a mutable type.
        #     ads2.read_sequence(CH_SEQUENCE, data_row)
        #
        #     elapsed = time.time() - timestamp
        #     if elapsed > 1:
        #         timestamp += 1
        #
        #         # Calculate moving average of input samples, subtract offset
        #         ch_unscaled = np.average(filter_buffer, axis=0) - CH_OFFSET
        #         ch_volts = ch_unscaled * CH_GAIN
        #
        #         nice_output([int(i) for i in ch_unscaled], ch_volts)

        print("ADC_sampling 2")
        # if (DEBUG == True):
        #     pass
        #     # Do a test read of the A/D ID register
        #     print("A/D ID now being read")
        #     myid = ads.ReadID()
        #     print("A/D ID is:", myid)

        # g.digital_pressure_value = ads.ReadADC()
        # temp = ads.ReadADC()
        # print ("Pressure value read at:", localtime, " =", temp)
        # print ("Pressure value read at:", localtime, " =", g.digital_pressure_value)

        g.digital_pressure_value = quick_read().read(filename="./app/input_files/Test_Value.txt")
        # print ("Global_cnt:", g.Global_cnt, "digital_pressure_value now", g.digital_pressure_value)
        return (g.digital_pressure_value)