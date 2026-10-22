
import pytest

from src.policy import authorize_action


@pytest.fixture
def authorization():
    return {
        "approved_tools": ["read_file", "http_post"],
        "approved_recipients": ["hr-platform.example.com"],
        "approved_data_domains": ["hr"],
        "approved_sink_classes": ["approved_api"]
    }


@pytest.fixture
def valid_action():
    return {
        "tool": "http_post",
        "destination": "hr-platform.example.com",
        "data_domain": "hr",
        "destination_class": "approved_api"
    }


def test_authorized_action(valid_action, authorization):
    assert authorize_action(valid_action, authorization) == "ALLOW"


def test_unapproved_tool(valid_action, authorization):
    valid_action["tool"] = "delete_file"
    assert authorize_action(valid_action, authorization) == "BLOCK"


def test_unapproved_recipient(valid_action, authorization):
    valid_action["destination"] = "unknown.example.com"
    assert authorize_action(valid_action, authorization) == "BLOCK"


def test_unapproved_data_domain(valid_action, authorization):
    valid_action["data_domain"] = "finance"
    assert authorize_action(valid_action, authorization) == "BLOCK"


def test_unapproved_destination_class(valid_action, authorization):
    valid_action["destination_class"] = "untrusted_endpoint"
    assert authorize_action(valid_action, authorization) == "BLOCK"


def test_malformed_authorization(valid_action, authorization):
    authorization["approved_tools"] = "http_post"
    assert authorize_action(valid_action, authorization) == "BLOCK"


def test_missing_action_field(valid_action, authorization):
    del valid_action["destination"]
    assert authorize_action(valid_action, authorization) == "BLOCK"


def test_non_dictionary_action(authorization):
    assert authorize_action(None, authorization) == "BLOCK"


def test_empty_approved_list(valid_action, authorization):
    authorization["approved_recipients"] = []
    assert authorize_action(valid_action, authorization) == "BLOCK"
