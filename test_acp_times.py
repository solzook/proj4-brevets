"""
Nose tests for acp_times.py
"""
import acp_times.py

def test_calc_open_basic():
    """
    initial test
    """
    assert acp_times.calc_open(0, 200) == 0
    assert acp_times.calc_open(250, 300) == (200/34 + 50/32)
    assert acp_times.calc_open(219, 200) == (200/34)

def test_calc_close_basic():
    """
    initial test
    """
    assert acp_times.calc_close(0, 1000) == 1
    assert acp_times.calc_close(500, 600) == (200/34 + 200/32 + 100/30)
    assert acp_times.calc_close(210, 200) == 13.5
