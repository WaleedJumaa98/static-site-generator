from md_parser.blocks import BlockType, block_to_block_type, markdown_to_blocks
from md_parser.inline import text_to_textnodes
from nodes.html_node import LeafNode, ParentNode
from nodes.text_node import TextType


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(
            "img", None, props={"src": text_node.url, "alt": text_node.text}
        )


def markdown_to_html_node(markdown):
    block_nodes = []
    html_blocks = markdown_to_blocks(markdown)

    for block in html_blocks:

        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            # Replace newlines with spaces for paragraphs
            paragraph_text = block.replace("\n", " ")
            children_node = text_to_children(paragraph_text)
            parent_node = ParentNode("p", children_node)
            block_nodes.append(parent_node)

        elif block_type == BlockType.HEADING:
            header_level = block.count("#")
            children_node = text_to_children(block[header_level:].strip())
            parent_node = ParentNode(
                f"h{header_level}",
                children_node,
            )
            block_nodes.append(parent_node)

        elif block_type == BlockType.CODE:
            code_content = block[3:-3].strip()
            code_node = LeafNode("code", code_content)
            parent_node = ParentNode("pre", [code_node])
            block_nodes.append(parent_node)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_lines = []
            for line in lines:
                # Remove leading > and optional space
                quote_lines.append(line[1:].strip())
            quote_content = "\n".join(quote_lines)
            children_node = text_to_children(quote_content)
            parent_node = ParentNode("blockquote", children_node)
            block_nodes.append(parent_node)

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.split("\n")
            children_nodes = []
            for item in list_items:
                item_content = item[2:].strip()
                item_children = text_to_children(item_content)
                children_nodes.append(ParentNode("li", item_children))
            parent_node = ParentNode("ul", children_nodes)
            block_nodes.append(parent_node)

        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.split("\n")
            children_nodes = []
            for item in list_items:
                item_content = item[item.find(". ") + 2 :].strip()
                item_children = text_to_children(item_content)
                children_nodes.append(ParentNode("li", item_children))
            parent_node = ParentNode("ol", children_nodes)
            block_nodes.append(parent_node)

    return ParentNode("div", block_nodes)


def text_to_children(markdown_text):
    # text is a string
    # Convert string to TextNodes (with inline markdown)
    text_nodes = text_to_textnodes(markdown_text)

    # Convert TextNodes to HTMLNodes
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes
