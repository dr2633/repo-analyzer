# python -m unittest tests/test_analyzer.py

import unittest
from src.repo_analyzer.analyzer import format_structure, count_files, count_directories, calculate_max_depth


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        # Mock repository structure for testing
        self.mock_structure = [
            {
                'type': 'directory',
                'name': 'src',
                'path': 'src',
                'contents': [
                    {'type': 'file', 'name': 'main.py', 'path': 'src/main.py', 'extension': '.py'},
                    {'type': 'file', 'name': 'utils.py', 'path': 'src/utils.py', 'extension': '.py'},
                    {'type': 'directory', 'name': 'subdir', 'path': 'src/subdir', 'contents': [
                        {'type': 'file', 'name': 'helper.py', 'path': 'src/subdir/helper.py', 'extension': '.py'}
                    ]}
                ]
            },
            {'type': 'file', 'name': 'README.md', 'path': 'README.md', 'extension': '.md'},
        ]

    # Test for format_structure function
    def test_format_structure(self):
        formatted_structure = format_structure(self.mock_structure)
        self.assertEqual(formatted_structure[0]['type'], 'directory')
        self.assertEqual(formatted_structure[0]['name'], 'src')
        self.assertEqual(formatted_structure[0]['contents'][0]['name'], 'main.py')
        self.assertEqual(formatted_structure[1]['type'], 'file')
        self.assertEqual(formatted_structure[1]['name'], 'README.md')

    # Test for count_files function
    def test_count_files(self):
        file_count = count_files(self.mock_structure)
        self.assertEqual(file_count, 4)  # 4 files in the structure

    # Test for count_directories function
    def test_count_directories(self):
        directory_count = count_directories(self.mock_structure)
        self.assertEqual(directory_count, 2)  # src and src/subdir

    # Test for calculate_max_depth function
    def test_calculate_max_depth(self):
        max_depth = calculate_max_depth(self.mock_structure)
        self.assertEqual(max_depth, 2)  # Maximum depth is 2 due to src/subdir


if __name__ == "__main__":
    unittest.main()



