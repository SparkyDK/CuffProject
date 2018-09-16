from app.System.pain_schedule.pain_schedule import past_states

def stub_pressure_adjustment(past_states)
    pressure_value = 0.0
    if (mypast_states[4] == "CONNECT_CUFF" and mypast_states[3] == "LOAD_RESERVOIR"):
        # Controlled pressure increase
        pressure_value = int(mycontrol_args['PRESSURE']) + 25
    elif (mypast_states[4] == "RELEASE" and mypast_states[3] == "CONNECT_CUFF"):
        # Controlled pressure release path
        pressure_value = int(mycontrol_args['PRESSURE']) - 10
    elif (mypast_states[4] == "RELEASE" and mypast_states[3] == "LOAD_RESERVOIR"):
        # Controlled pressure release path (in case of leaks)
        pressure_value = int(mycontrol_args['PRESSURE']) - 10
    elif (mypast_states[4] == "VENT"):
        # Venting case
        pressure_value = int(control_args['PATM'])
    else:
        # Don't change the pressure value at all
        pressure_value = mycontrol_args['PRESSURE']
    return(pressure_value)


class test_pressure_reading(self, past_states)
    self mypast_states = past_states

    stub_pressure_adjustment(past_states)




