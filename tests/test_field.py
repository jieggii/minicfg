import unittest
import unittest.mock

from minicfg.caster import AbstractCaster
from minicfg.field import NO_DEFAULT_VALUE, CastingError, Field, FieldValueNotProvidedError

from ._mock_provider import MockProvider


class TestField(unittest.TestCase):
    def test_field_initialization_with_default_values(self):
        field = Field(name="test_field")
        self.assertEqual(field.name, "test_field")
        self.assertEqual(field._default, NO_DEFAULT_VALUE)
        self.assertIsNone(field._caster)
        self.assertIsNone(field._description)
        self.assertFalse(field._file_field)
        self.assertEqual(field._value, None)

    def test_description(self):
        field = Field(name="test_field", description="description")
        self.assertEqual(field.description, "description")

    def test_default(self):
        field = Field(name="test_field", default="default value")
        self.assertEqual(field.default, "default value")

    def test_populate_using_provided_value(self):
        provider = MockProvider({"test_field": "hello world"})

        field = Field("test_field")
        field.populate(provider)

        self.assertEqual(field.value, "hello world")

    def test_populate_using_default(self):
        provider = MockProvider({})
        field = Field(name="test_field", default="hello")
        field.populate(provider)
        self.assertEqual(field.value, "hello")

    def test_populate_no_value_and_no_default(self):
        provider = MockProvider({})
        field = Field(name="test_field")
        with self.assertRaises(FieldValueNotProvidedError):
            field.populate(provider)

    def test_populate_casting_error(self):
        provider = MockProvider({"test_field": "hello"})

        class MockCaster(AbstractCaster):
            def typename(self) -> str | None:
                return None

            def cast(self, value: str) -> int:
                raise ValueError("casting error")

        field = Field(name="test_field", caster=MockCaster())
        with self.assertRaises(CastingError):
            field.populate(provider)

    def test_populate_with_file_field_only_file_field(self):
        provider = MockProvider({"test_field_FILE": "file_path"})

        field = Field(name="test_field", attach_file_field=True)
        with unittest.mock.patch("minicfg.field._read_raw_value_from_file", return_value="test value"):
            field.populate(provider)

        self.assertEqual(field.value, "test value")

    def test_populate_with_file_field_only_field(self):
        provider = MockProvider({"test_field": "value"})

        field = Field(name="test_field", attach_file_field=True)
        field.populate(provider)

        self.assertEqual(field.value, "value")

    def test_populate_with_file_field_both_provided(self):
        provider = MockProvider({"test_field": "value", "test_field_FILE": "file_path"})

        field = Field(name="test_field", attach_file_field=True)
        field.populate(provider)

        self.assertEqual(field.value, "value")

    def test_populate_with_file_field_no_value(self):
        provider = MockProvider({})

        field = Field(name="test_field", attach_file_field=True)
        with self.assertRaises(FieldValueNotProvidedError):
            field.populate(provider)

    def test_populate_with_file_field_no_value_default(self):
        provider = MockProvider({})

        field = Field(name="test_field", attach_file_field=True, default="default value")
        field.populate(provider)
        self.assertEqual(field.value, "default value")


if __name__ == "__main__":
    unittest.main()
