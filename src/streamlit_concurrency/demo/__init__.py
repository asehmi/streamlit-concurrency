from .bootstrap import logger
from . import example_func
from .page_src import render_page_src, read_repo_file

__all__ = [
    "example_func",
    "render_page_src",
    "read_repo_file",
]

logger.info(f"{__name__} loaded")
