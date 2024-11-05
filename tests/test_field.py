import unittest
from unittest.mock import Mock
from minicfg.field import Field, _NOT_SET
from minicfg.exceptions import CastingError, FieldConflictError, FieldValueNotProvidedError
from minicfg.provider import AbstractProvider
from minicfg.caster import AbstractCaster


class TestField(unittest.TestCase):
    def test_field_initialization_with_default_values(self):
        field = Field(name="test_field")
        self.assertEqual(field.name, "test_field")
        self.assertEqual(field._default, _NOT_SET)
        self.assertIsNone(field._caster)
        self.assertFalse(field._attach_file_field)
        self.assertEqual(field._populated_value, _NOT_SET)

    def test_field_populate_with_provider_value(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = "123"
        caster = Mock(spec=AbstractCaster)
        caster.cast.return_value = 123

        field = Field(name="test_field", caster=caster)
        field.populate(provider)

        self.assertEqual(field.populated_value, 123)
        provider.get.assert_called_with("test_field")
        caster.cast.assert_called_with("123")

    def test_field_populate_with_default_value(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = None

        field = Field(name="test_field", default=456)
        field.populate(provider)

        self.assertEqual(field.populated_value, 456)

    def test_field_populate_with_file_value(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.side_effect = lambda x: "file_path" if x == "test_field_FILE" else None

        field = Field(name="test_field", attach_file_field=True)
        with unittest.mock.patch("minicfg.field._read_raw_value_from_file", return_value="789"):
            field.populate(provider)

        self.assertEqual(field.populated_value, "789")

    def test_field_populate_with_file_value_raises_casting_error(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.side_effect = lambda x: "file_path" if x == "test_field_FILE" else None
        caster = Mock(spec=AbstractCaster)
        caster.cast.side_effect = ValueError("Invalid cast")

        field = Field(name="test_field", attach_file_field=True, caster=caster)
        with unittest.mock.patch("minicfg.field._read_raw_value_from_file", return_value="invalid_value"):
            with self.assertRaises(CastingError):
                field.populate(provider)

    def test_field_populate_raises_field_conflict_error(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.side_effect = lambda x: "value" if x == "test_field" else "file_path"

        field = Field(name="test_field", attach_file_field=True)
        with self.assertRaises(FieldConflictError):
            field.populate(provider)

    def test_field_populate_raises_casting_error(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = "invalid_value"
        caster = Mock(spec=AbstractCaster)
        caster.cast.side_effect = ValueError("Invalid cast")

        field = Field(name="test_field", caster=caster)
        with self.assertRaises(CastingError):
            field.populate(provider)

    def test_field_populate_raises_field_value_not_provided_error(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = None

        field = Field(name="test_field")
        with self.assertRaises(FieldValueNotProvidedError):
            field.populate(provider)


if __name__ == "__main__":
    unittest.main()