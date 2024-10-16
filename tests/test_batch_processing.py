# python -m unittest tests/test_batch_processing.py

import unittest
import os
import csv
from unittest.mock import patch, MagicMock
from src.repo_analyzer.analyzer import analyze_repository


class TestBatchProcessing(unittest.TestCase):
    def setUp(self):
        # Mock CSV file content with repository URLs
        self.mock_csv_file = 'test_repos.csv'
        with open(self.mock_csv_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['repository_url'])
            writer.writerow(['https://github.com/octocat/Hello-World'])
            writer.writerow(['https://github.com/octocat/Spoon-Knife'])

        # Prepare an output directory for storing JSON outputs
        self.output_dir = 'test_outputs'
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        # Clean up test files
        os.remove(self.mock_csv_file)
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            os.remove(file_path)
        os.rmdir(self.output_dir)

    @patch('src.repo_analyzer.analyzer.analyze_repository')
    def test_batch_process_repositories(self, mock_analyze_repository):
        # Mocking the output for repository analysis
        mock_analyze_repository.return_value = {
            'info': {'name': 'Hello-World', 'full_name': 'octocat/Hello-World'},
            'structure': [], 'summary': {}
        }

        # Batch processing function (replace with your actual batch function)
        def process_csv_and_analyze(csv_file, output_dir):
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    repo_url = row['repository_url']
                    result = analyze_repository(repo_url)
                    output_file = os.path.join(output_dir, f"repo_analysis_{result['info']['name']}.json")
                    with open(output_file, 'w') as f:
                        f.write(str(result))

        # Run the batch processing function
        process_csv_and_analyze(self.mock_csv_file, self.output_dir)

        # Check that JSON files are created for each repository
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'repo_analysis_Hello-World.json')))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'repo_analysis_Spoon-Knife.json')))
        self.assertEqual(mock_analyze_repository.call_count, 2)  # Ensure analyze_repository was called twice


if __name__ == "__main__":
    unittest.main()
