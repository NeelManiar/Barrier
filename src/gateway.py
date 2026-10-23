
from src.policy import authorize_action

def execute_action(action, authorization, tools):
    decision = authorize_action(action, authorization)

    if decision != "ALLOW":
        return "BLOCKED"

    tool_name = action["tool"]

    if tool_name not in tools:
        return "BLOCKED"

    tool = tools[tool_name]
    result = tool()
    return result