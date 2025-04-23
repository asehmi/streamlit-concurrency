import streamlit as st
import streamlit.runtime.scriptrunner as st_scriptrunner
from ._errors import UnsupportedCallSite

import logging

logger = logging.getLogger(__name__)

_orig_get_ctx = st_scriptrunner.get_script_run_ctx


def _strict_get_ctx(suppress_warning: bool = False):
    ctx = _orig_get_ctx(suppress_warning=False)
    if not ctx:
        raise UnsupportedCallSite("No script run context found.")
    return ctx


def _prohibit_get_ctx(suppress_warning: bool = False):
    raise UnsupportedCallSite("Unexpected call")


def patch_st_get_ctx(strict=False, prohibit=False):
    if prohibit:
        logger.warning("Patching get_script_run_ctx to prohibit its use")
        st_scriptrunner.get_script_run_ctx = _prohibit_get_ctx
    elif strict:
        logger.warning("Patching get_script_run_ctx to detect unexpected use")
        st_scriptrunner.get_script_run_ctx = _strict_get_ctx
    else:
        logger.warning("Restoring get_script_run_ctx")
        st_scriptrunner.get_script_run_ctx = _orig_get_ctx
