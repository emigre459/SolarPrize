import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random

def similarity_scoring(submissions, judges, judges_per_app, random_seed = None):
    '''
    Calculates the cosine similarity score between judges and submissions for each judge-submission pairing.

    NOTE: assumes keyword universe is identical for submissions and judges, meaning that judge-flagging keywords should already be dropped.

    Parameters
    ----------
    submssions: pandas DataFrame of with each column being a keyword and each row being a unique sumbission

    judges: pandas DataFrame of with each column being a keyword and each row being a unique judge

    random_seed: None (default) or int. If not None, sets the seed for the randomization algorithm used when picking a Judge after all nonzero-scoring Judges are already assigned. If set to an integer, this negates the stochasticity of the assignments and will result in identical assignments every time this is run.

    Returns
    -------
    pandas DataFrame wherein each column is a submission with a ranked-order list of Judges (highest-scoring first). The columns are sorted such that the farthest left one has the lowest sum of similarity scores across all Judges and the sum goes up as you go further to the right. This DataFrame should be considered a recommendation of who to assign to what submission
    '''

    #Set up the random seed so the results are always the same
    random.seed(random_seed)

    scores = pd.DataFrame(cosine_similarity(submissions,judges), 
        columns = judges.index.values, index = submissions.index).transpose()

    #Sort columns/submissions such that the one with the lowest sum of similarity scores is on the far left
        #and the sum of scores per submission rises from there
    scores = scores.reindex(scores.sum().sort_values().index, axis=1)

    assignment_recommendations = pd.DataFrame(data = None)

    for name in scores.columns.values:
        #How many of the top judges being selected have nonzero similarity scores?
        num_nonzero = len(scores[name].sort_values(ascending = False)[:judges_per_app].nonzero()[0])

        #Do any of the top N judges for this submission have a zero similarity score? If so, randomly select judge
            #from remaining group so we don't assign the highest alphabetical judge with zero score to all the low-scoring
            #ones
        if num_nonzero < judges_per_app:
            #Assign the nonzero-score names first
            temp = list(scores[name].sort_values(ascending = False).index.values[0:num_nonzero])
            
            #What are the names of the zero-score judges?
            working_names = list(scores[name].sort_values(ascending = False)[num_nonzero:].index.values)
            temp += random.sample(working_names, k = len(scores[name]) - num_nonzero)
            
            assignment_recommendations[name] = temp
        else:
            assignment_recommendations[name] = scores[name].sort_values(ascending = False).index.values
    
    return assignment_recommendations

def make_assignments(scores, submissions_objs, judges_objs):
    '''
    Uses similarity scores to assign Judges to Submissions

    Parameters
    ----------
    scores: pandas DataFrame of the format output by 
            assignments.similarity_scoring(). Provides similarity scores for every Submission-Judge pair.

    submissions_objs: list of Submission. All Submission objects created by 
                        the submissions scored in scores.

    judges_objs: list of Judge. All Judge objects created by 
                        the judges scored in scores.

    '''

    #Really lame looping through each element of the app_assignments 
        #DataFrame, but I can't think of how to do it better

    #TODO: post something on StackOverflow to see if we can make this more elegant

    for app_name in scores.columns:
        #Pull out the submission that corresponds to the column we're looking at
        submission = next((x for x in submissions_objs if x.id == app_name),
         None)
        
        for judge_name in scores[app_name]:
            #Pull out the Judge object that corresponds to the name at the top of the list
            judge = next((x for x in judges_objs if x.name == judge_name), 
                None)
            
            #Assign judge to submission, iterating over highest scores first, unless there's a constraint stopping you
                #(e.g. judge has already been assigned too many apps)
            try:
                submission.assign_judge(judge)
                
            #May be full on judges already or still be waiting for more flagged judges
            except AssertionError:
                pass