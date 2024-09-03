from actions import Action
STARSAT_CODES = {
    0xFFFFFFFF: Action.Repeat,
    0x90FD1BE4: Action.VolumeUp,
    0x90FDDB24: Action.VolumeDown,
    0x90FD936C: Action.PlayPause,
    0x90fd53ac: Action.Forwards,
    0x90fdd32c: Action.Backwards,
    0x90fdab54: Action.Previous,
    0x90fd51ae: Action.Next,
    0x90fdd12e: Action.Mute,
    0x90fd31ce: Action.Display,
    0x90fd916e: Action.TVRadio,
    0x90fd21de: Action.Mode,
    0x90fdbb44: Action.Wifi,
    0x90fd5ba4: Action.Ok,
    0x90fd7b84: Action.Up,
    0x90fd6b94: Action.Down,
    0x90fd0bf4: Action.PageUp,
    0x90fd33cc: Action.PageDown,
    0x90fdeb14: Action.Exit,
}

