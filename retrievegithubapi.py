"""Module  providing Python library to use the Github API v3."""
import csv
import os
import sys
from datetime import datetime, timedelta
from github import Github

# Code that will use the GitHub API to
# retrieve a summary of all opened, closed, and in progress pull requests
# Note: A merged PR is in closed state. Unmerged can be one of open or close


def search_for_pr(gitcreds, gitrepo, prstatus, startdate):
    """Function to retrieve pr"""

    stringified_date = startdate.strftime("%Y-%m-%d")
    if prstatus != "merged":
        query = "type:pr"+" is:"+prstatus+" repo:" + \
                gitrepo+" updated:>"+stringified_date
    else:
        query = "type:pr"+" is:"+prstatus+" repo:" + \
                gitrepo+" updated:>"+stringified_date

    pulls = gitcreds.search_issues(query, sort='updated', order='asc')
    return pulls


def get_specific_fields_of_pr(prdatadump, prstate):
    """Function accepts all fields of github PR and returns number,title etc"""
    cleaned_list = []
    for pull_request in prdatadump:
        if pull_request is not None:
            cleaned_item = {}
            cleaned_item['state'] = prstate
            cleaned_item['id'] = pull_request.number
            cleaned_item['title'] = pull_request.title
            cleaned_item['opened_on'] = pull_request.created_at
            cleaned_item['last_updated_date'] = pull_request.updated_at
            cleaned_item['closed_on'] = pull_request.closed_at
            cleaned_list.append(cleaned_item)
    return cleaned_list


def append_report(report_name, collection_of_pr_fields):
    """Function accepts collection of PR  and prints out its report"""
    report = open(report_name, 'a+', newline='', encoding='utf-8')
    csvwriter = csv.writer(report)
    if os.path.getsize(report_name) == 0:
        csvwriter.writerow(['ID of the PR', 'Title of the PR',
                            'Opened on', 'Last Updated', 'Closed at'])
    for row in collection_of_pr_fields:
        csvwriter.writerow([row['state'], row['id'], row['title'],
                            row['opened_on'], row['last_updated_date'],
                            row['closed_on']])
    report.close()


"""
def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):
    pass
    assert isinstance(send_to, list)

    msg = EmailMessage()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.set_content(MIMEText(text))

    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    for f in files or []:
        with open(f, "rb") as file_pointer:
            part = MIMEApplication(
                    file_pointer.read(),
                    Name=basename(f)
            )
        # after the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
"""


def main():
    """Launcher function"""

    now = datetime.now()
    file_suffix = now.strftime("%Y-%m-%d_%H%M")
    report_name = 'GitHub_PullRequest_'+file_suffix+'.csv'
    report_dir = '/var/tmp'
    report_name = report_dir + '/' + report_name

    # using an access token
    if os.getenv("GITHUB_TOKEN") is not None:
        access_token = os.environ.get("GITHUB_TOKEN")
    else:
        print("Populate the os env var GITHUB_TOKEN with your token. ")
        return 1

    # Pass the base_url and login
    github_creds = Github(login_or_token=access_token,
                          base_url='https://api.github.com')

    # Calculate last week's date
    days_to_subtract = 7
    startdate = datetime.today() - timedelta(days=days_to_subtract)

    # Set default  public repo, if not passed
    pub_repo = os.environ.get("PUBLIC_REPO", "kubernetes/kubernetes")
    if pub_repo == "kubernetes/kubernetes":
        print("set OS env var PUBLIC_REPO to override "+pub_repo)

    # Github PR has merged or unmerged state.
    # Merged always ends in closed state.
    # But unmerged state can indicate 'In progress'  or closed.
    state = ["merged", "unmerged"]

    emailbody = {}
# Your code prints a user-friendly summary
# of open, merged, and closed pull requests including
# counts of PRs as well as their titles.
    emailbody["tldr"] = """
Dear Mgr/Scrum-Master,
pfa summary report in csv format.
You will find the ID, title, relevant dates of these merged and unmerged PR
in the csv file.
"""

    for prstate in state:
        resulting_prs = search_for_pr(
            github_creds, pub_repo, prstate, startdate)
        emailbody[prstate] = f"""
In the public repository {pub_repo}, since \
{startdate.strftime('%Y-%m-%d')} till date, \
total count of {prstate} ( either open &/ closed ) \
pull requests are {resulting_prs.totalCount}
"""
        prstate_fields = get_specific_fields_of_pr(resulting_prs, prstate)
        append_report(report_name, prstate_fields)

    if "TO_EMAIL_ADDRESS" in os.environ:
        print("Fully functional in upcoming release")
        """
        from_address = os.environ['FROM_EMAIL_ADDRESS']
        # to_list expected input is comma separated
        to_list = os.environ['TO_EMAIL_ADDRESS'].split(",")
        smtp_server = os.environ['SMTP_SERVER']
        subj = 'Report of merged and unmerged GitHub PR in last week'
        send_mail(from_address, to_list, subj,
                  emailbody, [report_name], smtp_server)
        """
    else:
        # Print to console the details of the email you would send
        # (From, To, Subject, Body).
        from_address = "yours_truly@domain"
        # to_list expected input is comma separated
        to_list = "mgr@domain, scrummaster@domain"
        subj = 'Report of merged and unmerged GitHub PR in last week'
        print("Contents of the email would be")
        print(f" From: {from_address} \n \
                To: {to_list} \n \
                Subject: {subj} \n ")
        for line in emailbody:
            print(emailbody[line])
        print("CSV file  available locally at "+report_name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
