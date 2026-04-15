from textnode import TextNode, TextType

print("hello world")


def main():
    test_TextNode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(test_TextNode)


main()
