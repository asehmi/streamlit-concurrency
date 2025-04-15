from ._decorator_2 import wrap_async, wrap_sync


def test_1():
    @wrap_sync()
    def f(x: int, y: int) -> int:
        return x + y

    a = f(1, 2)
