---
title: Project Structure
description: The standard layout for a pookiedocs project
---

# Project Structure

A typical pookiedocs project looks like this:

```
myproject/
    docs/
        index.md
        getting-started.md
        guides/
            routing.md
            auth.md
            api-layer.html
        reference/
            config.md
            cli.md
    static/
        images/
            architecture-diagram.png
            logo.png
        files/
            sample-config.zip
    pookiedocs.config.py
```

## docs/

The `docs/` directory contains all source files. Every `.md` and `.html` file becomes a page. Subfolders become navigation sections. Nesting is supported at any depth.

## static/

The `static/` directory holds every asset you want to reference from pages: images, downloadable files, anything that is not a page itself. It sits at the project root alongside `docs/`, not inside it, so pookiedocs never mistakes a static file for a page.

## pookiedocs.config.py

Your site configuration. Contains one `DOCS = DocsConfig(...)` assignment. See [Configuration](configuration.md) for all available fields.

## Build output

After `pookiedocs build`:

```
dist/
    index.html
    getting-started.html
    guides/
        routing.html
        auth.html
        api-layer.html
    reference/
        config.html
        cli.html
    search-index.json
    static/
        images/
            architecture-diagram.png
        files/
            sample-config.zip
    assets/
        pookiedocs.css
        pookiedocs.js
```

The output is a fully self-contained static site. No server-side processing is needed to serve it.
