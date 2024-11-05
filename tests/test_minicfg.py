import unittest
from unittest.mock import Mock, patch

from minicfg.field import Field, FieldConflictError, CastingError, FieldValueNotProvidedError, _NOT_SET
from minicfg.provider import AbstractProvider
from minicfg.caster import AbstractCaster


class TestField(unittest.TestCase):

    def test_field_initialization(self):
        field = Field(name="test_field", default="default_value", attach_file_field=True)
        self.assertEqual(field.name, "test_field")
        self.assertEqual(field._default, "default_value")
        self.assertTrue(field._attach_file_field)
        self.assertEqual(field._populated_value, _NOT_SET)

    def test_field_name_property(self):
        field = Field(name="test_field")
        self.assertEqual(field.name, "test_field")
        field.name = "new_name"
        self.assertEqual(field.name, "new_name")

    def test_field_populated_value_property(self):
        field = Field()
        self.assertEqual(field.populated_value, _NOT_SET)
        field._populated_value = "populated_value"
        self.assertEqual(field.populated_value, "populated_value")

    def test_populate_with_raw_value(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = "raw_value"
        field = Field(name="test_field")
        field.populate(provider)
        self.assertEqual(field.populated_value, "raw_value")

    def test_populate_with_file_field(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.side_effect = lambda key: "file_path" if key == "test_field_FILE" else None
        field = Field(name="test_field", attach_file_field=True)
        with patch("minicfg.field._read_raw_value_from_file", return_value="file_value"):
            field.populate(provider)
        self.assertEqual(field.populated_value, "file_value")

    def test_populate_with_default_value(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = None
        field = Field(name="test_field", default="default_value")
        field.populate(provider)
        self.assertEqual(field.populated_value, "default_value")

    def test_populate_raises_field_conflict_error(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.side_effect = lambda key: "raw_value" if key == "test_field" else "file_value"
        field = Field(name="test_field", attach_file_field=True)
        with self.assertRaises(FieldConflictError):
            field.populate(provider)

    def test_populate_raises_casting_error(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = "raw_value"
        caster = Mock(spec=AbstractCaster)
        caster.cast.side_effect = Exception("casting error")
        field = Field(name="test_field", caster=caster)
        with self.assertRaises(CastingError):
            field.populate(provider)

    def test_populate_raises_field_value_not_provided_error(self):
        provider = Mock(spec=AbstractProvider)
        provider.get.return_value = None
        field = Field(name="test_field")
        with self.assertRaises(FieldValueNotProvidedError):
            field.populate(provider)


if __name__ == "__main__":
    unittest.main()