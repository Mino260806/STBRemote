import platform
import subprocess

import requests
from pynput.keyboard import Key, Controller

from actions import Action
from control.process.process_controller import ProcessController
from listener.base import Listener

keyboard = Controller()

if platform.system() == "Linux":
    chrome_exec = "google-chrome"
else:
    chrome_exec = "chrome"

def say(text):
    system = platform.system()
    if system == "Linux":
        subprocess.Popen(["spd-say", text], start_new_session=True)
    elif system == "Windows":
        subprocess.Popen(f'''PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}');"''', shell=True, start_new_session=True)


class BasicController:
    def __init__(self, chrome_data_dir=""):
        self.process_controller = ProcessController()
        self.listening = True
        self.chrome_data_dir = chrome_data_dir

    def key_press(self, key):
        def execute():
            if not self.listening:
                return
            keyboard.press(key)
            keyboard.release(key)

        return execute
    def get_stream_url(self):
        url = "http://192.168.1.100:2608"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text.strip()
        except requests.exceptions.ConnectionError:
            return None

    def play_stream(self):
        if not self.listening:
            return

        stream_url = self.get_stream_url()
        proxy = None
        browser = False
        if stream_url is None:
            say("No")
            return
        while stream_url.startswith(":"):
            if stream_url.startswith(":PROXY"):
                split = stream_url.split("]")
                proxy = split[0][len(":PROXY["):]
                stream_url = stream_url[stream_url.index("]")+1:]
            elif stream_url.startswith(":BROWSER"):
                browser = True
                stream_url = stream_url[len(":BROWSER"):]

        if not stream_url.startswith("http"):
            stream_url = "https://" + stream_url

        print(f"proxy is {proxy}")
        self.open_url(stream_url, proxy, browser)

    def open_url(self, stream_url, proxy=None, browser=False):
        if proxy or browser:
            command = f"{chrome_exec} " \
                      f"--user-data-dir=\"{self.chrome_data_dir}\" " \
                      f"--new-window "
            if proxy:
                command += f"--proxy-server=\"{proxy}\" "
            else:
                command += f"--no-proxy-server "

            if browser:
                command += f"\"{stream_url}\""
            else:
                command += f"\"chrome-extension://opmeopcambhfimffbomjgemehjkbbmji/pages/player.html#{stream_url}\""
            print(command)
            self.process_controller.run(command)

        else:
            self.process_controller.run(f"vlc {stream_url}")

    def toggle_listening(self):
        self.listening = not self.listening
        if self.listening:
            say("Controle On")
        else:
            say("Controle Off")

    def bind(self, listener: Listener):
        listener.bind(Action.VolumeUp, self.key_press(Key.media_volume_up))
        listener.bind(Action.VolumeDown, self.key_press(Key.media_volume_down))
        listener.bind(Action.PlayPause, self.key_press(Key.space))
        listener.bind(Action.Forwards, self.key_press(Key.right))
        listener.bind(Action.Backwards, self.key_press(Key.left))
        listener.bind(Action.Mute, self.key_press(Key.media_volume_mute))
        listener.bind(Action.Display, self.key_press("f"))
        listener.bind(Action.Mode, self.key_press(Key.tab))
        listener.bind(Action.TVRadio, self.toggle_listening)

        listener.bind(Action.Next, self.play_stream)
