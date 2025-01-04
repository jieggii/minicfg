import unittest
import unittest.mock

from minicfg import Field, Minicfg, minicfg_name
from minicfg.minicfg import _DEFAULT_NAME_SEP, minicfg_name_sep
from minicfg.provider import AbstractProvider

from ._mock_provider import MockProvider


class TestMinicfg(unittest.TestCase):
    def test_init_defaults(self):
        class Config(Minicfg):
            pass

        config = Config()
        self.assertEqual(config._name, None)
        self.assertEqual(config._name_sep, _DEFAULT_NAME_SEP)

    def test_init(self):
        class Config(Minicfg):
            field_name = Field()

        config = Config()
        self.assertEqual(config.field_name.name, "field_name")

    def test_init_nested(self):
        @minicfg_name("config")
        class Config(Minicfg):
            @minicfg_name("nested")
            class Nested(Minicfg):
                field_name = Field()

        config = Config()
        self.assertEqual(config.Nested.field_name.name, "config_nested_field_name")

    def test_init_nested_inherit_name(self):
        @minicfg_name("config")
        class Config(Minicfg):
            class Nested(Minicfg):
                field_name = Field()

        config = Config()
        self.assertEqual("config_field_name", config.Nested.field_name.name)

    def test_init_update_file_field_name(self):
        @minicfg_name("config")
        class Config(Minicfg):
            field_name = Field(attach_file_field=True)

        config = Config()
        self.assertEqual(f"config_field_name_FILE", config.field_name.file_field.name)

    def test_init_nested_sep(self):
        sep1 = "-"
        sep2 = "_"

        @minicfg_name("config")
        @minicfg_name_sep(sep1)
        class Config(Minicfg):
            @minicfg_name("nested")
            @minicfg_name_sep(sep2)
            class Nested(Minicfg):
                field_name = Field()

        config = Config()
        self.assertEqual(f"config{sep1}nested{sep2}field_name", config.Nested.field_name.name)

    def test_new_populated(self):
        class Config(Minicfg):
            field_name = Field()

        provider = MockProvider({"field_name": "hello"})
        config = Config.new_populated(provider)
        self.assertEqual("hello", config.field_name)

    def test_populate(self):
        class Config(Minicfg):
            field_name = Field()

        provider = MockProvider({"field_name": "hello"})
        config = Config()
        config.populate(provider)
        self.assertEqual("hello", config.field_name)

    def test_populate_nested(self):
        @minicfg_name("config")
        class Config(Minicfg):
            field_name = Field()

            @minicfg_name("nested1")
            class Nested1(Minicfg):
                field_name = Field()

                @minicfg_name("nested2")
                class Nested2(Minicfg):
                    field_name = Field()

        provider = MockProvider(
            {
                "config_field_name": "1",
                "config_nested1_field_name": "2",
                "config_nested1_nested2_field_name": "3",
            }
        )

        config = Config()
        config.populate(provider)

        self.assertEqual("1", config.field_name)
        self.assertEqual("2", config.Nested1.field_name)
        self.assertEqual("3", config.Nested1.Nested2.field_name)

    def test_iter(self):
        class Config(Minicfg):
            field_name = Field()

            class Child(Minicfg):
                field_name = Field()

        config = Config()

        for child in config:
            self.assertTrue(isinstance(child, Field) or isinstance(child, Minicfg))


class TestDecorators(unittest.TestCase):
    def test_minicfg_name(self):
        name = "TEST_NAME"

        @minicfg_name(name)
        class Config(Minicfg):
            pass

        config = Config()
        self.assertEqual(config._name, name)

    def test_minicfg_name_sep(self):
        sep = "test_sep"

        @minicfg_name_sep(sep)
        class Config(Minicfg):
            pass

        config = Config()
        self.assertEqual(config._name_sep, sep)


if __name__ == "__main__":
    unittest.main()
