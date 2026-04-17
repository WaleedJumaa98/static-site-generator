import os
from md_parser.converter import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        content = f.read()

    html_content = markdown_to_html_node(content).to_html()

    with open(template_path, "r") as f:
        template = f.read()

    html_page = template.replace("{{ Content }}", html_content)
    html_page = html_page.replace("{{ Title }}", extract_title(content))
    html_page = html_page.replace('href="/', f'href="{basepath}')
    html_page = html_page.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_page)


def generate_pages_recursive(content_dir, template_path, dest_dir, basepath="/"):
    for item in os.listdir(content_dir):
        item_path = os.path.join(content_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(item_path) and item.endswith(".md"):
            generate_page(item_path, template_path, dest_path.replace(".md", ".html"), basepath)
        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, dest_path, basepath)
