# Repository Structure Analyzer

This tool analyzes the structure of GitHub repositories, providing insights and a standardized format for use with Language Models (LLMs) in software development tasks.

## Features

- Fetches repository structure from GitHub
- Generates a summary of repository contents
- Produces JSON output for easy LLM integration

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
python -c "from src.repo_analyzer.utils import update_repository_structure; import os; update_repository_structure(os.getcwd())"
```


```python
from repo_analyzer import analyze_repository

repo_url = "https://github.com/username/repo"
analysis = analyze_repository(repo_url)
print(analysis)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.