"""Module  providing Python library to use the Github API v3."""
import csv
import os
from datetime import datetime, timedelta
from github import Github


def search_for_pr(gitcreds, gitrepo, prstatus, startdate):
    """Function to retrieve pr"""

    repository = gitcreds.get_repo(gitrepo)
    print("Name of repository is "+str(repository))
    print("Searching from"+str(startdate))
    stringified_date = startdate.strftime("%Y-%m-%d")
    if prstatus is not "merged":
        query = "type:pr"+" state:"+prstatus+" repo:" + \
                gitrepo+" created:>"+stringified_date
    else:
        query = "type:pr"+" is:"+prstatus+" repo:" + \
                gitrepo+" created:>"+stringified_date
    print("Executing search as"+query)
    pulls = gitcreds.search_issues(query, sort='updated', order='asc')
    return pulls


def append_report(report_name, collection_of_pr_fields):
    """Function accepts collection of PR  and prints out its report"""
    report = open(report_name, 'a+', newline='',encoding='utf-8')
    csvwriter = csv.writer(report)
    if os.path.getsize(report_name) == 0:
        csvwriter.writerow(['ID of the Pull Request', 'Title of the Pull Request',
                            'Opened on', 'Last Updated', 'Closed at'])
    for row in collection_of_pr_fields:
        csvwriter.writerow([row['state'], row['id'], row['title'],
                            row['opened_on'], row['last_updated_date'], row['closed_on']])
    report.close()
    print('Full Report complete')


def get_specific_fields_of_pr(prdatadump):
    """Function accepts all fields of  github PR and returns the number,title etc"""
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
    report_name = 'GitHub_PullRequest'+f'{report_time}:%Y-%m-%d_%H%M'+'.csv'
    report_dir = '/var/tmp/'
    report_name = report_dir + '/' + report_name

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
    state = ["merged", "closed", "open"]

    for prstate in state:
        resulting_prs = search_for_pr(
            github_creds, pub_repo, prstate, startdate)
        prstate_fields = get_specific_fields_of_pr(resulting_prs)
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
    main()
