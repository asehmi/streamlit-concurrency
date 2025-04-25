import threading
import pytest
import contextlib

from ._streamlit_hack import patch_st_get_ctx
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)


# fixtures


@pytest.fixture
def stricter_get_run_ctx():
    """Fixture to patch get_script_run_ctx to be stricter about its use."""
    patch_st_get_ctx(strict=True)
    yield
    patch_st_get_ctx()


@pytest.fixture
def prohibit_get_run_ctx():
    """Fixture to patch get_script_run_ctx to be stricter about its use."""
    patch_st_get_ctx(prohibit=True)
    yield
    patch_st_get_ctx()


@pytest.fixture
def stub_run_ctx_cm():
    return _create_stub_run_ctx_cm()


@contextlib.contextmanager
def _create_stub_run_ctx_cm():
    """Create a stub ScriptRunContext."""
    setattr(
        threading.current_thread(),
        SCRIPT_RUN_CONTEXT_ATTR_NAME,
        DummyScriptRunContext("stub_script_run_context"),
    )
    yield
    delattr(threading.current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME)


class DummyObject:
    def __init__(self, root: str = "dummy_object", path: tuple[str, ...] = tuple()):
        self.__path = path
        self.__root = root

    def __getattr__(self, name: str) -> "DummyObject":
        return DummyObject(root=self.__root, path=self.__path + (name,))

    def __repr__(self) -> str:
        return ".".join((self.__root,) + self.__path)

    def __str__(self) -> str:
        return ".".join((self.__root,) + self.__path)


class DummyScriptRunContext(DummyObject):
    # mock this property in real ScriptRunContext which is set from its_script_runner.session_state
    @property
    def session_state(self):
        # imitate
        return {}
