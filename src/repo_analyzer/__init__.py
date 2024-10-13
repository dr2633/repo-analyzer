"""
GitHub Repository Analyzer

This package provides tools to analyze GitHub repositories, including:
- Fetching repository structure using the GitHub API.
- Analyzing repository structure and generating JSON output.

Modules:
- github_api: Handles GitHub API interactions.
- analyzer: Parses and analyzes repository structures.
"""

from .github_api import GitHubAPI
from .analyzer import analyze_repository

__all__ = ['GitHubAPI', 'analyze_repository']

