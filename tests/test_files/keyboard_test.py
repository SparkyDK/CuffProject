from pynput import keyboard

def kbd_input(*args, **kwargs):
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

def on_press(key):
    try:
        pass
        #print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        pass
        #print('special key {0} pressed'.format(key))

def on_release(key):
    global keypress
    #print('{0} released'.format(key))
    keypress = format(key)
    #keypress = key
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def keyboard_user_input_simulation(past_states):
    self.mypast_states = past_states

    #def kbd_input(*args, **kwargs):
    #    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #        listener.join()

    print("*** <", old_keypress, ">a Elapsed: {0:.4f}".format(elapsed_time, ), "\tctrl:", control_args)
    if (DEBUG == True):
        # Simulate user touch screen input with a regular keyboard
        old_keypress, user_args, control_args, toggle = \
            keyboard_test(keypress, old_keypress, user_args, old_user_args, control_args,
                          pressure_parameters, toggle)

    # Read the current air pressure in the patient's cuff

    # DEBUG
    pressure_value = 0.0
    if (self.mypast_states[4] == "CONNECT_CUFF" and self.mypast_states[3] == "LOAD_RESERVOIR"):
    # Controlled pressure increase
        pressure_value = int(mycontrol_args['PRESSURE']) + 25
    elif (self.mypast_states[4] == "RELEASE" and self.mypast_states[3] == "CONNECT_CUFF"):
    # Controlled pressure release path
        pressure_value = int(mycontrol_args['PRESSURE']) - 10
    elif (self.mypast_states[4] == "RELEASE" and self.mypast_states[3] == "LOAD_RESERVOIR"):
    # Controlled pressure release path (in case of leaks)
        pressure_value = int(mycontrol_args['PRESSURE']) - 10
    elif (self.mypast_states[4] == "VENT"):
    # Venting case
        pressure_value = int(control_args['PATM'])
    else:
    # Don't change the pressure value at all
        pressure_value = mycontrol_args['PRESSURE']
    mycontrol_args['PRESSURE'] = pressure_value

    # test_value = 16000000
    # interpolated_value = Convert_to_mm_Hg(digital_value=test_value)

    return ( mycontrol_args )

def keyboard_test(keypress, old_keypress, user_args, old_user_args, control_args, pressure_parameters, toggle):
    # Use the keyboard to simulate user inputs from the touch screen

    if (keypress != old_keypress):
        old_keypress = keypress
        print("New key pressed: ", keypress)
    # user_args = {'GO': 0, 'STOP': 0, 'ABORT': 0, 'UP': 0, 'DOWN': 0,
    #             'override_pressure': pressure_parameters['PAINVALUE'], 'OVERRIDE': 0}

        if (keypress == "'x'"):
            print("'x' pressed")
            exit(0)
        elif (keypress == "'g'"):
            print("'g' pressed")
            if (user_args['GO'] == 1):
                user_args['GO'] = 0
            else:
                user_args['GO'] = 1
        elif (keypress == "'s'"):
            print("'s' pressed")
            if (user_args['STOP'] == 1):
                user_args['STOP'] = 0
            else:
                user_args['STOP'] = 1
        elif (keypress == "'a'"):
            print("'a' pressed")
            if (user_args['ABORT'] == 1):
                user_args['ABORT'] = 0
            else:
                user_args['ABORT'] = 1
        elif (keypress == "'u'"):
            print("'u' pressed")
            if (user_args['UP'] == 1):
                user_args['UP'] = 0
            else:
                user_args['UP'] = 1
        elif (keypress == "'d'"):
            print("'d' pressed")
            if (user_args['DOWN'] == 1):
                user_args['DOWN'] = 0
            else:
                user_args['DOWN'] = 1
        elif (keypress == "'r'"):
            control_args['PRESSURE'] += pressure_parameters['PAINTOLERANCE']
            print("'r' pressed to raise the pressure value to ", control_args['PRESSURE'])
        elif (keypress == "'l'"):
            control_args['PRESSURE'] -= pressure_parameters['PAINTOLERANCE']
            print("'l' pressed to lower the pressure value to ", control_args['PRESSURE'])
        elif (keypress == "'o'"):
            print("'o' pressed")
            user_args['override_pressure'] = 850
            if (user_args['OVERRIDE'] == 1):
                user_args['OVERRIDE'] = 0
            else:
                user_args['OVERRIDE'] = 1
        else:
            pass
        print("____________________________________________")
        print("Toggled something (old):", old_user_args)
        print("Toggled something (new):", user_args)
        print("____________________________________________")
        toggle += 1
        time.sleep(1)
    return(old_keypress, user_args, control_args, toggle)

    keypress = None
    old_keypress = None
    toggle = 0