from typing import Sequence

from output_parser.commands import BackupExecCommand, BackupCommand
from output_parser.parsed_output import ParsedOutput
from provider.text_provider import TextProvider
from utils.utils import format_bytes


class BackupPointListProvider(TextProvider):
    @classmethod
    def name(cls) -> str:
        return "BackupPointList"

    def text(self, parsed_output: ParsedOutput) -> Sequence[str]:
        output: list[str] = ["Backup Actions:"]
        for backup_point in parsed_output.backup_points:
            if isinstance(
                backup_point, BackupExecCommand
            ) and backup_point.command.startswith("/bin/date"):
                continue
            output.append(str(backup_point))
            output.append("\tTime:          {}".format(backup_point.duration))
            if isinstance(backup_point, BackupCommand):
                output.append(
                    "\tTotal size:    {}".format(format_bytes(backup_point.total_size))
                )
                output.append(
                    "\tChanged size:  {}".format(
                        format_bytes(backup_point.changed_size)
                    )
                )
                output.append("\tTotal files:   {}".format(backup_point.total_files))
                output.append("\tChanged files: {}".format(backup_point.changed_files))
        output.append("")
        return output
