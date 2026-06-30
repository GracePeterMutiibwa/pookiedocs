import json
import re
from pathlib import Path

from livereload import Server

from pookiedocs.builder import _deepCopyNavNodes
from pookiedocs.config import loadConfig
from pookiedocs.converter import convertMarkdown, convertHtml
from pookiedocs.scanner import scanDocs, buildNavTree, markActiveNode
from pookiedocs.theme import renderPage

_htmlTagPattern = re.compile(r"<[^>]+>")
_whitespacePattern = re.compile(r"\s+")


def serveDocs(host: str = "localhost", port: int = 3000, config_path: str = "pookiedocs.config.py") -> None:
    config = loadConfig(config_path)

    pageCache: dict[str, str] = {}
    searchIndexJson: str = "[]"

    themeAssetsDir = Path(__file__).parent / "theme" / "assets"
    staticDir = Path(config.staticDir).resolve()

    def _buildAll() -> None:
        pageEntries = scanDocs(config.docsDir)
        navNodes = buildNavTree(pageEntries)
        searchPayload: list[dict] = []
        newCache: dict[str, str] = {}

        for entry in pageEntries:
            if entry.fileType == "md":
                htmlBody, frontmatter = convertMarkdown(entry.sourcePath)
                entry.title = frontmatter.get("title", entry.title)
            else:
                htmlBody, title = convertHtml(entry.sourcePath)
                entry.title = title

            activeNav = markActiveNode(_deepCopyNavNodes(navNodes), entry.urlPath)
            newCache[entry.urlPath] = renderPage(entry, htmlBody, activeNav, config)

            searchPayload.append({
                "title": entry.title,
                "urlPath": entry.urlPath,
                "htmlBody": htmlBody,
            })

        pageCache.clear()
        pageCache.update(newCache)

        indexEntries = []
        for item in searchPayload:
            rawText = _htmlTagPattern.sub(" ", item["htmlBody"])
            plainText = _whitespacePattern.sub(" ", rawText).strip()
            indexEntries.append({
                "title": item["title"],
                "url": item["urlPath"],
                "excerpt": plainText[:200],
            })

        nonlocal searchIndexJson
        searchIndexJson = json.dumps(indexEntries, ensure_ascii=False)

    _buildAll()

    def _wsgiApp(environ, start_response):
        requestPath = environ.get("PATH_INFO", "/")

        if requestPath == "/search-index.json":
            body = searchIndexJson.encode("utf-8")
            start_response("200 OK", [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", str(len(body))),
            ])
            return [body]

        if requestPath.startswith("/assets/"):
            assetPath = themeAssetsDir / requestPath[len("/assets/"):]
            if assetPath.is_file():
                return _serveFile(assetPath, start_response)

        if requestPath.startswith("/static/"):
            staticFilePath = staticDir / requestPath[len("/static/"):]
            if staticFilePath.is_file():
                return _serveFile(staticFilePath, start_response)

        # Redirect bare .html extension requests to the clean URL
        if requestPath.endswith(".html"):
            cleanPath = requestPath[:-5] or "/"
            if cleanPath in pageCache:
                start_response("301 Moved Permanently", [
                    ("Location", cleanPath),
                    ("Content-Length", "0"),
                ])
                return [b""]

        if requestPath in pageCache:
            body = pageCache[requestPath].encode("utf-8")
            start_response("200 OK", [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Content-Length", str(len(body))),
            ])
            return [body]

        body = b"<html><body><h1>404 Not Found</h1></body></html>"
        start_response("404 Not Found", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ])
        return [body]

    def _serveFile(file_path: Path, start_response):
        mimeTypes = {
            ".css": "text/css",
            ".js": "application/javascript",
            ".html": "text/html",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".json": "application/json",
            ".zip": "application/zip",
            ".pdf": "application/pdf",
            ".woff": "font/woff",
            ".woff2": "font/woff2",
            ".ttf": "font/ttf",
        }
        contentType = mimeTypes.get(file_path.suffix.lower(), "application/octet-stream")
        try:
            data = file_path.read_bytes()
        except OSError:
            body = b"<html><body><h1>404 Not Found</h1></body></html>"
            start_response("404 Not Found", [("Content-Type", "text/html")])
            return [body]
        start_response("200 OK", [
            ("Content-Type", contentType),
            ("Content-Length", str(len(data))),
        ])
        return [data]

    # Server(app=_wsgiApp) passes the WSGI app through the constructor so
    # livereload's own application() method wraps it correctly with
    # LiveScriptContainer, which handles script injection and calling convention.
    liveServer = Server(app=_wsgiApp)

    def _onDocChange():
        try:
            _buildAll()
        except Exception as error:
            print(f"Rebuild error: {error}")

    liveServer.watch(config.docsDir, _onDocChange)

    if Path(config_path).exists():
        liveServer.watch(config_path, _onDocChange)

    print("pookiedocs dev server")
    print(f"http://{host}:{port}")
    print("Live reload: on")

    liveServer.serve(host=host, port=port, open_url=False)
