import State

class IDLE(State):
    def __init__(self, FSM):
        super(IDLE, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        #print "\n* IDLE * \twith args=",  self.args
        self.Pain = self.args['PAIN']
        self.Running = self.args['RUNNING']
        self.P = self.args['P']
        #while (P<Pup and P>Plow):
        #    print ("In Idle")
        if (self.Pain == 1):
            if (self.Running==1):
            # Running a schedule
                if (self.P<Plow):
                # Pressure not high enough
                   self.FSM.ToTransition("toLOAD_RESERVOIR")
            else:
            # This shouldn't happen (i.e. PAIN required but not in a schedule, so we should vent
                self.FSM.ToTransition("toVENT")
        else:
        # No pain required
            if (self.Running == 1):
            # No pain required in this schedule phase.  Save solenoid wear and tear when truly idle by checking against atmospheric pressure
                if (self.P > Patm ):
                # Continue to vent to keep P below Patm
                    self.FSM.ToTransition("toVENT")
            else:
            # Don't let the user adjust the pain threshold if running a schedule.
            # Stay in IDLE, unless a new entry is being entered by the user or if pressure creeps above atmospheric
                if (self.P > Patm):
                # Keep pressure at atmospheric pressure anyway, even if not running a schedule
                    self.FSM.ToTransition("toVENT")
                elif (Pnew == 1):
                # Allow user to update pain pressure threshold
                    self.FSM.ToTransition("toNEW_ENTRY")
                else:
                # Stay in IDLE
                    pass
    def Exit(self):
            print ("Exiting Idle")