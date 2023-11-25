import configparser
from typing import Optional, Sequence


class Config:
    def __init__(self, section: str, path: str = "/etc/rsnapshot_parser.conf"):
        self._parser: configparser.ConfigParser = configparser.ConfigParser()
        self._parser.read(path)
        self.path: str = path
        self._section: str = section

    def get_str(self, key: str, default_value: str = "") -> str:
        if self._parser.has_option(section=self._section, option=key):
            return self._parser.get(section=self._section, option=key)
        return default_value

    def get_bool(self, key: str, default_value: bool = False) -> bool:
        if self._parser.has_option(section=self._section, option=key):
            return self._parser.getboolean(section=self._section, option=key)
        return default_value

    def get_int(self, key: str, default_value: int = False) -> int:
        if self._parser.has_option(section=self._section, option=key):
            return self._parser.getint(section=self._section, option=key)
        return default_value

    def get_str_list(
        self, key: str, default_value: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        if self._parser.has_option(section=self._section, option=key):
            return list(
                map(
                    str.strip,
                    self._parser.get(section=self._section, option=key).split(","),
                )
            )
        if default_value is None:
            default_value = []
        return default_value
