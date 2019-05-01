import pytest

from tests.helper import Success, state, dummy_checks
from protowhat.Test import TestFail as TF
from protowhat.sct_syntax import ExGen, F
from protowhat.utils import legacy_signature, _debug

state = pytest.fixture(state)
dummy_checks = pytest.fixture(dummy_checks)


def test_debug(state, dummy_checks):
    state.do_test(Success("msg"))
    Ex = ExGen(state, dummy_checks)
    try:
        Ex().noop().child_state() >> F(attr_scts={"_debug": _debug})._debug("breakpoint name")
    except TF as e:
        assert "breakpoint name" in str(e)
        assert "history" in str(e)
        assert "child_state" in str(e)
        assert "test" in str(e)


def test_legacy_signature():
    @legacy_signature(old_arg1="arg1", old_arg2="arg2")
    def func(arg1, arg2=1):
        return arg1 + arg2

    assert func(1) == 2
    assert func(arg1=1) == 2
    assert func(old_arg1=1) == 2
    assert func(1, arg2=2) == 3
    assert func(1, old_arg2=2) == 3
    assert func(arg1=1, old_arg2=2) == 3
    assert func(old_arg1=1, arg2=2) == 3
    assert func(old_arg1=1, old_arg2=2) == 3
