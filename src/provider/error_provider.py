from typing import Sequence

from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import FailedState, NotExecutedState
from provider.text_provider import TextProvider


class ErrorProvider(TextProvider):
    @classmethod
    def name(cls) -> str:
        return "Error"

    def text(self, parsed_output: ParsedOutput) -> Sequence[str]:
        failed = parsed_output.commands_with_state(FailedState)
        not_executed = parsed_output.commands_with_state(NotExecutedState)
        if len(failed) == 0 and len(not_executed) == 0:
            return ["No Errors", ""]
        output = []
        if failed:
            output.append("{} Commands failed:")
            for failed_command in failed:
                output.append(str(failed_command))
                if failed_command.errormessage:
                    output.append("\t{}".format(failed_command.errormessage))
            output.append("")
        if not_executed:
            output.append("{} Commands not executed:")
            for failed_command in failed:
                output.append(str(failed_command))
            output.append("")
        return output
