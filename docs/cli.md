---
title: CLI Reference
description: Every pookiedocs command and option
---

# CLI Reference

## pookiedocs init

Scaffolds a new docs project in the current directory.

```bash
pookiedocs init
```

```
Project name: My Project
Created docs/index.md
Created pookiedocs.config.py
Run: pookiedocs dev
```

Creates:
- `docs/index.md` with a minimal welcome page
- `pookiedocs.config.py` with the project name and sensible defaults

Fails if `docs/` or `pookiedocs.config.py` already exist.

## pookiedocs dev

Starts the live-reload development server. Serves pages from memory — does not write to `outputDir`.

```bash
pookiedocs dev
pookiedocs dev --port 4000
pookiedocs dev --host 0.0.0.0
```

```
pookiedocs dev server
http://localhost:3000
Live reload: on
```

| Option | Default | Description |
|---|---|---|
| `--host` | `localhost` | Host to bind to |
| `--port` | `3000` | Port to listen on |
| `--config` | `pookiedocs.config.py` | Path to config file |

## pookiedocs serve

Builds the site then serves the output directory as a production HTTP server. This is the command to use in Docker, on a VPS, or on any platform that runs a persistent process.

```bash
pookiedocs serve
pookiedocs serve --port 8080
pookiedocs serve --host 0.0.0.0 --port 8080
```

```
Building...
Converted 12 pages
Generated search index
Copied theme assets
Output: dist/
pookiedocs
http://0.0.0.0:3000
```

| Option | Default | Description |
|---|---|---|
| `--host` | `0.0.0.0` | Host to bind to |
| `--port` | `3000` | Port to listen on |
| `--config` | `pookiedocs.config.py` | Path to config file |

## pookiedocs build

Builds the static site and exits. Use this when deploying to a static file host (Cloudflare Pages, Netlify, GitHub Pages).

```bash
pookiedocs build
pookiedocs build --output myfolder
```

```
Building...
Converted 12 pages
Generated search index
Copied theme assets
Output: dist/
```

| Option | Default | Description |
|---|---|---|
| `--output` | value from config | Override `outputDir` for this run only |
| `--config` | `pookiedocs.config.py` | Path to config file |

## pookiedocs version

Prints the installed pookiedocs version.

```bash
pookiedocs version
pookiedocs 0.1.0
```
