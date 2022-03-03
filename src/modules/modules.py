from modules.gotify import GotifyModule
from modules.outputModule import EmptyModule
from modules.text import TextModule

all_modules = {
    "text": TextModule(),
    "gotify": GotifyModule(),
}


def get_output_module(module_name: str):
    module_name = module_name.lower()
    if module_name in all_modules:
        return all_modules[module_name]
    else:
        print("Module {} not found".format(module_name))
        return EmptyModule()
