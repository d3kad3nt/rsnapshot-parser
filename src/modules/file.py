from collections.abc import Sequence

from parser.ParsedOutput import ParsedOutput
from provider.providers import get_provider, get_text_from_providers
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
        providers = self._config.get_str_list("providers", ["Summary, Statistics"])
        output: Sequence[str] = get_text_from_providers(providers, parsed_output)
        filepath = self._config.get_str("filepath")
        if filepath:
            #TODO error handling with filename
            with open(filepath, "w") as output_file:
                output_file.writelines(output)





