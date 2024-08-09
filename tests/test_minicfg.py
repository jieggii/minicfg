import unittest
from unittest.mock import MagicMock, patch, mock_open
from minicfg import Minicfg, minicfg_prefix, minicfg_provider
from minicfg.field import Field, AbstractField, _NOT_SET
from minicfg.provider import AbstractProvider, EnvProvider
from minicfg.exceptions import FieldConflictError, FieldValueNotProvidedError


# Mock Field and AbstractProvider for testing purposes
class MockField(Field):
    def __init__(self, name=None, default=_NOT_SET, caster=None, attach_file_field=False):
        super().__init__(name, default, caster, attach_file_field)

    def name_with_prefix(self, prefix):
        return f"{prefix}{self.name}" if prefix else self.name


class MockProvider(AbstractProvider):
    def __init__(self, values):
        self.values = values

    def get(self, key: str) -> str | None:
        return self.values.get(key)


class TestMinicfg(unittest.TestCase):

    def setUp(self):
        self.provider = MockProvider({
            "testfield1": "value1",
            "testfield2": "value2",
            "testfield1_FILE": "file_content"
        })
        self.minicfg = Minicfg(prefix="test", provider=self.provider)

    @patch('minicfg.minicfg._read_raw_value_from_file', return_value="file_content")
    def test_populate(self, mock_read):
        field = MockField(name="field1")
        self.minicfg.field1 = field

        self.minicfg.populate()

        self.assertTrue(self.minicfg.is_populated)
        self.assertEqual("value1", self.minicfg.field1.value)

    def test_field_conflict_error(self):
        field = MockField(name="field1", attach_file_field=True)
        self.minicfg.field1 = field
        file_field = MockField(name="field1_FILE")
        self.minicfg.field1_FILE = file_field

        with self.assertRaises(FieldConflictError):
            self.minicfg.populate()

    def test_field_value_not_provided_error(self):
        field = MockField(name="field3")
        self.minicfg.field3 = field

        with self.assertRaises(FieldValueNotProvidedError):
            self.minicfg.populate()

    def test_dict_method(self):
        field = MockField(name="field1")
        self.minicfg.field1 = field
        self.minicfg.populate()

        result = self.minicfg.dict()
        self.assertIn("field1", result)
        self.assertEqual(result["field1"], "value1")

    def test_dict_not_populated(self):
        with self.assertRaises(RuntimeError):
            self.minicfg.dict()

    def test_minicfg_prefix_decorator(self):
        @minicfg_prefix("prefix")
        class PrefixedMinicfg(Minicfg):
            pass

        obj = PrefixedMinicfg()
        self.assertEqual(obj._prefix, "prefix_")

    def test_minicfg_provider_decorator(self):
        mock_provider = MagicMock()

        @minicfg_provider(mock_provider)
        class ProviderMinicfg(Minicfg):
            pass

        obj = ProviderMinicfg()
        self.assertEqual(obj._default_provider, mock_provider)


if __name__ == "__main__":
    unittest.main()
