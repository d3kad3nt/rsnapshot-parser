from collections.abc import Iterable, Sequence
from typing import Type

from modules.email import EMailModule
from modules.gotify import GotifyModule
from modules.outputModule import EmptyModule, OutputModule
from modules.text import TextModule

all_modules: Iterable[Type[OutputModule]] = {
    TextModule,
    GotifyModule,
    EMailModule
}


def get_output_module(module_name: str):
    module_name = module_name.lower()
    for module in all_modules:
        if module.name().lower() == module_name:
            return module()
    else:
        print("Module {} not found".format(module_name))
        return EmptyModule()


def get_all_module_names() -> Sequence[str]:
    names: list[str] = []
    for module in all_modules:
        names.append(module.name())
    return names
