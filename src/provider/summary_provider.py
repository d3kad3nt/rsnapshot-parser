from typing import Sequence

from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import NotExecutedState, SuccessState, FailedState
from provider.text_provider import TextProvider
from utils.utils import format_bytes


class SummaryProvider(TextProvider):
    @classmethod
    def name(cls) -> str:
        return "Summary"

    def text(self, parsed_output: ParsedOutput) -> Sequence[str]:
        output = [
            "Backup at {} for {}".format(parsed_output.start_time, parsed_output.duration),
            "{} Backup Commands executed".format(
                parsed_output.commands_not_with_state_count(NotExecutedState)),
            "{} Backup Commands succeeded".format(
                parsed_output.commands_with_state_count(SuccessState)),
            "{} Backup Commands failed".format(parsed_output.commands_with_state_count(FailedState)),
            "{} Backup Commands not executed".format(parsed_output.commands_with_state_count(NotExecutedState)),
            "Copied {} files with {}".format(parsed_output.changed_files, format_bytes(parsed_output.changed_size)),
            ""]
        return output
