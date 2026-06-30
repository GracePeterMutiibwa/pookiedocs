---
title: File and Folder Routing
description: How pookiedocs maps source files to URLs and output files
---

# File and Folder Routing

pookiedocs scans `docsDir` recursively at startup and at build time. Every `.md` and `.html` file found becomes a page. Every folder becomes a navigation section.

## Route mapping

| Source file | Output file | URL |
|---|---|---|
| `docs/index.md` | `dist/index.html` | `/` |
| `docs/getting-started.md` | `dist/getting-started.html` | `/getting-started` |
| `docs/guides/routing.md` | `dist/guides/routing.html` | `/guides/routing` |
| `docs/guides/auth.html` | `dist/guides/auth.html` | `/guides/auth` |
| `docs/reference/cli.md` | `dist/reference/cli.html` | `/reference/cli` |

## Nesting depth

Folders can be nested at any depth. pookiedocs walks the full directory tree.

```
docs/
    guides/
        advanced/
            custom-storage.md    ->    /guides/advanced/custom-storage
```

## File ordering

Within each folder, files are ordered alphabetically. To control the order, prefix filenames with numbers:

```
docs/
    01-introduction.md
    02-installation.md
    03-configuration.md
```

The number prefix is stripped from the page title and URL automatically:

| Filename | URL | Nav title |
|---|---|---|
| `01-introduction.md` | `/introduction` | Introduction |
| `02-installation.md` | `/installation` | Installation |

## index.md and index.html

A file named `index.md` or `index.html` inside any folder becomes the index page for that folder.

```
docs/guides/index.md    ->    /guides/
```

The root `docs/index.md` becomes the site homepage at `/`.
