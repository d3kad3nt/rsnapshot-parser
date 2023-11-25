from collections.abc import Sequence

from output_parser.parsed_output import ParsedOutput
from provider.providers import get_text_from_providers
from utils.config import Config
from . import output_module


class FileModule(output_module.OutputModule):
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
            # TODO error handling with filename
            with open(filepath, "w", encoding="UTF-8") as output_file:
                output_file.writelines(output)
