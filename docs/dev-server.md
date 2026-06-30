---
title: Dev Server
description: Running the pookiedocs development server with live reload
---

# Dev Server

```bash
pookiedocs dev
```

## What the dev server does

- Serves the docs site at `http://localhost:3000` by default
- Watches `docsDir` and `pookiedocs.config.py` for changes
- Rebuilds the affected page on change
- Reloads the browser automatically via livereload

The dev server serves pages from memory. It does not write to `outputDir`. Run `pookiedocs build` separately to produce static output, or use `pookiedocs serve` to build and serve in one step.

## Output on start

```
pookiedocs dev server
http://localhost:3000
Live reload: on
```

## Options

```bash
pookiedocs dev --port 4000
pookiedocs dev --host 0.0.0.0
pookiedocs dev --host 0.0.0.0 --port 4000
```

| Option | Default | Description |
|---|---|---|
| `--host` | `localhost` | Host to bind the server to. Use `0.0.0.0` to accept connections from other machines on the network. |
| `--port` | `3000` | Port for the dev server |
| `--config` | `pookiedocs.config.py` | Path to an alternate config file |

## Static assets in dev mode

Static files from `staticDir` are served directly from disk at the `/static/` path. Changes to static files are reflected immediately without a rebuild.

## Production serving

For production use `pookiedocs serve` instead. It builds the site first and then serves the output directory with a standard HTTP server — suitable for Docker and long-running processes.
