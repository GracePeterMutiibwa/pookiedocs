from pathlib import Path
import jinja2

_templatesDir = Path(__file__).parent / "templates"
_jinja2Env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(_templatesDir)),
    autoescape=jinja2.select_autoescape(["html"]),
)

_systemFontStack = (
    "\"Roboto\", -apple-system, BlinkMacSystemFont, \"Segoe UI\", Helvetica, Arial, sans-serif"
)


def _buildBreadcrumbs(nav_nodes, current_url, site_name, base_url):
    """Return ancestor trail to current_url, or [] for top-level pages."""
    def search(nodes, target, trail):
        for node in nodes:
            trail_with_node = trail + [node]
            if node.urlPath == target:
                return trail_with_node
            if node.children:
                result = search(node.children, target, trail_with_node)
                if result:
                    return result
        return None

    found = search(nav_nodes, current_url, [])
    if not found:
        return []

    # Only render breadcrumbs when the page lives inside at least one section
    has_section_ancestor = any(n.urlPath is None for n in found[:-1])
    if not has_section_ancestor:
        return []

    crumbs = [{"title": site_name, "url": base_url}]
    for node in found:
        crumbs.append({"title": node.title, "url": node.urlPath})
    return crumbs


def renderPage(page_entry, html_body, nav_nodes, config) -> str:
    if config.fontFamily == "system":
        fontFamilyCss = _systemFontStack
    else:
        fontFamilyCss = f'"{config.fontFamily}", {_systemFontStack}'

    try:
        template = _jinja2Env.get_template("page.html")
    except jinja2.TemplateNotFound as error:
        raise RuntimeError(
            f"Theme template not found at {_templatesDir / 'page.html'}. "
            f"Check that the pookiedocs package is installed correctly. Error: {error}"
        )

    breadcrumbs = _buildBreadcrumbs(nav_nodes, page_entry.urlPath, config.name, config.baseUrl)

    return template.render(
        siteName=config.name,
        fontFamilyCss=fontFamilyCss,
        pageTitle=page_entry.title,
        pageContent=html_body,
        navNodes=nav_nodes,
        searchEnabled=True,
        baseUrl=config.baseUrl,
        currentUrl=page_entry.urlPath,
        logoUrl=config.logo,
        breadcrumbs=breadcrumbs,
    )
