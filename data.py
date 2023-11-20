from datetime import datetime
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

GHTOKEN = os.getenv("GHTOKEN")
GHURL = os.getenv("GHURL")
GHORG = os.getenv("GHORG")

print(GHURL, GHORG)

def get_repo(org=GHORG, repos=True, *args):
    if repos:
        return requests.get(f"{GHURL}/orgs/{org}/repos").json()

    headers = {'Authorization': f'token {GHTOKEN}'}
    url = f"{GHURL}/repos/{org}"
    for arg in args:
        url += f"/{arg}"
    return requests.get(url, headers=headers).json()

def filter_images(json_list):
    for content in json_list:
        if content['type'] == 'file' and content['path'].endswith(('.jpg','.gif','.png')):
            image_url = content['download_url']
            return image_url

    return None

def get_data(org=GHORG):
    repo_list = []
    for repo in get_repo(org=org, repos=True):
        project = repo['name']

        repo = get_repo(org, False, project)
        tags = get_repo(org, False, project, "tags")
        contents = get_repo(org, False, project, "contents")
        commits = sorted(get_repo(org, False, project, "commits"), key=lambda commit: commit['commit']['author']['date'])
        languages = get_repo(org, False, project, "languages")

        #Mapping Data
        item = { "user": repo['parent']['owner']['login'],
                 "repo": repo,
                 "avatar": repo['parent']['owner']['avatar_url'],
                 "description": repo['description'],
                 "tags": tags,
                 "images": filter_images(contents),
                 "commits": commits,
                 "commit_count": len(commits),
                 "commit_latest": commits[-1],
                 "commit_latest_date": commits[-1]['commit']['author']['date'],
                 "commit_latest_message": commits[-1]['commit']['message'],
                 "commit_histogram_daily": get_commit_histogram(commits),
                 "languages": languages,
               }

        repo_list.append(item)

    with open('data.json', 'w') as f:
        json.dump(repo_list, f)

    return repo_list

def get_commit_histogram(commits):
    dates = []
    for commit in commits:
        dates.append(datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ").day)
    return dates

def sparkline(data, figsize=(4,0.25),**kwags):
    data = list(data)
    fig,ax = plt.subplots(1,1,figsize=figsize,**kwags)
    ax.plot(data)

    for k,v in ax.spines.items():
        v.set_visible(False)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.plot(len(data)-1, data[len(data)-1], 'r.')

    ax.fill_between(range(len(data)), data, len(data)*[min(data)], alpha=0.1)

    img = BytesIO()
    plt.savefig(img, transparent=True, bbox_inches='tight')
    img.seek(0)
#     plt.show()
    plt.close()

    return base64.b64encode(img.read()).decode("utf-8")
