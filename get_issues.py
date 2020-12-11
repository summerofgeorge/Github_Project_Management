# get_issues.py
#load modules
import requests
import os
from pprint import pprint
import config #Where to save your Github token
import pandas as pd
import json

#Get user input parameters
repo_name = input("Enter the name of the GH Repo you want Issues collected from:\n example: data-science")
REPO = str(repo_name)
value = input("enter the state of issues you want:\n options: open, closed, all")
params = {"content_type" : "Issue", "state":value}

# Define the input parameters
token = config.GITHUB_TOKEN
acc = "application/vnd.github.inertia-preview+json" #this is the Accept type you must have for working with Projects in the current Github Api
#params = {"content_type" : "Issue", "state":"open"} #notice the content type is for issues and the issue state is open
HEADERS = {'Accept': f'{acc}','Authorization': f'token {token}'}
OWNER = "Thinkful-Ed"
#REPO = "data-science"

ISSUES_DICT = {}
def get_issues_by_repository(repository):
    url = "https://api.github.com/repos/{}/{}/issues".format(OWNER, repository)
    headers = HEADERS
    r = requests.get(
        url=url,
        headers=headers, 
        params=params

    )
    issues = r.json()
    while "next" in r.links:
        print("\tNext Page: {}".format(r.links["next"]["url"]))
        r = requests.get(
            url=r.links["next"]["url"],
            headers=headers,
            params=params
        )
        issues.extend(r.json())
    ISSUES_DICT.update({repository: issues})
    return issues

today = pd.to_datetime('now').date()
issue_dict = get_issues_by_repository(REPO)
df = pd.DataFrame.from_dict(issue_dict)
df['date'] = pd.to_datetime(df['created_at']).dt.date
filename = params['state']+'_issues_'+str(REPO)+'_'+str(today)+'.csv'
df.to_csv(filename, index =False)