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
8. Copies theme assets to `dist/assets/`
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

## Deployment

The build output is a fully self-contained static site. Copy the `outputDir` folder to any static file host. See the [Deployment](deployment.md) guide for step-by-step instructions for Cloudflare Pages, Netlify, GitHub Pages, Docker, and a VPS with nginx.

## Stale files

If `outputDir` already exists, pookiedocs clears it completely before writing. No stale files from previous builds are left behind.
