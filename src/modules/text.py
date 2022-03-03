from collections.abc import Sequence

from parser.Commands import BackupCommand, BackupExecCommand
from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import *
from utils.config import Config
from utils.utils import print_list, format_bytes
from . import outputModule


class TextModule(outputModule.OutputModule):

    def __init__(self):
        self._config: Config = Config(section="text")

    def output(self, parsed_output: ParsedOutput):
        output: list[str] = []
        output += self._summary(parsed_output)
        output += self._errors(parsed_output)
        output += self._list_backup_points(parsed_output)
        formatted_output: list[str] = []
        for line in output:
            formatted_output.append(line.rstrip() + "\n")
        self._to_file(formatted_output)
        self._to_stdout(formatted_output)

    def _to_file(self, output: Sequence[str]):
        filepath = self._config.get_value("filepath")
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
            "Backup at {} for {}".format(parsed_output.start_time, parsed_output.duration),
            "{} Backup Commands executed".format(
                parsed_output.commands_not_with_state_count(NotExecutedState)),
            "{} Backup Commands succeeded".format(
                parsed_output.commands_with_state_count(SuccessState)),
            "{} Backup Commands failed".format(parsed_output.commands_with_state_count(FailedState)),
            "{} Backup Commands not executed".format(parsed_output.commands_with_state_count(NotExecutedState)),
            ""]
        return output

    @staticmethod
    def _errors(parsed_output: ParsedOutput) -> Sequence[str]:
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

    @staticmethod
    def _list_backup_points(parsed_output: ParsedOutput) -> Sequence[str]:
        output: list[str] = ["Backup Actions:"]
        for backup_point in parsed_output.backupPoints:
            if isinstance(backup_point, BackupExecCommand) and backup_point.command.startswith("/bin/date"):
                continue
            output.append(str(backup_point))
            output.append("\tTime:\t\t\t{}".format(backup_point.duration))
            if isinstance(backup_point, BackupCommand):
                output.append("\tTotal size:\t\t{}".format(format_bytes(backup_point.total_size)))
                output.append("\tChanged size:\t{}".format(format_bytes(backup_point.changed_size)))
                output.append("\tTotal files:\t{}".format(backup_point.total_files))
                output.append("\tChanged files:\t{}".format(backup_point.changed_files))
        return output