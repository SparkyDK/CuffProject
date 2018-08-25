from array import array
from fysom import Fysom

#from time import clock
#from time import time
#from time import asctime
#from time import localtime

import time
import threading

from collections import deque
import math

#from threading import Timer

## ====================================================

DEBUG = True
Global_cnt = 0

# Only allow 8 periods in the schedule, because of GUI limitations
Max_num_schedules = 8

#array for pain schedule to be read
pain_schedule = []
time_schedule = []

#default pressure values
Pmax = 0 #max pressure
Pup = 0 #upper pressure limit
Plow = 0 #lower pressure limit
Patm = 0 #atmospheric pressure
P = 0 #current pressure
Pnew = 0 #new pressure value)

# Only the following parameter labels are supported and these are defined in this dictionary
d = dict(PATM=0, PAINH=0, PAINL=0, PMAX=0)
Max_num_Parameters = len(d)
# print (d)

#Pain = False
Pain = 0

#default button values
#STOP = True
#ABORT = True
#ENTER = False
#GO = False
STOP = 1
ABORT = 1
ENTER = 0
GO = 0

#input_controls = dict (GO,  STOP,  ABORT,  Pain,  ENTER)
controls = [None] * 5
controls[0] = GO
controls[1] = STOP
controls[2] = ABORT
controls[3] = Pain
controls[4] = ENTER

state_history = ["None"] * 5

#read values from txt file to array
filename = 'Schedule.txt'
with open(filename,  'r') as f:
    f.seek(0)
    lines = f.readlines()
    num_lines = len(lines)
    print "\nRead file", filename, ": ",  lines
    # print "\ndetected ",  num_lines,  " lines of schedule"
    if (num_lines > Max_num_schedules):
    # Check that there are no more than the allowed number of schedules (no blank lines are allowed in the file either)
        raise ValueError("Only a total of ", Max_num_schedules, " schedule statement lines are allowed in the file [", num_lines, " lines were detected]")
        sys.exit('Error!: Too many schedules')  
    
    for i in range (0, Max_num_schedules):
        action, value = (lines[i].strip()).split("_",1)
        value = int (value)
        # Before adding action, check to ensure it is either PAIN or NIL (no other labels supported)
        # Exit the program with an error message, if not
        if (action=='PAIN' or action=='NILL'):
            pain_schedule.append(action)
        else:
            raise ValueError("Only NILL or PAIN actions are allowed! [e.g. NILL_60 or PAIN_999], but [", action, "] was detected")
            sys.exit("error!: Only NILL or PAIN actions are allowed!")
        # Before adding value, make sure that it is between 0 and 999 and exit otherwise
        # print ("value=", value)
        if (value>=0 and value <=999):
            time_schedule.append(value)
        else:
            raise ValueError("Interval values, measured in seconds, must be in range [0,999], but a value of [", value, "] was detected")
            sys.exit('Error!: Interval value not in range [0,999]')
        
    print "\nPain and time schedules:"
    print (pain_schedule)
    print (time_schedule)
   # for i in range (0,7):
       # action, value = (lines[i].strip('\n')).split("_",1)
       # pain_schedule.append(action)
       # time_schedule.append(value)
   # print (pain_schedule)
   # print (time_schedule)
 
