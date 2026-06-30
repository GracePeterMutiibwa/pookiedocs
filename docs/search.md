---
title: Search
description: Built-in client-side search in pookiedocs
---

# Search

pookiedocs generates a `search-index.json` file at build time. The index contains the title, URL, and a plain text excerpt of every page.

```json
[
    {
        "title": "Getting Started",
        "url": "/getting-started",
        "excerpt": "Install pookiedocs with pip. Python 3.10 or higher is required..."
    }
]
```

## Search box placement

The search input sits in the sidebar header, directly below the site name, on every page. On mobile it appears inside the slide-in sidebar overlay in the same position relative to the navigation tree.

## How search works

The search box queries `search-index.json` client-side using plain JavaScript. No server-side search endpoint is needed.

Search matches page titles and excerpts. Matching is case-insensitive and partial, so typing `rout` matches a page titled `Routing`.

Results appear in a dropdown beneath the search box as you type. Each result shows the page title and a short excerpt. Clicking a result navigates to that page and closes the dropdown.

If no pages match the current query, the dropdown shows a plain message: "No results found."

## Keyboard behaviour

- **Escape**: clears the search input and closes the dropdown
- **Click outside the search box**: closes the dropdown without clearing the input
