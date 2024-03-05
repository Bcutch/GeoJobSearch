import json

# this file contains the function(s) used to retrieved the test doubles for job listings
# this can be retrieved by calling the function, getSavedJobListings()
# this will return the list of job dictionaries containing the job posting data to use

# WARNING: IF THE jobListings.json FILE DIRECTORY CHANGES, THIS FILE WON'T WORK

def getSavedJobListings() -> list:
    """ converts json joblistings to list
    
    Returns:
        list: list of dictionary containing job listing data
    """
    
    jobListingsPath = "python/jobListings.json"
    jobData = []
    
    with open(jobListingsPath, "r") as fp:
        jobData = json.load(fp)
    return jobData
