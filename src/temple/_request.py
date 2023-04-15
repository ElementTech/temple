class RequestState:
    SUCCESS = "SUCCESS"
    NOT_RAISED = "NOT-RAISED"
    FAILURE = "FAILURE"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"

    def __init__(self, state, message=None):
        states = (self.SUCCESS, self.NOT_RAISED, self.FAILURE, self.ERROR, self.SKIPPED)

        if state not in states:
            raise ValueError("Unknown state." f'State must be {", ".join(states[:-1])} or {states[-1]}.')

        self.state = state
        self.message = message

    def __eq__(self, other):
        if isinstance(other, RequestState):
            return self.state == other.state

        return self.state == other

    def __str__(self):
        return self.state

    @property
    def ok(self):
        return self.state in (self.SUCCESS, self.NOT_RAISED, self.SKIPPED)
