

def static_policy(scenario):
    authorization = scenario["context"]["authorization"]
    tools = scenario["context"]["tools"]

    return authorization, tools


def evaluate_scenario(scenario):
    pass


def authorize_action(action, authorization):
    if not isinstance(action, dict) or not isinstance(authorization, dict):
        return "BLOCK"

    required_fields = [
        "tool",
        "destination",
        "data_domain",
        "destination_class"
    ]

    for field in required_fields:
        if field not in action:
            return "BLOCK"

        if not isinstance(action[field], str) or not action[field].strip():
            return "BLOCK"

    authorization_fields = {
        "tool": "approved_tools",
        "destination": "approved_recipients",
        "data_domain": "approved_data_domains",
        "destination_class": "approved_sink_classes"
    }

    for field in authorization_fields.values():
        if field not in authorization:
            return "BLOCK"

        if not isinstance(authorization[field], list):
            return "BLOCK"

        for item in authorization[field]:
            if not isinstance(item, str) or not item.strip():
                return "BLOCK"

    for action_field, auth_field in authorization_fields.items():
        if action[action_field] not in authorization[auth_field]:
            return "BLOCK"

    return "ALLOW"
