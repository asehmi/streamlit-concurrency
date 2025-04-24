import logging
from .log_sink import create_log_sink

logger = logging.getLogger(__name__)


def test_log_sink_all_logs():
    with create_log_sink() as (log_records, log_lines):
        logger.warning("test1")
        logger.warning("test2")

    assert next(l for l in log_lines if "test1" in l) is not None
    assert next(l for l in log_lines if "test2" in l) is not None
    assert next((l for l in log_lines if "test3" in l), None) is None


def test_log_sink_skip_formattr():
    with create_log_sink(format=None) as (log_records, log_lines):
        logger.warning("test1")

    assert len(log_lines) == 0
    assert len(log_records) > 0
