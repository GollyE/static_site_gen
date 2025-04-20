from textnode import *
from htmlnode import *
from inline import *
from markdown_blocks import *
import os
import shutil


def main():
    delete_and_copy()

def delete_contents(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Delete file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Delete folder and its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def delete_and_copy():
    delete_contents(public_folder)
    return f"deleted the contents of {public_folder}"


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    public_folder = os.path.normpath(os.path.join(current_dir, '..', 'public'))

    
main()

