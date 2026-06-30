---
title: Getting Started
description: Install pookiedocs and create your first documentation site
---

# Getting Started

## Install

```bash
pip install pookiedocs
```

Python 3.10 or higher is required.

## Create a new project

Run `pookiedocs init` inside a new folder:

```bash
mkdir my-project
cd my-project
pookiedocs init
```

You will be prompted for a project name:

```
Project name: My Project
Created docs/index.md
Created pookiedocs.config.py
Run: pookiedocs dev
```

This creates two files:

- `docs/index.md` - your first page
- `pookiedocs.config.py` - your site configuration

## Start the dev server

```bash
pookiedocs dev
```

```
pookiedocs dev server
http://localhost:3000
Live reload: on
```

Open `http://localhost:3000` in your browser. Edit `docs/index.md` and the browser reloads automatically.

## Serve in production

```bash
pookiedocs serve
```

Builds the site and serves it on `0.0.0.0:3000`. Use this command in Docker, on a VPS, or on any platform that runs a persistent process. See the [Deployment](deployment.md) guide for examples.

## Build for static hosting

```bash
pookiedocs build
```

```
Building...
Converted 1 pages
Generated search index
Copied theme assets
Output: dist/
```

The `dist/` folder is a fully self-contained static site ready to deploy to Cloudflare Pages, Netlify, GitHub Pages, or any static file host.

## Add more pages

Create any `.md` file inside `docs/` and it becomes a page. Create a folder to group related pages. The navigation is generated automatically.

```
docs/
    index.md
    getting-started.md
    guides/
        routing.md
        auth.md
```
