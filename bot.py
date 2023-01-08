from github import Github
from my_token import MY_TOKEN


g = Github(MY_TOKEN)

for repo in g.get_user().get_repos():
    print(repo.name)