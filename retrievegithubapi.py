"""Module  providing Python library to use the Github API v3."""
import csv
import os
import sys
from datetime import datetime, timedelta
from time import strftime
from github import Github


def search_for_pr(gitcreds, gitrepo, prstatus, startdate):
    """Function to retrieve pr"""

    repository = gitcreds.get_repo(gitrepo)
    print("Name of repository is "+str(repository))
    print("Searching from "+str(startdate))
    stringified_date = startdate.strftime("%Y-%m-%d")
    if prstatus != "merged":
        query = "type:pr"+" is:"+prstatus+" repo:" + \
                gitrepo+" updated:>"+stringified_date
    else:
        query = "type:pr"+" is:"+prstatus+" repo:" + \
                gitrepo+" updated:>"+stringified_date

    pulls = gitcreds.search_issues(query, sort='updated', order='asc')
    print("Total count of "+prstatus+" pull requests are "
          + str(pulls.totalCount))
    return pulls


def append_report(report_name, collection_of_pr_fields):
    """Function accepts collection of PR  and prints out its report"""
    report = open(report_name, 'a+', newline='', encoding='utf-8')
    csvwriter = csv.writer(report)
    if os.path.getsize(report_name) == 0:
        csvwriter.writerow(['ID of the PR', 'Title of the PR',
                            'Opened on', 'Last Updated', 'Closed at'])
    for row in collection_of_pr_fields:
        csvwriter.writerow([row['state'], row['id'], row['title'],
                            row['opened_on'], row['last_updated_date'], row['closed_on']])
    report.close()
    print('Full Report complete')


def get_specific_fields_of_pr(prdatadump):
    """Function accepts all fields of github PR and returns number,title etc"""
    print(dir(prdatadump))
    cleaned_list = []
    for pull_request in prdatadump:
        if pull_request is not None:
            cleaned_item = {}
            cleaned_item['state'] = pull_request.state
            cleaned_item['id'] = pull_request.number
            cleaned_item['title'] = pull_request.title
            cleaned_item['opened_on'] = pull_request.created_at
            cleaned_item['last_updated_date'] = pull_request.updated_at
            cleaned_item['closed_on'] = pull_request.closed_at
            cleaned_list.append(cleaned_item)
    return cleaned_list


def main():
    """Launcher function"""

    report_time = datetime.now
    report_name = 'GitHub_PullRequest'+'.csv'
    report_dir = '/var/tmp/'
    report_name = report_dir + '/' + report_name

    # using an access token
    access_token = os.environ.get("GITHUB_TOKEN")
    # Pass the base_url and login
    github_creds = Github(login_or_token=access_token,
                          base_url='https://api.github.com')

    # Calculate last week's date
    days_to_subtract = 7
    startdate = datetime.today() - timedelta(days=days_to_subtract)

    # Sample public repo
    pub_repo = os.environ.get("PUBLIC_REPO")

    # Github PR has merged or unmerged state.
    # Merged always ends in closed state.
    # But unmerged state can indicate 'In progress'  or closed.
    state = ["merged", "unmerged"]

    for prstate in state:
        resulting_prs = search_for_pr(
            github_creds, pub_repo, prstate, startdate)
        prstate_fields = get_specific_fields_of_pr(resulting_prs)
        if "TO_EMAIL_ADDRESS" in os.environ:
            append_report(report_name, prstate_fields)

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
    sys.exit(main())
