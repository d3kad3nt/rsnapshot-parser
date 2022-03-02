from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import *
from utils.utils import print_list
from . import outputModule


class TextModule(outputModule.OutputModule):
    def output(self, parsed_output: ParsedOutput):
        summary = self._summary(parsed_output)
        print_list(summary)

    @staticmethod
    def _summary(parsed_output: ParsedOutput):
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
    def _errors(parsed_output: ParsedOutput):
        failed = parsed_output.commands_not_with_state(FailedState)
