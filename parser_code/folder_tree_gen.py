import os

def print_tree(folder_path, indent=""):
    try:
        # List the contents of the directory
        files_and_folders = os.listdir(folder_path)
    except PermissionError:
        return  # Ignore folders/files without permission

    # Sort files and folders for better tree structure
    files_and_folders.sort()

    for index, item in enumerate(files_and_folders):
        path = os.path.join(folder_path, item)
        
        # Print the tree structure
        connector = "└── " if index == len(files_and_folders) - 1 else "├── "
        print(f"{indent}{connector}{item}")

        # If the item is a folder, recursively print its contents
        if os.path.isdir(path):
            new_indent = indent + ("    " if index == len(files_and_folders) - 1 else "│   ")
            print_tree(path, new_indent)

# Example usage
folder_path = "D:\\Code_genie\\Kishore\\parser_code"
print_tree(folder_path)
