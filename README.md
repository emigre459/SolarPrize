# Purpose

Prize challenges with judges reviewing them can be unwieldy sucks on manpower. This code is designed to take a *very* simple case of keyword selection and develop similarity scores between judges with specific expertise and submission that require that expertise. 

Effectively, we use simple keyword vectors for applications (chosen by the applicants themselves from a limited dropdown list) and use those same keywords to describe the expertise of a group of external judges (whose expertise keywords are chosen by hand by prize staff). By vectorizing the binary presence of these keywords in these two groups, we can then determine a similarity score that helps speed up the process of matching prize judges with applications that are most relevent to their field of knowledge.

# The Data

The data intended for input herein are prize submission metadata from herox.com, a prizes and challenges hosting platform. 

**Note that any applications that have no keywords will be dropped from the data and not assigned to any judges.**

# The Algorithm

**NOTE:** the code automatically outputs columns in the CSV file in the order that the judges should be assigned, by assuming that judges with the lowest sum of similarity scores are the least flexible in terms of what they are assigned and thus should be assigned first, leaving the more flexible judges for later. *This approach can be broken, however, by judges with low similarity scores across the board, so be wary!*