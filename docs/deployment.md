---
title: Deployment
description: Deploy a pookiedocs static site to Cloudflare Pages, Netlify, GitHub Pages, Docker, and a VPS
---

# Deployment

Run the build command to produce a self-contained static site:

```bash
pookiedocs build
```

Everything needed to serve the site - HTML pages, the search index, CSS, and JavaScript - is written to `outputDir` (default `dist/`). Copy that folder to any static file host.

## Cloudflare Pages

1. Push your project to a GitHub or GitLab repository.
2. In the Cloudflare dashboard go to **Workers & Pages > Create > Pages > Connect to Git**.
3. Select your repository and set the following build settings:

| Setting                | Value                                        |
| ---------------------- | -------------------------------------------- |
| Build command          | `pip install pookiedocs && pookiedocs build` |
| Build output directory | `dist`                                       |

4. Click **Save and Deploy**. Every push to your default branch triggers a new deployment.

If you pin a specific version, install it in the build command:

```bash
pip install pookiedocs==0.1.0 && pookiedocs build
```

## Netlify

Create a `netlify.toml` at the root of your repository:

```toml
[build]
  command   = "pip install pookiedocs && pookiedocs build"
  publish   = "dist"

[build.environment]
  PYTHON_VERSION = "3.12"
```

Push the file and connect the repository in the Netlify dashboard. Netlify picks up `netlify.toml` automatically on every push.

Alternatively, use the Netlify CLI to deploy a local build manually:

```bash
pookiedocs build
npx netlify-cli deploy --dir dist --prod
```

## GitHub Pages

Add a workflow file at `.github/workflows/deploy.yml`:

```yaml
name: Deploy docs

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pookiedocs
      - run: pookiedocs build --output _site
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Enable **GitHub Pages** in your repository settings and set the source to **GitHub Actions**.

If your site is served from a subdirectory (e.g. `https://username.github.io/my-project/`), set `baseUrl` in your config:

```python
from pookiedocs.config import DocsConfig

DOCS = DocsConfig(
    name="My Project",
    baseUrl="/my-project/",
)
```

## VPS with nginx

Build the site locally or in CI and copy the output to your server:

```bash
pookiedocs build
rsync -avz --delete dist/ user@your-server:/var/www/docs/
```

Serve the folder with nginx:

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

For HTTPS, use Certbot:

```bash
sudo certbot --nginx -d docs.example.com
```

## Docker

Add a `Dockerfile` at the root of your project:

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pookiedocs && pookiedocs build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

Build and run:

```bash
docker build -t my-docs .
docker run -p 8080:80 my-docs
```

The site is available at `http://localhost:8080`. The final image contains only nginx and the built HTML - no Python in production.

This image works anywhere that runs containers: GCP Cloud Run, AWS App Runner, Fly.io, Railway, a plain VPS with Docker installed, or any other container platform.
