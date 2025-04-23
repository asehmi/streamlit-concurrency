import logging
import contextlib
import itertools
import streamlit.logger as st_logger

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def create_log_record_sink(
    level: int = logging.INFO,
    logger_names: frozenset[str] | None = None,
    format: str
    | None = "%(asctime)s %(levelname)s %(threadName)s %(name)s - %(funcName)s: %(message)s",
    capture_streamlit_log: bool = False,
):
    """Attach a log sink to Python root logger or stream to capture LogRecord-s and formatted log lines"""
    records: list[logging.LogRecord] = []
    lines: list[str] = []

    formatter = format and logging.Formatter(format)

    handler = logging.NullHandler(level)

    def append_log(record: logging.LogRecord) -> bool:
        if logger_names is None or record.name in logger_names:
            records.append(record)

            if formatter:
                lines.append(formatter.format(record))
            return True
        return False

    handler.handle = append_log

    log_src = st_logger.get_logger("root") if capture_streamlit_log else logging.root

    log_src.addHandler(handler)

    yield records, lines

    log_src.removeHandler(handler)


def test_log_sink():
    with create_log_record_sink() as (log_records, log_lines):
        logger.warning("test")
        logger.warning("test2")

    for rec, line in itertools.zip_longest(log_records, log_lines):
        print(rec, "=>", line)
