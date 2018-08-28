class pain_schedule:
    def update(self, current_counter, control_args, user_args):
        # Update PAIN, STARTED, SCHEDULE_INDEX, PAUSE fields of the control arguments and the current_counter values

        actions = PressureReader().read("./tests/test_files/TEST_Pressure_Values.txt")
        self.assertEqual({'PAINH': '920', 'PAINL': '900', 'PATM': '750', 'PMAX': '970'}, actions)
        return (control_args)
