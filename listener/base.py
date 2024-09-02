from actions import Action


class Listener:
    def __init__(self):
        self.bindings = {}
        self.last_action = None

    def listen(self):
        pass

    def bind(self, action: Action, function):
        self.bindings[action] = function

    def dispatch_action(self, action):
        if action is Action.Repeat \
                and self.last_action is not None \
                and self.last_action.repeatable:
            self.bindings[self.last_action]()
            return
        if action in self.bindings:
            self.last_action = action
            self.bindings[action]()
        else:
            self.last_action = None
