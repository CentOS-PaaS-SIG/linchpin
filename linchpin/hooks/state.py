class State(object):
    VALID_STATES = ["preup", "predown", "postup", "postdown"]
    #VALID_SUB_STATES = ["preup", "predown", "postup", "postdown"]
    def __init__(self, state, sub_state ):
        if self._validate_state(state):
            self.state = state
        else:
            raise Exception("Invalid State mentioned")
        if sub_state == None:
            self.sub_state = sub_state
        elif self._validate_sub_state(sub_state):
            self.sub_state = sub_state
        else:
            raise Exception("Invalid SubState mentioned")
    def _validate_state(self, state):
        return state in State.VALID_STATES
    def _validate_sub_state(self, sub_state):
        """Should change logic to validate the substate as per state"""
        return sub_state in State.VALID_SUB_STATES
    def __repr__(self):
        if self.sub_state:
            return "%s::%s" % (self.state, self.sub_state)
        else:
            return self.state
