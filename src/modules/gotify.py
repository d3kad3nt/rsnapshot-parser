import json
import sys
import urllib.parse
import urllib.request
from urllib.error import URLError

from modules.output_module import OutputModule
from output_parser.parsed_output import ParsedOutput
from output_parser.result_states import FailedState
from utils.config import Config


class GotifyModule(OutputModule):
    @classmethod
    def name(cls) -> str:
        return "Gotify"

    def __init__(self):
        self._config = Config(section=self.name().lower())
        self._url = self._config.get_str(key="url")
        self._api_token = self._config.get_str(key="api_token")

    def output(self, parsed_output: ParsedOutput):
        if parsed_output.successful:
            message = "Finished after {}".format(parsed_output.duration)
            self._send_message(title="Backup Successful", message=message, priority=3)

        else:
            message = self._failed_backup_message(parsed_output)
            self._send_message(title="Backup Failed", message=message, priority=9)

    def _send_message(self, title: str, message: str, priority: int = 5):
        url = "{url}/message?token={token}".format(url=self._url, token=self._api_token)
        content = {"message": message, "priority": priority, "title": title}
        query_string = json.dumps(content)
        request = urllib.request.Request(
            url,
            headers={"Content-Type": "application/json"},
            method="POST",
            data=query_string.encode("ascii"),
        )
        try:
            urllib.request.urlopen(request)
        except URLError as e:
            print("Error while connecting to gotify: {}".format(e), file=sys.stderr)

    @staticmethod
    def _failed_backup_message(parsed_output: ParsedOutput):
        if parsed_output.empty_log:
            return "The Log is empty"
        elif parsed_output.commands_with_state_count(FailedState) > 0:
            return "{} Backup Points failed".format(
                parsed_output.commands_with_state_count(FailedState)
            )
        else:
            return "Unknown Error"
