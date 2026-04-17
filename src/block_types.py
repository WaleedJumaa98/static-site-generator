from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    elif block.startswith(">"):
        blocks = block.split("\n")
        for b in blocks:
            if not b.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    elif block.startswith("- "):
        blocks = block.split("\n")
        for b in blocks:
            if not b.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    elif block[0].isdigit():
        blocks = block.split("\n")
        for i in range(len(blocks)):
            if not blocks[i].startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH

        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH
