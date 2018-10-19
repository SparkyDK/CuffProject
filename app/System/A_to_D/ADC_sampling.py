#from app.System.A_to_D.pyads1256 import ADS1256

from app.GUI import g
# from app.constants.CONSTANTS import DEBUG
from app.filereaders.quick_read_test import quick_read

import numpy as np
# import itertools
from app.System.A_to_D.ADS1256_definitions import *

import time

from app.System.A_to_D.PiPyADC import ADS1256
import app.System.A_to_D.ADS1256_default_config as myconfig

CH_OFFSET = np.array((0), dtype=np.int)
GAIN_CAL = np.array((1.0), dtype=np.float)
print("CH_offset:", CH_OFFSET, "and GAIN_CAL:", GAIN_CAL)
# Input pin from the pressure transducer (jumper should *not* be installed between AD0 and ADJ)
# Otherwise potentiometer will be connected to AD0... "potentially" damaging pressure transducer :-)
PRESSURE = POS_AIN0 | NEG_AINCOM
# PRESSURE_INVERTED = POS_AINCOM | NEG_AIN0
# # Light dependant resistor from the Waveshare high-precision A/D board (if jumper installed between AD1 and LDR):
# LDR = POS_AIN1 | NEG_AINCOM
# # The other external input screw terminals of the Waveshare board:
# EXT2, EXT3, EXT4 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM, POS_AIN4 | NEG_AINCOM
# EXT5, EXT6, EXT7 = POS_AIN5 | NEG_AINCOM, POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
# CH_SEQUENCE = (POTI, LDR, EXT2, EXT3, EXT4, EXT7, POTI_INVERTED, SHORT_CIRCUIT)
CH_SEQUENCE = (PRESSURE,)
print("Ch_sequence:", CH_SEQUENCE)
FILTER_SIZE = 32

class ADC_sampling:

    def __init__(self, adc):
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


        # We only have one input, but we will use the sequential read anyway!
        # CH_SEQUENCE = (PRESSURE)

        #  CALIBRATION  CONSTANTS
        # The ADS1256 has internal gain and offset calibration registers, but these are
        # applied to all channels without making any difference.
        # For individual calibration values, e.g. to compensate external
        # circuitry parasitics, we can compensate in software.

        # Even though we only have one input, we still use an array construct

        # We will use a simple moving average of 32 samples, as a simple de-noising filter
        # This will represent about 16ms of samples (at 2kHz sampling rate)
        # We can reduce this number, later, if there isn't much noise

        # Change the default sample rate of the ADS1256 to 2000 samples per second
        # Correct value will depend on how long the conversion process takes and the frequency
        # content that we expect, vis a vis aliasing noise... We assume pressure values will be stable
        # (i.e. have no frequency content higher than 1kHz... period of 1ms in the time domain ....)
        # Relay settling times are specified at about 20ms and code is configured with this latency.
        # Not sure about the penalty for doing this (power, noise, ...?) but this value
        # can be increased up to 30,000 (pick DRATE_30000).  This is fine, according
        # to the TI data sheet for the ADS1256 (http://www.ti.com/product/ADS1256)
        adc.drate = DRATE_2000
        # Gain and offset self-calibration:
        adc.cal_self()
        # Get ADC chip ID and check if chip is connected correctly.
        chip_ID = adc.chip_ID
        #print("\nADC reported a numeric ID value of: {}.".format(chip_ID))
        #print("\nRead chip ID of ", chip_ID," for ADS1256")
        #if (chip_ID != 3):
        #   print ("\nchip_ID not the expected one)
        #   g.adc.pi.spi_close(g.adc.spi_id)
        #   exit(0)

    def get_current_pressure(self, adc):

        ads2 = adc
        # Channel gain must be multiplied by LSB weight in volts per digit to
        # display each channels input voltage. The result is a np.array again here:
        CH_GAIN = ads2.v_per_digit * GAIN_CAL

        # Numpy 2D array as buffer for raw input samples. Each row is one complete
        # sequence of samples for eight input channel pin pairs. Each column stores
        # the number of FILTER_SIZE samples for each channel.
        rows, columns = FILTER_SIZE, len(CH_SEQUENCE)
        filter_buffer = np.zeros((rows, columns), dtype=np.int)
        #print ("rows=", rows, " and columns=", columns)

        # Using code taken from: https://github.com/SeanDHeath/PyADS1256
        # ads = ADS1256()

        # Argument1:  Tuple (list) of 8-bit code values for differential
        #             input channel pins to read sequentially in a cycle.
        #             (See definitions for the REG_MUX register)
        #
        #             Example:
        #             ch_sequence=(POS_AIN0|NEG_AIN1, POS_AIN2|NEG_AINCOM)
        #
        # Argument2:  List (array, buffer) of signed integer conversion
        #             results for the sequence of input channels.
        #
        # Returns:    List (array, buffer) of signed integer conversion
        #             results for the sequence of input channels.

        # Using code taken from: https://github.com/ul-gh/PiPyADC/blob/master/pipyadc.py
        # Fill the buffer first once before displaying continuously updated results

        #one_pressure_sample = ads2.read_oneshot(PRESSURE)

        #if (one_pressure_sample != 0):
        #    print ("Read a single pressure value =", one_pressure_sample)

        for row_number, data_row in enumerate(filter_buffer):
            # Do the data acquisition of the multiplexed input channels.
            # The ADS1256 read_sequence() method automatically fills into
            # the buffer specified as the second argument:
            ads2.read_sequence(CH_SEQUENCE, data_row)
            #print ("Reading filter buffer row=", data_row, " and row_number=", row_number)

        # Calculate moving average of all (axis defines the starting point) input samples, subtracting the offset
        ch_unscaled = np.average(filter_buffer, axis=0) - CH_OFFSET
        ch_volts = ch_unscaled * CH_GAIN
        #print ("\nFilter buffer:\n", filter_buffer)
        print ("average value=",ch_unscaled)

        #g.digital_pressure_value = ch_unscaled
        #print ("Global_cnt:", g.Global_cnt, "digital_pressure_value now", g.digital_pressure_value)

        #print ("raw values:", filter_buffer)
        #print ("averaged values=", ch_unscaled, " and equivalent voltage=", ch_volts)

        # g.digital_pressure_value = ads.ReadADC()
        # temp = ads.ReadADC()
        # print ("Pressure value read at:", localtime, " =", temp)
        # print ("Pressure value read at:", localtime, " =", g.digital_pressure_value)

        g.digital_pressure_value = quick_read().read(filename="./app/input_files/Test_Value.txt")
        #print ("digital_pressure_value read from file is now", g.digital_pressure_value, "sample ave.=",ch_unscaled)
        return (g.digital_pressure_value)