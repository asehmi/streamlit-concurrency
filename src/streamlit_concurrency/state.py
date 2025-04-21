import streamlit
from typing import Generic, Type, TypeVar, Any
from ._func_util import assert_has_script_thread

S = TypeVar("S")

st_f = f""


class StateRef(Generic[S]):
    """
    A reference to a state object that can be used to access and modify the state.
    """

    def __init__(
        self,
        storage: dict,
        key: str,
    ):
        self.__storage = storage
        self.__key = key


def use_state(key: str, namespace: str | None = None, type_: Type[S] ) -> S:
    assert_has_script_thread("use_state(key, namespace)")
    storage = streamlit.session_state.get("_streamlit_concurrency_states")
    if storage is None:
        storage = {}
        streamlit.session_state["_streamlit_concurrency_states"] = storage
    full_key = f"{namespace}:|:{key}"
    return StateRef(storage, full_key)
