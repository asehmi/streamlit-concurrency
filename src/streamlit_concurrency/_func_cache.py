from datetime import timedelta
from streamlit.runtime.caching.cache_data_api import (
    CachePersistType,
)
from streamlit.runtime.caching.hashing import HashFuncsDict
from typing import Callable, Optional, TypedDict, Hashable, Union


class CacheConf(TypedDict):
    """params for streamlit.cache_data"""

    ttl: float | timedelta | str | None
    max_entries: int | None
    # not suported. Passing in a value will raise
    # show_spinner: Optional[bool]
    persist: CachePersistType | bool | None
    hash_funcs: HashFuncsDict | None
    # TODO: use this to provide more exact hash
    extra_entropy: Union[Hashable, Callable[[], Hashable]]
