'''
Created on Jan 18, 2012

@author: Nathan
'''

from sys import _getframe
from abc import ABCMeta
from proxy import Symbol
from decorator import decorator
from inspect import getcallargs

def _frame_value(name):
    # We have to break out of all the decorators in order to get the outer scope
    frame = _getframe(3)
    return frame.f_locals[name]

class Constraints(ABCMeta):
    """
    Metaclass which provides constraint verification for objects.  Constraints
    are specified as arguments to the __new__ method.  Constraints can be either
    no argument callables or Symbol expressions.
    
    isinstance(obj, ConstraintsInstance) will return True iff obj satisfies all
    constraints.
    
    """

    def __init__(self, *args):
        pass

    def __new__(self, *args):
        return super(Constraints, self).__new__(
            self,
            "Constraint",
            (ConstraintBase,),
            {"args":args}
        )

    def __instancecheck__(self, other):
        # We need to replace the placeholder object with other
        return all(
            not isinstance(arg, Symbol) and arg(other) or \
            arg.__evaluate__(other) for arg in self.args
        )


class ConstraintBase(object):
    """Constraint base class.  Constraints are usable as descriptors."""

    def __init__(self, callable=None, name=None):
        if name is None and isinstance(callable, basestring):
            # If someone wants to pass name where callable should be, we are ok with that.
            (name, callable) = (callable, name)
        self.name = name
        self.callable = callable

    def __get__(self, obj, type=None):
        return getattr(self, "value", None)

    def __set__(self, obj, value):
        if isinstance(value, type(self)):
            self.value = value
        else:
            raise AssertionError("Specified value (%s) does not satisfy this"
                                 " constraint" % value)

    def __delete__(self, obj):
        try:
            del self.value
        except AttributeError:
            pass

    @classmethod
    def precondition(self, callable=None, name=None):
        """
        Returns a Precondition instance.
        
        :param callable: A no argument callable.
        :param name: The name of the variable to verify.
        :type name: string

        .. note::
            
            `callable`, if specified, takes precedence over `name` in situations
            where either could be used.  If `name` is not specified and `callable`
            is a string, `callable` will be used as `name`.
        """
        return Precondition(self,
            callable or getattr(self, "callable", None),
            name or getattr(self, "name", None)
        )

    @classmethod
    def postcondition(self, callable=None, name=None):
        """
        Returns a Postcondition instance.
        
        :param callable: A no argument callable.
        :param name: The name of the variable to verify.
        :type name: string

        .. note::
            
            `callable`, if specified, takes precedence over `name` in situations
            where either could be used.  If `name` is not specified and `callable`
            is a string, `callable` will be used as `name`.
        """
        return Postcondition(self,
            callable or getattr(self, "callable", None),
            name or getattr(self, "name", None)
        )

    @classmethod
    def invariant(self, callable=None, name=None):
        """
        Returns an Invariant instance.
        
        :param callable: A no argument callable.
        :param name: The name of the variable to verify.
        :type name: string

        .. note::
            
            `callable`, if specified, takes precedence over `name` in situations
            where either could be used.  If `name` is not specified and `callable`
            is a string, `callable` will be used as `name`.
        """
        return Invariant(self,
            callable or getattr(self, "callable", None),
            name or getattr(self, "name", None)
        )


class ConditionBase(object):
    """Contract style condition base class."""

    def __init__(self, constraint, target=None, name=None):
        self.constraint = constraint
        if name is None and isinstance(target, basestring):
            # If someone wants to pass name where callable should be, we are ok with that.
            (name, target) = (target, name)
        self.target = target
        self.name = name

    def __call__(self, f):
        return decorator(self.decorator, f)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Precondition(ConditionBase):
    """
    Condition object specifying a precondition.  Usable as a decorator or
    context manager.
    
    .. note::
    
        You must specify a string argument name for the precondition or the decorator
        will not function properly.
    """

    def __enter__(self):
        value = (getattr(self, "target", None) or (lambda: _frame_value(self.name)))()
        if not isinstance(value, self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " pre-condition" % value)

    def decorator(self, f, *args, **kwargs):
        """
        Precondition decorator, looks at the bound value of the arg with the
        key equal to self.name.
        """
        arg_values = getcallargs(f, *args, **kwargs)
        arg = arg_values[self.name]
        if not isinstance(arg, self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " pre-condition" % arg)
        return f(*args, **kwargs)


class Postcondition(ConditionBase):
    """
    Condition object specifying an postcondition.  Usable as a decorator
    or context manager.
    
    .. note::
    
        The decorator constrains the return value of the decorated function.  It
        ignores the callable and name attributes of the condition if they are present.
    """

    def __exit__(self, exc_type, exc_val, exc_tb):
        value = (getattr(self, "target", None) or (lambda: _frame_value(self.name)))()
        if not isinstance(value, self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " post-condition" % value)

    def decorator(self, f, *args, **kwargs):
        result = f(*args, **kwargs)
        if not isinstance(result, self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " post-condition" % result)
        return result


class Invariant(ConditionBase):
    """Condition object specifying an invariant.  Usable as a context manager."""

    def __enter__(self):
        value = (getattr(self, "target", None) or (lambda: _frame_value(self.name)))()
        if not isinstance(value, self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " invariant condition" % value)

    def __exit__(self, exc_type, exc_val, exc_tb):
        value = (getattr(self, "target", None) or (lambda: _frame_value(self.name)))()
        if not isinstance(value, self.constraint):
            raise AssertionError("The value (%s) did not meet the specified"
                                 " invariant condition" % value)

    def __call__(self, f):
        raise NotImplementedError("Invariant objects do not provide decorator functionality")
