---
title: Building
description: Building a static site with pookiedocs build
---

# Building

```bash
pookiedocs build
```

## What the build command does

1. Reads `pookiedocs.config.py`
2. Scans `docsDir` recursively
3. Converts all markdown files to HTML
4. Passes all HTML files through the theme wrapper
5. Generates the navigation tree
6. Generates `search-index.json`
7. Copies `staticDir` contents to `outputDir/static/`
8. Copies theme assets to `outputDir/assets/`
9. Writes all output to `outputDir`

## Output

```
Building...
Converted 12 pages
Generated search index
Copied theme assets
Output: dist/
```

## Options

Override the output directory without changing your config:

```bash
pookiedocs build --output myfolder
```

Use an alternate config file:

```bash
pookiedocs build --config path/to/pookiedocs.config.py
```

## Stale files

If `outputDir` already exists, pookiedocs clears it completely before writing. No stale files from previous builds are left behind.

## Serving the output

There are three ways to serve the built site depending on your use case:

| Use case | Command |
|---|---|
| Local development with live reload | `pookiedocs dev` |
| Production server (Docker, VPS, containers) | `pookiedocs serve` |
| Static file host (Cloudflare, Netlify, GitHub Pages) | `pookiedocs build` then deploy `dist/` |

See the [Deployment](deployment.md) guide for step-by-step instructions.
