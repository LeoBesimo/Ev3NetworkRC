import enum
import inputs
import warnings


class LibraryError(RuntimeError):
    # Raise when attempted to run Library as standalone file
    pass

class UnpluggedError(RuntimeError):
    # Raise when no controller is connected
    pass

class InputMethods(enum.Enum):
    # Sync event
    Sync = 18

    # Sticks / Triggers

    LStickX = 0
    LStickY = 1
    RStickX = 2
    RStickY = 3

    LTrigger = 4
    RTrigger = 5

    DPadY = 6
    DPadX = 7

    # Buttons

    Select = 8
    Start = 9

    A = 10
    B = 11
    X = 12
    Y = 13

    LStickButton = 14
    RStickButton = 15

    LShoulder = 16
    RShoulder = 17

    def get(self):
        return self.name, self.value


class ControllerHandler:

    def __enter__(self):
        pass

    def __exit__(self, a1, a2, a3):
        pass

    def __init__(self):
        pass

    @staticmethod
    def handleKeys(event):
        code = event.code
        if code == "BTN_EAST":
            return InputMethods.B, event.state

        elif code == "BTN_SOUTH":
            return InputMethods.A, event.state

        elif code == "BTN_NORTH":
            return InputMethods.Y, event.state

        elif code == "BTN_WEST":
            return InputMethods.X, event.state

        elif code == "BTN_SELECT":
            return InputMethods.Select, event.state

        elif code == "BTN_START":
            return InputMethods.Start, event.state

        elif code == "BTN_THUMBL":
            return InputMethods.LStickButton, event.state

        elif code == "BTN_THUMBR":
            return InputMethods.RStickButton, event.state

        elif code == "BTN_TL":
            return InputMethods.LShoulder, event.state

        elif code == "BTN_TR":
            return InputMethods.RShoulder, event.state

    @staticmethod
    def handleJoysticks(event):
        code = event.code
        if code == "ABS_X":
            return InputMethods.LStickX, event.state

        elif code == "ABS_Y":
            return InputMethods.LStickY, event.state

        elif code == "ABS_RX":
            return InputMethods.RStickX, event.state

        elif code == "ABS_RY":
            return InputMethods.RStickY, event.state

        elif code == "ABS_HAT0X":
            return InputMethods.DPadX, event.state

        elif code == "ABS_HAT0Y":
            return InputMethods.DPadY, event.state

        elif code == "ABS_Z":
            return InputMethods.LTrigger, event.state

        elif code == "ABS_RZ":
            return InputMethods.RTrigger, event.state

    def handleInputs(self, event):
        if event.ev_type == "Key":
            return self.handleKeys(event)
        elif event.ev_type == "Absolute":
            return self.handleJoysticks(event)
        else:
            return InputMethods.Sync, 0

    def getInputs(self):
        try:
            events = inputs.get_gamepad()

            customEvents = []

            for event in events:
                tempEvent = self.handleInputs(event)
                if tempEvent[0] is not InputMethods.Sync:
                    customEvents.append(tempEvent)

            return customEvents

        except UnpluggedError:
            warnings.warn("No Controller Connected")


if __name__ == "__main__":
    raise LibraryError()
