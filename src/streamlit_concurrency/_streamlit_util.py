import contextlib
import threading
from typing import Optional
import streamlit as st
import streamlit.runtime.scriptrunner as st_scriptrunner

from streamlit.runtime.scriptrunner import (
    ScriptRunContext,
)
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)

import logging

from ._errors import UnsupportedCallSite

logger = logging.getLogger(__name__)


def assert_st_script_run_ctx(callee: str) -> ScriptRunContext:
    """Assert that the current thread is the script thread."""
    ctx = st_scriptrunner.get_script_run_ctx(suppress_warning=True)
    if ctx is None:
        raise UnsupportedCallSite(
            f"{callee} must be called in a thread with ScriptRunContext. Typically a thread streamlit created to run a page."
        )
    return ctx


def _format_script_run_ctx(ctx: Optional[ScriptRunContext]):
    return (
        f"ScriptRunContext(session={ctx.session_id}, page_script_hash={ctx.page_script_hash})"
        if ctx
        else None
    )


@contextlib.contextmanager
def create_script_run_context_cm(ctx: ScriptRunContext):
    """Create a context manager that

    - when enter, adds given script_run_ctx to the current thread
    - when exit, un-adds it from current thread

    TODO: add assertion to ensure a thread cannot enter twice
    """
    existing_ctx = st_scriptrunner.get_script_run_ctx(suppress_warning=True)
    existing_ctx_repr = _format_script_run_ctx(existing_ctx)

    ctx_repr = _format_script_run_ctx(ctx)
    if existing_ctx is not None and existing_ctx is not ctx:
        raise RuntimeError(
            f"Current thread {threading.current_thread().name} had an unexpected ScriptRunContext: {existing_ctx}."
        )

    st_scriptrunner.add_script_run_ctx(thread=threading.current_thread(), ctx=ctx)
    logger.debug(
        "Attached captured ScriptRunContext %s . Current thread had %s .",
        ctx_repr,
        existing_ctx_repr,
    )
    yield

    # restore the original value, whether it was None or not (this can't be done with add_script_run_ctx)
    setattr(threading.current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, existing_ctx)
    assert st_scriptrunner.get_script_run_ctx(suppress_warning=True) is existing_ctx
    logger.debug("Restored to original ScriptRunContext %s", existing_ctx_repr)
