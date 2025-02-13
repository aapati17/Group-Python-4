import os
import shutil
import javalang
import git
import git.repo
from collections import defaultdict

def _clone_github_repo(repo_url: str, local_path: str) -> None:
    """
    If user selects to get LCOMHS for a public GitHub repository

    param: repo_url: remote GitHub Repository URL
    param: local_path: local repository to clone the repository
    """
    git.repo.clone_from(repo_url, local_path)


def _get_java_files(directory: any) -> list[any]:
    """
    Extract all Java files from the Repository

    param: directory: location of local directory
    """
    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    
    return java_files


def _parse_java_code(file_path: any) -> dict[any]:
    """
    Parse all Java files from the Repository

    param: directory: location of local directory
    return: dictionary of details for a Java class
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    try:
        tree = javalang.parse.parse(content)
    except javalang.parser.JavaSyntaxError as e:
        print(f"Error parsing {file_path}: {e}")
        return None
    
    class_info = {'methods': set(), 'fields': set(), 'method_fields': defaultdict(set)}

    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        # Process variables
        for field in node.fields:
            for declarator in field.declarators:
                class_info['fields'].add(declarator.name)
        
        # Process methods
        for method in node.methods:
            method_name = method.name
            class_info['methods'].add(method_name)

            # Analyze method body to find field access
            if method.body:
                for statement in method.body:
                    if isinstance(statement, javalang.tree.MemberReference):
                        if statement.member in class_info['fields']:
                            class_info['method_fields'][method.name].add(statement.member)
    
    return class_info


def calculate_lcomhs(class_info: dict[any]) -> float:
    """
    Calculating LCOMHS metric using formula:
    LCOMHS = (M - sum(MF) / F) / (M - 1)
    """
    M = len(class_info['methods'])
    F = len(class_info['fields'])

    if M <= 1 or F == 0:
        return 0    # LCOMHS is undefined for these cases
    
    sum_MF = sum(len(fields) for fields in class_info['method_fields'].values())

    lcomhs = (M - sum_MF / F) / (M - 1)
    return max(0, min(lcomhs, 2))

def process_directory(directory) -> any:
    """
    Process all Java files in a directory and calculate LCOMHS metrics

    param: directory: location of local directory
    return: average LCOMHS metric (if found) otherwise an error message
    """
    java_files = _get_java_files(directory)
    lcomhs_values = []

    for file in java_files:
        print(f"Processing: {file}")
        class_info = _parse_java_code(file)

        if not class_info:
            continue

        lcomhs = calculate_lcomhs(class_info)
        lcomhs_values.append(lcomhs)
    
    if lcomhs_values:
        avg_lcomhs = sum(lcomhs_values) / len(lcomhs_values)
        return avg_lcomhs
    else:
        return ("No valid Java files found or parsed.")