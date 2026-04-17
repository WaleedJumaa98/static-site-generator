# Static Site Generator

A Python static site generator that converts Markdown files into a fully-linked HTML website. Write content in Markdown, run one command, and get a ready-to-deploy site.

## How it works

```
content/*.md  +  template.html  →  docs/*.html
static/                         →  docs/  (CSS, images, etc.)
```

The generator:
1. Copies everything in `static/` to `docs/`
2. Walks `content/`, converts each `.md` file to HTML using a template, and writes the result to `docs/`

## Project structure

```
static-site-generator/
├── main.sh              # Local dev server
├── build.sh             # Build for GitHub Pages deployment
├── test.sh              # Run all tests
├── template.html        # HTML template ({{ Title }}, {{ Content }})
│
├── content/             # Markdown source files
│   ├── index.md
│   ├── contact/
│   └── blog/
│
├── static/              # Static assets copied as-is to docs/
│   ├── index.css
│   └── images/
│
├── docs/                # Generated output (served by GitHub Pages)
│
├── src/                 # Python source
│   ├── main.py          # Entry point
│   │
│   ├── ssg/             # Site generation
│   │   ├── builder.py   # Page generation + title extraction
│   │   └── assets.py    # Static file copying
│   │
│   ├── md_parser/       # Markdown parsing pipeline
│   │   ├── blocks.py    # Block-level parsing (headings, lists, code, quotes)
│   │   ├── inline.py    # Inline parsing (bold, italic, links, images)
│   │   └── converter.py # Converts parsed markdown to HTML node tree
│   │
│   └── nodes/           # Data models
│       ├── text_node.py  # Inline text representation
│       └── html_node.py  # HTML node tree (LeafNode, ParentNode)
│
└── tests/               # Unit tests (mirrors src/ structure)
```

## Usage

### Local development

```bash
bash main.sh
```

Builds the site with basepath `/` and starts a server at `http://localhost:8888`.

### Build for GitHub Pages

```bash
bash build.sh
```

Builds the site with the correct basepath for GitHub Pages (`/static-site-generator/`), then commit and push `docs/`.

### Run tests

```bash
bash test.sh
```

## Adding content

1. Create a new `.md` file under `content/`, e.g. `content/blog/my-post/index.md`
2. The first `# Heading` in the file becomes the page `<title>`
3. Run `bash main.sh` — the page is generated at `docs/blog/my-post/index.html`

## Supported Markdown

| Syntax | Output |
|---|---|
| `# Heading` through `###### Heading` | `<h1>` – `<h6>` |
| `**bold**` | `<b>` |
| `_italic_` | `<i>` |
| `` `code` `` | `<code>` |
| `[text](url)` | `<a href="url">` |
| `![alt](url)` | `<img>` |
| ` ``` ` fenced block ` ``` ` | `<pre><code>` |
| `> quote` | `<blockquote>` |
| `- item` | `<ul><li>` |
| `1. item` | `<ol><li>` |

## Deployment

The site deploys to GitHub Pages from the `docs/` folder on `main`.

**GitHub repo settings:** Settings → Pages → Source → Deploy from branch → `main` / `docs`

After making changes:

```bash
bash build.sh
git add docs/
git commit -m "rebuild site"
git push
```
