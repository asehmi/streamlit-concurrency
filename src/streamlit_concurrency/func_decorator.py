import inspect
from typing import (
    Awaitable,
    Callable,
    Literal,
    Optional,
    ParamSpec,
    TypeVar,
    Union,
    Coroutine,
    overload,
)
from ._func_cache import CacheConf
from ._decorator_async import transform_async
from ._decorator_sync import transform_sync
from ._errors import UnsupportedExecutor

R = TypeVar("R")
P = ParamSpec("P")


class FuncDecorator:
    def __init__(
        self,
        cache: Optional[CacheConf | dict] = None,
        executor: Literal["thread", "process"] = "thread",
        with_script_run_context: bool = False,
    ):
        if cache and cache.get("show_spinner"):
            # show_spinner uses spinner widget and requires a ScriptRunContext.
            # Not support it is just simpler.
            raise ValueError("cache.show_spinner is not supported.")
        self.__cache = cache
        self.__executor = executor
        self.__with_script_run_context = with_script_run_context

    @overload  # for async function
    def __call__(
        self,
        func: Union[
            Callable[P, Awaitable[R]],
            Callable[P, Coroutine[None, None, R]],
        ],
    ) -> Callable[P, Coroutine[None, None, R]]: ...

    @overload  # for sync function
    def __call__(
        self,
        func: Callable[P, R],
    ) -> Callable[P, Coroutine[None, None, R]]: ...

    def __call__(self, func):
        assert callable(func), "expected a Callable"
        assert not inspect.isgeneratorfunction(func) and not inspect.isasyncgenfunction(
            func
        ), "expected a non-generator Callable"
        if inspect.iscoroutinefunction(func):
            return transform_async(
                func,
                cache=self.__cache,
                executor=self.__executor,  # type: ignore
                with_script_run_context=self.__with_script_run_context,
            )
        else:
            return transform_sync(
                func,
                cache=self.__cache,
                executor=self.__executor,  # type: ignore
                with_script_run_context=self.__with_script_run_context,
            )


def run_in_executor(
    cache: Optional[CacheConf | dict] = None,
    # TODO: support process pool executor (Th)
    # TODO: support custom executor
    executor: Literal["thread", "process"] = "thread",
    with_script_run_context: bool = False,
) -> FuncDecorator:
    if executor != "thread":
        raise UnsupportedExecutor("Executors other than 'thread' is not supported yet.")
    return FuncDecorator(
        cache=cache, executor=executor, with_script_run_context=with_script_run_context
    )
