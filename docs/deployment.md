---
title: Deployment
description: Deploy a pookiedocs site to Docker, Cloudflare Pages, Netlify, GitHub Pages, and a VPS
---

# Deployment

pookiedocs supports two deployment paths:

- **Built-in server** — run `pookiedocs serve` and pookiedocs builds the site then serves it. No external web server needed. Best for Docker and container platforms.
- **Static export** — run `pookiedocs build` and copy the `dist/` folder to any static file host.

## Docker

The simplest production deployment. pookiedocs builds and serves your docs in a single container with no external dependencies.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pookiedocs
EXPOSE 3000
CMD ["pookiedocs", "serve", "--port", "3000"]
```

Build and run:

```bash
docker build -t my-docs .
docker run -p 3000:3000 my-docs
```

The site is available at `http://localhost:3000`. Deploy the image to GCP Cloud Run, AWS App Runner, Fly.io, Railway, or any platform that runs containers.

To use a different port:

```bash
docker run -p 8080:8080 my-docs pookiedocs serve --port 8080
```

## Cloudflare Pages

1. Push your project to a GitHub or GitLab repository.
2. In the Cloudflare dashboard go to **Workers & Pages > Create > Pages > Connect to Git**.
3. Select your repository and set the following build settings:

| Setting | Value |
|---|---|
| Build command | `pip install pookiedocs && pookiedocs build` |
| Build output directory | `dist` |

4. Click **Save and Deploy**. Every push to your default branch triggers a new deployment.

To pin a specific version:

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

To deploy a local build manually:

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
