---
title: HTML Pages
description: Using HTML files as documentation pages
---

# HTML Pages

HTML files are supported alongside markdown files. pookiedocs wraps their content in the default theme exactly like markdown pages.

## How it works

The content of the `<body>` tag is extracted and injected into the theme layout. If no `<body>` tag is present, the entire file content is used as the page body.

The page title is read from the `<title>` tag. If no `<title>` tag is present, the title is derived from the filename.

## Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>API Reference</title>
</head>
<body>
    <h1>API Reference</h1>
    <table>
        <thead>
            <tr>
                <th>Method</th>
                <th>Path</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>GET</td>
                <td>/api/posts</td>
                <td>List all posts</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

## When to use HTML pages

HTML pages are useful for:

- Tables that are easier to write in HTML than markdown
- Pages that need custom markup
- Migrating existing HTML documentation without conversion

For most documentation content, markdown is simpler and sufficient.
