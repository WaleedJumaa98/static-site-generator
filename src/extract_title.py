def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            # Remove the "# " and return the title
            return line[2:].strip()

    raise Exception("No h1 header found")
