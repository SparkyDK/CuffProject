class run_system(self):

    Global_cnt += 1
    # Keep a state history
    returned_state = airctrl.FSM.GetCurState()
    # pop out the highest-index entry from the state history
    past_states.popleft()
    # Add the newest state value to the lowest-index entry of the state history
    past_states.append(returned_state)

    localtime = time.asctime(time.localtime(time.time()))
    #print(localtime, " (elapsed=", elapsed_time)

    old_elapsed_time = elapsed_time
    elapsed_time = time.time() - start_time

    if math.floor(elapsed_time) != math.floor(old_elapsed_time):
        # Only process the pain schedule each time a second ticks to the next truncated value
        second_tickover = True
    else:
        second_tickover = False

    # Read pressure value from transducer and ADC here
    Read_Cuff_Pressure(control_args, past_states)

    print("*** <", old_keypress, ">a Elapsed: {0:.4f}".format(elapsed_time, ), "\tctrl:", control_args)

    if (DEBUG == True):
        # Simulate user touch screen input with a regular keyboard
        old_keypress, user_args, control_args, toggle = \
            keyboard_test(keypress, old_keypress, user_args, old_user_args, control_args,
                          pressure_parameters, toggle)

    # Read the current air pressure in the patient's cuff
    control_args = Read_Cuff_Pressure(control_args, past_states)

    # Poll for user input and update the GUI based on the control arguments
    # Then update the user signals: {'GO','STOP','ABORT','override_pressure','OVERRIDE'} appropriately
    old_user_args = user_args.copy()
    # user_args = gui.update(Global_cnt, current_counter, control_args, user_args)

    # Update or override the control signals: {'PAIN','STARTED','SCHEDULE_INDEX','PAUSE'}
    # Execute the asynchronous part of the state machine that implements the control decisions
    # with the newly-updated control signals and newly-sampled pressure value
    try:
        old_control_args = control_args.copy()
        control_args, current_counter, pressure_parameters, schedule_finished, toggle = \
            airctrl.FSM.ControlDecisions(current_counter, imported_schedule, control_args, old_user_args,
                                         user_args,
                                         pressure_parameters, second_tickover, schedule_finished, toggle)
        if (schedule_finished == True):
            # At the end of the pain schedule, hold the state machine in the vent state and turn off pain
            # Could send it back to IDLE, as an alternative, but what if there is some residual pressure
            # in the cuff at the end of the experiment...
            airctrl.FSM.SetState("VENT")
            control_args['PAIN'] = 0

        # Execute the state machine
        airctrl.FSM.Execute(control_args)

    except KeyboardInterrupt:
        print("\nDone")
