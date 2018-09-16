from app.filereaders.A_to_D_lookup_table import A_to_D_lookup

# Allows interpolation between empirically-determined pressure transducer values and mm_Hg values
from scipy import interpolate


def Read_Cuff_Pressure(control_args, past_states):
    mycontrol_args = control_args

    # Do the A/D conversion and read the converted value
    pass  # Add the A/D read instruction here to set up the real sampled digital_pressure_value
    # digital_pressure_value = polled value or handled interrupt value after sensing and A/D conversion
    # It may also be necessary to average/filter the value, depending on its stability/performance ... TBD
    #digital_pressure_value = 16000000  # debug only!
    mycontrol_args['PRESSURE'] = Convert_to_mm_Hg(digital_value=digital_pressure_value)
    mycontrol_args['PRESSURE'] = pressure_value

    # test_value = 16000000
    # interpolated_value = Convert_to_mm_Hg(digital_value=test_value)

    return (mycontrol_args)


def Convert_to_mm_Hg(digital_value):
    digital_input = digital_value
    # Convert to mm of Hg and return the value using an interpolated table of values, determined empirically
    # Assume that we have a 24-bit A/D, which results in values in a range of [0, 16777216]
    digital_values, mmHg_values = A_to_D_lookup().read(filename="./app/input_files/A_to_D_lookup_table.txt")

    length = len(digital_values)
    for i in range(0, length):
        # convert to integers
        digital_values[i] = int(digital_values[i])
        mmHg_values[i] = int(mmHg_values[i])

    interpolation_function = interpolate.interp1d(digital_values, mmHg_values)

    # print ("Starting lookup table values are:", digital_values, mmHg_values)
    interpolated_value = math.floor(interpolation_function(digital_input))
    # print ("Took in ", digital_input, " and interpolated it to a corresponding mm Hg value of", interpolated_value)

    return (interpolated_value)
