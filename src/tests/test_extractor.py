import unittest
from markdown.extractor import extract_markdown_links, extract_markdown_images


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images("This is text without an image")
        self.assertListEqual([], matches)

    def test_extract_markdown_image_no_alt_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_no_url(self):
        matches = extract_markdown_images("This is text with an ![image]()")
        self.assertListEqual([("image", "")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links("This is text without a link")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_link_text(self):
        matches = extract_markdown_links(
            "This is text with a link [](https://www.boot.dev)"
        )
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_no_url(self):
        matches = extract_markdown_links("This is text with a link [to boot dev]()")
        self.assertListEqual([("to boot dev", "")], matches)


if __name__ == "__main__":
    unittest.main()
