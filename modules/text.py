from collections.abc import Sequence

from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import *
from utils.utils import print_list
from . import outputModule


class TextModule(outputModule.OutputModule):
    def output(self, parsed_output: ParsedOutput):
        summary = self._summary(parsed_output)
        errors = self._errors(parsed_output)
        print_list(summary)
        print()
        print_list(errors)

    @staticmethod
    def _summary(parsed_output: ParsedOutput) -> Sequence[str]:
        output = [
            "Backup at {}".format(parsed_output.start_time),
            "{} Backup Commands executed".format(
                parsed_output.commands_not_with_state_count(NotExecutedState)),
            "{} Backup Commands succeeded".format(
                parsed_output.commands_with_state_count(SuccessState)),
            "{} Backup Commands failed".format(parsed_output.commands_with_state_count(FailedState)),
            "{} Backup Commands not executed".format(parsed_output.commands_with_state_count(NotExecutedState))]
        return output

    @staticmethod
    def _errors(parsed_output: ParsedOutput) -> Sequence[str]:
        failed = parsed_output.commands_with_state(FailedState)
        not_executed = parsed_output.commands_with_state(NotExecutedState)
        if len(failed) == 0 and len(not_executed) == 0:
            return ["No Errors"]
        output = []
        if failed:
            output.append("{} Commands failed:")
            for failed_command in failed:
                output.append(str(failed_command))
                if failed_command.errormessage:
                    output.append("\t{}".format(failed_command.errormessage))
        return output

