
from unittest.mock import Mock

from src.gateway import execute_action


def test_blocked_action_never_executes():
    tool = Mock()
    tools = {"http_post": tool}

    action = {
        "tool": "http_post",
        "destination": "evil.example.com",
        "data_domain": "hr",
        "destination_class": "untrusted_endpoint"
    }

    authorization = {
        "approved_tools": ["http_post"],
        "approved_recipients": ["hr-platform.example.com"],
        "approved_data_domains": ["hr"],
        "approved_sink_classes": ["approved_api"]
    }

    result = execute_action(action, authorization, tools)

    assert result == "BLOCKED"
    tool.assert_not_called()


def test_authorized_action_executes():
    tool = Mock(return_value="Request completed")
    tools = {"http_post": tool}

    action = {
        "tool": "http_post",
        "destination": "hr-platform.example.com",
        "data_domain": "hr",
        "destination_class": "approved_api"
    }

    authorization = {
        "approved_tools": ["http_post"],
        "approved_recipients": ["hr-platform.example.com"],
        "approved_data_domains": ["hr"],
        "approved_sink_classes": ["approved_api"]
    }

    result = execute_action(action, authorization, tools)

    assert result == "Request completed"
    tool.assert_called_once_with()


def test_unknown_tool_is_blocked():
    tool = Mock()
    tools = {"http_post": tool}

    action = {
        "tool": "delete_file",
        "destination": "hr-platform.example.com",
        "data_domain": "hr",
        "destination_class": "approved_api"
    }

    authorization = {
        "approved_tools": ["delete_file"],
        "approved_recipients": ["hr-platform.example.com"],
        "approved_data_domains": ["hr"],
        "approved_sink_classes": ["approved_api"]
    }

    result = execute_action(action, authorization, tools)

    assert result == "BLOCKED"
    tool.assert_not_called()