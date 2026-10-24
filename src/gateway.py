from src.policy import authorize_action


def execute_action(action, authorization, tools):
    if not isinstance(action, dict):
        return "BLOCKED"

    tool_name = action.get("tool")
    arguments = action.get("arguments", {})

    if not isinstance(tool_name, str) or not tool_name.strip():
        return "BLOCKED"

    if not isinstance(arguments, dict):
        return "BLOCKED"

    if tool_name not in tools:
        return "BLOCKED"

    # Build the exact action that will be authorized.
    checked_action = {
        "tool": tool_name,
        "destination": arguments.get("destination"),
        "data_domain": arguments.get("data_domain"),
        "destination_class": arguments.get("destination_class"),
    }

    # Block if authorization fails.
    decision = authorize_action(checked_action, authorization)

    if decision != "ALLOW":
        return "BLOCKED"

    # Only execute after authorization succeeds.
    tool = tools[tool_name]

    return tool(**arguments)