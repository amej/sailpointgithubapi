# sailpointgithubapi
The repository contains the implementation for generating email based report containing the closed,merged and open github PRs for a given public repository.
Author:
Ameya Sathe


Prerequisite:
Mandatory:
Python 3.9
Python package PyGithub
Python package python-csv
An OS environment variable GITHUB_TOKEN set to personal access token
Existence of /var/tmp

Optional:
PUBLIC_REPO set to github based public repository in form of org/repo .  Default value: kubernetes/kubernetes


How to run:
Standalone command:
1.  export GITHUB_TOKEN = bak-blah-buk-blah ; export PUBLIC_REPO = ...
2. python https://github.com/amej/sailpointgithubapi/blob/main/retrievegithubapi.py 

Using Container engine:
1. podman pull quay.io/asathe/githubapi@sha256:a954c6f436569ed238b33f8629b7d38ecf7b62c83b40d7f9a8b7e4328a8d5d34
2. podman run -e GITHUB_TOKEN=blahblah -e PUBLIC_REPO=...  quay.io/asathe/githubapi@sha256:a954c6f436569ed238b33f8629b7d38ecf7b62c83b40d7f9a8b7e4328a8d5d34
