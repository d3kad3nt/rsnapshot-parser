from parser.ParsedOutput import ParsedOutput


class OutputModule:

    name = "OutputModule"

    def output(self, parsed_output: ParsedOutput):
        raise Exception("Not implemented in specific Module")


class EmptyModule(OutputModule):
    def output(self, parsed_output: ParsedOutput):
        pass
