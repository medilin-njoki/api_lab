import requests
from collections import Counter
import json


def api_get(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data", response.status_code)

def print_json_str(str):
    print(json.dumps(str, indent=4))

def get_top(list, n):
    counts = Counter(list)
    return counts.most_common(n)

def print_github_user_stats(github_user):
    # **Name:** Linus Torvalds  
    # - **Username:** torvalds  
    # - **Bio:** Software engineer, creator of Linux  
    # - **Public Repos:** 6  
    # - **Followers:** 250K  
    # - **Following:** 0  
    # - **Location:** Portland, OR  
    # - **Profile URL:** [https://github.com/torvalds](https://github.com/torvalds)  
    url = f"https://api.github.com/users/{github_user}"  # Replace <username> with the GitHub user

    data = api_get(url=url)

    print(f'Name: {data["name"]}')
    print(f'    Username: {data["login"]}')
    print(f'    Bio: {data["bio"]}')
    print(f'    Public Repos: {data["public_repos"]}')
    print(f'    Followers: {data["followers"]}')
    print(f'    Following: {data["following"]}')
    print(f'    Location: {data["location"]}')
    print(f'    Profile URL: {data["html_url"]}')
    print('')
    return data

def print_github_user_repos(repos_url):
    # ### Repositories

    # #### project1
    # - View Repo ([link here](#))  
    # - Stars: 160K  
    # - Language: C  
    # - Last Updated: 2024-10-02  
    # url = 'https://api.github.com/users/torvalds/repos'

    repos = api_get(url=repos_url)

    public_repos = [repo for repo in repos if not repo['private']]
    langages = []
    starred = {}

    print('## Repositories')
    print('')
    for repo in public_repos:
        print(f'*** {repo["name"]}')
        print(f'- View Repo {repo["html_url"]}')
        print(f'- Stars {repo["stargazers_count"]}')
        print(f'- Language {repo["language"]}')
        print(f'- Last Updated {repo["updated_at"].split('T')[0]}')
        print(f"url = '{repo['url']}'")
        print('')
        langages.append(repo['language'])
        starred[repo['name']] = repo['stargazers_count']
    return langages, starred

def print_top_langages(langages, n, total_number_of_repos):
    # ### Most Used Languages

    # - Python (80%)  
    # - SQL (10%) 

    print('## Most Used Languages')
    for top_langage in get_top(langages, n):
        print(f'- {top_langage[0]} ({top_langage[1]/total_number_of_repos*100}%)')
    print('')

def print_top_starred(starred, n):
    # ### Most Starred Repos

    # - project1 – 160K stars  
    # - project2 – 4.5K stars  
    # - linux-project3 – 1.2K stars  

    print('## Most Starred Repos')
    print('')
    for top_starred_project in sorted(starred.items(), key=lambda item: item[1], reverse=True)[0:n]:
        print(f'- {top_starred_project[0]} - {round(top_starred_project[1]/1000,1)}K starts')
    print('')

def print_all_github_user_stats(github_user):
    data = print_github_user_stats(github_user)
    langages, starred = print_github_user_repos(data['repos_url'])
    print_top_langages(langages, 2, data['public_repos'])
    print_top_starred(starred, 3)