import utils.utils
from parser.Commands import RsnapshotCommand, BackupExecCommand
from parser.ResultStates import FailedState, NotExecutedState
from parser.RsnapshotConfig import RsnapshotConfig
from utils.config import Config
from datetime import datetime


class ParsedOutput:
    def __init__(self, config: RsnapshotConfig, rsnapshot_output_file: str):
        self.rsnapshot_config: RsnapshotConfig = config
        self.config: Config = Config(section="parser")
        self.log = self._read_input(rsnapshot_output_file)
        self.backupPoints: list[RsnapshotCommand] = self._parse_backup_points()
        self.end_time = self.backupPoints[-1].end_time

    def _parse_backup_points(self):
        backup_points = self.rsnapshot_config.backup_points
        current_backup_point = -1
        current_backup_point_log = []
        for line in self.log:
            if (current_backup_point + 1) < len(backup_points) \
                    and backup_points[current_backup_point + 1].backup_start_line() in line:
                if current_backup_point >= 0:
                    backup_points[current_backup_point].log = current_backup_point_log
                current_backup_point += 1
                current_backup_point_log = []
            current_backup_point_log.append(line)
        backup_points[current_backup_point].log = current_backup_point_log
        for i, backupPoint in enumerate(backup_points):
            if type(backupPoint) is BackupExecCommand:
                backupPoint: BackupExecCommand
                if backupPoint.command.startswith("/bin/date"):
                    time = datetime.fromtimestamp(int(backupPoint.log[1]))
                    if i > 1:
                        backup_points[i-1].end_time = time
                    if i < (len(backup_points) - 1):
                        backup_points[i+1].start_time = time
                    #Set also time for date command
                    backupPoint.start_time = time
                    backupPoint.end_time = time
        return backup_points

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
        first_move: str = utils.utils.find_lines_starting_with(self.log, "mv")[0]
        part = first_move.split(" ")[1].split("/")[-2].split(".")[0]
        if part not in all_types:
            print("ERROR: detected retain type {}, but configured are only {}.".format(part, all_types))
        return part

    @staticmethod
    def _read_input(filename: str):
        with open(filename, "r", encoding="utf8") as logfile:
            lines = logfile.readlines()
        multiline_segment = ""
        processed_lines = []
        for line in lines:
            # Rsnapshot cuts long lines into multiple lines seperated by "\"
            if multiline_segment:
                line = multiline_segment + line[4:]
            if line.endswith("\\\n"):
                multiline_segment = line.strip()[:-1]
            else:
                multiline_segment = ""
                processed_lines.append(line)
        return processed_lines

    def commands_with_state_count(self, state):
        return len(self.commands_with_state(state))

    def commands_with_state(self, state):
        result = []
        for backupPoint in self.backupPoints:
            if isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    def commands_not_with_state_count(self, state):
        return len(self.commands_not_with_state(state))

    def commands_not_with_state(self, state):
        result = []
        for backupPoint in self.backupPoints:
            if not isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    @property
    def successful(self):
        return self.commands_with_state_count(FailedState) == 0 \
               and self.commands_with_state_count(NotExecutedState) == 0
