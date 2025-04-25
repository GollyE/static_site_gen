from markdown_blocks import *
from htmlnode import *
import os
import shutil
from pathlib import Path


def generate_page(rel_from_path, rel_template_path,rel_dest_path,basepath):
    print(f"Generating page from {Path(rel_from_path)} to {rel_dest_path} using {rel_template_path}.")
    with open(Path(rel_from_path), 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    with open(Path(rel_template_path), 'r', encoding='utf-8') as template_f:
        template_content = template_f.read()
    
    dest_file_name = rel_dest_path.removesuffix(".md")
    dest_file_name = f"{dest_file_name}.html"
    


    os.makedirs(os.path.dirname(dest_file_name), exist_ok=True)
    
    md_htmlnode = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)
    html_string = md_htmlnode.to_html()
    
    template_replaced_title = template_content.replace("{{ Title }}", title)
    final_html_content = template_replaced_title.replace("{{ Content }}", html_string)
    final_html_content = final_html_content.replace('href="/', f'href="{basepath}')
    final_html_content = final_html_content.replace('src="/', f'src="{basepath}')

    # Write to destination file
    
    with open(dest_file_name, 'w') as dest_file:
        dest_file.write(final_html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)

        #dest_file_name = filename.removesuffix(".md")
        #dest_file_name = f"{dest_file_name}.html"
        dest_file_path = os.path.join(dest_dir_path,filename)
        
        #print(f"the file path is {file_path}")
        #print(f"the dest file path is {dest_file_path}")
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                generate_page(file_path,template_path,dest_file_path,basepath)   
                #print(f"in file loop with {file_path}, {template_path}, and {dest_file_path}")  
            elif os.path.isdir(file_path):
                generate_pages_recursive(file_path,template_path,dest_file_path,basepath)
                a = f"is directory error"
        except Exception as e:
            print(f'Operation failed:{file_path}. Reason: {e}')