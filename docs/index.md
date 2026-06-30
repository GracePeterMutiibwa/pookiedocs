---
title: pookiedocs
description: A minimal Python documentation site generator
---

# pookiedocs

A minimal Python documentation site generator. Reads markdown and HTML files from a folder, converts them to a clean static site, and serves them in development with live reload. No magic, no plugin system, no theming API.

## Quick start

```bash
pip install pookiedocs
pookiedocs init
pookiedocs serve
```

Open `http://localhost:3000` and start writing.

## What pookiedocs does

- Reads `.md` and `.html` files from your `docs/` folder
- Converts them to a clean, responsive static site
- Generates a sidebar navigation automatically from your folder structure
- Builds a client-side search index at build time
- Serves pages with live reload in development

## What pookiedocs does not do

- Plugin system
- Shortcode language
- Theming DSL
- YAML configuration
- Opinionated folder conventions beyond what this documentation describes

## Requirements

Python 3.10 or higher.

## Next steps

- [Getting Started](getting-started.md) to install and create your first site
- [Configuration](configuration.md) to learn about all available options
- [CLI Reference](cli.md) for every command
