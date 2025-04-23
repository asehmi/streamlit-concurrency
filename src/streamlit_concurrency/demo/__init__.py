from .bootstrap import logger
from . import example_func
from .log_sink import create_log_record_sink, test_log_sink
from .page_src import render_page_src, read_repo_file

__all__ = [
    "example_func",
    "create_log_record_sink",
    "test_log_sink",
    "render_page_src",
    "read_repo_file",
]

logger.info(f"{__name__} loaded")
