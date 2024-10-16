import unittest
from unittest.mock import patch, MagicMock
from src.repo_analyzer.github_api import GitHubAPI


class TestGitHubAPI(unittest.TestCase):
    def setUp(self):
        # Initialize GitHubAPI with a mock token
        self.api = GitHubAPI(token='mock_token')

    @patch('src.repo_analyzer.github_api.Github.get_repo')
    def test_get_repo_structure(self, mock_get_repo):
        # Mock the response from get_repo and the tree structure
        mock_repo = MagicMock()
        mock_repo.get_git_tree.return_value = MagicMock(tree=[
            MagicMock(path='src/main.py', type='blob'),
            MagicMock(path='src/utils.py', type='blob'),
            MagicMock(path='src', type='tree'),
        ])
        mock_get_repo.return_value = mock_repo

        structure = self.api.get_repo_structure('https://github.com/octocat/Hello-World')

        self.assertEqual(len(structure), 3)
        self.assertEqual(structure[0]['name'], 'src/main.py')

    @patch('src.repo_analyzer.github_api.Github.get_repo')
    def test_get_repo_info(self, mock_get_repo):
        # Mock the response for repository info
        mock_repo = MagicMock()
        mock_repo.name = 'Hello-World'
        mock_repo.full_name = 'octocat/Hello-World'
        mock_repo.description = 'My first repository on GitHub!'
        mock_repo.stargazers_count = 2694
        mock_repo.forks_count = 2380
        mock_get_repo.return_value = mock_repo

        info = self.api.get_repo_info('https://github.com/octocat/Hello-World')

        self.assertEqual(info['name'], 'Hello-World')
        self.assertEqual(info['stars'], 2694)


if __name__ == "__main__":
    unittest.main()
