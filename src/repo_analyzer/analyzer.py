import os
import requests
from github import Github
import json

def get_repo_structure(repo_url):
    # Extract owner and repo name from URL
    parts = repo_url.split('/')
    owner, repo_name = parts[-2], parts[-1]

    # Initialize PyGithub
    g = Github()  # You might need to use an access token for private repos

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

def generate_repo_summary(repo_structure):
    summary = {
        'total_files': 0,
        'total_directories': 0,
        'file_types': {},
        'top_level_structure': []
    }

    def count_items(structure):
        for item in structure:
            if item['type'] == 'file':
                summary['total_files'] += 1
                ext = os.path.splitext(item['name'])[1]
                summary['file_types'][ext] = summary['file_types'].get(ext, 0) + 1
            else:
                summary['total_directories'] += 1
                count_items(item['contents'])

    count_items(repo_structure)

    # Summarize top-level structure
    for item in repo_structure:
        if item['type'] == 'directory':
            summary['top_level_structure'].append(f"Directory: {item['name']}")
        else:
            summary['top_level_structure'].append(f"File: {item['name']}")

    return summary

def main(repo_url):
    repo_structure = get_repo_structure(repo_url)
    repo_summary = generate_repo_summary(repo_structure)

    # Convert to JSON for easy input to LLM
    json_output = json.dumps({
        'structure': repo_structure,
        'summary': repo_summary
    }, indent=2)

    print(json_output)
    # In a real scenario, you might want to save this to a file or pass it directly to an LLM

if __name__ == "__main__":
    repo_url = "https://github.com/username/repo"  # Replace with actual repo URL
    main(repo_url)