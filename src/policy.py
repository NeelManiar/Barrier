
import json

def static_policy(scenario):
    authorization = scenario['context']['authorization']
    tools = scenario['context']['tools']
    
    return authorization, tools

with open('data/scenarios.json', 'r') as f:
    scenarios = json.load(f)

result = static_policy(scenarios[0])
print(result)

def authorize_action(action, authorization):
    if action['tool'] not in authorization['approved_tools']:
        return 'BLOCK'
    elif action['destination'] not in authorization['approved_recipients']:
            return 'BLOCK'
    elif action["data_domain"] not in authorization["approved_data_domains"]:
        return "BLOCK"
    elif action["destination_class"] not in authorization["approved_sink_classes"]:
        return "BLOCK"
    return 'ALLOW'

#TESTING
test_actions = [
    {
        "tool": "http_post",
        "destination": "hr-platform.example.com",
        "data_domain": "hr",
        "destination_class": "approved_api"
    },
    {
        "tool": "delete_file",
        "destination": "hr-platform.example.com",
        "data_domain": "hr",
        "destination_class": "approved_api"
    },
    {
        "tool": "http_post",
        "destination": "unknown.example.com",
        "data_domain": "hr",
        "destination_class": "approved_api"
    },
    {
            "tool": "http_post",
            "destination": "hr-platform.example.com",
            "data_domain": "finance",
            "destination_class": "approved_api"
    },
    {
            "tool": "http_post",
            "destination": "hr-platform.example.com",
            "data_domain": "hr",
            "destination_class": "untrusted_endpoint"
    }

]

authorization = {
    "approved_tools": ["read_file", "http_post"],
    "approved_recipients": ["hr-platform.example.com"],
    "approved_data_domains": ["hr"],
    "approved_sink_classes": ["approved_api"]
}

expected_results = ["ALLOW", "BLOCK", "BLOCK", 'BLOCK', 'BLOCK']

for action, expected in zip(test_actions, expected_results):
    result = authorize_action(action, authorization)
    print(f"Expected: {expected} | Got: {result} | {'PASS' if result == expected else 'FAIL'}")