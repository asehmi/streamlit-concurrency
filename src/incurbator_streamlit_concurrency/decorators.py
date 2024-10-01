from functools import singledispatch
from typing import Callable, Optional, TypedDict, Union, Unpack
from concurrent.futures import Executor
from enum import StrEnum
from concurrent.futures import Executor


class Param(TypedDict):
    executor: Optional[Union[str, Executor]]
    cache_session: Optional[bool]
    cache_global: Optional[bool]
    cache_size: Optional[int]


class CacheLocation(StrEnum):
    session = "session" # wrapped function must be called in a thread (either a Script Thread) , or an other 
    # GLOBAL = "global"
    executor = 'executor'
    CUSTOM = 'cache_key'


class ExecutorType(StrEnum):
    threaded = "threaded"
    process = "process"



class DecoratorParams(TypedDict):
    copy_script_run_context: Optional[bool]
    executor: Optional[Union[Executor, ExecutorType]]
    cache_location: Optional[Union[CacheLocation, Callable]] 
    cache_size: Optional[int]


class CachedCallable():
    def __init__(self, get_cache_storage: Callable, f: Callable):
        self.get_cache_storage = get_cache_storage
        self.f = f
    
    def __call__(self, *args, **kwargs):
        cache_storage = self.get_cache_storage()
        return self.f(*args, **kwargs)

def wrap_callable(callable, params: Unpack[DecoratorParams]) -> Callable:
    executor = params.get("executor")
    match executor:
        case ExecutorType.threaded | None:
            from .executors import sfc_thread_pool_executor
            executor = sfc_thread_pool_executor
        case _ if isinstance(executor, Executor):
            pass
        # case _ if callable(executor):
            # executor = executor()
        case _:
            raise ValueError(f"unrecognized executor: {executor}")
    assert isinstance(executor, Executor), f"executor must be an instance of concurrent.futures.Executor, got {executor}"

    # TODO
    copy_script_run_context = params.get("copy_script_run_context", False)
    if copy_script_run_context:
        raise NotImplemented("copy_script_run_context is not implemented yet")

    cache_location = params.get("cache_location", None)
    def get_cache_storage() -> dict:

    

    def wrapped(*args, **kwargs):
        # TODO
        return callable(*args, **kwargs)

    return wrapped

def run_in_executor(**params: Unpack[DecoratorParams]) -> Callable:
    # too bad we cannot name it 🍛
    def curried(f: Callable):
        assert callable(f), "callable expected. e.g. run_in_executor()(f)"
        return wrap_callable(f, params)
    return curried

@singledispatch
def run_in_worker_thread(
    maybe_callable: Optional[Callable] = None, **kwargs
) -> Callable:
    raise AssertionError("should not be here")


@run_in_worker_thread.register
def impl_none(none: None, **kwargs) -> Callable:
    return lambda callable: _wrapper(callable, **kwargs)


@run_in_worker_thread.register
def impl_callable(callable: Callable, **kwargs) -> Callable:
    return _wrapper(callable, **kwargs)


def _wrapper(f: Callable, **kwargs):
    return f
