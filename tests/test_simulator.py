"""
test_simulator.py

Unit-tests for the simulator.run_one function.
"""

from simulator.simulator import run_one


def test_run_one_returns_bool_and_int() -> None:
    delivered, hops = run_one(0.0)
    assert isinstance(delivered, bool)
    assert isinstance(hops, int)
    assert hops >= 0

    delivered1, hops1 = run_one(1.0)
    assert isinstance(delivered1, bool)
    assert isinstance(hops1, int)
    assert hops1 >= 0
