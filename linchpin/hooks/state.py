

class State(object):

    # currently unimplemented
    VALID_SUB_STATES = []

    def __init__(self, state, sub_state=None, ctx=None):
        """
        Initialize the State object with the current state, sub_state,
        and context as needed

        :param state: valid state
        :param sub_state: valid sub_state (default: None)
        :param ctx: valid context object, useful for configuration options
        """

        # Not sure if we really need to validate this data
        # It seems unnecessary, but could be valuable.
        # Additionally, because the states bits have been reworked, this
        # sort of validation no longer works as designed.
        self.ctx = ctx
        self.state = state
        self.sub_state = sub_state

#        if self._validate_state(state):
#            self.state = state
#        else:
#            raise StateError("Invalid State mentioned")

#        if sub_state == None:
#            self.sub_state = sub_state
#        elif self._validate_sub_state(sub_state):
#            self.sub_state = sub_state
#        else:
#            raise StateError("Invalid SubState mentioned")

    def _validate_state(self, state):
        """
        Validates the state based on linchpin.conf

        :param state: state name
        """

        VALID_STATES = self.ctx.cfgs["states"].keys()
        return state in VALID_STATES

    def _validate_sub_state(self, sub_state):
        """
        Not implemented yet
        ideally should validated substates of state based on linchpin.conf
        """

        return sub_state in State.VALID_SUB_STATES

    def __repr__(self):
        """
        Representational override of state object
        """

        if self.sub_state:
            return "{0}::{1}".format(self.state, self.sub_state)
        else:
            return self.state
