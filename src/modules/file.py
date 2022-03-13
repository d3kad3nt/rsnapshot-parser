from collections.abc import Sequence

from parser.ParsedOutput import ParsedOutput
from provider.providers import get_provider
from utils.config import Config
from utils.utils import print_list
from . import outputModule


class FileModule(outputModule.OutputModule):

    @classmethod
    def name(cls) -> str:
        return "File"

    def __init__(self):
        self._config: Config = Config(section=self.name().lower())

    def output(self, parsed_output: ParsedOutput):
        output: list[str] = []
        providers = self._config.get_str_list("providers", ["Summary, Statistics"])
        for provider in providers:
            lines = get_provider(provider).text(parsed_output)
            for line in lines:
                output.append(line.rstrip() + "\n")
            output.append("\n")

        self._to_file(output)

    def _to_file(self, output: Sequence[str]):
        filepath = self._config.get_str("filepath")
        if filepath:
            #TODO error handling with filename
            with open(filepath, "w") as output_file:
                output_file.writelines(output)





