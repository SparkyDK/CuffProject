class pain_schedule:
    def update(self, current_counter, control_args, user_args):
        # Update PAIN, STARTED, SCHEDULE_INDEX, PAUSE fields of the control arguments and the current_counter values
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0}
        # control_args = {'SCHEDULE_INDEX': 0, 'PAIN': 0, 'STARTED': 0, 'PAUSE': 0, 'FORCE': 0,
        #                'PAINH': painh, 'PAINL': painl,
        #               'PATM': pressure_parameters['PATM'], 'PMAX': pressure_parameters['PMAX']}

        force = user_args['OVERRIDE']
        schedule_index = control_args['SCHEDULE_INDEX']
        count = current_counter[schedule_index]

        return (control_args)
