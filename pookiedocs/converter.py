import re
from pathlib import Path

import mistune
import yaml

from pookiedocs.scanner import deriveTitle

_markdownRenderer = mistune.create_markdown(plugins=["strikethrough", "table", "task_lists"])

_h1Pattern = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
_frontmatterPattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_bodyPattern = re.compile(r"<body[^>]*>(.*?)</body>", re.IGNORECASE | re.DOTALL)
_titleTagPattern = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_htmlTagPattern = re.compile(r"<[^>]+>")
_internalHrefPattern = re.compile(r'href="([^"#][^"]*\.(?:md|html)(?:#[^"]*)?)"')
_numericPrefixPattern = re.compile(r"(?:^|(?<=/))(\d+-)")


def _rewriteInternalLinks(html: str) -> str:
    def replaceHref(match):
        href = match.group(1)
        if href.startswith(("http://", "https://", "/", "#", "mailto:")):
            return match.group(0)
        fragment = ""
        if "#" in href:
            href, fragment = href.split("#", 1)
            fragment = "#" + fragment
        # Strip .md or .html extension
        if href.endswith(".md"):
            urlPath = href[:-3]
        else:
            urlPath = href[:-5]
        # Strip numeric prefixes from every path component (e.g. 05-changelog -> changelog)
        parts = urlPath.split("/")
        parts = [re.sub(r"^\d+-", "", p) for p in parts]
        urlPath = "/".join(parts)
        if urlPath == "index":
            urlPath = "./"
        elif urlPath.endswith("/index"):
            urlPath = urlPath[:-5]
        return f'href="{urlPath}{fragment}"'
    return _internalHrefPattern.sub(replaceHref, html)


def convertMarkdown(source_path: str) -> tuple[str, dict]:
    resolvedPath = Path(source_path).resolve()

    try:
        rawContent = resolvedPath.read_text(encoding="utf-8")
    except OSError as error:
        raise RuntimeError(
            f"Failed to read markdown file '{resolvedPath}': {error}. "
            f"Check that the file exists and is readable."
        ) from error

    frontmatter: dict = {}
    markdownBody = rawContent

    frontmatterMatch = _frontmatterPattern.match(rawContent)
    if frontmatterMatch:
        try:
            frontmatter = yaml.safe_load(frontmatterMatch.group(1)) or {}
        except yaml.YAMLError as error:
            raise RuntimeError(
                f"Failed to parse YAML frontmatter in '{resolvedPath}': {error}. "
                f"Check that the frontmatter block between --- delimiters is valid YAML."
            ) from error
        markdownBody = rawContent[frontmatterMatch.end():]

    try:
        htmlBody = _rewriteInternalLinks(_markdownRenderer(markdownBody))
    except Exception as error:
        raise RuntimeError(
            f"Failed to convert markdown in '{resolvedPath}' to HTML: {error}. "
            f"Check for malformed markdown syntax."
        ) from error

    # Title priority: frontmatter > first h1 > filename
    if "title" not in frontmatter:
        h1Match = _h1Pattern.search(htmlBody)
        if h1Match:
            frontmatter["title"] = _htmlTagPattern.sub("", h1Match.group(1)).strip()
        else:
            frontmatter["title"] = deriveTitle(resolvedPath.name)

    return htmlBody, frontmatter


def convertHtml(source_path: str) -> tuple[str, str]:
    resolvedPath = Path(source_path).resolve()

    try:
        rawContent = resolvedPath.read_text(encoding="utf-8")
    except OSError as error:
        raise RuntimeError(
            f"Failed to read HTML file '{resolvedPath}': {error}. "
            f"Check that the file exists and is readable."
        ) from error

    bodyMatch = _bodyPattern.search(rawContent)
    htmlBody = bodyMatch.group(1).strip() if bodyMatch else rawContent.strip()

    titleMatch = _titleTagPattern.search(rawContent)
    if titleMatch:
        title = _htmlTagPattern.sub("", titleMatch.group(1)).strip()
    else:
        title = deriveTitle(resolvedPath.name)

    return htmlBody, title
