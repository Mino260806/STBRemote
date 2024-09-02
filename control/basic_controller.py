import platform
import subprocess

import requests
from pynput.keyboard import Key, Controller

from actions import Action
from control.process.process_controller import ProcessController
from listener.base import Listener

keyboard = Controller()


def say(text):
    system = platform.system()
    if system == "Linux":
        subprocess.Popen(["spd-say", text], start_new_session=True)
    elif system == "Windows":
        subprocess.Popen(f'''PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}');"''', shell=True, start_new_session=True)


class BasicController:
    def __init__(self):
        self.process_controller = ProcessController()
        self.listening = True

    def key_press(self, key):
        def execute():
            if not self.listening:
                return
            keyboard.press(key)
            keyboard.release(key)

        return execute
    def get_stream_url(self):
        url = "http://192.168.1.100:2608"

        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()

    def play_stream(self):
        if not self.listening:
            return

        stream_url = self.get_stream_url()
        if not stream_url.startswith("http"):
            stream_url = "https://" + stream_url

        self.process_controller.run(["vlc", stream_url])

    def toggle_listening(self):
        self.listening = not self.listening
        if self.listening:
            say("Off")
        else:
            say("On")

    def bind(self, listener: Listener):
        listener.bind(Action.VolumeUp, self.key_press(Key.media_volume_up))
        listener.bind(Action.VolumeDown, self.key_press(Key.media_volume_down))
        listener.bind(Action.PlayPause, self.key_press(Key.space))
        listener.bind(Action.Forwards, self.key_press(Key.right))
        listener.bind(Action.Backwards, self.key_press(Key.left))
        listener.bind(Action.Mute, self.key_press(Key.media_volume_mute))
        listener.bind(Action.Display, self.key_press("f"))
        listener.bind(Action.TVRadio, self.toggle_listening)

        listener.bind(Action.Next, self.play_stream)
