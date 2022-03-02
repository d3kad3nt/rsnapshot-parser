from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import *
from . import outputModule


class TextModule(outputModule.OutputModule):
    def output(self, parsed_output: ParsedOutput):
        print("Backup at {}".format(parsed_output.start_time))
        print(
            "{} Backup Commands executed".format(
                parsed_output.commands_not_with_status_count(NotExecutedState)
            )
        )
        print(
            "{} Backup Commands succeeded".format(
                parsed_output.commands_with_state_count(SuccessState)
            )
        )
        print(
            "{} Backup Commands failed".format(
                parsed_output.commands_with_state_count(FailedState)
            )
        )
        not_executed = parsed_output.commands_with_state_count(NotExecutedState)
        print("{} Backup Commands not executed".format(not_executed))
