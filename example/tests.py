from casemaker import AssertingTestCase, OperatorTestCase
import operator

class TestSomething(AssertingTestCase):

    _ASSERT_EQUAL = [
        (3, operator.add, (1, 2,)),
    ]
    
    _ASSERT_NOT_EQUAL = [
        (3, operator.add, (1, 4,)),
    ]

    _ASSERT_RAISES = [
        (ValueError, int, ('kkkk',))
    ]


class TestSomethingElse(OperatorTestCase):

    _BIN_OPERATOR_TESTS = [
        ('+', 1, 2, 3),
        ('-', 4, 3, 1),
        ]

    _UNARY_OPERATOR_TESTS = [
        ('not', 1, False),
        ('~', 1, -2),
        ]


if __name__ == '__main__':
    import unittest
    unittest.main()
