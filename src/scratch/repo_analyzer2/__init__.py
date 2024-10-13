"""
GitHub Repository Analyzer

This package provides tools to analyze GitHub repositories, including:
- Fetching repository structure using the GitHub API.
- Converting the repository structure into a JSON format.
- Loading repository structure from a JSON file.

Modules:
- github_api: Handles GitHub API interactions.
- analyzer: Parses and analyzes repository structures.
- json_converter: Converts repository structures to and from JSON format.
"""

from .github_api import GitHubAPI
from .analyzer import analyze_repository
from .json_converter import to_json, from_json

# Defining __all__ to control what is exported when `import *` is used
__all__ = ['GitHubAPI', 'analyze_repository', 'to_json', 'from_json']
