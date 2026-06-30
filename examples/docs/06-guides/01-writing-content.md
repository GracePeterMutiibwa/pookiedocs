---
title: Writing Content
---

# Writing Content

Author pages in Markdown. Files named `01-page.md`, `02-page.md` etc. are served at clean URLs (`/page`) in numeric order.

## Frontmatter

Add a `title` key at the top of any Markdown file to override the auto-derived title:

```markdown
---
title: My Custom Title
---

# Page content here
```

## Static images

Place files in `staticDir` and reference them with an absolute path:

```markdown
![Logo](/static/images/logo.svg)
```

## Internal links

Link to other pages by filename - the `.md` extension is stripped automatically:

```markdown
[Configuration](../03-configuration.md)
```

Numeric prefixes are stripped too, so `03-configuration.md` links resolve to `/configuration`.
