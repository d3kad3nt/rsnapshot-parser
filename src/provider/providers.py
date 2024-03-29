from collections.abc import Iterable, Sequence
from typing import Type

from output_parser.parsed_output import ParsedOutput
from provider.backup_point_list_provider import BackupPointListProvider
from provider.error_provider import ErrorProvider
from provider.statistics_provider import StatisticsProvider
from provider.summary_provider import SummaryProvider
from provider.text_provider import TextProvider, EmptyTextProvider

all_providers: Iterable[Type[TextProvider]] = {
    SummaryProvider,
    ErrorProvider,
    StatisticsProvider,
    BackupPointListProvider,
}


def get_provider(provider_name: str) -> TextProvider:
    provider_name = provider_name.lower()
    for provider in all_providers:
        if provider.name().lower() == provider_name:
            return provider()
    print("Provider {} not found".format(provider_name))
    return EmptyTextProvider()


def get_all_module_names() -> Sequence[str]:
    names: list[str] = []
    for provider in all_providers:
        names.append(provider.name())
    return names


def get_text_from_providers(
    providers: Sequence[str], parsed_output: ParsedOutput
) -> Sequence[str]:
    output: list[str] = []
    for provider in providers:
        lines = get_provider(provider).text(parsed_output)
        for line in lines:
            output.append(line.rstrip() + "\n")
        output.append("\n")
    return output
