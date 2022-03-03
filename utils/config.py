import configparser
from typing import Optional


class Config:

    def __init__(self, path: str = "/etc/rsnapshot_parser.conf", section: str = ""):
        self._parser: configparser.ConfigParser = configparser.ConfigParser()
        self._parser.read(path)
        self.path: str = path
        self._default_section: str = section

    def get_value(self, key: str, section: Optional[str] = None, default_value: str = "") -> str:
        if not section:
            section = self._default_section
        if self._parser.has_option(section=section, option=key):
            return self._parser.get(section=section, option=key)
        return default_value

    def get_bool_value(self, key: str, section: Optional[str] = None, default_value: bool = False) -> bool:
        if not section:
            section = self._default_section
        if self._parser.has_option(section=section, option=key):
            return self._parser.getboolean(section=section, option=key)
        return default_value
