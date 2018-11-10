import pandas as pd

class Judge():
    '''
    A class defining objects that represent prize judges, including their expertise keywords and identifying info.
    '''

    def __init__(self, name, max_review_count, flag = False):
        '''
        Constructor for Judge objects.

        Parameters
        ----------
        name: str. Full name of judge.

        max_review_count: int. Maximum allowed number of applications/submissions that the Judge is allowed to review

        flag: boolean. Indicates that there's something special about this judge that we should take note of (e.g. flag = True for business judges to make sure they get assigned as appropriately per submission)
        '''

        self.name = name
        self.max_count = max_review_count
        self.flag = flag

        self.assignments = []

    def assign(self, submission):
        '''
        Assigns Judge object to submission for review.

        Parameters
        ----------
        submission: a Submission object
        '''

        #Make sure we haven't fully loaded this Judge up yet and that they aren't being assigned twice to the same app
        if len(self.assignments) < self.max_count and submission not in self.assignments:
            self.assignments.append(submission)
            return self

        #Too many assignments
        elif len(self.assignments) >= self.max_count:
            raise AssertionError("Too many Submissions assigned to this Judge")

        #Already assigned to this Submission!
        elif submission in self.assignments:
            raise ValueError("Judge already assigned to this Submission")

    def __str__(self): 
        return f"Judge Name: {self.name}\nFlagged: {self.flag}\nNumber of assigned reviews: {len(self.assignments)}"


    #TODO: to_dict() method for pushing out {Judge_name: [Flag Status, Number of Assignments]} so you can use DataFrame.from_dict() to append rows

    def to_df(self):
        '''
        Converts judge attributes into pandas DataFrame structure

        Returns
        -------
        pandas DataFrame of format columns = Judge Name, Flag Status, Number of Assignments
        '''

        return pd.DataFrame({'Judge Name': [self.name], 
            'Flag Status': [self.flag], 
            'Number of Assignments': [len(self.assignments)]})