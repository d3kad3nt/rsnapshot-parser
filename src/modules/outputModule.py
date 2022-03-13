import abc

from parser.ParsedOutput import ParsedOutput


class OutputModule(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        pass

    @abc.abstractmethod
    def output(self, parsed_output: ParsedOutput) -> None:
        pass


class EmptyModule(OutputModule):
    @property
    def name(self) -> str:
        return "Empty Module"

    def output(self, parsed_output: ParsedOutput):
        pass
