import os
from md_parser.converter import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, "r") as f:
        content = f.read()

    content_node = markdown_to_html_node(content)
    html_content = content_node.to_html()

    # Read template
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(content)

    # Replace placeholders
    html_page = template.replace("{{ Content }}", html_content)
    html_page = html_page.replace("{{ Title }}", title)

    # Replace paths with basepath
    html_page = html_page.replace('href="/', f'href="{basepath}')
    html_page = html_page.replace('src="/', f'src="{basepath}')

    # Create directories if needed
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the file
    with open(dest_path, "w") as f:
        f.write(html_page)
