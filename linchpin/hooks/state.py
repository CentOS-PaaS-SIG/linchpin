from linchpin.exceptions import StateError 

class State(object):

    # currently unimplemented
    VALID_SUB_STATES = []

    def __init__(self, state, sub_state , api=None):
        self.api = api
        if self._validate_state(state):
            self.state = state
        else:
            raise StateError("Invalid State mentioned")
        if sub_state == None:
            self.sub_state = sub_state
        elif self._validate_sub_state(sub_state):
            self.sub_state = sub_state
        else:
            raise StateError("Invalid SubState mentioned")

    def _validate_state(self, state):
        VALID_STATES = self.api.ctx.cfgs["states"].keys()
        return state in VALID_STATES

    def _validate_sub_state(self, sub_state):
        """Should change logic to validate the substate as per state"""
        return sub_state in State.VALID_SUB_STATES

    def __repr__(self):
        if self.sub_state:
            return "%s::%s" % (self.state, self.sub_state)
        else:
            return self.state
