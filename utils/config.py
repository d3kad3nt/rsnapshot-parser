import configparser


class Config:

    def __init__(self, path="/etc/rsnapshot_parser.conf", section=""):
        self._parser = configparser.ConfigParser()
        self._parser.read(path)
        self.path = path
        self._default_section = section

    def get_value(self, key, section="", default_value=""):
        if len(section) == 0:
            section = self._default_section
        if self._parser.has_option(section=section, option=key):
            return self._parser.get(section=section, option=key)
        return default_value
