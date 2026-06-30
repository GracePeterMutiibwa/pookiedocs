---
title: Configuration
---

# Configuration

Create `pookiedocs.config.py` in your project root:

```python
from pookiedocs.config import DocsConfig

DOCS = DocsConfig(
    name="My Project",
    docsDir="docs",
    outputDir="dist",
)
```
