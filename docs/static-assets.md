---
title: Static Assets
description: Images, downloads, and other assets in pookiedocs
---

# Static Assets

Images, downloadable files, and any other non-page asset live in `staticDir`, which defaults to `static` at the project root. This folder sits alongside `docsDir`, not inside it, so pookiedocs never scans it for pages.

```
myproject/
    docs/
        guides/
            architecture.md
    static/
        images/
            architecture-diagram.png
        files/
            sample-config.zip
```

## Referencing static assets

Static assets are referenced with a path starting at `/static/`. The path is always relative to the site root, never relative to the page making the reference. This means the same reference works whether it appears in `docs/index.md` or `docs/guides/advanced/page.md`.

In markdown:

```markdown
![Architecture diagram](/static/images/architecture-diagram.png)

Download the [sample config](/static/files/sample-config.zip).
```

In HTML pages:

```html
<img src="/static/images/architecture-diagram.png" alt="Architecture diagram">
<a href="/static/files/sample-config.zip">Download sample config</a>
```

## Build behaviour

At build time, the entire contents of `staticDir` are copied as-is into `outputDir/static/`. No processing, no renaming, no optimization. What is in `static/` ends up exactly as-is in `dist/static/`.

## Dev server behaviour

The dev server serves `staticDir` at the `/static/` path directly from disk. Changes to files inside `staticDir` are reflected immediately without a rebuild.
