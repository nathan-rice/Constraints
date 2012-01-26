Constraints - Sleek contract-style validation tools
===================================================

Constraints provides flexible validation tools for a variety of circumstances.
All validation in constraints is done by type checking.  Constraints provides
a special abstract base class (Constraints) which facilitates on the fly
construction of validation types.  Constraints also provides a special class
(Symbol) which can be used to generate natural, easy to read constraint expressions.

for example::

   >>> from constraints.proxy import Symbol
   >>> from constraints.types import Constraints
   >>> X = Symbol()
   >>> SizeConstraint = Constraints(X * 2 + 1 >= 5)
   >>> ModuloConstraint = Constraints(X % 2 != 0, X != 3)
   >>> CharacterConstraint = Constraints(X[-1] == "h")
   # My apologies for the lambda spam.  I provide some functions in
   # constraints.util for this purpose...
   >>> callable_expr = lambda x: all(lambda x: isinstance(x, SizeConstraint), x)
   >>> CollectionConstraint = Constraint(callable_expr)
   >>> isinstance(1, SizeConstraint)
   False
   >>> isinstance(2, SizeConstraint)
   True
   >>> isinstance(1, ModuloConstraint)
   True
   >>> isinstance("blah", CharacterConstraint)
   True
   >>> isinstance([2, 3, 4, 5], CollectionConstraint)
   True
   
Constraint instances also provide descriptors which will verify values at set
time.  For example::

   >>> class Foo(object):
   ...    x = Constraints(X > 2)
   ... 
   >>> bar = Foo()
   >>> bar.x = 1
   Traceback (most recent call last):
      ...
   AssertionError: Specified value (1) does not satisfy this constraint
   
Design by contract style preconditions, postconditions and invariants are also
supported, and can be used either as context managers or function decorators::

   >>> x_pre = SizeConstraint.precondition("x")
   >>> x_post = SizeConstraint.postcondition("x")
   >>> x = 1
   >>> with x_pre:
   ...   do_stuff()
   ...
   Traceback (most recent call last):
      ...
   AssertionError: The value (1) did not meet the specified pre-condition
   >>> x = 5
   >>> with x_post:
   ...   x -= 4
   ...
   Traceback (most recent call last):
      ...
   AssertionError: The value (1) did not meet the specified post-condition
   >>> @x_pre
   ... def foo(x):
   ...    return x
   ...
   >>> foo(1)
   Traceback (most recent call last):
      ...
   AssertionError: The value (1) did not meet the specified pre-condition
   >>> @x_post
   ... def foo(x):
   ...    return x - 5
   ...
   >>> foo(6)   
   Traceback (most recent call last):
      ...
   AssertionError: The value (1) did not meet the specified post-condition
   
Symbol objects are very flexible, and provide a nice
way to specify your constraints without resorting to a domain specific language.
Symbol objects are fairly simple;  whenever an operation is performed on them,
they capture it and return a new Symbol object wrapping the operation so that
it can be performed with concrete input at a later time.  There are exceptions
to this, for example isinstance, which uses the metaclass method, and the type
constructors (str, int, bool, etc) which throw an error if the correct type is
not returned.
   