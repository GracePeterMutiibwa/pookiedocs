import os
import shutil
from pathlib import Path

from pookiedocs.config import DocsConfig, loadConfig
from pookiedocs.converter import convertMarkdown, convertHtml
from pookiedocs.scanner import scanDocs, buildNavTree, markActiveNode
from pookiedocs.search import buildSearchIndex
from pookiedocs.theme import renderPage


def copyStaticAssets(static_dir: str, output_dir: str) -> None:
    sourceDir = Path(static_dir).resolve()
    destinationDir = Path(output_dir) / "static"

    if not sourceDir.exists():
        print(f"Note: staticDir '{sourceDir}' not found, skipping static asset copy.")
        return

    try:
        if destinationDir.exists():
            shutil.rmtree(destinationDir)
        shutil.copytree(str(sourceDir), str(destinationDir))
    except OSError as error:
        raise RuntimeError(
            f"Failed to copy static assets from '{sourceDir}' to '{destinationDir}': {error}. "
            f"Check that both paths are accessible and you have write permission to the output directory."
        ) from error


def _copyThemeAssets(output_dir: str) -> None:
    themeAssetsDir = Path(__file__).parent / "theme" / "assets"
    destinationDir = Path(output_dir) / "assets"

    try:
        if destinationDir.exists():
            shutil.rmtree(destinationDir)
        shutil.copytree(str(themeAssetsDir), str(destinationDir))
    except OSError as error:
        raise RuntimeError(
            f"Failed to copy theme assets from '{themeAssetsDir}' to '{destinationDir}': {error}. "
            f"Check that the pookiedocs package is installed correctly."
        ) from error


def buildSite(config_path: str = "pookiedocs.config.py", output_override: str | None = None) -> None:
    config = loadConfig(config_path)

    if output_override:
        config.outputDir = output_override

    outputDir = Path(config.outputDir).resolve()

    print("Building...")

    if outputDir.exists():
        try:
            shutil.rmtree(outputDir)
        except OSError as error:
            raise RuntimeError(
                f"Failed to clear output directory '{outputDir}': {error}. "
                f"Check that no files inside it are locked or in use."
            ) from error

    try:
        outputDir.mkdir(parents=True)
    except OSError as error:
        raise RuntimeError(
            f"Failed to create output directory '{outputDir}': {error}. "
            f"Check that you have write permission to the parent directory."
        ) from error

    pageEntries = scanDocs(config.docsDir)
    navNodes = buildNavTree(pageEntries)

    pageCount = 0
    searchPayload: list[dict] = []

    for entry in pageEntries:
        try:
            if entry.fileType == "md":
                htmlBody, frontmatter = convertMarkdown(entry.sourcePath)
                title = frontmatter.get("title", entry.title)
                entry.title = title
            else:
                htmlBody, title = convertHtml(entry.sourcePath)
                entry.title = title
        except RuntimeError as error:
            raise RuntimeError(
                f"Failed to convert '{entry.sourcePath}': {error}"
            ) from error

        activeNav = markActiveNode(
            _deepCopyNavNodes(navNodes), entry.urlPath
        )

        renderedHtml = renderPage(entry, htmlBody, activeNav, config)

        outputFilePath = outputDir / entry.outputPath

        try:
            outputFilePath.parent.mkdir(parents=True, exist_ok=True)
            outputFilePath.write_text(renderedHtml, encoding="utf-8")
        except OSError as error:
            raise RuntimeError(
                f"Failed to write output file '{outputFilePath}': {error}. "
                f"Check that the output directory is writable."
            ) from error

        searchPayload.append({
            "title": entry.title,
            "urlPath": entry.urlPath,
            "htmlBody": htmlBody,
        })

        pageCount += 1

    print(f"Converted {pageCount} pages")

    buildSearchIndex(searchPayload, str(outputDir))
    print("Generated search index")

    copyStaticAssets(config.staticDir, str(outputDir))
    _copyThemeAssets(str(outputDir))
    print("Copied theme assets")

    print(f"Output: {config.outputDir}/")


def _deepCopyNavNodes(nodes):
    from pookiedocs.scanner import NavNode
    result = []
    for node in nodes:
        copied = NavNode(
            title=node.title,
            urlPath=node.urlPath,
            children=_deepCopyNavNodes(node.children),
            isActive=node.isActive,
        )
        result.append(copied)
    return result
