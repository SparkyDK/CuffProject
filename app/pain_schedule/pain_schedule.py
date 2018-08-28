class pain_schedule:
    def __init__(self):
        pass
    def update(self, current_counter, control_args, user_args):
        self.current_counter = current_counter
        self.control_args = control_args
        self.user_args = user_args

        #print ("pain_Schedule:")
        #print (self.current_counter)
        #print (self.control_args)
        #print (self.user_args)

        # Update PAIN, STARTED, SCHEDULE_INDEX, PAUSE fields of the control arguments and the current_counter values
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0}
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
        #                'PAINH': painh, 'PAINL': painl,
        #               'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}

        force = self.user_args['OVERRIDE']
        schedule_index = self.control_args['SCHEDULE_INDEX']
        #print ("Schedule_index=", schedule_index)
        count = self.current_counter[schedule_index]

        return (self.control_args)
