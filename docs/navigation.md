---
title: Navigation
description: How pookiedocs generates sidebar navigation from your folder structure
---

# Navigation

Navigation is generated automatically from the folder structure. No manual nav definition is required.

## Structure

The nav tree mirrors the `docs/` directory exactly. Folders become collapsible sections. Files become links.

```
docs/
    index.md
    getting-started.md
    guides/
        routing.md
        auth.md
    reference/
        config.md
        cli.md
```

Generates this nav:

```
Home
Getting Started
Guides
    Routing
    Auth
Reference
    Config
    CLI
```

## Active state

The current page link is marked active automatically based on the current URL. The corresponding sidebar section is expanded.

## Title formatting

File and folder names are converted to human-readable titles by replacing hyphens and underscores with spaces and capitalizing the first letter of each word.

| Filename | Nav title |
|---|---|
| `getting-started.md` | Getting Started |
| `api_reference.md` | Api Reference |
| `01-introduction.md` | Introduction |

Number prefixes (`01-`, `02-` etc.) are stripped from both the title and the URL.

## Ordering

Within each folder, items are sorted alphabetically. To control the order, prefix filenames with numbers:

```
docs/
    01-introduction.md
    02-installation.md
    03-configuration.md
```

## Sections

Folder sections are collapsible. They collapse and expand without JavaScript, using the native HTML `<details>` and `<summary>` elements. The section containing the active page is expanded by default.
