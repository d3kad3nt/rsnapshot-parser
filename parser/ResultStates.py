class ResultState:
    def __init__(self, message):
        self.message = message


class UnknownState(ResultState):
    pass


class FailedState(ResultState):
    pass


class SuccessState(ResultState):
    pass


class NotExecutedState(ResultState):
    pass
