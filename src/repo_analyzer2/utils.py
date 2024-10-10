import os
from datetime import datetime

def get_directory_structure(root_dir, max_depth=None):
    """
    Generate the directory structure starting from root_dir.

    Args:
        root_dir (str): The root directory to start from.
        max_depth (int, optional): Maximum depth to traverse. Defaults to None (no limit).

    Returns:
        list: A list of dictionaries representing the directory structure.
    """
    structure = []
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        if max_depth is not None and level > max_depth:
            continue  # Skip directories beyond the max depth
        indent = ' ' * 4 * level
        folder = os.path.basename(root)
        if level == 0:
            structure.append({'type': 'dir', 'name': 'github-repo_analyzer2', 'contents': []})
            current = structure[0]['contents']
        else:
            current.append({'type': 'dir', 'name': folder, 'contents': []})
            current = current[-1]['contents']
        for f in files:
            current.append({'type': 'file', 'name': f})
    return structure


def filter_repo_structure(structure):
    """
    Filter the repository structure to include only desired directories and files.

    Args:
        structure (list): The original directory structure.

    Returns:
        dict: The filtered directory structure.
    """
    # List of directories and files to include
    desired_dirs = ['src', 'tests', 'examples', 'web', 'templates', 'static', 'css', 'js']
    desired_files = ['.gitignore', 'README.md', 'requirements.txt', 'setup.py', 'repository_structure.txt',
                     '__init__.py', 'analyzer.py', 'github_api.py', 'json_converter.py', 'utils.py',
                     'test_analyzer.py', 'test_github_api.py', 'test_json_converter.py', 'analyze_example_repo.py',
                     'app.py', 'index.html', 'style.css', 'main.js']

    def filter_item(item):
        # If it's a directory and in desired_dirs, process its contents recursively
        if item['type'] == 'dir':
            if item['name'] in desired_dirs or item['name'] == 'github-repo_analyzer2':
                filtered_contents = [filter_item(i) for i in item['contents']]
                filtered_contents = [i for i in filtered_contents if i is not None]
                if filtered_contents or item['name'] == 'github-repo_analyzer2':  # Include non-empty directories
                    return {'type': 'dir', 'name': item['name'], 'contents': filtered_contents}
        # If it's a file and in desired_files, include it
        elif item['type'] == 'file' and item['name'] in desired_files:
            return item
        return None  # Exclude items that don't match the filters

    return filter_item(structure[0])


def structure_to_text(structure, indent=''):
    """
    Convert the filtered structure dictionary to a text representation.

    Args:
        structure (dict): The directory structure to convert.
        indent (str, optional): The indentation level for pretty formatting. Defaults to ''.

    Returns:
        list: A list of lines representing the directory structure in text format.
    """
    text = []
    if structure['type'] == 'dir':
        if structure['name'] != 'github-repo_analyzer2':
            text.append(f"{indent}{structure['name']}/")
        if not structure['contents']:
            text.append(f"{indent}    (empty directory)")  # Note for empty directories
        for item in structure['contents']:
            text.extend(structure_to_text(item, indent + '    '))
    else:
        text.append(f"{indent}{structure['name']}")
    return text


def update_repository_structure(root_dir=None, max_depth=None):
    """
    Update the repository_structure.txt file with the current directory structure.

    Args:
        root_dir (str, optional): The root directory of the repository. Defaults to the current working directory.
        max_depth (int, optional): Maximum depth to traverse. Defaults to None (no limit).
    """
    if root_dir is None:
        root_dir = os.getcwd()

    try:
        # Get the full directory structure and filter it
        structure = get_directory_structure(root_dir, max_depth)
        filtered_structure = filter_repo_structure(structure)
        structure_text = structure_to_text(filtered_structure)

        # Write the directory structure to the repository_structure.txt file
        with open(os.path.join(root_dir, 'repository_structure.txt'), 'w') as f:
            f.write('\n'.join(structure_text))
            f.write(f"\n\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Repository structure updated in {root_dir}/repository_structure.txt")
    except Exception as e:
        print(f"Error updating repository structure: {e}")


if __name__ == "__main__":
    # Update the repository structure and save it to repository_structure.txt
    update_repository_structure(max_depth=3)  # You can modify max_depth if needed
