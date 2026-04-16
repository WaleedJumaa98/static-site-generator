import re


def extract_markdown_images(image):

    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", image)
    return matches


def extract_markdown_links(link):

    matches = re.findall(r"\[(.*?)\]\((.*?)\)", link)
    return matches
