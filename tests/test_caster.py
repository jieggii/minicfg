import unittest

from minicfg.caster import AbstractCaster, BoolCaster, FloatCaster, IntCaster, JSONCaster, ListCaster


class TestIntCaster(unittest.TestCase):
    def setUp(self):
        self.caster = IntCaster()

    def test_typename(self):
        self.assertEqual("int", self.caster.typename)

    def test_positive(self):
        result = self.caster.cast("123123")
        self.assertEqual(result, 123123)

    def test_negative(self):
        result = self.caster.cast("-123123")
        self.assertEqual(result, -123123)

    def test_non_numeric(self):
        with self.assertRaises(ValueError):
            self.caster.cast("abcdef")

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.caster.cast("")


class TestFloatCaster(unittest.TestCase):
    def setUp(self):
        self.caster = FloatCaster()

    def test_type_name(self):
        self.assertEqual("float", self.caster.typename)

    def test_positive(self):
        result = self.caster.cast("123.456")
        self.assertEqual(result, 123.456)

    def test_negative(self):
        result = self.caster.cast("-123.456")
        self.assertEqual(result, -123.456)

    def test_non_numeric(self):
        with self.assertRaises(ValueError):
            self.caster.cast("abcdef")

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.caster.cast("")


class TestBoolCaster(unittest.TestCase):
    def setUp(self):
        self.caster = BoolCaster()

    def test_typename(self):
        self.assertEqual("bool", self.caster.typename)

    def test_true_values(self):
        true_values = ["true", "yes", "on", "enable", "enabled", "1"]
        for value in true_values:
            self.assertTrue(self.caster.cast(value))

    def test_false_values(self):
        false_values = ["false", "no", "off", "disable", "disabled", "0"]
        for value in false_values:
            self.assertFalse(self.caster.cast(value))

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            self.caster.cast("invalid")


class TestListCaster(unittest.TestCase):
    def setUp(self):
        self.separator = ","
        self.caster = ListCaster(sep=self.separator)

    def test_typename_str(self):
        self.assertEqual("list[str]", self.caster.typename)

    def test_typename_with_item_caster_with_typename(self):
        class MockCaster(AbstractCaster):
            @property
            def typename(self) -> str:
                return "item-caster-typename"

            def cast(self, value: str) -> str:
                raise NotImplementedError()

        list_caster = ListCaster(sep=self.separator, item_caster=MockCaster())
        self.assertEqual("list[item-caster-typename]", list_caster.typename)

    def test_typename_with_item_caster_without_typename(self):
        class MockCaster(AbstractCaster):
            @property
            def typename(self) -> str | None:
                return None

            def cast(self, value: str) -> str:
                raise NotImplementedError()

        list_caster = ListCaster(sep=self.separator, item_caster=MockCaster())
        self.assertEqual("list", list_caster.typename)

    def test_list_of_strings(self):
        result = self.caster.cast("a,b,c")
        self.assertEqual(result, ["a", "b", "c"])

    def test_list_with_int_caster(self):
        int_caster = IntCaster()
        list_caster = ListCaster(sep=self.separator, item_caster=int_caster)
        result = list_caster.cast("1,2,3")
        self.assertEqual(result, [1, 2, 3])

    def test_list_with_json_caster(self):
        json_caster = JSONCaster()
        list_caster = ListCaster(sep=";", item_caster=json_caster)
        result = list_caster.cast('{"hello": "world", "foo": "bar"};{"hi": "friend"}')
        self.assertEqual(result, [{"hello": "world", "foo": "bar"}, {"hi": "friend"}])

    def test_list_with_invalid_item(self):
        int_caster = IntCaster()
        list_caster = ListCaster(sep=self.separator, item_caster=int_caster)
        with self.assertRaises(ValueError):
            list_caster.cast("1,invalid,3")


class TestJSONCaster(unittest.TestCase):
    def setUp(self):
        self.caster = JSONCaster()

    def test_typename(self):
        self.assertEqual("json", self.caster.typename)

    def test_json_object(self):
        py_dict = {"str": "hello!", "int": 1, "flag": True, "float": 1.1}
        json = '{"str": "hello!", "int": 1, "flag": true, "float": 1.1}'

        self.assertEqual(py_dict, self.caster.cast(json))

    def test_json_array(self):
        py_list = ["hello!", 1, True, 1.1]
        json = '["hello!", 1, true, 1.1]'

        self.assertEqual(py_list, self.caster.cast(json))

    def test_custom_load(self):
        def custom_load(value: str) -> dict:
            return {"custom": value}

        caster = JSONCaster(load=custom_load)
        self.assertEqual({"custom": "test"}, caster.cast("test"))

    def test_invalid_json(self):
        json = "bla bla bla"

        with self.assertRaises(ValueError):
            self.caster.cast(json)


if __name__ == "__main__":
    unittest.main()
