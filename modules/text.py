from parser.ResultStates import *
from utils.utils import printList
from . import outputModule
from datetime import datetime


class TextModule(outputModule.OutputModule):
    def output(self, logOutput):
        print("Backup at {}".format(datetime.now()))
        print(
            "{} Backup Commands executed".format(
                logOutput.commandsNotWithStatusCount(NotExecutedState)
            )
        )
        print(
            "{} Backup Commands succeeded".format(
                logOutput.commandsWithStatusCount(SuccessState)
            )
        )
        print(
            "{} Backup Commands failed".format(
                logOutput.commandsWithStatusCount(FailedState)
            )
        )
        notExecuted = logOutput.commandsWithStatusCount(NotExecutedState)
        print("{} Backup Commands not executed".format(notExecuted))
        # if notExecuted > 0:
        #     i = 52
        #     print(logOutput.commandsNotWithStatus(NotExecutedState)[i])
        #     print(logOutput.commandsNotWithStatus(NotExecutedState)[i + 1])
        #     print()
        #     printList(logOutput.commandsNotWithStatus(NotExecutedState)[i].log, end="")
            # printList(logOutput.commandsWithStatus(NotExecutedState))
