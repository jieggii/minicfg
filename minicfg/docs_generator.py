import dataclasses

from minicfg import Field, Minicfg
from minicfg.field import NO_DEFAULT_VALUE


def _generate_markdown_table(headers: list[str], data: list[list[str]]) -> str:
    """
    Generate a Markdown table from the given headers and data.
    :param headers: list of header strings.
    :param data: table data.
    :return: Markdown table string.
    """

    # Determine the maximum width for each column
    column_widths = [max(len(str(item)) for item in column) for column in zip(*([headers] + data))]

    # Create the header row with padding
    header_row = "| " + " | ".join(f"{header:<{column_widths[i]}}" for i, header in enumerate(headers)) + " |"
    separator_row = "| " + " | ".join("-" * width for width in column_widths) + " |"

    # Add data rows with padding
    data_rows = ""
    for row in data:
        data_rows += "\n| " + " | ".join(f"{str(item):<{column_widths[i]}}" for i, item in enumerate(row)) + " |"

    # Combine header, separator, and data rows
    return header_row + "\n" + separator_row + data_rows


@dataclasses.dataclass
class FieldMeta:
    """
    FieldMeta class represents metadata about a field.
    """

    name: str
    type: str | None  # None means that the type is not specified
    default: str | None  # None means that the default value is not specified
    description: str | None

    @classmethod
    def from_field(cls, field: Field) -> "FieldMeta":
        return cls(
            name=field.name,
            type=field.caster.typename if field.caster else "str",
            default=str(field.default) if field.default is not NO_DEFAULT_VALUE else None,
            description=field.description,
        )


class DocsGenerator:
    """
    DocsGenerator class generates documentation for the Minicfg instance
    """

    _config_name: str
    _fields: list[FieldMeta]
    _child_generators: list["DocsGenerator"]

    def __init__(self, config: Minicfg):
        self._config_name = config.name or config.__class__.__name__
        self._fields = []
        self._child_generators = []

        for child in config:
            if isinstance(child, Field):
                self._fields.append(FieldMeta.from_field(child))
                if child.file_field:
                    self._fields.append(FieldMeta.from_field(child.file_field))
            elif isinstance(child, Minicfg):
                self._child_generators.append(DocsGenerator(child))
            else:
                raise ValueError(f"unexpected child type: {type(child)}")

    def as_plaintext(self) -> str:
        """
        Generate a plaintext documentation for the Minicfg instance.
        :return: plaintext documentation string.
        """

        result = f"{self._config_name}\n"
        for field in self._fields:
            result += f" - {field.name}"
            if field.type:
                result += f": {field.type}"
            if field.default:
                result += f" = {field.default}"
            if field.description:
                result += f"  # {field.description}"

            result += "\n"

        child_plaintexts = "\n".join(child.as_plaintext() for child in self._child_generators)
        return f"{result}\n{child_plaintexts}"

    def as_markdown(self) -> str:
        """
        Generate a Markdown documentation for the Minicfg instance.
        :return: Markdown documentation string.
        """

        table_data: list[list[str]] = []
        for field in self._fields:
            table_data.append(
                [
                    f"`{field.name}`",
                    f"`{field.type}`" if field.type else "N/A",
                    f"`{field.default}`" if field.default else "N/A",
                    field.description or "",
                ]
            )

        table = _generate_markdown_table(["Name", "Type", "Default", "Description"], table_data)
        child_markdowns = "\n".join(child.as_markdown() for child in self._child_generators)

        return f"**{self._config_name}**\n{table}\n\n{child_markdowns}"
