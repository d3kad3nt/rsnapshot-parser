from typing import Sequence

from parser.Commands import BackupExecCommand, BackupCommand
from parser.ParsedOutput import ParsedOutput
from provider.text_provider import TextProvider
from utils.utils import format_bytes


class BackupPointListProvider(TextProvider):
    @classmethod
    def name(cls) -> str:
        return "BackupPointList"

    def text(self, parsed_output: ParsedOutput) -> Sequence[str]:
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
        output.append("")
        return output
