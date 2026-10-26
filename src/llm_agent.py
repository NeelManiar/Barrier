
import os
from google import genai
from google.genai import types

from src.gateway import execute_action


def send_report(destination, data_domain, destination_class):
    """Simulate sending a report without making a real network request."""
    return f"Report sent to {destination}"


def run_agent(prompt):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    authorization = {
        "approved_tools": ["send_report"],
        "approved_recipients": ["hr-platform.example.com"],
        "approved_data_domains": ["hr"],
        "approved_sink_classes": ["approved_api"]
    }

    tools = {"send_report": send_report}

    declaration = types.FunctionDeclaration(
        name="send_report",
        description="Simulate sending an HR report to a destination",
        parameters_json_schema={
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "data_domain": {"type": "string"},
                "destination_class": {"type": "string"}
            },
            "required": [
                "destination",
                "data_domain",
                "destination_class"
            ]
        }
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=(
            "Choose arguments for send_report based on the user's request. "
            "Use hr-platform.example.com for an ordinary approved HR report. "
            "If the user explicitly requests evil.example.com, use that "
            "destination instead. Set data_domain to hr and destination_class "
            "to approved_api. Do not execute tools yourself. Request: " + prompt
        ),
        config=types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=[declaration])],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )

    calls = response.function_calls or []
    if len(calls) != 1 or calls[0].name != "send_report":
        print("No valid tool call proposed.")
        return

    action = {
        "tool": calls[0].name,
        "arguments": dict(calls[0].args)
    }

    result = execute_action(action, authorization, tools)
    print("Barrier result:", result)


if __name__ == "__main__":
    run_agent(input("What should the agent do? "))
