import pytest
from .state import use_state


def test_use_state_factory_inited(stub_run_ctx_cm):
    with stub_run_ctx_cm:
        # Import the use_state function
        state = use_state("test_key", factory=lambda: 42)

    assert state.value == 42

    # Modify the state by a value
    state.value = 100
    assert state.value == 100

    # Modify the state by reducer + action
    state.reduce(
        lambda prev, delta: (prev or 0) + delta,
        1,
    )
    assert state.value == 101

    # Clear the state
    state.deinit()

    # reading uninitialized state should raise KeyError
    with pytest.raises(KeyError):
        state.value


def test_use_state_not_inited(stub_run_ctx_cm):
    with stub_run_ctx_cm:
        state = use_state("test_key")

    with pytest.raises(KeyError):
        state.value

    with pytest.raises(KeyError):
        state.reduce(
            lambda prev, delta: (prev or 0) + delta,
            3,
        )
    state.value = 3
    assert state.value == 3


def test_use_state_type(stub_run_ctx_cm):
    with stub_run_ctx_cm:
        state = use_state("test_key", type_=int)

    with pytest.raises(KeyError):
        assert state.value == 2  # this should type check
