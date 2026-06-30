---
title: Markdown Pages
description: Writing documentation pages in markdown
---

# Markdown Pages

Markdown files are converted to HTML using `mistune`. All standard markdown syntax is supported: headings, paragraphs, lists, code blocks with language hints, blockquotes, tables, inline code, bold, italic, strikethrough, task lists, and links.

## Frontmatter

An optional YAML frontmatter block at the top of a markdown file sets the page title and description.

```markdown
---
title: Getting Started
description: How to install and run your first pookiedocs site
---

# Getting Started

Install pookiedocs with pip...
```

If no frontmatter is provided, pookiedocs derives the title from the first `h1` heading in the file. If there is no `h1`, the title is derived from the filename by replacing hyphens with spaces and capitalizing each word.

### Supported frontmatter fields

| Field | Description |
|---|---|
| `title` | Page title shown in the browser tab and sidebar navigation |
| `description` | Short description used in the page meta tag |

## Code blocks

Fenced code blocks with a language hint are rendered with syntax highlighting classes applied by mistune. The default theme applies neutral highlight styling.

````markdown
```python
from pookiedocs.config import DocsConfig

DOCS = DocsConfig(name="My Docs")
```
````

## Tables

Standard markdown tables are supported:

```markdown
| Column A | Column B |
|---|---|
| Value 1  | Value 2  |
```

Tables scroll horizontally inside their own container on narrow viewports, preserving column relationships.

## Task lists

```markdown
- [x] Done item
- [ ] Pending item
```

## Strikethrough

```markdown
~~struck through text~~
```
