import abc
from collections.abc import Sequence

from output_parser.parsed_output import ParsedOutput


class TextProvider(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        pass

    @abc.abstractmethod
    def text(self, parsed_output: ParsedOutput) -> Sequence[str]:
        pass


class EmptyTextProvider(TextProvider):
    @classmethod
    def name(cls) -> str:
        return "EmptyText"

    def text(self, parsed_output: ParsedOutput) -> Sequence[str]:
        return []
