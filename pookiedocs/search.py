import json
import re
from pathlib import Path

_htmlTagPattern = re.compile(r"<[^>]+>")
_whitespacePattern = re.compile(r"\s+")


def buildSearchIndex(page_entries_with_html: list[dict], output_dir: str) -> None:
    indexPath = Path(output_dir) / "search-index.json"
    indexEntries = []

    for item in page_entries_with_html:
        rawText = _htmlTagPattern.sub(" ", item["htmlBody"])
        plainText = _whitespacePattern.sub(" ", rawText).strip()
        excerpt = plainText[:200]

        indexEntries.append({
            "title": item["title"],
            "url": item["urlPath"],
            "excerpt": excerpt,
        })

    try:
        indexPath.parent.mkdir(parents=True, exist_ok=True)
        indexPath.write_text(json.dumps(indexEntries, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as error:
        raise RuntimeError(
            f"Failed to write search index to '{indexPath}': {error}. "
            f"Check that the output directory is writable."
        ) from error
