'''
create a Judge class that tracks name, keywords, and business flag and Submission class tracking ID, keywords, Judges
'''

import math

class Submission():
    '''
    A class defining objects that represent prize submissions/applications, including data related to the relevant technical concepts/keywords describing the application and the submission ID.
    '''

    def __init__(self, submission_id, target_num_judges, min_num_flag_judges = 0):
        '''
        Constructor for Submission objects

        Parameters
        ----------
        submission_id: str. Name or some other identifier of the Submission being created.

        target_num_judges: int. The number of unique Judge objects that should be assigned to this Submission

        min_num_flag_judges: int. The minumum number of flagged judges (e.g. business-savvy judges) that must be assigned to this Submission. A value of 0 indicates that flags can be ignored (flagged Judge objects aren't treated as special compared to unflagged Judge objects).
        '''

        self.id = submission_id

        self.target_num = target_num_judges

        #In case min_num_flag_judges is actually float...
        self.min_num_flag = math.floor(min_num_flag_judges)

        self.assigned_judges = []
        self.flag_count = 0
        self.unflagged_count = 0


    def assign_judge(self, judge):

        '''
        Assigns Judge object to review this application/submission. Checks to make sure the Judge being assigned is the right kind (flagged vs. not) and that max number of Judges isn't exceeded.

        Parameters
        ----------
        judge: Judge object that represents the person you want to review Submission. 
        '''

        #How many spots are still being held for flagged and unflagged judges?
        flagged_slots_left = self.min_num_flag - self.flag_count
        unflagged_slots_left = self.target_num - self.min_num_flag - self.unflagged_count

        #Make sure we haven't already assigned all the judges we need
        if len(self.assigned_judges) < self.target_num:
            #Are there any flagged judges required and 
                #have we not hit that number yet?
            if self.min_num_flag > 0 and self.flag_count < self.min_num_flag:
                #Assign judge if flag = True and increment the counter
                if judge.flag:
                    self.assigned_judges.append(judge.assign(self))
                    self.flag_count += 1

                #Assign judge if there are non-flag slots left
                elif unflagged_slots_left > 0:
                    self.assigned_judges.append(judge.assign(self))
                    self.unflagged_count += 1

                #No unflagged slots left and Judge isn't flagged
                else:
                    raise AssertionError("Judge doesn't satisfy Submission flag requirements")

            #Assign judge, as flags don't matter
            else: 
                self.assigned_judges.append(judge.assign(self))
                self.unflagged_count += 1
        else:
            raise AssertionError("Too many Judges assigned to this Submission")


    def __str__(self): 
        return f"Submission ID: {self.id}\nTarget Number of Judges: {self.target_num}\nNumber of Assigned Judges: {len(self.assigned_judges)}\nNumber of Assigned Flagged Judges: {self.flag_count}\nNumber of Assigned Unflagged Judges: {self.unflagged_count}"