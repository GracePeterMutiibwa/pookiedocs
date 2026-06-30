import os
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PageEntry:
    sourcePath: str
    outputPath: str
    urlPath: str
    title: str
    fileType: str
    relativeSourcePath: str = ""  # original relative path (with numeric prefix) used for sort order


@dataclass
class NavNode:
    title: str
    urlPath: str | None
    children: list = field(default_factory=list)
    isActive: bool = False


_numericPrefixPattern = re.compile(r"^\d+-")
_allowedExtensions = {".md", ".html"}


def deriveTitle(filename: str) -> str:
    stem = Path(filename).stem
    stem = _numericPrefixPattern.sub("", stem)
    stem = stem.replace("-", " ").replace("_", " ")
    return stem.title()


def deriveUrlPath(relative_output_path: str, base_url: str = "/") -> str:
    parts = Path(relative_output_path)
    base = base_url.rstrip("/")

    if parts.name == "index.html":
        parentPart = parts.parent
        if str(parentPart) == ".":
            return base + "/"
        return base + "/" + str(parentPart).replace(os.sep, "/") + "/"

    withoutExtension = parts.with_suffix("")
    return base + "/" + str(withoutExtension).replace(os.sep, "/")


def _deriveOutputPath(relative_source_path: str) -> str:
    p = Path(relative_source_path)
    # Strip numeric prefix from every directory component and the filename stem
    cleanParts = [_numericPrefixPattern.sub("", part) for part in p.parts[:-1]]
    cleanStem = _numericPrefixPattern.sub("", p.stem)
    cleanExt = ".html" if p.suffix == ".md" else p.suffix
    cleanName = cleanStem + cleanExt
    if cleanParts:
        return str(Path(*cleanParts) / cleanName)
    return cleanName


def scanDocs(docs_dir: str) -> list[PageEntry]:
    resolvedDocsDir = Path(docs_dir).resolve()

    if not resolvedDocsDir.exists():
        raise FileNotFoundError(
            f"Docs directory not found at '{resolvedDocsDir}'. "
            f"Check that docsDir in your config points to an existing folder."
        )

    pageEntries = []

    try:
        for dirPath, dirNames, fileNames in os.walk(resolvedDocsDir):
            dirNames.sort()
            for fileName in sorted(fileNames):
                filePath = Path(dirPath) / fileName
                if filePath.suffix not in _allowedExtensions:
                    continue

                try:
                    relativePath = filePath.relative_to(resolvedDocsDir)
                except ValueError as error:
                    raise RuntimeError(
                        f"Failed to compute relative path for '{filePath}' under '{resolvedDocsDir}': {error}"
                    ) from error

                relativeSourceStr = str(relativePath)
                relativeOutputPath = _deriveOutputPath(relativeSourceStr)
                urlPath = deriveUrlPath(relativeOutputPath)
                title = deriveTitle(fileName)
                fileType = "md" if filePath.suffix == ".md" else "html"

                pageEntries.append(
                    PageEntry(
                        sourcePath=str(filePath),
                        outputPath=relativeOutputPath,
                        urlPath=urlPath,
                        title=title,
                        fileType=fileType,
                        relativeSourcePath=relativeSourceStr,
                    )
                )
    except OSError as error:
        raise RuntimeError(
            f"Failed to scan docs directory '{resolvedDocsDir}': {error}. "
            f"Check that the directory is readable and accessible."
        ) from error

    return pageEntries


def buildNavTree(page_entries: list[PageEntry]) -> list[NavNode]:
    # Use relativeSourcePath (original, with numeric prefix) for tree structure and sort order.
    # outputPath (prefix-stripped) is only used for URLs.
    rootTree: dict = {"_pages": [], "_sections": {}}

    for entry in page_entries:
        sourceParts = Path(entry.relativeSourcePath or entry.outputPath).parts
        currentLevel = rootTree

        for part in sourceParts[:-1]:
            if part not in currentLevel["_sections"]:
                currentLevel["_sections"][part] = {"_pages": [], "_sections": {}}
            currentLevel = currentLevel["_sections"][part]

        currentLevel["_pages"].append(entry)

    return _buildNodesFromTree(rootTree)


def _buildNodesFromTree(tree: dict) -> list[NavNode]:
    nodes: list[NavNode] = []

    # Index pages first; remaining pages keep insertion order (already sorted by
    # original filename from scanDocs, so numeric prefix order is preserved).
    indexPages = [p for p in tree["_pages"] if Path(p.outputPath).name == "index.html"]
    otherPages = [p for p in tree["_pages"] if Path(p.outputPath).name != "index.html"]

    for entry in indexPages:
        nodes.append(NavNode(title=entry.title, urlPath=entry.urlPath, children=[]))

    for entry in otherPages:
        nodes.append(NavNode(title=entry.title, urlPath=entry.urlPath, children=[]))

    # Sort sections by their original directory name (has numeric prefix, so numeric order holds)
    for sectionName in sorted(tree["_sections"].keys()):
        sectionTitle = deriveTitle(sectionName)
        children = _buildNodesFromTree(tree["_sections"][sectionName])
        nodes.append(NavNode(title=sectionTitle, urlPath=None, children=children))

    return nodes


def markActiveNode(nav_nodes: list[NavNode], current_url: str) -> list[NavNode]:
    for node in nav_nodes:
        if node.urlPath == current_url:
            node.isActive = True
        if node.children:
            markActiveNode(node.children, current_url)
    return nav_nodes
