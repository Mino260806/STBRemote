import os

from config import Config
from control.basic_controller import BasicController
from listener.input import InputListener
from listener.seriall import StarsatSerialListener


def get_listener():
    if os.environ.get("STBLISTENER") == "input":
        return InputListener()
    return StarsatSerialListener()


if __name__ == '__main__':
    config = Config()

    listener = get_listener()
    controller = BasicController(
            chrome_data_dir=config.get_value("Chrome", "user_data_dir")
    )

    controller.bind(listener)

    listener.listen()
