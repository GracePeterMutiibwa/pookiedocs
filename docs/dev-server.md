---
title: Dev Server
description: Running the pookiedocs development server with live reload
---

# Dev Server

```bash
pookiedocs serve
```

## What the dev server does

- Serves the docs site at `http://localhost:3000` by default
- Watches `docsDir` and `pookiedocs.config.py` for changes using watchdog
- Rebuilds the affected page on change
- Reloads the browser automatically via livereload

The dev server serves pages from memory. It does not write to `outputDir`. Run `pookiedocs build` separately to produce static output.

## Output on start

```
pookiedocs dev server
http://localhost:3000
Live reload: on
```

## Options

```bash
pookiedocs serve --port 4000
pookiedocs serve --host 0.0.0.0
pookiedocs serve --host 0.0.0.0 --port 4000
```

| Option | Default | Description |
|---|---|---|
| `--host` | `localhost` | Host to bind the server to. Use `0.0.0.0` to accept connections from other machines on the network. |
| `--port` | `3000` | Port for the dev server |

## Static assets in dev mode

Static files from `staticDir` are served directly from disk at the `/static/` path. Changes to static files are reflected immediately without a rebuild.
