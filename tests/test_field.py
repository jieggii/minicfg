import unittest
from typing import Any

from minicfg.field import _NOT_SET, AbstractCaster, AbstractProvider, CastingError, Field, FieldPopulationResult


class MockCaster(AbstractCaster):
    def cast(self, value: str) -> Any:
        if value == "invalid":
            raise ValueError("Invalid value")
        return value.upper()


class MockProvider(AbstractProvider):
    def __init__(self, values):
        self._values = values

    def get(self, key: str) -> str | None:
        return self._values.get(key)


class TestField(unittest.TestCase):
    def test_initialization_and_properties(self):
        field = Field(name="test_field", default="default_value", caster=MockCaster(), attach_file_field=True)

        self.assertEqual(field.name, "test_field")
        self.assertEqual(field._default, "default_value")
        self.assertIsInstance(field._caster, MockCaster)
        self.assertTrue(field.attach_file_field)
        self.assertIs(field.value, _NOT_SET)

    def test_name_with_prefix(self):
        field = Field(name="field_name")
        self.assertEqual(field.name_with_prefix("prefix_"), "prefix_field_name")
        self.assertEqual(field.name_with_prefix(None), "field_name")

    def test_populate_using_raw_value(self):
        field = Field(caster=MockCaster())

        result = field.populate_using_raw_value("raw_value")
        self.assertEqual(field.value, "RAW_VALUE")
        self.assertTrue(result.populated)

        field = Field(caster=MockCaster())
        with self.assertRaises(CastingError):
            field.populate_using_raw_value("invalid")

    def test_populate_using_provider(self):
        provider = MockProvider(values={"field_name": "provider_value"})
        field = Field(name="field_name", default="default_value", caster=MockCaster())

        result = field.populate_using_provider(provider, "field_name")
        self.assertEqual(field.value, "PROVIDER_VALUE")
        self.assertTrue(result.populated)

        provider = MockProvider(values={})
        field = Field(name="field_name", default="default_value", caster=MockCaster())

        result = field.populate_using_provider(provider, "field_name")
        self.assertEqual(field.value, "default_value")
        self.assertTrue(result.populated)
        self.assertTrue(result.default_value_used)

        result = field.populate_using_provider(provider, "non_existent_field")
        self.assertTrue(result.populated)
        self.assertTrue(result.default_value_used)


if __name__ == "__main__":
    unittest.main()
