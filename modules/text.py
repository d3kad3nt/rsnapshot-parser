from collections.abc import Sequence

from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import *
from utils.config import Config
from utils.utils import print_list
from . import outputModule


class TextModule(outputModule.OutputModule):

    def __init__(self):
        self._config: Config = Config(section="text")

    def output(self, parsed_output: ParsedOutput):
        output: list[str] = []
        output += self._summary(parsed_output)
        output.append("")
        output += self._errors(parsed_output)
        formatted_output: list[str] = []
        for line in output:
            formatted_output.append(line.rstrip() + "\n")
        self._to_file(formatted_output)
        self._to_stdout(formatted_output)

    def _to_file(self, output: Sequence[str]):
        filepath = self._config.get_value("filepath")
        print(filepath)
        if filepath:
            #TODO error handling with filename

            with open(filepath, "w") as output_file:
                output_file.writelines(output)

    def _to_stdout(self, output: Sequence[str]):
        if self._config.get_bool_value("stdout", default_value=False):
            print_list(output, end="")

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

