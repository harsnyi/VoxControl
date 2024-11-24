from tool import Tool

tools = {}

def add_machine(tool_id, name):
    tools[tool_id] = Tool(name)

def get_tools(tool_id):
    return tools.get(tool_id)

def get_all_machines():
    return [tool.to_dict() for tool in tools.values()]
