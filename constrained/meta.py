'''
Created on Jan 18, 2012

@author: Nathan
'''


from abc import ABCMeta
from proxy import SymbolicObject
from decorator import decorator
from inspect import getcallargs


def arg_decorator(dec_f):
    def _decorator_factory(f, *args, **kwargs):
        return decorator(dec_f(*args, **kwargs), f)
    return _decorator_factory


class Constraints(ABCMeta):

    def __init__(self, *args):
        pass

    def __new__(self, *args):
        return super(Constraints, self).__new__(
            self,
            "Constraint",
            (object,),
            {"args":args}
        )

    def __instancecheck__(self, other):
        # We need to replace the placeholder object with other
        return all(
            not isinstance(arg, SymbolicObject) and arg(other) or \
            arg.__evaluate__(other) for arg in self.args
        )


class Constraint(object):

    __metaclass__ = Constraints

    def __get__(self):
        return getattr(self, "value", None)

    def __set__(self, value):
        if isinstance(value, self):
            self.value = value
        else:
            raise AssertionError("Specified value does not satisfy this constraint")

    def __delete__(self):
        try:
            del self.value
        except AttributeError:
            pass

    def precondition(self, variable):
        return Precondition(self, variable)

    def postcondition(self, variable):
        return Postcondition(self, variable)

    def invariant(self, variable):
        return Invariant(self, variable)


class Precondition(object):
    """Precondition context manager"""

    def __init__(self, constraint, target):
        self.target = target
        self.constraint = constraint

    def __enter__(self):
        if not isinstance(self.target(), self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " pre-condition" % self.target)

    def __exit__(self):
        pass

    @arg_decorator
    def __call__(self, name):
        def _check(f, *args, **kwargs):
            arg = getcallargs(f, args, kwargs)[name]
            if not isinstance(arg, self.constraint):
                raise AssertionError("The value (%s) did not meet the specified"
                                     " pre-condition" % arg)
            return f(*args, **kwargs)
        return _check



class Postcondition(object):
    """Postcondition context manager"""

    def __init__(self, constraint, target):
        self.target = target
        self.constraint = constraint

    def __enter__(self):
        pass

    def __exit__(self):
        if not isinstance(self.target(), self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " post-condition" % self.target)

    @arg_decorator
    def __call__(self, name):
        def _check(f, *args, **kwargs):
            arg = getcallargs(f, args, kwargs)[name]
            if not isinstance(arg, self.constraint):
                raise AssertionError("The value (%s) did not meet the specified"
                                     " post-condition" % arg)
            return f(*args, **kwargs)
        return _check


class Invariant(object):
    """Invariant context manager"""

    def __init__(self, constraint, target):
        self.target = target
        self.constraint = constraint

    def __enter__(self):
        if not isinstance(self.target(), self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " invariant condition" % self.target)

    def __exit__(self):
        if not isinstance(self.target(), self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " invariant condition" % self.target)

