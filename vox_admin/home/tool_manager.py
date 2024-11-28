from home.tool import Tool

tools = [
    Tool(1, "Dining Lights", "running"),
    Tool(2, "Hall Lights", "stopped"),
    Tool(3, "Robotic Vacuum Cleaner", "stopped"),
    Tool(4, "Kitchen Lights", "stopped"),
    Tool(5, "Garden Sprinkler", "stopped"),
    Tool(6, "Air Purifier", "stopped"),
    Tool(7, "Bedroom AC", "stopped"),
    Tool(8, "Water Heater", "stopped")
]


def add_tool(tool_id, name):
    tools.append(Tool(tool_id, name))

def get_tool(tool_id):
    for tool in tools:
        if tool.id == int(tool_id):
            return tool
    return None

def get_all_tools():
    return [tool.to_dict() for tool in tools]
