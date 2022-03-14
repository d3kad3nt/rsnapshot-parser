import json
import urllib.parse
import urllib.request

from modules.outputModule import OutputModule
from parser.ParsedOutput import ParsedOutput
from parser.ResultStates import FailedState
from utils.config import Config


class GotifyModule(OutputModule):

    @classmethod
    def name(cls) -> str:
        return "Gotify"

    def __init__(self):
        self._config = Config(section=self.name().lower())
        self._url = self._config.get_str(key="url")
        self._api_token = self._config.get_str(key="api_token")

    def output(self, log_output: ParsedOutput):
        if log_output.successful:
            message = "Finished after {}".format(log_output.duration)
            self._send_message(title="Backup Successful", message=message, priority=3)

        else:
            message = self._failed_backup_message(log_output)
            self._send_message(title="Backup Failed", message=message, priority=9)

    def _send_message(self, title, message, priority=5):
        url = "{url}/message?token={token}".format(url=self._url, token=self._api_token)
        content = {
            "message": message,
            "priority": priority,
            "title": title
        }
        query_string = json.dumps(content)
        request = urllib.request.Request(url,
                                         headers={"Content-Type": "application/json"},
                                         method="POST",
                                         data=query_string.encode("ascii"))
        urllib.request.urlopen(request)

    @staticmethod
    def _failed_backup_message(parsed_output: ParsedOutput):
        if parsed_output.empty_log:
            return "The Log is empty"
        elif parsed_output.commands_with_state_count(FailedState) > 0:
            return "{} Backup Points failed".format(parsed_output.commands_with_state_count(FailedState))
        else:
            return "Unknown Error"
