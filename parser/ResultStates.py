class ResultState:
    def __init__(self, message: str):
        self._message: str = message

    @property
    def message(self) -> str:
        return self._message


class UnknownState(ResultState):
    pass


class FailedState(ResultState):
    pass


class SuccessState(ResultState):
    pass


class NotExecutedState(ResultState):
    pass
