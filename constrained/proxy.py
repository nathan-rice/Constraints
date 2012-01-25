'''
Created on Jan 18, 2012

@author: Nathan
'''

from decorator import decorator
import operator
import types

def create_cell(obj):
    """
    Create a cell object which references `obj`.
    """
    return (lambda: obj).func_closure[0]

def copy_func(f, code=None, globals_=None, name=None, argdefs=None, closure=None):
    """
    Create a copy of a function, replacing any portions specified.
    """
    return types.FunctionType(
        code or f.func_code,
        globals_ or f.func_globals,
        name or f.func_name,
        argdefs or f.func_defaults,
        closure or f.func_closure
    )

@decorator
def chainable(f, self, *args, **kwargs):
    """Chainable functions return OperationProxy objects."""
    return type(self)(f(self, *args, **kwargs), self)


class SymbolicObject(object):

    def __init__(self, f=None, parent=None):
        self._f = f
        self.parent = parent

    @property
    def f(self):
        return self._f()

    @f.setter
    def f(self, func):
        if not isinstance(func, (types.FunctionType, SymbolicObject)):
            self._f = lambda: func
        else:
            self._f = func

    def __evaluate__(self, f):
        current = self
        while current.parent is not None:
            current = current.parent
        current.f = f
        return self.f

    @chainable
    def __call__(self, *args, **kwargs):
        return lambda: self.f(*args, **kwargs)

    @chainable
    def __getattr__(self, attr):
        return lambda: getattr(self.f, attr)

    @chainable
    def __reversed__(self):
        return lambda: reversed(self.f)

    @chainable
    def __getitem__(self, item):
        return lambda: self.f[item]

    @chainable
    def __hash__(self):
        return lambda: hash(self.f)

    @chainable
    def __invert__(self):
        return lambda:~self.f

    @chainable
    def __index__(self):
        return lambda: operator.index(self.f)

    @chainable
    def __neg__(self):
        return lambda:-self.f

    @chainable
    def __pos__(self):
        return lambda:+self.f

    @chainable
    def __abs__(self):
        return lambda: abs(self.f)

    @chainable
    def __add__(self, other):
        return lambda: self.f + other

    @chainable
    def __sub__(self, other):
        return lambda: self.f - other

    @chainable
    def __mul__(self, other):
        return lambda: self.f * other

    @chainable
    def __floordiv__(self, other):
        return lambda: self.f // other

    @chainable
    def __mod__(self, other):
        return lambda: self.f % other

    @chainable
    def __divmod__(self, other):
        return lambda: divmod(self.f, other)

    @chainable
    def __pow__(self, other, modulo=None):
        return lambda: pow(self.f, other, modulo)

    @chainable
    def __lshift__(self, other):
        return lambda: self.f << other

    @chainable
    def __rshift__(self, other):
        return lambda: self.f >> other

    @chainable
    def __div__(self, other):
        return lambda: self.f / other

    @chainable
    def __truediv__(self, other):
        return lambda: self.f.__truediv__(other)

    @chainable
    def __radd__(self, other):
        return lambda: other + self.f

    @chainable
    def __rand__(self, other):
        return lambda: other & self.f

    @chainable
    def __rdiv__(self, other):
        return lambda: other / self.f

    @chainable
    def __rdivmod__(self, other):
        return lambda: divmod(other, self.f)

    @chainable
    def __rfloordiv__(self, other):
        return lambda: other // self

    @chainable
    def __rlshift__(self, other):
        return lambda:other << self

    @chainable
    def __rmod__(self, other):
        return lambda:other % self

    @chainable
    def __rmul__(self, other):
        return lambda: other * self

    @chainable
    def __ror__(self, other):
        return lambda: other | self

    @chainable
    def __rpow__(self, other):
        return lambda: pow(other, self)

    @chainable
    def __rrshift__(self, other):
        return lambda: other >> self

    @chainable
    def __rsub__(self, other):
        return lambda: other - self

    @chainable
    def __rtruediv__(self, other):
        return lambda: self.__rtruediv__(other)

    @chainable
    def __rxor__(self, other):
        return lambda: other ^ self

    @chainable
    def __contains__(self, item):
        return lambda: item in self.f

    @chainable
    def __eq__(self, other):
        return lambda: self.f == other

    @chainable
    def __ne__(self, other):
        return lambda: self.f != other

    @chainable
    def __le__(self, other):
        return lambda: self.f <= other

    @chainable
    def __lt__(self, other):
        return lambda: self.f < other

    @chainable
    def __gt__(self, other):
        return lambda: self.f > other

    @chainable
    def __ge__(self, other):
        return lambda: self.f >= other

    @chainable
    def __cmp__(self, other):
        return lambda: cmp(self.f, other)

    @chainable
    def __and__(self, other):
        return lambda: self.f & other

    @chainable
    def __xor__(self, other):
        return lambda: self.f ^ other

    @chainable
    def __or__(self, other):
        return lambda: self.f | other

    @chainable
    def __iand__(self, other):
        return lambda: self.f.__iand__(other)

    @chainable
    def __ixor__(self, other):
        return lambda: self.f.__ixor__(other)

    @chainable
    def __ior__(self, other):
        return lambda: self.f.__ior__(other)

    @chainable
    def __iadd__(self, other):
        return lambda: self.f.__iadd__(other)

    @chainable
    def __isub__(self, other):
        return lambda: self.f.__isub__(other)

    @chainable
    def __imul__(self, other):
        return lambda: self.f.__imul__(other)

    @chainable
    def __idiv__(self, other):
        return lambda: self.f.__idiv__(other)

    @chainable
    def __itruediv__(self, other):
        return lambda: self.f.__itruediv__(other)

    @chainable
    def __ifloordiv__(self, other):
        return lambda: self.f.__ifloordiv__(other)

    @chainable
    def __imod__(self, other):
        return lambda: self.f.__imod__(other)

    @chainable
    def __ipow__(self, other, modulo=None):
        return lambda: self.f.__ipow__(other, modulo)

    @chainable
    def __ilshift__(self, other):
        return lambda: self.f.__ilshift__(other)

    @chainable
    def __irshift__(self, other):
        return lambda: self.f.__irshift__(other)