filename = 'TEST_Pressure_Values.txt'
with open(filename, 'r') as file:
    file.seek(0)       
    lines=file.readlines()
    num_lines=len(file.readlines())
    print "\nRead file ",  filename, ": ",   lines,  "\n"
    if (num_lines > Max_num_Parameters):
    # Check that there are no more than the allowed number of parameter entries (no blank lines are allowed in the file either) 
        raise ValueError("Only a total of ", Max_num_Parameters, " lines allowed in the file")
        sys.exit('Error!: Too many parameters lines provided in the file')

    for i in range (0, Max_num_Parameters):
        action, value = (lines[i].strip()).split("_",1)
        if (action in d):
        # Check that the action is one that is supported 
            d[action] = value
            i += 1
        else:
        # Exit the program with an appropriate error message, if not
            raise ValueError("Only 4 value types are allowed [in any order]: PAINH_xxx, PAINL_xxx, PATM_xxx, PMAX_xxx [xxx is given in mm Hg]")
            sys.exit('Error!: Not a supported pressure parameter type')
            # Use these variables instead of the dictionary entry values, as a short-form convenience	
    print "d:", d
    Pmax = int(d['PMAX'])
    Pup = int(d['PAINH'])
    Plow = int(d['PAINL'])
    Patm = int(d['PATM'])
    
    # print "Pmax=",  Pmax,  " Pup=",  Pup,  " Plow=",  Plow,  "Patm=",  Patm
    
    if (Patm<Plow and Plow<Pup and Pup<Pmax):
    # Ensure that the values are correctly sized, relative to each other (i.e. Pmax is bigger than Pup, Pup is bigger than Plow,... etc.)
        print "Pmax=", Pmax, " Pup=", Pup, " Plow=", Plow, " and Patm=", Patm
    else:
        raise ValueError("Need Pmax > Pup > Plow > Patm but, instead, have Pmax=", Pmax, "Pup=", Pup, " Plow=", Plow, " and Patm=", Patm)
        sys.exit('Error!: Need Pmax > Pup > Plow > Patm')

    print "\n"

## ====================================================

## ====================================================

# TRANSITIONS
class Transition(object):
    def __init__(self, toState):
        self.toState=toState
    def Execute(self):
        pass
        #print ("Transitioning")

## ====================================================
# STATES

