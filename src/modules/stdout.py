from collections.abc import Sequence

from output_parser.parsed_output import ParsedOutput
from provider.providers import get_text_from_providers
from utils.config import Config
from utils.utils import print_list
from . import output_module


class StdoutModule(output_module.OutputModule):
    @classmethod
    def name(cls) -> str:
        return "StdOut"

    def __init__(self):
        self._config: Config = Config(section=self.name().lower())

    def output(self, parsed_output: ParsedOutput):
        providers = self._config.get_str_list("providers", ["Summary"])
        output: Sequence[str] = get_text_from_providers(providers, parsed_output)
        print_list(output, end="")
