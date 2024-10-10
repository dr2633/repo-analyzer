import os
from datetime import datetime


def get_directory_structure(root_dir):
    """
    Generate the directory structure starting from root_dir.
    """
    structure = []
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
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
    Filter the repository structure to include desired directories and files.
    """
    desired_dirs = [
        'src', 'tests', 'examples', 'web',
        'templates', 'static', 'css', 'js'
    ]
    desired_files = [
        '.gitignore', 'README.md', 'requirements.txt', 'setup.py',
        'repository_structure.txt', '__init__.py', 'analyzer.py',
        'github_api.py', 'json_converter.py', 'utils.py',
        'test_analyzer.py', 'test_github_api.py', 'test_json_converter.py',
        'analyze_example_repo.py', 'app.py', 'index.html', 'style.css', 'main.js'
    ]

    def filter_item(item):
        if item['type'] == 'dir':
            if item['name'] in desired_dirs or item['name'] == 'github-repo_analyzer2':
                filtered_contents = [filter_item(i) for i in item['contents']]
                filtered_contents = [i for i in filtered_contents if i is not None]
                if filtered_contents or item['name'] == 'github-repo_analyzer2':
                    return {'type': 'dir', 'name': item['name'], 'contents': filtered_contents}
        elif item['type'] == 'file' and item['name'] in desired_files:
            return item
        return None

    return filter_item(structure[0])


def structure_to_text(structure, indent=''):
    """
    Convert the filtered structure dictionary to a text representation.
    """
    text = []
    if structure['type'] == 'dir':
        if structure['name'] != 'github-repo_analyzer2':
            text.append(f"{indent}{structure['name']}/")
        for item in structure['contents']:
            text.extend(structure_to_text(item, indent + '    '))
    else:
        text.append(f"{indent}{structure['name']}")
    return text


def update_repository_structure(root_dir=None):
    """
    Update the repository_structure.txt file with the current directory structure.
    """
    if root_dir is None:
        root_dir = os.getcwd()

    structure = get_directory_structure(root_dir)
    filtered_structure = filter_repo_structure(structure)
    structure_text = structure_to_text(filtered_structure)

    with open(os.path.join(root_dir, 'repository_structure.txt'), 'w') as f:
        f.write('\n'.join(structure_text))
        f.write(f"\n\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    update_repository_structure()