from actions import Action
from listener.base import Listener


class InputListener(Listener):
    def listen(self):
        while True:
            action_name = input("Action: ")
            action = Action.get(action_name)
            self.dispatch_action(action)
