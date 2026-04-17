import os
from generate_page import generate_page


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(item_path) and item.endswith(".md"):
            html_dest_path = dest_path.replace(".md", ".html")
            generate_page(item_path, template_path, html_dest_path, basepath)

        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, dest_path, basepath)
