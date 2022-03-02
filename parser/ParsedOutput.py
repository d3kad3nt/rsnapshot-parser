import utils.utils
from parser.Commands import RsnapshotCommand, BackupExecCommand
from parser.ResultStates import FailedState, NotExecutedState
from parser.RsnapshotConfig import RsnapshotConfig
from utils.config import Config
from datetime import datetime
from collections.abc import Iterable, Collection


class ParsedOutput:
    def __init__(self, config: RsnapshotConfig, input):
        self.rsnapshot_config: RsnapshotConfig = config
        self.config: Config = Config(section="parser")
        self.log = self.readInput(input)
        self.backupPoints: list[RsnapshotCommand] = self.parseBackupPoints()
        self.end_time = self.backupPoints[-1].end_time

    def parseBackupPoints(self):
        backupPoints = self.rsnapshot_config.backup_points
        currentBackupPoint = -1
        currentBackupPointLog = []
        for line in self.log:
            if (currentBackupPoint + 1) < len(backupPoints) and backupPoints[currentBackupPoint + 1].backup_start_line() in line:
                if currentBackupPoint >= 0:
                    backupPoints[currentBackupPoint].log = currentBackupPointLog
                currentBackupPoint += 1
                currentBackupPointLog = []
            currentBackupPointLog.append(line)
        backupPoints[currentBackupPoint].log = currentBackupPointLog
        for i, backupPoint in enumerate(backupPoints):
            if type(backupPoint) is BackupExecCommand:
                if backupPoint.command.startswith("/bin/date"):
                    time = datetime.fromtimestamp(int(backupPoint.log[1]))
                    if i > 1:
                        backupPoints[i-1].end_time = time
                    if i < (len(backupPoints) - 1):
                        backupPoints[i+1].start_time = time
                    #Set also time for date command
                    backupPoint.start_time = time
                    backupPoint.end_time = time
        return backupPoints

    @property
    def start_time(self):
        time_format = "%H:%M"
        start_time_str = self.config.get_value(key="start_{}".format(self.retain_type))
        start_time = datetime.strptime(start_time_str, time_format)
        return datetime.combine(self.backupPoints[0].start_time.date(), start_time.time())

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def retain_type(self):
        all_types = self.rsnapshot_config.retain_types
        first_move: str = utils.utils.findLinesStartingWith(self.log, "mv")[0]
        part = first_move.split(" ")[1].split("/")[-2].split(".")[0]
        if part not in all_types:
            print("ERROR: detected retain type {}, but configured are only {}.".format(part, all_types))
        return part

    def readInput(self, filename: str):
        with open(filename, "r", encoding="utf8") as logfile:
            lines = logfile.readlines()
        linestart = ""
        reallines = []
        for line in lines:
            # Rsnapshot cuts long lines into multiple lines seperated by "\"
            if linestart:
                line = linestart + line[4:]
            if line.endswith("\\\n"):
                linestart = line.strip()[:-1]
            else:
                linestart = ""
                reallines.append(line)
        return reallines

    def commands_with_state_count(self, state):
        return len(self.commands_with_state(state))

    def commands_with_state(self, state):
        result = []
        for backupPoint in self.backupPoints:
            if isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    def commands_not_with_status_count(self, state):
        return len(self.commands_not_with_state(state))

    def commands_not_with_state(self, state):
        result = []
        for backupPoint in self.backupPoints:
            if not isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    def was_successful(self):
        return self.commands_with_state_count(FailedState) == 0 and self.commands_with_state_count(NotExecutedState) == 0
