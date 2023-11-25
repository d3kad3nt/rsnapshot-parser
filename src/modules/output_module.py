import abc

from output_parser.parsed_output import ParsedOutput


class OutputModule(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        pass

    @abc.abstractmethod
    def output(self, parsed_output: ParsedOutput) -> None:
        pass


class EmptyModule(OutputModule):
    @classmethod
    def name(cls) -> str:
        return "Empty Module"

    def output(self, parsed_output: ParsedOutput):
        pass
