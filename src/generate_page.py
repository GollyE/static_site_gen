from markdown_blocks import *
from htmlnode import *
import os
import shutil
from pathlib import Path


def generate_page(rel_from_path, rel_template_path,rel_dest_path):
    print(f"Generating page from {Path(rel_from_path)} to {rel_dest_path} using {rel_template_path}.")
    with open(Path(rel_from_path), 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    with open(Path(rel_template_path), 'r', encoding='utf-8') as template_f:
        template_content = template_f.read()
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(rel_dest_path), exist_ok=True)
    
    md_htmlnode = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)
    html_string = md_htmlnode.to_html()
    
    template_replaced_title = template_content.replace("{{ Title }}", title)
    final_html_content = template_replaced_title.replace("{{ Content }}", html_string)
    
    # Write to destination file
    with open(rel_dest_path, 'w') as dest_file:
        dest_file.write(final_html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                pass        
            elif os.path.isdir(file_path):
                pass
        except Exception as e:
            print(f'Operation failed:{file_path}. Reason: {e}')
        
    
    pass