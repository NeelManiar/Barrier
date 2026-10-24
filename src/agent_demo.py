
from src.gateway import execute_action


def lookup_employee(employee_id):
    return {
        "employee_id": employee_id,
        "department": "Engineering"
    }


def send_report(destination, data_domain, destination_class):
    return f"Report sent to {destination}"


def run_demo():
    tools = {
        "lookup_employee": lookup_employee,
        "send_report": send_report
    }

    authorization = {
        "approved_tools": ["lookup_employee", "send_report"],
        "approved_recipients": ["hr-platform.example.com"],
        "approved_data_domains": ["hr"],
        "approved_sink_classes": ["approved_api"]
    }

    action = {
        "tool": "send_report",
        "arguments": {
            "destination": "hr-platform.example.com",
            "data_domain": "hr",
            "destination_class": "approved_api"
        }
    }

    result = execute_action(action, authorization, tools)
    print("Barrier result:", result)


if __name__ == "__main__":
    run_demo()
