import pytest

def demo():
    return "Dave"


def test_demo():
    assert  demo() == "Dave"