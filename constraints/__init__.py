'''
Created on Jan 18, 2012

@author: Nathan
'''

from proxy import SymbolicObject
from types import Constraints

def test_instancecheck():
    assert isinstance(3, const1)
    assert not isinstance(-100, const1)
    assert isinstance(5, const2)
    assert not isinstance(2, const2)
    assert isinstance("bleh", const3)
    assert not isinstance("bleH", const3)
    assert isinstance("bleh", const4)
    assert isinstance("bleH", const4)
    assert not isinstance("blab", const4)

def test_descriptor_assertfail():
    bar = Test()
    try:
        bar.x = 1
        assert False
    except AssertError:
        pass

def test_descriptor_assertfail():
    bar = Test()
    bar.x = 3
    assert bar.x == 3

def test_contextmanager_pre():
    x = 5
    with const1.precondition("x"):
        x -= 10
    pass

def test_contextmanager_post():
    x = -5
    with const1.postcondition("x"):
        x += 10
    pass

def test_contextmanager_inv():
    x = 5
    with const1.invariant("x"):
        x = x
    pass

def test_contextmanager_pre_assertfail():
    x = 1
    try:
        with const1.precondition("x"):
            x -= 10
        assert False
    except AssertionError:
        pass

def test_contextmanager_post_assertfail():
    x = 5
    try:
        with const1.postcondition("x"):
            x -= 10
        assert False
    except AssertionError:
        pass

def test_contextmanager_inv_assertfail():
    x = 1
    try:
        with const1.invariant("x"):
            x -= 10
        assert False
    except AssertionError:
        pass
    x = 5
    try:
        with const1.invariant("x"):
            x -= 10
        assert False
    except AssertionError:
        pass

def test_decorator_pre():
    @const1.precondition("x")
    def foo(x):
        return x + 5
    assert foo(2) == 7

def test_decorator_post():
    @const1.postcondition("x")
    def foo(x):
        return x + 5
    assert foo(0) == 5

def test_decorator_inv():
    try:
        @const1.invariant("x")
        def foo(x):
            return x + 5
        assert False
    except NotImplementedError:
        pass

def test_decorator_pre_assertfails():
    @const1.precondition("x")
    def foo(x):
        return x + 5
    try:
        foo(0) == 5
        assert False
    except AssertionError:
        pass

def test_decorator_post_assertfails():
    @const1.postcondition("x")
    def foo(x):
        return x + 5
    try:
        foo(-5) == 0
        assert False
    except AssertionError:
        pass


if __name__ == "__main__":
    import nose
    X = SymbolicObject(3)
    const1 = Constraints(X * 2 + 1 >= 5)
    const2 = Constraints(X % 2 != 0, X != 3)
    const3 = Constraints(X[-1] == "h")
    const4 = Constraints(X[-1].upper() == "H")
    class Test(object):
        x = const1()
    nose.runmodule()
