import requests
from github import Github
import os

def get_repo_structure(repo_url):
    # Extract owner and repo name from URL
    parts = repo_url.split('/')
    owner, repo_name = parts[-2], parts[-1]

    # Initialize PyGithub
    g = Github(os.getenv('GITHUB_TOKEN'))  # Use environment variable for token

    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")

    def traverse_tree(tree, path=''):
        structure = []
        for content in tree.tree:
            if content.type == 'tree':
                structure.append({
                    'type': 'directory',
                    'name': content.path,
                    'path': os.path.join(path, content.path),
                    'contents': traverse_tree(repo.get_git_tree(content.sha), os.path.join(path, content.path))
                })
            else:
                structure.append({
                    'type': 'file',
                    'name': content.path,
                    'path': os.path.join(path, content.path)
                })
        return structure

    # Get the default branch
    default_branch = repo.default_branch

    # Get the tree of the default branch
    tree = repo.get_git_tree(sha=default_branch, recursive=True)

    # Traverse the tree and build the structure
    repo_structure = traverse_tree(tree)

    return repo_structure