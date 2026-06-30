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
Run: pookiedocs serve
```

Creates:
- `docs/index.md` with a minimal welcome page
- `pookiedocs.config.py` with the project name and sensible defaults

Fails if `docs/` or `pookiedocs.config.py` already exist.

## pookiedocs serve

Starts the dev server with live reload.

```bash
pookiedocs serve
pookiedocs serve --port 4000
pookiedocs serve --host 0.0.0.0
pookiedocs serve --host 0.0.0.0 --port 4000
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

## pookiedocs build

Builds the static site.

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

## pookiedocs version

Prints the installed pookiedocs version.

```bash
pookiedocs version
pookiedocs 0.1.0
```
