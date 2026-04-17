import sys
from copy_content import copy_files_recursive
from generate_pages_recursive import generate_pages_recursive


def main():
    # Get basepath from CLI argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Copy static files
    copy_files_recursive("static", "docs")

    # Generate all pages with the basepath
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
