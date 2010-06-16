
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Case Maker creates test case methods.

class TestSomething(unittest.TestCase):
    __metaclass__ = AssertingMetaClass

    _ASSERT_EQUAL = [
        (3, operator.add, (1, 2,)),
    ]
    
    _ASSERT_NOT_EQUAL = [
        (3, operator.add, (1, 4,)),
    ]

    _ASSERT_RAISES = [
        (ValueError, int, ('kkkk',))
    ]

This will define 3 test cases using assertEqual, assertNotEqual and 
assertRaises.
"""

import unittest
import operator


def _make_assert_equal(expecting, func, args=None, kwargs=None):

    def inner(self):
        new_kwargs = kwargs or {}
        new_args = args or ()
        self.assertEqual(func(*new_args, **new_kwargs), expecting)
    return inner

def _make_assert_not_equal(expecting, func, args=None, kwargs=None):

    def inner(self):
        new_kwargs = kwargs or {}
        new_args = args or ()
        self.assertNotEqual(func(*new_args, **new_kwargs), expecting)
    return inner

def _make_assert_raises(exc, func, args=None, kwargs=None):

    def inner(self):
        new_kwargs = kwargs or {}
        new_args = args or ()
        self.assertRaises(exc, func, *new_args, **new_kwargs)
    return inner

_BIN_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.div,
    '%': operator.mod,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '&': operator.and_,
    '!': operator.or_,
    '^': operator.xor,
    'in': operator.contains,
    'is': operator.is_,
    'is not': operator.is_not,
}

_UNARY_OPERATORS = {
    'not': operator.not_,
    '~': operator.inv,
}

_OPERATOR_NAMES = {
    '+': 'plus',
    '-': 'minus',
    '*': 'mult',
    '/': 'div',
    '%': 'mod',
    '>': 'gt',
    '>=': 'gte',
    '<': 'lt',
    '<=': 'lte',
    '==': 'eq',
    '!=': 'ne',
    'in': 'in',
    'is': 'is',
    'is_not': 'is_not',
    'not': 'not',
    '~': 'inv',
    '^': 'xor',
    '|': 'or',
    '&': 'and',
    '>>': 'rshift',
    '<<': 'lshift',
}

def _make_bin_operator_test(operator, operand1, operand2, expecting):

    def inner(self):
       self.assertEquals(_BIN_OPERATORS[operator](operand1, operand2),
                         expecting)
    return inner


def _make_unary_operator_test(operator, operand1, expecting):

    def inner(self):
        self.assertEquals(_UNARY_OPERATORS[operator](operand1), expecting)
    return inner


class AssertingMetaClass(type):
    """Meta class which creates test methods for simple assertions.
    """

    _FACTORY_MAP = {
        '_ASSERT_EQUAL': _make_assert_equal,
        '_ASSERT_NOT_EQUAL': _make_assert_not_equal,
        '_ASSERT_RAISES': _make_assert_raises}

    _TEST_CASE = dict([(k, 0) for k in _FACTORY_MAP.keys()])

    def __new__(cls, name, bases, attrs):
        new_class = super(AssertingMetaClass, cls)\
            .__new__(cls, name, bases, attrs)

        for attr, value in attrs.iteritems():

            if attr in cls._FACTORY_MAP:
                lattr = attr.lower()
                for test in value:
                    mname = 'test_asserting_%s_%d' % (
                        lattr, cls._TEST_CASE[attr])
                    cls._TEST_CASE[attr] += 1
                    test_method = \
                        cls._FACTORY_MAP[attr](*test)
                    test_method.__name__ = mname
                    setattr(new_class, mname, test_method)
        
        return new_class


class OperatorMetaClass(type):
    """Meta class which creates methods for operators
    """
    
    _TEST_CASE = dict([(k, 0) for k in _OPERATOR_NAMES.values()])

    def __new__(cls, name, bases, attrs):
        new_class = super(OperatorMetaClass, cls)\
            .__new__(cls, name, bases, attrs)

        if '_BIN_OPERATOR_TESTS' in attrs:
            for test in attrs['_BIN_OPERATOR_TESTS']:
                n = _OPERATOR_NAMES[test[0]]
                mname = 'test_bin_operator_%s_%d' % (n,
                                                     cls._TEST_CASE[n])
                cls._TEST_CASE[n] += 1
                new_method = _make_bin_operator_test(*test)
                new_method.__name__ = mname
                setattr(new_class, mname, new_method)

        if '_UNARY_OPERATOR_TESTS' in attrs:
            for test in attrs['_UNARY_OPERATOR_TESTS']:
                n = _OPERATOR_NAMES[test[0]]
                mname = 'test_operator_%s_%d' % (n,
                                                 cls._TEST_CASE[n])
                cls._TEST_CASE[n] += 1
                new_method = _make_unary_operator_test(*test)
                new_method.__name__ = mname
                setattr(new_class, mname, new_method)

        return new_class


class AssertingTestCase(unittest.TestCase):

    __metaclass__ = AssertingMetaClass


class OperatorTestCase(unittest.TestCase):
    
    __metaclass__ = OperatorMetaClass
