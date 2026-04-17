import os
from pathlib import Path
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # List all entries in the content directory
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        # If it's a file and it's a markdown file
        if os.path.isfile(item_path) and item.endswith(".md"):
            # Generate the HTML page
            html_dest_path = dest_path.replace(".md", ".html")
            generate_page(item_path, template_path, html_dest_path)

        # If it's a directory, recurse into it
        elif os.path.isdir(item_path):
            # Recursively generate pages in the subdirectory
            generate_pages_recursive(item_path, template_path, dest_path)
