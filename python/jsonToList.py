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

def getSavedJobsIndeed():
    """returns joblistings sorted for indeed

    Returns:
        indeedJobListings, linkedInJobListings
    """
    indeedJobListings = []
    
    listings = getSavedJobListings()
    for job in listings:
        if job["url"][int(len("https://")):].split('/')[0] == "ca.indeed.com":
            # add job to indeed
            indeedJobListings.append(job)
            
    return indeedJobListings
    
    
def getSavedJobsLinkedIn():
    """returns joblistings sorted for linkedin

    Returns:
        linkedInJobListings
    """
    linkedInJobListings = []
    
    listings = getSavedJobListings()
    for job in listings:
        if job["url"][int(len("https://")):].split('/')[0] == "www.linkedin.com":
            # add job to linkedin
            linkedInJobListings.append(job)
            
    return linkedInJobListings