class State(object):
    def __init__(self, FSM):
        self.FSM = FSM
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args=args
    def Exit(self):
        pass
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
class NEW_ENTRY(State):
    def __init__(self, FSM):
        super (NEW_ENTRY, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args=args
        print "\n* NEW_ENTRY *"
        Pmax = int(Pnew)
        Plow = int(Pmax - 20)
        #Pnew = 0
        self.FSM.ToTransition("toIdle")
    def Exit(self):
        print ("Exiting New Entry")
class ISOLATE_VENT(State):
    def __init__(self, FSM):
        super (ISOLATE_VENT, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        print "\n* ISOLATE_VENT * \twith args:",  self.args
        self.FSM.ToTransition("toVENT")
    def Exit(self):
        print ("Exiting ISOLATE_VENT")
class VENT(State):
    def __init__(self, FSM):
        super (VENT, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        print "\n* VENT * \t with args:",  self.args
        #while (self.P>Patm):
        if (self.P>Patm):
            print ("Need to vent, since pressure is greater than atmospheric pressure")
        else:
            self.FSM.ToTransition("toIDLE")
    def Exit(self):
        print("Exiting Vent")
class LOAD_RESERVOIR(State):
    def __init__(self, FSM):
        super (LOAD_RESERVOIR, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']
        print "\n*LOAD_RESERVOIR \twith self.args:",  self.args,  " and args:",  args
        if (self.Pain == 1):
            if (int(self.P)<Plow):
            # Still on track to add pain pressure
                print "Going to add more air with P=",  self.P,  "Plow=",  Plow,  " and Pup=",  Pup,  "at time: ", time.asctime(time.localtime(time.time() ) ),  "elapsed (",  time.time() - start_time,  ")"
                self.FSM.ToTransition("toISOLATE_RESERVOIR")
            elif (self.P>=Plow and self.P<= Pup):
                print "Pain pressure looks right, so we are done with P=",  self.P
                self.FSM.ToTransition("toIDLE")
            else:
            # Pressure is above the min and max pain thresholds
                print "Not sure how we got here with P=",  self.P,  "but pain pressure is too high"
                if (self.P>Pmax):
                    print "Emergency venting P=",  self.P
                    self.FSM.ToTransition("toISOLATE_VENT")
                else:
                    print "Controlled venting P=", self.P,  "Plow=",  Plow,  " and Pup=",  Pup
                    self.FSM.ToTransition("toISOLATE_RELEASE")            
        else:
        # We should usually never get here, without requiring pain.  This shouldn't happen, so get out safely, venting
            print "This usually doesn't happen with P=",  self.P,  " and Pain=",  self.Pain
            self.FSM.ToTransition("toISOLATE_VENT")
    def Exit(self):
        print ("Exiting Load Reservoir")
class ISOLATE_RESERVOIR(State):
    def __init__(self, FSM):
        super (ISOLATE_RESERVOIR, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        print "\n* ISOLATE_RESERVOIR * \twith args:",  self.args
        self.FSM.ToTransition("toCONNECT_CUFF")
    def Exit(self):
        print ("Exiting Isolate Reservoir")
class CONNECT_CUFF(State):
    def __init__(self, FSM):
        super (CONNECT_CUFF, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']        
        print "\n* CONNECT_CUFF * \twith args:",  self.args
        if (self.Pain == 1):
            if (self.P<Plow):
            # Need to add air
                print "Still need to add more air with P=",  self.P,  "Plow=",  Plow,  " and Pup=",  Pup
                self.FSM.ToTransition("toISOLATE")
            elif (self.P>=Plow and self.P<=Pup):
            # In the zone
                print "In the zone with P=",  self.P
                self.FSM.ToTransition("toIDLE")
            elif (self.P>=Plow and self.P>Pup):
            # Overshot the maximum pain pressure value
                print "Overshot pressure maximum with P=",  self.P,  "Plow=",  Plow,  " and Pup=",  Pup
                self.FSM.ToTransition("toISOLATE_RELEASE")
        else:
        # No pain required
            self.FSM.ToTransition("toISOLATE_VENT")
    def Exit(self):
        print ("Exiting Connect Cuff")
class ISOLATE_RELEASE(State):
    def __init__(self, FSM):
        super (ISOLATE_RELEASE, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']        
        print "\n* ISOLATE_RELEASE * \t with args:",  self.args
        if self.P>Pup:
            self.FSM.ToTransition("toRELEASE")
        #if (self.Pain == 1 and P<Plow):
        #    self.FSM.ToTransition("toISOLATE")
        if (self.Pain == 1 and self.P>Plow and self.P<Pup):
            self.FSM.ToTransition("toIDLE")
    def Exit(self):
        print ("Exiting Isolate Release")
class RELEASE(State):
    def __init__(self, FSM):
        super (RELEASE, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        self.P = self.args['P']
        self.Pain = self.args['PAIN']        
        print "\n* RELEASE * \t with args:",  self.args
        if (self.Pain == 1):
            if (self.P<Plow):
            # Need to top up pressure again
                self.FSM.ToTransition("toISOLATE")
            elif (self.P>Plow and self.P<Pup):
            # Pressure in the zone
                self.FSM.ToTransition("toIDLE")
            else:
            # Pressure is greater than Plow, but not in the zone, so it is too high
                self.FSM.ToTransition("toISOLATE_RESERVOIR")
        else:
        # Should not be here, since no pain is required so vent and go back to IDLE
                self.FSM.ToTransition("toISOLATE_VENT")
                
    def Exit(self):
        print ("Exiting Vent")
class ISOLATE(State):
    def __init__(self, FSM):
        super (ISOLATE, self).__init__(FSM)
    def Enter(self):
        pass
    def Execute(self,  args):
        self.args = args
        print "\n* ISOLATE * \t with args:",  self.args
        self.FSM.ToTransition("toLOAD_RESERVOIR")
    def Exit(self):
        print ("Exiting Isolate")
range
## ====================================================
##State Machine
class FSM(object):
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None
        self.args = []
        self.names = {}

    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition

    def AddState(self, stateName, state):
        self.states[stateName]=state
        self.names[state] = stateName
        
    def SetState (self, stateName):
        self.curState=self.states[stateName]
    
    def GetCurState (self):
        #self.name = self.curState
        return(self.names[self.curState] )

    def ToTransition (self, toTrans):
        self.trans=self.transitions[toTrans]

    def Execute(self,  args):
        self.args = args
        #print "((FSM)) args are:",  args
        if (self.trans):
            self.curState.Exit()
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.curState.Enter()
            self.trans = None
        
        #self.curState.Execute(args)
        # Want to be able to modify pressure for debug purposes

        self.curState.Execute(self.args)
## ====================================================
#character class

Char = type("Char",(object,),{})

class System(Char):
    def __init__(self):
        self.FSM = FSM(self)
        
        ##STATES
        self.FSM.AddState("IDLE",IDLE(self.FSM))
        self.FSM.AddState("VENT",VENT(self.FSM))
        self.FSM.AddState("LOAD_RESERVOIR",LOAD_RESERVOIR(self.FSM))
        self.FSM.AddState("ISOLATE_RESERVOIR",ISOLATE_RESERVOIR(self.FSM))
        self.FSM.AddState("CONNECT_CUFF",CONNECT_CUFF(self.FSM))
        self.FSM.AddState("ISOLATE_RELEASE",ISOLATE_RELEASE(self.FSM))
        self.FSM.AddState("RELEASE",RELEASE(self.FSM))
        self.FSM.AddState("ISOLATE",ISOLATE(self.FSM))
        self.FSM.AddState("ISOLATE_VENT",ISOLATE_VENT(self.FSM))
        self.FSM.AddState("NEW_ENTRY",NEW_ENTRY(self.FSM))
        
        #TRANSITIONS
        self.FSM.AddTransition("toIDLE",Transition("IDLE"))
        self.FSM.AddTransition("toVENT",Transition("VENT"))
        self.FSM.AddTransition("toLOAD_RESERVOIR",Transition("LOAD_RESERVOIR"))
        self.FSM.AddTransition("toISOLATE_RESERVOIR",Transition("ISOLATE_RESERVOIR"))
        self.FSM.AddTransition("toCONNECT_CUFF",Transition("CONNECT_CUFF"))
        self.FSM.AddTransition("toISOLATE_RELEASE",Transition("ISOLATE_RELEASE"))
        self.FSM.AddTransition("toRELEASE",Transition("RELEASE"))
        self.FSM.AddTransition("toISOLATE",Transition("ISOLATE"))
        self.FSM.AddTransition("toISOLATE_VENT",Transition("ISOLATE_VENT"))
        self.FSM.AddTransition("toNEW_ENTRY",Transition("NEW_ENTRY"))
        # default to IDLE
        self.FSM.SetState("IDLE")
        
    def Execute(self,  args):
        self.args = args
        # Want to be able to modify pressure value for debug purposes
        #self.FSM.Execute(args)
        
        self.FSM.Execute(self.args)

## ====================================================
#RUN


def main_code(*args, **kwargs):
#while (True == True):
#if (RUN == True):
# Always true?  
# If we use a 1-second event to call this  entire block as re-entrant code, then the while loop should be an if statement 

    #print "main_code: args = ",  args
    #print "main_code: kwargs = ",  kwargs
    # dict( old_GO=0,  PAUSE=False, old_STOP=0, old_ABORT=1, schedule_started=False,  schedule_index=1,  Global_cnt=0,  P=Patm,  elapsed_time=0,  old_elapsed_time=0 )

    #Copy_pain = kwargs['Pain']
    #GO = kwargs['GO']
    old_GO = kwargs['old_GO']
    #STOP = kwargs['STOP']
    old_STOP = kwargs['old_STOP']
    #ABORT = kwargs['ABORT']
    old_ABORT = kwargs['old_ABORT']
    PAUSE = kwargs['PAUSE']
    Current_Pressure = kwargs['P']
    schedule_started = kwargs['schedule_started']
    old_schedule_started = kwargs['old_schedule_started']
    schedule_index = kwargs['schedule_index']
    Global_cnt = kwargs['Global_cnt']
    Global_cnt += 1
    elapsed_time = kwargs['elapsed_time']
    old_elapsed_time = kwargs['old_elapsed_time']
    
    pain_time = kwargs['pain_time']
    old_pain = kwargs['old_pain']
        
    # Elapsed time is a real-valued seconds counter, measuring total time program has executed  
    # Our schedule has units of seconds and we need to know when seconds tick over
    if ( math.floor(elapsed_time) != math.floor(old_elapsed_time) ):
        second_tickover = True
    else:
        second_tickover = False
    
    pain_schedule = args[0]
    time_schedule = args[1]
    for i in range (0,  Max_num_schedules):
        Current_counter [i] = args[2][i]
        # print "i=", i, " and value = ", Current_counter[i]  
    if (schedule_index < Max_num_schedules):
        Pain = pain_schedule[schedule_index]
    else:
        Pain = 'NILL'

    GO = args[3][0]
    STOP = args[3][1]
    ABORT = args[3][2]
    local_PAIN = args[3][3]
    local_ENTER = args[3][4]
        
    past_states = deque(args[4])
    #print past_states
 
    localtime = time.asctime(time.localtime(time.time()) )
    if (DEBUG==True and True==False):
#    if (DEBUG==True):
        if (schedule_index < Max_num_schedules):
            print localtime, " (elapsed=",  elapsed_time,  "): CNT=", Global_cnt, "State=", c.FSM.GetCurState(), "schedule_started=", schedule_started, "GO=", GO, " STOP=",  STOP,  "ABORT=",  ABORT,  "PAUSE=",  PAUSE,  "Pain=",  Pain,  "P=", Current_Pressure, "Pain_dex=",  schedule_index,  "Pain_cnt=",  Current_counter[schedule_index]
        else:
            print localtime, " (elapsed=",  elapsed_time,  "): CNT=", Global_cnt, "State=", c.FSM.GetCurState(), "schedule_started=", schedule_started, "GO=", GO, " STOP=",  STOP,  "ABORT=",  ABORT,  "PAUSE=",  PAUSE,  "Pain=",  Pain,  "P=", Current_Pressure, "Pain_dex=",  schedule_index,         
        #print "Setting Pain=",  Pain
    
    # The following are global asynchronous (to FSM) checks for necessary transitions to ISOLATE_VENT, before state machine executes
    if ( second_tickover == True ):
        # Only check every second to give the relays time to do their thing and allow progression out of ISOLATE_VENT to VENT
        if ( P>Pmax ):
            print "Pressure value (", P,  ") exceeds max value (", Pmax
            schedule_started=False
            PAUSE = False        
            GO = 0
            old_GO = 0
            #STOP = True
            old_STOP = 1
            ABORT = 1
            old_ABORT = 1
            schedule_index = 0
            c.FSM.SetState("ISOLATE_VENT")
        
    if (DEBUG == True):
    # debug statement only!
        ABORT = False
        #print "\tDebug: Global count = ",  Global_cnt
    
    # ABORT Button processing
    if (ABORT==1):
    # Abort button just pressed, so reset everything
        GO = 0
        old_GO = 0
        STOP = 0
        old_STOP = 0
        PAUSE = False        
        schedule_index = 0
        print ("ABORT just pressed; schedule ended and now venting pressure")
        Pain = 'NILL'
        cc.FSM.SetState("ISOLATE_VENT")
    elif (ABORT==1 and old_ABORT==1):
    # ABORT still False; user still pressing button.  Don't force a state transition again unless user releases button and presses again
        pass
    elif (ABORT==0):
    # ABORT button not being pressed at all
        pass
    else:
    # This should never happen
        Pain = 'NILL'
        GO = 0
        old_GO = 0
        STOP = 0
        old_STOP = 0
        PAUSE = False        
        schedule_index = 0
        c.FSM.SetState("ISOLATE_VENT")
        raise ValueError("Error!: Something weird happened with the ABORT button processing")
        
    
    if (DEBUG == True and (Global_cnt==500 or Global_cnt==4000 or Global_cnt==5000) ):
    # debug statement only!
        GO = 1
        print "\tDebug: Go activated with Global count = ",  Global_cnt
        
    if (DEBUG == True and (Global_cnt==1000 or Global_cnt==4500) ):
    # debug statement only!
        GO = 0
        print "\tDebug: Go de-ctivated with Global count = ",  Global_cnt
    
    # GO Button processing
    if ( (GO==0 and old_GO==1 and STOP==0) or (schedule_started==True and PAUSE==False) ):
    # GO button just released and the STOP button not also pressed (STOP has priority), 
    # then we start the schedule, or maybe the schedule is already underway; 
        if (schedule_started==False):
        # just starting a brand new schedule (i.e. GO button just released without a schedule running already)
            schedule_index = 0
            for j in range ( 0, Max_num_schedules-1):
                # Initialize the real-time counters with the values read from the file
                Current_counter[j] = time_schedule[j]
            schedule_started=True # Now schedule is underway
            print "Starting the schedule"
            
        if (schedule_started==True and PAUSE==True and GO==0 and old_GO==1 and STOP==0):
        # Come out of pause mode by pressing and then releasing GO button, provided already running a schedule
            PAUSE=False

        if (schedule_index < Max_num_schedules):
        # Still executing a valid schedule in the sequence, but not done yet
        # Changed ths to an if statement (i.e. I am assuming re-entrant code)  
        # Read the string value extracted from the file  
            Pain = pain_schedule[schedule_index]
            if (Current_counter[schedule_index] > 1):
            # Still not done this phase
            # Need to make sure that program execution dwells here for a second???  
            # We assume that the entire main loop is re-entrant code, that is called each second
            # Alternatively, we could check to see if the seconds counter has changed or not, using a variable Previous_counter 
            # As another alternative, we could sleep/wait, but this blocks and wastes CPU, potnentially making the Pi unresponsive to user input
                if ( second_tickover == True ):
                    Current_counter[schedule_index] -= 1
                    print "Schedule Counter adjusted: Schedule:", schedule_index, " with counter value = ",  Current_counter[schedule_index]
            else:
            # Current phase is now complete (Current_counter value is zero ... or negative)
            # Reset the displayed/current value back to the starting value, but make it negative to indicate progress
                # and go to the next phase of the schedule
                if ( second_tickover == True ):
                    print "Finished schedule phase ",  schedule_index,  "\n"
                    Current_counter[schedule_index] = -1 * time_schedule[schedule_index]
                    schedule_index += 1   
        else:
        # Done executing the schedule sequence
            print "Finished executing schedule"
            GO = 0
            old_GO = 0
            STOP = 0
            old_STOP = 0
            schedule_started = False
            PAUSE = False        
            schedule_index = 0
            Pain = 'NILL'
            print ("Schedule Complete")
            c.FSM.SetState("ISOLATE_VENT")
    elif (GO==0 and old_GO==0  and STOP==0 and PAUSE==False):
    # GO still False; the normal case in the middle of a schedule or maybe for the very initial case else
        pass
    elif (GO==1  and STOP==0  and PAUSE==False):
    # GO just pressed (or still being pressed).... don't do anything yet, but wait until the button is released
        pass
    elif (schedule_started==True  and STOP==0 and PAUSE==False):
        pass
    elif (STOP==1):
    # STOP button has priority, so we ignore GO button and go on to the processing of STOP button next
        pass
    elif (PAUSE==True):
    # In Pause mode
        pass
    else:
    # This should never happen
        c.FSM.SetState("ISOLATE_VENT")
        raise ValueError("Error!: Something weird happened with the GO button processing")
        Pain = 'NILL'
        GO = 0
        old_GO = 0
        STOP = 0
        old_STOP = 0            
        schedule_index = 0

    if (DEBUG == True and Global_cnt==20 ):
    # debug statement only!
        STOP = 1
        print "\tDebug: Stop activated with Global count = ",  Global_cnt
        
    if (DEBUG == True and (Global_cnt==30 or Global_cnt==2) ):
    # debug statement only!
        STOP = 0
        print "\tDebug: Stop de-activated with Global count = ",  Global_cnt

    # STOP Button processing
    if (STOP==1 and old_STOP==0):
    # Stop button just pressed
        GO = 0
        old_GO = 0
        if (schedule_started):
        # Only need to pause, if we are already running a schedule
        # To cover the case where the researcher stops the experiment in the middle of a pain cycle
        # we could make NIL the default behaviour, rather than leaving the patient in pain 
        #...hmmmm... we will use the RELEASE/RESET button instead for the pain-free stopping option
            #Pain = 'NILL'
            PAUSE = True
            # Could always implement a toggle using 'STOP' button pressing, instead of or as well as using GO
            # if (PAUSE==False):
            #   PAUSE = True
            # else:
            #   PAUSE = False
            print ("Back to idle; STOP just pressed; schedule paused")
            c.FSM.SetState("IDLE")
        else:
        # Otherwise, if there is no schedule running, ignore the STOP button press altogether
            pass
    elif (STOP==1 and old_STOP==1):
    # STOP button still being pressed
        pass
    elif (STOP==0):
    # STOP button not being pressed at all
        pass
    else:
    # This should never happen
        c.FSM.SetState("ISOLATE_VENT")
        raise ValueError("Error!: Something weird happened with the STOP button processing")
        Pain = 'NILL'
        GO = 0
        old_GO = 0
        STOP = 1
        old_STOP = 1          
        schedule_index=0
   
    old_GO = GO
    old_STOP = STOP
    old_ABORT = ABORT
    
    if (Pain == 'PAIN'):
        #kwargs['Pain'] = 1
        args[3][3] = True
        Pain_signal = 1
        #print "Seting Pain variable true"
    elif (Pain == 'NILL'):
        #kwargs['Pain'] = 0
        Pain_signal = 0
        args[3][3] = False
        #print "Seting Pain variable false"
    else:
        #kwargs['Pain'] = 0
        Pain_signal = 0
        args[3][3] = False
        print "Error!: Pain has a value of ",  Pain, " which is neither PAIN or NILL"

    if ( (Pain_signal != old_pain) or (schedule_started==True and old_schedule_started==False) ):
        timediff = time.time() - pain_time
        print "Pain signal changed to ",  Pain_signal,  "after ",  round(timediff),  "(", timediff, ") seconds"
        pain_time = time.time()
    old_pain = Pain_signal
    old_schedule_started = schedule_started

    kwargs['Global_cnt'] = Global_cnt
    #kwargs['ABORT'] = ABORT
    kwargs['old_ABORT'] = old_ABORT
    #kwargs['GO'] = GO
    kwargs['old_GO'] = old_GO
    #kwargs['STOP'] = STOP
    kwargs['old_STOP'] = old_STOP
    kwargs['P'] = Current_Pressure
    kwargs['PAUSE'] = PAUSE
    kwargs['schedule_started'] = schedule_started
    kwargs['old_schedule_started'] = old_schedule_started
    kwargs['schedule_index'] = schedule_index
    
    kwargs['pain_time'] = pain_time
    kwargs['old_pain'] = old_pain
    
    old_elapsed_time = elapsed_time
    elapsed_time = time.time() - start_time
    #print "elapsed_time=",  elapsed_time,  " and old_elapsed_time=",  old_elapsed_time
    #print "elapsed_time (truncated)=",  math.floor(elapsed_time),  " and old_elapsed_time (truncated)=",  math.floor(old_elapsed_time)
    kwargs['elapsed_time'] = elapsed_time
    kwargs['old_elapsed_time'] = old_elapsed_time
    
    args[3][0] = GO
    args[3][1] = STOP 
    args[3][2] = ABORT
    
    returned_state =   c.FSM.GetCurState() 
    # pop out the highest-index entry from the state history
    past_states.popleft()
    # Add the newest state value to the lowest-index entry of the state history
    past_states.append(returned_state)
    
    #print "state_history:",  past_states
    for i in range (0,  5):
        args[4][i] = past_states[i]
        #print i, ":",  past_states[i],  " "

    if (DEBUG == True):
        #print "returned_state: ",  returned_state
        if (past_states[4] == "CONNECT_CUFF" and past_states[3]=="ISOLATE_RESERVOIR" and past_states[2]=="LOAD_RESERVOIR"):
        # Controlled pressure increase
            Current_Pressure = int(Current_Pressure) + 25
        if (past_states[4] == "RELEASE" and past_states[3]=="ISOLATE_RELEASE" and past_states[2]=="CONNECT_CUFF"):
        # Controlled pressure release path 
            Current_Pressure = int(Current_Pressure) - 10
        if (past_states[4] == "RELEASE" and past_states[3]=="ISOLATE_RELEASE" and past_states[2]=="LOAD_RESERVOIR"):
        # Controlled pressure release path (in case of leaks)
            Current_Pressure = int(Current_Pressure) - 10
        if (past_states[4] == "VENT"):
        # Venting case
            Current_Pressure = int(Patm)
        kwargs['P'] = Current_Pressure
    
#    valid_states = {
#        'IDLE': 'state', 
#        'VENT': 'state', 
#        'LOAD_RESERVOIR': 'state', 
#        'ISOLATE_RESERVOIR': 'state', 
#        'CONNECT_CUFF': 'state', 
#        'ISOLATE_RELEASE': 'state', 
#        'RELEASE': 'state', 
#        'ISOLATE': 'state',     
#        'ISOLATE_VENT': 'state', 
#        'NEW_ENTRY': 'state'     
#    } 
    
    # Execute the state mathine
    #print "Calling FSM with Pressure=",  Current_Pressure,  "and GO=",  GO,  " STOP=", STOP, "Pain_signal=",  Pain_signal
    if (schedule_started==True): 
        running=1
    else:
        running=0
    if (PAUSE==True):
        pause_value=1
    else:
        pause_value=0
    control_args = {'GO' : GO, 'STOP': STOP,  'PAIN': Pain_signal,  'P': Current_Pressure,  'RUNNING': running,  'PAUSE': pause_value}

    try:
        c.Execute(control_args)
    except KeyboardInterrupt:
        print ("\nDone")    

    
    for i in range (0,  Max_num_schedules):
        args[2][i] = Current_counter[i]
        #print "Setting counter ",  i,  " to a value of ",  args[2][i]
        
    try:
#        t = threading.Timer( 1.0, main_code, args, kwargs )
        # Can ajust the timing here to make control more "responsive".  
        # Need to make sure that relays have enough time to close and open, but FSM *should* handle the race conditions, if not
        t = threading.Timer( 0.01, main_code, args, kwargs )
        t.start()
    except KeyboardInterrupt:
        print ("\nDone")
    # end of main_code re-entrant block
    exit(0)





if __name__ == "__main__":
    
    try:
    # Create an instance of the system
        c = System()
        #default state is idle (after venting in the ISOLATE_VENT state)
        c.FSM.SetState("ISOLATE_VENT")
    except KeyboardInterrupt:
        print ("\nDone")    

    # Initialize the timers
    start_time = time.time()
    time.clock()

    #main_args = dict( Pain=False,  GO=False, old_GO=False,  PAUSE=False, STOP=False, old_STOP=False,  ABORT=True, old_ABORT=True, schedule_started=False,  schedule_index=1,  Global_cnt=0 )
    main_args = dict( old_GO=0,  PAUSE=False, old_STOP=0, old_ABORT=1, schedule_started=False,  old_schedule_started=False,  schedule_index=0,  Global_cnt=0,  P=Patm,  elapsed_time=0,  old_elapsed_time=0,  pain_time=start_time, old_pain=0)

    # Execute the state mathine for the first time
    control_args = {'GO' : 0, 'STOP': 0,  'PAIN': 0,  'P': Patm,  'RUNNING': 0,  'PAUSE':0}
    try:
        c.Execute( control_args )
    except KeyboardInterrupt:
        print ("\nDone")    
    
    # print "pain_schedule",  pain_schedule
    # print "time_schedule",  time_schedule
    
    Current_counter = [None] * (Max_num_schedules)
    
    for i in range (0,  Max_num_schedules):
        # Initialize the schedule indices using the data from the file
        Current_counter[i] = time_schedule[i]
        print "Setting counter ",  i,  " to a value of ",  Current_counter[i], 

    #args = [pain_schedule,  time_schedule,  Current_counter]
    args = [pain_schedule,  time_schedule,  Current_counter,  controls,  state_history]
    try:
        t = threading.Timer( 1.0, main_code, args, main_args )
        t.start()
        
    except KeyboardInterrupt:
        print ("\nDone")
    
 # Currently the transition to 'NEW_ENTRY' is defined only in the state 'IDLE'
 # If we wanted to be able to reach 'NEW_Entry" from all states we could define the transition as asynchronous
 # Problem - Pressure alues imported from document are seen as 'str' and not 'int' 
 # so convert them... or just use them as strings (which was my choice)
