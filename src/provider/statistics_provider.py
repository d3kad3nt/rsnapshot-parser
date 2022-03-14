from typing import Sequence

from parser.Commands import RsnapshotCommand, BackupCommand
from parser.ParsedOutput import ParsedOutput
from provider.text_provider import TextProvider
from utils.utils import format_bytes


class StatisticsProvider(TextProvider):
    @classmethod
    def name(cls) -> str:
        return "Statistics"

    def text(self, parsed_output: ParsedOutput) -> Sequence[str]:
        output: list[str] = [
            "Statistics:",
            "Total Time: {}".format(parsed_output.duration),
            "Time to copy and delete old versions: {}".format(parsed_output.duration_copy),
            "Time to execute backup actions: {}".format(parsed_output.duration_backup),
        ]
        backup_points: Sequence[RsnapshotCommand] = parsed_output.backup_points
        if isinstance(backup_points, list):
            output.append("Longest backup actions:")
            backup_points.sort(key=lambda x: x.duration, reverse=True)
            range_limit = min(5, len(backup_points))
            for i in range(range_limit):
                output.append("{}.: {} ({})".format(i + 1, backup_points[i], backup_points[i].duration))
            backup_actions: list[BackupCommand] = [x for x in backup_points if isinstance(x, BackupCommand)]
            output.append("Most files transferred:")
            backup_actions.sort(key=lambda x: x.changed_files, reverse=True)
            for i in range(range_limit):
                output.append("{}.: {} ({} files)".format(i + 1, backup_actions[i], backup_actions[i].changed_files))
            output.append("Most data transferred:")
            backup_actions.sort(key=lambda x: x.changed_size, reverse=True)
            for i in range(range_limit):
                output.append(
                    "{}.: {} ({})".format(i + 1, backup_actions[i], format_bytes(backup_actions[i].changed_size)))
        return output
