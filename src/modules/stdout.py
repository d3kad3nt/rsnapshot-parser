from collections.abc import Sequence

from parser.ParsedOutput import ParsedOutput
from provider.providers import get_provider
from utils.config import Config
from utils.utils import print_list
from . import outputModule


class StdoutModule(outputModule.OutputModule):

    @classmethod
    def name(cls) -> str:
        return "StdOut"

    def __init__(self):
        self._config: Config = Config(section=self.name().lower())

    def output(self, parsed_output: ParsedOutput):
        output: list[str] = []
        providers = self._config.get_str_list("providers", ["Summary"])
        for provider in providers:
            lines = get_provider(provider).text(parsed_output)
            for line in lines:
                output.append(line.rstrip() + "\n")
            output.append("\n")
        print_list(output, end="")
