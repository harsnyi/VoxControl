class Controller:
    def __init__(self):
        self.COMMANDS = {
            "turn": {
                "on": "ID",
                "off": "ID"
            }
        }

    def run_command(self, text: str):
        text = text.lower()
        command_parts = text.split()

        print("Command parts:", command_parts)

        return self.recognize_command(command_parts)

    def recognize_command(self, command_parts) -> tuple:
        if len(command_parts) < 2:
            return "Invalid command. It should have at least two parts."

        action = command_parts[0]
        
        modifier = command_parts[1]
        act = {}
        if action in self.COMMANDS:
            if modifier in self.COMMANDS[action]:
                result = f"Executing command: {action} {modifier}"
                if len(command_parts) > 2:
                    device_id = command_parts[2]
                    result += f" - Targeting device with ID: {device_id}"
                    act = {"action": action, "modifier":modifier, "id": device_id}
                else:
                    result += " - No device ID provided."
                return (act, result)
            else:
                return ({}, f"Invalid modifier '{modifier}' for command '{action}'.")
        else:
            return ({}, f"Unknown command '{action}'.")
