"""
This simple tool will help you generating documentation for your minicfg classes.

Usage: minicfg [--format <format>] <path>
Example: minicfg --format plaintext my_package.my_module.MyConfig
"""

import argparse
import importlib
from enum import Enum

from minicfg.docs_generator import DocsGenerator


class _Format(Enum):
    """
    Output format enum.
    """

    PLAINTEXT = "plaintext"
    MARKDOWN = "markdown"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "minicfg", description="This simple tool will help you generating documentation for your minicfg classes."
    )
    parser.add_argument("path", type=str, help="Path to the minicfg class (e.g. my_package.my_module.MyConfig)")
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        choices=[f.value for f in _Format],
        default=_Format.MARKDOWN.value,
        help="Output format (plaintext or markdown)",
    )

    return parser.parse_args()


def main():
    args = _parse_args()

    module_name, class_name = args.path.rsplit(".", 1)
    module = importlib.import_module(module_name)

    minicfg_class = getattr(module, class_name)
    minicfg_instance = minicfg_class()

    docs_generator = DocsGenerator(minicfg_instance)
    docs: str
    match args.format:
        case _Format.PLAINTEXT.value:
            docs = docs_generator.as_plaintext()
        case _Format.MARKDOWN.value:
            docs = docs_generator.as_markdown()
        case _:
            raise ValueError(f"unexpected format {args.format}")

    print(docs)


if __name__ == "__main__":
    main()
