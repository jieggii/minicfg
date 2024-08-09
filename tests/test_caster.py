import unittest
from minicfg.caster import IntCaster, FloatCaster, BoolCaster, ListCaster

class TestIntCaster(unittest.TestCase):
    def setUp(self):
        self.caster = IntCaster()

    def test_positive(self):
        result = self.caster.cast("123123")
        self.assertEqual(result, 123123)

    def test_negative(self):
        result = self.caster.cast("-123123")
        self.assertEqual(result, -123123)

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.caster.cast("")

class TestFloatCaster(unittest.TestCase):
    def setUp(self):
        self.caster = FloatCaster()

    def test_positive(self):
        result = self.caster.cast("123.456")
        self.assertEqual(result, 123.456)

    def test_negative(self):
        result = self.caster.cast("-123.456")
        self.assertEqual(result, -123.456)

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.caster.cast("")

class TestBoolCaster(unittest.TestCase):
    def setUp(self):
        self.caster = BoolCaster()

    def test_true_values(self):
        true_values = ["true", "yes", "on", "enable", "1"]
        for value in true_values:
            self.assertTrue(self.caster.cast(value))

    def test_false_values(self):
        false_values = ["false", "no", "off", "disable", "0"]
        for value in false_values:
            self.assertFalse(self.caster.cast(value))

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            self.caster.cast("invalid")

class TestListCaster(unittest.TestCase):
    def setUp(self):
        self.separator = ","
        self.caster = ListCaster(sep=self.separator)

    def test_list_of_strings(self):
        result = self.caster.cast("a,b,c")
        self.assertEqual(result, ["a", "b", "c"])

    def test_list_with_int_caster(self):
        int_caster = IntCaster()
        list_caster = ListCaster(sep=self.separator, item_caster=int_caster)
        result = list_caster.cast("1,2,3")
        self.assertEqual(result, [1, 2, 3])

    def test_list_with_invalid_item(self):
        int_caster = IntCaster()
        list_caster = ListCaster(sep=self.separator, item_caster=int_caster)
        with self.assertRaises(ValueError):
            list_caster.cast("1,invalid,3")


if __name__ == "__main__":
    unittest.main()
