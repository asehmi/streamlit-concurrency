import datetime
import asyncio
from typing import Iterable
import pandas as pd
import logging
from streamlit_concurrency.log_sink import create_log_sink

logger = logging.getLogger(__name__)


async def capture_logs_render_df(
    dest,
    duration: float = 3,
    update_interval=0.2,
    level=logging.INFO,
    logger_names: Iterable[str] | None = None,
):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    with create_log_sink(level=level, logger_names=logger_names) as (records, lines):

        def render_logs():
            if not records:
                dest.write("waiting for logs...")
                return
            df = pd.DataFrame(
                {
                    "time": datetime.datetime.fromtimestamp(r.created),
                    "thread": r.threadName,
                    "message": r.message,
                    "args": r.args,
                }
                for r in records
            )
            dest.dataframe(df)

        while datetime.datetime.now() < deadline:
            render_logs()
            await asyncio.sleep(update_interval)
    render_logs()
