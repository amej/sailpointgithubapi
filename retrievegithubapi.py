"""Module providing Python library to use the Github API v3."""
import os
from datetime import datetime, timedelta
from github import Github


def search_for_pr(gitcreds, gitrepo, prstatus, startdate):
    """Function to retrieve pr"""

    repository = gitcreds.get_repo(gitrepo)
    print("Name of repository is ")
    print(repository)
    print(startdate)
    startrange = startdate.strftime("%Y-%m-%d")
    query = "type:pr"+" state:"+prstatus+" repo:" + \
        gitrepo+" created:"+startrange+"..*"
    print(query)
    pulls = gitcreds.search_issues(query, sort='created', order='asc')
    for pull_request in pulls:
        print(pull_request.number, pull_request.title)


# def retrieve_pr_title(gitcreds,gitrepo,prstatus):
#    """Function to retrieve pr title"""

 #   repo = gitcreds.get_repo(gitrepo)
  #  print("Name of repository is ")
   # print(repo)
    #pulls = repo.get_pulls(state=prstatus, sort='created', base='master')
    # for each_pr in pulls:
     #   print (each_pr)


def main():
    """Launcher function"""
    # using an access token
    access_token = os.environ.get("GITHUB_TOKEN")
    # Pass the base_url and login
    github_creds = Github(login_or_token=access_token,
                          base_url='https://api.github.com')

    # This porridge is hot, that porridge is cold, these prs need to be younger than a week .
    days_to_subtract = 7
    startdate = datetime.today() - timedelta(days=days_to_subtract)

    # Sample repo
    pub_repo = os.environ.get("PUBLIC_REPO")
    state = ["open", "closed"]

    for prstate in state:
        search_for_pr(github_creds, pub_repo, prstate, startdate)
    # retrieve_pr_title(github_creds,SAMPLE,"open")


# write code that will use the GitHub API to
# retrieve a summary of all opened, closed, and in progress pull requests
# Opened


# in the last week for a given repository
# and print an email summary report
# that might be sent to a manager or Scrum-master.
# Choose any public target GitHub repository you like that has had at least 3 pull requests
#  in the last week.
# Format the content email as you see fit, with the goal to allow the reader to easily digest
#  the events of the past week.

# Please print to console the details of the email you would send (From, To, Subject, Body).
# As part of the submission, you are welcome to create a Dockerfile to build an image
# that will run the program, however, other ways of implementing this is acceptable.
# Your code demonstrates use of variables, looping structures, and control structures
# Your code prints a user-friendly summary of open, merged, and closed pull requests
# including counts of PRs as well as their titles. Use your judgement on what you think
#  is important information.

if __name__ == '__main__':
    main()
