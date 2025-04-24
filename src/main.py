from textnode import *
from htmlnode import *
from inline import *
from markdown_blocks import *
import os
import shutil
from pathlib import Path
from generate_page import *


def main():
    delete_and_copy('public','static')
    #title = (extract_title("This is normal text\n\n# heading1   \n\n\n\n"))
    #print(f"the title is {title} and it is {len(title)} long")
    generate_pages_recursive("content", "template.html", "public")
    #generate_page("content", "template.html", "public")
    return 

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

def delete_and_copy(dest_rel_path="",source_rel_path=""):
    public_folder = os.path.normpath(os.path.join(current_dir, '..', dest_rel_path))
    static_folder = os.path.normpath(os.path.join(current_dir, '..', source_rel_path))

    delete_contents(public_folder)
    base_dir = Path("static")
    #print(f"the path is {base_dir}")
    # create a list of the folders/files in static
    tree_list = os.listdir(static_folder)
    #print(tree_list, static_folder)
    
    copy_files(tree_list,static_folder,public_folder)
    #for item in tree_list:
    #    print(f" the item is a file? {os.path.isfile(os.path.join(static_folder,item))}")
    return 

def copy_files(parent_directory_list, current_filepath="",dest_path=""):
    #print(f"the parent directory list is {parent_directory_list}")
    #print(f"the cfp is {current_filepath}")
    
    if dest_path == "":
        dest_path = 'public'
    #print(f"the dest_path is {dest_path}")
    os.makedirs(dest_path, exist_ok=True)
    paths = []
    if parent_directory_list == []: 
        return 
    for item in parent_directory_list:
        new_path = os.path.join(current_filepath,item)
        new_dest = os.path.join(dest_path,item)
        
        
        #print(f"the new path is {new_path}")
        if  os.path.isfile(new_path) == True:
            #print(f"copying file {new_path}")
            shutil.copy(new_path, dest_path)
            #print("finished file copy")
        else:
            #print(f"calling recursive function on {new_path} with dest path {new_dest}")

            copy_files(os.listdir(new_path),new_path,new_dest)
    return 
if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
#    public_folder = os.path.normpath(os.path.join(current_dir, '..', 'public'))
#    static_folder = os.path.normpath(os.path.join(current_dir, '..', 'static'))
    
main()

