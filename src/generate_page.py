import os
from md_parser.converter import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read the content of from_path
    with open(from_path, "r") as f:
        content = f.read()
    content_node = markdown_to_html_node(content)
    html_content = content_node.to_html()
    # Read the template
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(content)

    template_with_content = template.replace("{{ Content }}", html_content)
    template_with_content_and_title = template_with_content.replace(
        "{{ Title }}", title
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_with_content_and_title)
