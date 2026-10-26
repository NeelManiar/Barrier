# Barrier
### Context-Aware Authorization for AI Agents

Barrier is a research prototype exploring a simple question: **How do we control what an AI agent is allowed to do, even when the model proposes an unsafe action?**

Rather than relying on an LLM to decide whether its own actions are safe, Barrier places a deterministic authorization gateway between the agent and its tools. The gateway evaluates each proposed action against an explicit policy before allowing execution.

## How it works

```text
User Request
     |
     v
LLM proposes a tool call
     |
     v
Barrier Gateway
     |
     v
Authorization Policy
     |
     +---- ALLOW ----> Execute tool
     |
     +---- BLOCK ----> Reject action
```

The model interprets the request and proposes an action. Barrier independently checks whether the action is authorized.

## Current implementation

Barrier is being developed incrementally, with each version adding a distinct capability.

### v0.1 — Dataset foundation
- Prepared scenarios from CrossMCP-Bench.
- Built a dataset preparation pipeline to normalize scenarios for experimentation.

### v0.2 — Static authorization gateway
- Implemented deterministic authorization checks.
- Validated authorization inputs and required action fields.
- Added a gateway that checks proposed actions before tool execution.
- Added automated tests for authorization decisions and blocked execution.

### v0.3 — LLM-connected agent
- Integrated a Gemini model to propose structured tool calls.
- Routed model-proposed actions through the Barrier gateway.
- Implemented a simulated report-sending tool.
- Verified that an approved destination could execute successfully.
- Verified that a request targeting an unapproved destination was blocked.
- Ran the project test suite successfully.

## Example

The current prototype uses a simulated HR-reporting workflow.

**Approved destination**

`hr-platform.example.com`

The destination is present in the configured authorization policy, so the action can proceed when the other required fields are also approved.

**Unapproved destination**

`evil@example.com`

The action is rejected because the destination does not match the configured allowlist.

The tool is simulated: no real HR report is sent and no external destination is contacted.

## Getting started

### Requirements
- Python
- `pytest`
- Google Gen AI SDK for the LLM-connected demonstration
- A Gemini API key for live model calls

Install the required packages:

```bash
python -m pip install pytest google-genai
```

Set your API key as the `GEMINI_API_KEY` environment variable. Do not hardcode or commit API keys.

### Run the deterministic demo

From the project root:

```bash
python -m src.agent_demo
```

### Run the LLM-connected demo

```bash
python -m src.llm_agent
```

This requires a valid API key, an available model, and working API access.

### Run the project tests

```bash
python -m pytest -v tests/
```

## Design principles

**1. Separate proposal from authorization**

An LLM proposing an action does not automatically make that action permissible.

**2. Check the action that will actually execute**

Authorization decisions must be based on the tool and relevant arguments passed to the gateway, rather than trusting the model's description of its intended action.

**3. Default to blocking invalid actions**

Malformed actions, missing authorization fields, and values outside the configured allowlists should not proceed.

**4. Make behaviour testable**

Authorization logic is deterministic and can be tested independently of the language model.

## Limitations

Barrier is an early-stage research prototype, not a production-ready security product.

- The current workflow uses a simulated tool rather than a real enterprise integration.
- Authorization depends on explicitly configured policy fields and allowlists.
- The current implementation does not establish comprehensive protection against prompt injection, compromised tools, or every form of malicious action.
- Passing tests demonstrates the behaviour covered by those tests, not complete security.
- The prototype has not yet been comprehensively evaluated against the full CrossMCP-Bench dataset.

## Roadmap

- Expand the range of realistic toy-agent workflows.
- Evaluate authorization decisions across a broader set of benchmark scenarios.
- Explore more context-sensitive policies, including action risk and data sensitivity.
- Investigate integration patterns for real agent frameworks and tool interfaces.

## Project status

Barrier is an evolving engineering and research project focused on making AI-agent authorization explicit, testable, and independent of the model's own decisions.

The goal is to build and evaluate the security layer incrementally rather than claim a complete solution prematurely.
