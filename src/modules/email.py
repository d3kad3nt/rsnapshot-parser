import smtplib
import ssl
import email.message
from collections.abc import Sequence

from modules import outputModule
from parser.ParsedOutput import ParsedOutput
from provider.providers import get_text_from_providers
from utils.config import Config


class EMailModule(outputModule.OutputModule):

    @classmethod
    def name(cls) -> str:
        return "EMail"

    def __init__(self):
        self._config: Config = Config(section=self.name().lower())

    def output(self, parsed_output: ParsedOutput):
        providers = self._config.get_str_list("providers", ["Summary"])
        output: Sequence[str] = get_text_from_providers(providers, parsed_output)
        subject: str = self.get_subject(parsed_output)

        password = self._config.get_str("password")
        sender_address = self._config.get_str("sender_address")
        receiver_address = self._config.get_str("receiver_address")
        sender_name = self._config.get_str("sender_name")
        message: email.message.Message = email.message.Message()
        if sender_name:
            message['From'] = "{} <{}>".format(sender_name, sender_address)
        else:
            message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject
        message.set_payload("".join(output))

        with self.get_connection() as server:
            server.login(user=sender_address, password=password)
            server.sendmail(from_addr=sender_address, to_addrs=receiver_address, msg=message.as_string())

    def get_connection(self):
        encryption = self._config.get_str("encryption", "SSL")
        host = self._config.get_str("host")
        port: int
        context: ssl.SSLContext = ssl.create_default_context()

        if encryption.lower() in ["ssl", "tls"]:
            port = self._config.get_int("port", 465)
            return smtplib.SMTP_SSL(host=host, port=port)
        elif encryption.lower() == "starttls":
            port = self._config.get_int("port", 587)
            server = smtplib.SMTP(host=host, port=port)
            server.starttls(context=context)
            return server
        else:
            raise Exception("Unknown encryption :{}. Only SSL, TLS and STARTTLS are supported".format(encryption))

    @staticmethod
    def get_subject(parsed_output: ParsedOutput) -> str:
        if parsed_output.successful:
            return "Rsnapshot Success"
        else:
            return "Rsnapshot Error"
