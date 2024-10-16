import unittest
import os
from unittest.mock import patch, MagicMock
from src.repo_analyzer.analyzer import analyze_repository

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Prepare an output directory for storing JSON outputs
        self.output_dir = 'test_outputs'
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        # Clean up the test output directory
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            os.remove(file_path)
        os.rmdir(self.output_dir)

    @patch('src.repo_analyzer.github_api.GitHubAPI.get_repo_structure')
    @patch('src.repo_analyzer.github_api.GitHubAPI.get_repo_info')
    def test_analyze_repository(self, mock_get_repo_info, mock_get_repo_structure):
        # Mock repository structure and info
        mock_get_repo_info.return_value = {'name': 'Hello-World', 'full_name': 'octocat/Hello-World'}
        mock_get_repo_structure.return_value = [
            {'type': 'file', 'name': 'README.md', 'path': 'README.md', 'extension': '.md'}
        ]

        # Run the repository analyzer
        result = analyze_repository('https://github.com/octocat/Hello-World')

        # Ensure result has the expected structure and info
        self.assertEqual(result['info']['name'], 'Hello-World')
        self.assertEqual(result['structure'][0]['name'], 'README.md')

if __name__ == "__main__":
    unittest.main()
