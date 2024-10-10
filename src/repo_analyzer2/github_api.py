"""
GitHub API interaction module for the Repository Analyzer.
"""

import os
import logging
import time
from github import Github, GithubException, RateLimitExceededException
from urllib.parse import urlparse
from datetime import datetime


class GitHubAPI:
    def __init__(self, token=None):
        """
        Initializes the GitHubAPI class with a GitHub token.

        Args:
            token (str, optional): A GitHub token for authenticated requests.
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError(
                "GitHub token is required. Set GITHUB_TOKEN environment variable "
                "or pass it to the constructor. You can create a token at https://github.com/settings/tokens"
            )
        self.github = Github(self.token)

    def get_repo_structure(self, repo_url):
        """
        Fetches the repository structure recursively via the GitHub API.

        Args:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            list: A nested dictionary representing the repository's structure.
        """
        owner, repo_name = self._parse_repo_url(repo_url)
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            default_branch = repo.default_branch
            tree = repo.get_git_tree(sha=default_branch, recursive=True)
            return self._traverse_tree(tree, repo)
        except RateLimitExceededException:
            self._handle_rate_limit()
            return self.get_repo_structure(repo_url)
        except GithubException as e:
            raise Exception(f"Error fetching repository: {e}")

    def _handle_rate_limit(self):
        """
        Handles GitHub API rate limits by waiting until the rate limit resets.
        """
        rate_limit = self.github.get_rate_limit().core
        reset_time = rate_limit.reset - datetime.now().timestamp()
        logging.warning(f"Rate limit exceeded. Waiting for {reset_time} seconds.")
        time.sleep(reset_time)

    def _parse_repo_url(self, repo_url):
        """
        Parses a GitHub URL and extracts the owner and repository name.

        Args:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            tuple: The owner and repository name.
        """
        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")
        return path_parts[-2], path_parts[-1]

    def _traverse_tree(self, tree, repo, path=''):
        """
        Recursively traverses the GitHub repository tree.

        Args:
            tree (github.GitTree): The repository tree object.
            repo (github.Repository.Repository): The repository object.
            path (str, optional): The current file path during traversal.

        Returns:
            list: The nested directory structure.
        """
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
        """
        Retrieves metadata about the GitHub repository.

        Args:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            dict: Repository metadata.
        """
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


if __name__ == "__main__":
    # Test the GitHubAPI class
    logging.basicConfig(level=logging.INFO)

    api = GitHubAPI()
    test_repo_url = "https://github.com/octocat/Hello-World"

    print("Testing get_repo_structure:")
    structure = api.get_repo_structure(test_repo_url)
    print(structure[:2])  # Print first two items to avoid long output

    print("\nTesting get_repo_info:")
    info = api.get_repo_info(test_repo_url)
    print(info)
