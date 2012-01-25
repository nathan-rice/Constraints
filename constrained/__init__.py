'''
Created on Jan 18, 2012

@author: Nathan
'''

from proxy import SymbolicObject
from meta import Constraints
import util


if __name__ == "__main__":
    X = SymbolicObject(3)
    const = Constraints(X * 2 + 1 >= 5, X % 2 != 0)
    const2 = Constraints(X[-1] == "h")
    const3 = Constraints(X[-1].upper() == "H")
    assert isinstance(3, const)
    assert not isinstance(2, const)
    assert not isinstance(-100, const)
    assert not isinstance("bleH", const2)
    assert isinstance("bleh", const3)
