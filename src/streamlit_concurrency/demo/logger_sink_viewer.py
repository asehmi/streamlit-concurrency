import datetime
import asyncio
import pandas as pd
import logging
from streamlit_concurrency.log_sink import create_log_sink


async def capture_logs_render_df(
    dest, duration: float, update_interval=0.05, log_level=logging.INFO
):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    with create_log_sink(level=log_level) as (records, lines):
        while datetime.datetime.now() < deadline:
            df = pd.DataFrame(
                {
                    "time": r.created,
                    "thread": r.threadName,
                    "message": r.message,
                    "args": r.args,
                }
                for r in records
            )
            dest.dataframe(df)

        await asyncio.sleep(update_interval)
