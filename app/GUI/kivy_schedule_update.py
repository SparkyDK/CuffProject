import time
from app.constants.CONSTANTS import MAX_NUM_SCHEDULES, MAX_NUM_PHASES
class kivy_schedule_update:
    def schedule_update(self, all_schedules):
        self.all_schedules = all_schedules

        #print (self.all_schedules)

        self.schedule1 = self.all_schedules[0]
        self.schedule2 = self.all_schedules[1]
        self.schedule3 = self.all_schedules[2]
        self.schedule4 = self.all_schedules[3]

        self.s1_phase1 = str(self.schedule1[0][2])
        self.s1_phase2 = str(self.schedule1[1][2])
        self.s1_phase3 = str(self.schedule1[2][2])
        self.s1_phase4 = str(self.schedule1[3][2])
        self.s1_phase5 = str(self.schedule1[4][2])
        self.s1_phase6 = str(self.schedule1[5][2])
        self.s1_phase7 = str(self.schedule1[6][2])
        self.s1_phase8 = str(self.schedule1[7][2])

        self.s2_phase1 = str(self.schedule2[0][2])
        self.s2_phase2 = str(self.schedule2[1][2])
        self.s2_phase3 = str(self.schedule2[2][2])
        self.s2_phase4 = str(self.schedule2[3][2])
        self.s2_phase5 = str(self.schedule2[4][2])
        self.s2_phase6 = str(self.schedule2[5][2])
        self.s2_phase7 = str(self.schedule2[6][2])
        self.s2_phase8 = str(self.schedule2[7][2])

        self.s3_phase1 = str(self.schedule3[0][2])
        self.s3_phase2 = str(self.schedule3[1][2])
        self.s3_phase3 = str(self.schedule3[2][2])
        self.s3_phase4 = str(self.schedule3[3][2])
        self.s3_phase5 = str(self.schedule3[4][2])
        self.s3_phase6 = str(self.schedule3[5][2])
        self.s3_phase7 = str(self.schedule3[6][2])
        self.s3_phase8 = str(self.schedule3[7][2])

        self.s4_phase1 = str(self.schedule4[0][2])
        self.s4_phase2 = str(self.schedule4[1][2])
        self.s4_phase3 = str(self.schedule4[2][2])
        self.s4_phase4 = str(self.schedule4[3][2])
        self.s4_phase5 = str(self.schedule4[4][2])
        self.s4_phase6 = str(self.schedule4[5][2])
        self.s4_phase7 = str(self.schedule4[6][2])
        self.s4_phase8 = str(self.schedule4[7][2])


        return (self.s1_phase1, self.s1_phase2, self.s1_phase3, self.s1_phase4,\
                self.s1_phase5, self.s1_phase6, self.s1_phase7, self.s1_phase8,\
                self.s2_phase1, self.s2_phase2, self.s2_phase3, self.s2_phase4,\
                self.s2_phase5, self.s2_phase6, self.s2_phase7, self.s2_phase8,\
                self.s3_phase1, self.s3_phase2, self.s3_phase3, self.s3_phase4,\
                self.s3_phase5, self.s3_phase6, self.s3_phase7, self.s3_phase8,\
                self.s4_phase1, self.s4_phase2, self.s4_phase3, self.s4_phase4,\
                self.s4_phase5, self.s4_phase6, self.s4_phase7, self.s4_phase8)
