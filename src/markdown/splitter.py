from nodes.text_node import TextType, TextNode
from markdown.extractor import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown: missing closing delimiter")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                if len(part) != 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                if len(part) != 0:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)

        if not matches:
            new_nodes.append(node)
            continue

        edited_node = node
        for image_alt, image_url in matches:
            sections = edited_node.text.split(f"![{image_alt}]({image_url})", 1)
            if len(sections[0]) != 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_url))
            edited_node.text = sections[1]

        if len(edited_node.text) != 0:
            new_nodes.append(TextNode(edited_node.text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        if not matches:
            new_nodes.append(node)
            continue

        edited_node = node
        for link_text, link_url in matches:
            sections = edited_node.text.split(f"[{link_text}]({link_url})", 1)
            if len(sections[0]) != 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            edited_node.text = sections[1]

        if len(edited_node.text) != 0:
            new_nodes.append(TextNode(edited_node.text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    split_text = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD
    )
    split_text = split_nodes_delimiter(split_text, "_", TextType.ITALIC)
    split_text = split_nodes_delimiter(split_text, "`", TextType.CODE)
    split_text = split_nodes_image(split_text)
    split_text = split_nodes_link(split_text)

    return split_text
