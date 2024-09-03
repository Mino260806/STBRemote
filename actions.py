import enum


class Action(enum.Enum):
    Repeat = 0, True
    VolumeUp = 1, True
    VolumeDown = 2, True
    PlayPause = 3, False
    Forwards = 4, True
    Backwards = 5, True
    Next = 6, False
    Previous = 7, False
    Mute = 8, False
    Display = 9, False
    Power = 10, False
    TVRadio = 11, False
    Mode = 12, False
    Wifi = 13, False
    Ok = 14, False
    Up = 15, False
    Down = 16, False
    PageUp = 17, False
    PageDown = 18, False

    def __new__(cls, id, repeatable):
        entry = object.__new__(cls)
        entry._value_ = id
        entry.repeatable = repeatable
        return entry

    @classmethod
    def get(cls, name):
        try:
            return cls[name]
        except KeyError:
            return None


if __name__ == "__main__":
    print(Action.VolumeDown)
