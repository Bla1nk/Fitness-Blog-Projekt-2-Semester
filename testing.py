import unittest


class ValueClass:
    value = None

    def __init__(self, v=1):
        self.value = v

    def set(self, v) -> None:
        self.value = v

    def get(self) -> int:
        return self.value

    def absolute_value(self) -> int:
        return abs(self.value)

    def is_zero(self) -> bool:
        return self.value == 0

    def is_positive(self) -> bool:
        return self.value >= 0

    def is_negative(self) -> bool:
        return not self.is_positive()

    def invert(self) -> None:
        self.value = self.value * -1


class TestValueClassPositiveValue(unittest.TestCase):
    my_value = None

    def setUp(self):
        self.my_value = ValueClass(42)

    def test_value_set_by_constructor(self):
        # test if the value set within the constructor is the same (check with get)
        self.assertEqual(self.my_value.get(), 42)

    def test_positive_is_zero(self):
        # test if a positive value is zero
        self.assertFalse(self.my_value.is_zero())

    def test_positive_is_positive(self):
        # test if a positive value is positive
        self.assertTrue(self.my_value.is_positive())

    def test_positive_is_negative(self):
        # test if a positive value is negative
        self.assertFalse(self.my_value.is_negative())

    def test_positive_absolute(self):
        # test the absolute value of a positive
        self.assertTrue(self.my_value.absolute_value(), 42)


class TestValueClassOthers(unittest.TestCase):

    def setUp(self):
        # DO NOT USE setUp for this test class
        pass

    def test_default_constructor(self):
        # test when class is initialized with default constructor that value is 1
        v = ValueClass()
        self.assertEqual(v.get(), 1)

    def test_set_value(self):
        v = ValueClass()
        # test if positive value is set correctly (check with get)
        v.set(12)
        self.assertEqual(v.get(), 12)
        # test if negative value is set correctly (check with get)
        v.set(-33)
        self.assertEqual(v.get(), -33)
        # test if zero is set correctly (check with get)
        v.set(0)
        self.assertEqual(v.get(), 0)
        pass

    def test_is_zero(self):
        v = ValueClass()
        # test if positive value is zero
        v.set(2)
        self.assertFalse(v.is_zero())
        # test if negative value is zero
        v.set(-2)
        self.assertFalse(v.is_zero())
        # test if zero is zero
        v.set(0)
        self.assertTrue(v.is_zero())
        pass

    def test_invert(self):
        v = ValueClass()
        # test invert positive value to negative
        v.set(23)
        v.invert()
        self.assertEqual(v.get(), -23)
        # test invert negative value to positive
        v.set(-64)
        v.invert()
        self.assertEqual(v.get(), 64)
        # test invert zero
        v.set(0)
        v.invert()
        self.assertEqual(v.get(), 0)
        pass


if __name__ == '__main__':
    unittest.main()