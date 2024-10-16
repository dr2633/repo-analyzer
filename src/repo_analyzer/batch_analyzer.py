# python src/repo_analyzer/batch_analyzer.py

import os
import csv  # or json
from src.repo_analyzer.analyzer import analyze_repository, print_analysis
import json

def read_repository_list(file_path):
    repositories = []
    with open(file_path, 'r') as f:
        # For CSV:
        reader = csv.reader(f)
        for row in reader:
            repositories.append(row[0])
        # For JSON:
        # repositories = json.load(f)
    return repositories

def main():
    input_file = '/repository-urls/repositories.csv'  # Updated file path
    output_dir = 'outputs/repositories'  # Custom folder for saving JSON files

    os.makedirs(output_dir, exist_ok=True)
    repositories = read_repository_list(input_file)

    for repo_url in repositories:
        try:
            analysis_result = analyze_repository(repo_url)
            print_analysis(analysis_result)

            repo_name = analysis_result['info']['name']
            json_filename = f"repo_analysis_{repo_name}.json"
            json_filepath = os.path.join(output_dir, json_filename)

            # Save the JSON output
            with open(json_filepath, 'w') as f:
                json.dump(analysis_result, f, indent=2, default=str)
            print(f"Saved analysis for {repo_name} to {json_filepath}")

        except Exception as e:
            print(f"Error processing {repo_url}: {e}")

if __name__ == "__main__":
    main()
