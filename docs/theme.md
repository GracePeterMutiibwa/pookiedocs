---
title: Default Theme
description: The default pookiedocs theme layout, typography, colors, and responsive behaviour
---

# Default Theme

The default theme is a clean, minimal layout. White background, neutral text color, readable font stack, a left sidebar for navigation, and a search box in the sidebar header. The layout is fully responsive across desktop, tablet, and mobile.

## Layout

```
+------------------+----------------------------------+
| Site name        |                                  |
| [Search........] |                                  |
+------------------+  Page content                    |
| Navigation       |                                  |
|   Home           |                                  |
|   Getting Started|                                  |
|   Guides         |                                  |
|     Routing      |                                  |
|     Auth         |                                  |
+------------------+----------------------------------+
```

The search box sits directly below the site name at the top of the sidebar, above the navigation tree.

## Typography

Font family is controlled by `fontFamily` in `DocsConfig`. The default `"system"` uses:

```
-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
```

- Body text: 16px, line height 1.6
- Code: monospace system font stack, not affected by `fontFamily`
- Headings: plain weight progression, no decorative styling

## Colors

| Element | Color |
|---|---|
| Background | `#ffffff` |
| Body text | `#1a1a1a` |
| Sidebar background | `#f5f5f5` |
| Sidebar border | `#e0e0e0` |
| Active nav link | `#000000` |
| Inactive nav link | `#555555` |
| Code background | `#f0f0f0` |
| Border | `#e0e0e0` |
| Search box background | `#ffffff` |
| Search box border | `#cccccc` |
| Search result hover | `#f0f0f0` |

## Responsive behaviour

| Breakpoint | Width | Layout |
|---|---|---|
| Desktop | 1024px and above | Sidebar fixed at 260px, content fills remaining width |
| Tablet | 600px to 1023px | Sidebar fixed at 200px, content adjusts |
| Mobile | below 600px | Sidebar hidden behind a menu toggle, slides in as an overlay |

On mobile, a menu toggle button appears in a top bar. Tapping it slides the sidebar in from the left as an overlay that includes the search box and full navigation. Tapping the toggle again, tapping outside the sidebar, or selecting a nav link closes the overlay.

Code blocks scroll horizontally within their own container on narrow viewports rather than forcing the whole page to scroll. Tables also scroll horizontally within their own container.

## Theme assets

The theme ships two files bundled with the package: `pookiedocs.css` and `pookiedocs.js`. Both are copied to `dist/assets/` at build time. You never edit these files directly.
