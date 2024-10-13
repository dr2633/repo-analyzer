# GitHub Repository Analyzer

## Overview

The **GitHub Repository Analyzer** is a tool designed to extract, analyze, and evaluate the structure of GitHub repositories. It provides a JSON representation of a repository’s structure and enables users to compare it against best practices or a defined "gold standard" structure. This repository aims to improve the consistency, maintainability, and scalability of codebases by offering insights into the layout and organization of project files.

## Motivation 

A well-organized repository improves collaboration, reduces onboarding time for new developers, and ensures that projects are easier to maintain over time. However, there is often a disconnect between a repository's actual structure and best practices for organizing code, tests, documentation, and configuration files.

The GitHub Repository Analyzer addresses this gap by:
- Providing an automated way to assess the structure of any repository.
- Offering suggestions on improving repository organization.
- Facilitating the comparison of repository structures across similar projects, enabling the development of a "best practices" template for various domains (e.g., machine learning, web development, system programming).

With this tool, developers and teams can ensure their repositories adhere to best practices and are well-organized for long-term development.

---

## Instructions for Accessing and Using a GitHub Token

In order to interact with GitHub’s API, you'll need to generate and use a personal access token (PAT). Follow these steps to set it up:

### 1. Generate a GitHub Token:
- Go to [GitHub's Personal Access Tokens Page](https://github.com/settings/tokens).
- Click on **Generate new token**, provide a name and expiration date.
- Under **Scopes**, select `repo` (this allows access to repository contents).
- Generate and copy the token.

### 2. Set Your Token as an Environment Variable:
Open your terminal or command prompt and export the token as an environment variable:

```bash
export GITHUB_TOKEN='<YOUR_GITHUB_TOKEN>'
```

Replace `<YOUR_GITHUB_TOKEN>` with your actual token.

### 3. Verify Your Token:
You can check if the token has been correctly set using:

```bash
echo $GITHUB_TOKEN
```

### 4. Test Your Token:
Run the `check_token.py` script to verify that the token is working:

```bash
python check_token.py
```

### 5. Run the Analyzer:
After setting up the token, you can run the GitHub Repository Analyzer with the following command:

```bash
python src/repo_analyzer/analyzer.py <REPOSITORY_URL>
```

This will output the repository structure in JSON format and store the results for evaluation.

---

## Features

- **Extract Repository Structure**: Fetch the repository’s directory and file structure from GitHub and generate a JSON representation.
- **Evaluate Against Best Practices**: Compare the current structure against a "gold standard" or best practices structure to identify areas for improvement.
- **Natural Language Explanation (Optional)**: Generate an optional natural language summary of the repository’s structure based on the output.
- **Customizable Mapping Rules**: Define mapping rules for refactoring and reorganizing repositories to adhere to best practices.

---

## Example Usage

### Analyzing a Repository:
To analyze the structure of a GitHub repository, run the following command:

```bash
python src/repo_analyzer/analyzer.py https://github.com/octocat/Hello-World
```

This will:
- Retrieve the structure of the repository.
- Generate a JSON file representing the structure.
- Optionally, generate a natural language explanation of the structure.

### Mapping to a Gold Standard:
You can modify the repository's structure to match a "best practices" layout by configuring the mapping rules in the analyzer. This allows you to refactor repositories automatically.

---

## Motivation for Evaluating Repository Structure

### Why is Repository Structure Important?
A well-structured repository:
- **Improves collaboration**: Clear separation of concerns and organization helps developers understand where to find things, reducing time spent on onboarding and project navigation.
- **Enhances maintainability**: Consistent directory layouts and clear documentation make long-term maintenance easier, especially as projects scale.
- **Facilitates automation**: Standardized layouts enable smoother integrations with continuous integration and deployment pipelines, ensuring that the right files are in the right places for builds, tests, and deployments.

### Developing an Evaluation Framework:
The GitHub Repository Analyzer allows for a systematic evaluation of repository structures by:
- Extracting file and directory organization.
- Comparing the structure with best practices (e.g., ensuring files are located in `src/`, `tests/`, etc.).
- Providing automated refactoring suggestions based on predefined mapping rules.
- Encouraging consistency across projects by applying the same evaluation standards to different repositories.

---

## Contributing

If you'd like to contribute to this project:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

We welcome contributions that improve the analyzer, add additional evaluation metrics, or extend its functionality to other types of repositories.

---

## License

This project is licensed under the **Apache License 2.0**.
