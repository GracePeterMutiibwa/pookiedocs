import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DocsConfig:
    name: str
    docsDir: str = "docs"
    staticDir: str = "static"
    outputDir: str = "dist"
    baseUrl: str = "/"
    fontFamily: str = "system"
    logo: str | None = None


def loadConfig(config_path: str = "pookiedocs.config.py") -> DocsConfig:
    resolvedPath = Path(config_path).resolve()

    if not resolvedPath.exists():
        raise FileNotFoundError(
            f"Config file not found at '{resolvedPath}'. "
            f"Create a pookiedocs.config.py file in your project root with a DOCS = DocsConfig(...) assignment."
        )

    moduleName = "pookiedocs_user_config"
    spec = importlib.util.spec_from_file_location(moduleName, resolvedPath)

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not load config from '{resolvedPath}'. "
            f"Check that the file is valid Python and readable."
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = module

    try:
        spec.loader.exec_module(module)
    except Exception as error:
        raise ImportError(
            f"Error while executing config file '{resolvedPath}': {error}. "
            f"Check that pookiedocs.config.py contains no syntax errors and all imports resolve."
        ) from error

    if not hasattr(module, "DOCS"):
        raise AttributeError(
            f"Config file '{resolvedPath}' has no DOCS attribute. "
            f"Add: DOCS = DocsConfig(name='My Project') to the file."
        )

    docsValue = module.DOCS

    if not isinstance(docsValue, DocsConfig):
        raise TypeError(
            f"DOCS in '{resolvedPath}' must be a DocsConfig instance, "
            f"got {type(docsValue).__name__} instead."
        )

    return docsValue
