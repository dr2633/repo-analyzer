import os
import json


def aggregate_analysis(output_dir):
    stats = {
        'total_repos': 0,
        'avg_file_count': 0,
        'avg_directory_count': 0,
        'common_file_types': {}
    }

    json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]

    for json_file in json_files:
        with open(os.path.join(output_dir, json_file), 'r') as f:
            repo_data = json.load(f)
            stats['total_repos'] += 1
            stats['avg_file_count'] += repo_data['summary']['file_count']
            stats['avg_directory_count'] += repo_data['summary']['directory_count']

            for file_type, count in repo_data['summary']['file_types'].items():
                stats['common_file_types'][file_type] = stats['common_file_types'].get(file_type, 0) + count

    # Compute averages
    stats['avg_file_count'] /= stats['total_repos']
    stats['avg_directory_count'] /= stats['total_repos']

    print("Aggregate Statistics:", stats)


if __name__ == "__main__":
    aggregate_analysis('outputs/repositories/')
