import os
import json
from github import Github, GithubException
from urllib.parse import urlparse


class GitHubAPI:
    def __init__(self, token=None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError(
                "GitHub token is required. Set GITHUB_TOKEN environment variable or pass it to the constructor.")
        self.github = Github(self.token)

    def get_repo_structure(self, repo_url):
        owner, repo_name = self._parse_repo_url(repo_url)
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            default_branch = repo.default_branch
            tree = repo.get_git_tree(sha=default_branch, recursive=True)
            return self._traverse_tree(tree, repo)
        except GithubException as e:
            raise Exception(f"Error fetching repository: {e}")

    def _parse_repo_url(self, repo_url):
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")
        return path_parts[-2], path_parts[-1]

    def _traverse_tree(self, tree, repo, path=''):
        structure = []
        for content in tree.tree:
            if content.type == 'tree':
                structure.append({
                    'type': 'directory',
                    'name': content.path,
                    'path': os.path.join(path, content.path),
                    'contents': self._traverse_tree(repo.get_git_tree(content.sha), repo,
                                                    os.path.join(path, content.path))
                })
            else:
                structure.append({
                    'type': 'file',
                    'name': content.path,
                    'path': os.path.join(path, content.path)
                })
        return structure

    def get_repo_info(self, repo_url):
        owner, repo_name = self._parse_repo_url(repo_url)
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            return {
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'watchers': repo.watchers_count,
                'language': repo.language,
                'created_at': repo.created_at,
                'updated_at': repo.updated_at,
                'default_branch': repo.default_branch,
                'open_issues': repo.open_issues_count,
                'license': repo.license.name if repo.license else None,
            }
        except GithubException as e:
            raise Exception(f"Error fetching repository info: {e}")


def analyze_repository(repo_url):
    api = GitHubAPI()
    structure = api.get_repo_structure(repo_url)
    info = api.get_repo_info(repo_url)

    analysis = {
        'info': info,
        'file_count': count_files(structure),
        'directory_count': count_directories(structure),
        'max_depth': calculate_max_depth(structure),
        'file_types': count_file_types(structure),
    }

    return analysis


def count_files(structure, count=0):
    for item in structure:
        if item['type'] == 'file':
            count += 1
        elif item['type'] == 'directory':
            count = count_files(item['contents'], count)
    return count


def count_directories(structure, count=0):
    for item in structure:
        if item['type'] == 'directory':
            count += 1
            count = count_directories(item['contents'], count)
    return count


def calculate_max_depth(structure, current_depth=0):
    max_depth = current_depth
    for item in structure:
        if item['type'] == 'directory':
            depth = calculate_max_depth(item['contents'], current_depth + 1)
            max_depth = max(max_depth, depth)
    return max_depth


def count_file_types(structure):
    file_types = {}

    def count(items):
        for item in items:
            if item['type'] == 'file':
                ext = os.path.splitext(item['name'])[1].lower() or 'no_extension'
                file_types[ext] = file_types.get(ext, 0) + 1
            elif item['type'] == 'directory':
                count(item['contents'])

    count(structure)
    return file_types


def print_analysis(analysis):
    print("\nRepository Analysis:")
    print(f"Repository Name: {analysis['info']['name']}")
    print(f"Description: {analysis['info']['description']}")
    print(f"Stars: {analysis['info']['stars']}")
    print(f"Forks: {analysis['info']['forks']}")
    print(f"File Count: {analysis['file_count']}")
    print(f"Directory Count: {analysis['directory_count']}")
    print(f"Max Directory Depth: {analysis['max_depth']}")
    print("\nFile Types:")
    for file_type, count in analysis['file_types'].items():
        print(f"  {file_type}: {count}")


def main(repo_url):
    analysis_result = analyze_repository(repo_url)
    print_analysis(analysis_result)

    # Convert to JSON for easy input to LLM
    json_output = json.dumps(analysis_result, indent=2, default=str)
    print("\nJSON Output:")
    print(json_output)
    # In a real scenario, you might want to save this to a file or pass it directly to an LLM


if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL to analyze: ")
    main(repo_url)