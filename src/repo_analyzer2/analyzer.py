import json
from datetime import datetime

def analyze_repository(repo_url):
    api = GitHubAPI()
    structure = api.get_repo_structure(repo_url)
    info = api.get_repo_info(repo_url)

    analysis = {
        'info': info,
        'structure': format_structure(structure),
        'summary': {
            'file_count': count_files(structure),
            'directory_count': count_directories(structure),
            'max_depth': calculate_max_depth(structure),
            'file_types': count_file_types(structure),
        }
    }

    return analysis

def print_analysis(analysis):
    print("\nRepository Analysis:")
    print(f"Repository Name: {analysis['info']['name']}")
    print(f"Description: {analysis['info']['description']}")
    print(f"Stars: {analysis['info']['stars']}")
    print(f"Forks: {analysis['info']['forks']}")
    print(f"File Count: {analysis['summary']['file_count']}")
    print(f"Directory Count: {analysis['summary']['directory_count']}")
    print(f"Max Directory Depth: {analysis['summary']['max_depth']}")
    print("\nFile Types:")
    for file_type, count in analysis['summary']['file_types'].items():
        print(f"  {file_type}: {count}")


def main(repo_url, output_dir):
    try:
        analysis_result = analyze_repository(repo_url)
        print_analysis(analysis_result)

        nl_generator = NLExplanationGenerator()
        explanation = nl_generator.generate_explanation(analysis_result)

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"repo_analysis_{timestamp}.json"
        json_filepath = os.path.join(output_dir, json_filename)

        # Serialize the JSON, ensuring datetime objects are converted to strings
        with open(json_filepath, 'w') as f:
            json.dump(analysis_result, f, indent=2, default=str)  # <-- Add default=str
        print(f"\nFull analysis saved to {json_filepath}")

        nl_filename = f"repo_explanation_{timestamp}.txt"
        nl_filepath = os.path.join(output_dir, nl_filename)

        with open(nl_filepath, 'w') as f:
            f.write(explanation)
        print(f"\nNatural language explanation saved to {nl_filepath}")

        print("\nNatural Language Explanation:")
        print(explanation)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
