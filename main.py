from actions import Action
from control.basic_controller import BasicController
from listener.seriall import StarsatSerialListener

if __name__ == '__main__':
    listener = StarsatSerialListener()
    controller = BasicController()

    controller.bind(listener)

    listener.listen()
