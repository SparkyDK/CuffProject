from app.filereaders.A_to_D_lookup_table import A_to_D_lookup
from app.System.A_to_D.ADC_sampling import ADC_sampling

# Allows interpolation between empirically-determined pressure transducer values and mm_Hg values
from scipy import interpolate
import math

def Read_Cuff_Pressure(adc, control_args, past_states):
    mycontrol_args = control_args

    # Do the A/D conversion on the voltage from the pressure transducer using the ADC sampling board and
    # then read the converted value (which will be a proportional digital value to the actual voltage)
    # digital_pressure_value = polled value or handled interrupt value after sensing and A/D conversion
    # It may also be necessary to average/filter the value, depending on its stability/performance ... TBD

    # Set up the real sampled digital_pressure_value
    # Maybe put this in a non-blocking thread, depending on time required for conversion
    a_to_d = ADC_sampling(adc)

    digital_pressure_value = float(a_to_d.get_current_pressure(adc))
    mycontrol_args['PRESSURE'] = Convert_to_mm_Hg(digital_value=digital_pressure_value)
    #print ("pressure_sampling.py: Pressure in control args set to", mycontrol_args['PRESSURE'])
    return (mycontrol_args, digital_pressure_value, a_to_d.average_pressure)

def Convert_to_mm_Hg(digital_value):
    digital_input = digital_value
    #print ("Converting a value =", digital_input)
    # Convert to mm of Hg and return the value using an interpolated table of values, determined empirically
    # Assume that we have a 24-bit A/D, which results in values in a range of [0, 16777216]
    digital_values, mmHg_values = A_to_D_lookup().read(filename="./app/input_files/A_to_D_lookup_table.txt")

    length = len(digital_values)
    for i in range(0, length):
        # convert to integers
        digital_values[i] = float(digital_values[i])
        mmHg_values[i] = float(mmHg_values[i])

    interpolation_function = interpolate.interp1d(digital_values, mmHg_values)
    #print ("interpolation function:", interpolation_function)

    # print ("Starting lookup table values are:", digital_values, mmHg_values)
    interpolated_value = math.floor(interpolation_function(float(digital_input)))
    #interpolated_value = 740
    #print ("Took in ", digital_input, " and interpolated it to mm Hg value of", interpolated_value)

    #calculated_value = 0.00012159*digital_value + 687.19
    #print ("********** Interpolated value: ", interpolated_value, "calculated value: ", calculated_value)

    return (interpolated_value)