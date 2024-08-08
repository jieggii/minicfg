import unittest

from minicfg.caster import IntCaster


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


if __name__ == '__main__':
    unittest.main()
