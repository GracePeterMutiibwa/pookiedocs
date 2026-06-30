# pookiedocs

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/pookiedocs/badge/?version=latest)](https://pookiedocs.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/pookiedocs.svg)](https://pypi.org/project/pookiedocs/)

A minimal Python documentation site generator. Reads markdown and HTML files from a folder, converts them to a clean static site, and serves them — in development with live reload, in production with a built-in HTTP server.

## Installation

```bash
pip install pookiedocs
```

## Quick start

```bash
pookiedocs init
pookiedocs dev
```

`pookiedocs dev` starts a live-reload server at `http://localhost:3000`. Edit any file and the browser refreshes automatically.

## Production

```bash
pookiedocs serve
```

Builds the site and serves it on `0.0.0.0:3000`. No separate web server needed — drop this command into a Dockerfile and you're done.

## Build only

```bash
pookiedocs build
```

Writes a fully self-contained static site to `dist/`. Deploy by pointing any static file host at that folder.

## Deployment

**Docker** - the simplest path to production:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pookiedocs
EXPOSE 3000
CMD ["pookiedocs", "serve", "--port", "3000"]
```

```bash
docker build -t my-docs .
docker run -p 3000:3000 my-docs
```

Deploy the image to GCP Cloud Run, AWS App Runner, Fly.io, Railway, or any container platform.

**Cloudflare Pages** - set the build command to `pip install pookiedocs && pookiedocs build` and the output directory to `dist`.

**Netlify** - add a `netlify.toml`:

```toml
[build]
  command = "pip install pookiedocs && pookiedocs build"
  publish = "dist"
```

**GitHub Pages** - add a workflow that runs `pookiedocs build --output _site` and uploads the `_site` artifact with `actions/upload-pages-artifact`.

**VPS** - build locally, `rsync` the `dist/` folder to your server, and serve it with nginx:

```nginx
server {
    listen 80;
    server_name docs.example.com;
    root /var/www/docs;
    index index.html;

    location / {
        try_files $uri $uri/ $uri.html =404;
    }
}
```

See the [Deployment guide](https://pookiedocs.readthedocs.io/en/latest/deployment/) for full examples including the complete GitHub Actions workflow and HTTPS setup with Certbot.

## Documentation

Full documentation is available at https://pookiedocs.readthedocs.io

## License

MIT
