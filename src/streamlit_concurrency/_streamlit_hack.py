"""
Monkey patch streamlit for test

NOTE other code MUST not import functions from st_scriptrunner as
they get monkey patched in test. Import the containing module instead.
"""

import logging

import streamlit.runtime.scriptrunner as st_scriptrunner
import streamlit.delta_generator as st_delta_generator
from ._errors import UnsupportedCallSite

logger = logging.getLogger(__name__)

_orig_get_ctx = st_scriptrunner.get_script_run_ctx


def _strict_get_ctx(suppress_warning: bool = False):
    ctx = _orig_get_ctx(suppress_warning=False)
    if not ctx:
        raise UnsupportedCallSite("No script run context found.")
    return ctx


def _prohibit_get_ctx(suppress_warning: bool = False):
    raise UnsupportedCallSite("Call to get_script_run_ctx is prohibited.")


def patch_st_get_ctx(strict=False, prohibit=False):
    sites = (
        # the definition
        st_scriptrunner,
        # modules importing the function by name
        st_delta_generator,  # used by spinner used by cache_data "show_spinner"
    )
    if prohibit:
        logger.debug("Patching get_script_run_ctx to always throw")
        for site in sites:
            site.get_script_run_ctx = _prohibit_get_ctx  # type: ignore
    elif strict:
        logger.debug("Patching get_script_run_ctx to throw instead of warn")
        for site in sites:
            site.get_script_run_ctx = _strict_get_ctx  # type: ignore
    else:
        logger.debug("Restoring get_script_run_ctx")
        for site in sites:
            site.get_script_run_ctx = _orig_get_ctx  # type: ignore
