# Barrier
### Context-Aware Authorization for AI Agents

Barrier is a research prototype exploring how to control what an AI agent is allowed to do, even when its model proposes an unsafe action.

Instead of trusting an LLM to authorize its own actions, Barrier places a deterministic authorization gateway between the agent and its tools. Every proposed action is checked against an explicit policy before execution.

---

## How It Works

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

**Core principle:** An AI model can propose an action, but the authorization layer decides whether it is allowed.

---

## Development Progress

| Version | Milestone | Status |
|---|---|---|
| v0.1 | Dataset preparation and normalization | ☑ Complete |
| v0.2 | Static authorization policy, gateway and tests | ☑ Complete |
| v0.3 | LLM-connected agent and authorization enforcement | ☑ Complete |

### v0.1 — Dataset Foundation
- Prepared scenarios from CrossMCP-Bench.
- Built a dataset preparation pipeline.
- Normalized scenarios for further experimentation.

### v0.2 — Static Authorization Gateway
- Implemented deterministic authorization checks.
- Validated required action and authorization fields.
- Built a gateway to check actions before execution.
- Added automated authorization tests.
- Tested that unauthorized actions do not execute.

### v0.3 — LLM-Connected Agent
- Integrated Gemini to propose structured tool calls.
- Routed model-proposed actions through the Barrier gateway.
- Implemented a simulated report-sending tool.
- Verified successful execution for an approved destination.
- Verified blocking of an unapproved destination.
- Passed the project test suite.

---

## Example

The current prototype demonstrates authorization using a simulated HR-reporting workflow.

**Approved destination:** `hr-platform.example.com`

The destination matches the configured allowlist, so the action passes authorization and the simulated tool executes.

**Unapproved destination:** `evil@example.com`

The LLM proposes the action, but Barrier rejects it because the destination is not approved. The tool does not execute.

No real HR report is sent and no external destination is contacted.

---

## Getting Started

### Requirements
- Python
- `pytest`
- Google Gen AI SDK
- A Gemini API key for live model calls

### 1. Install dependencies

```bash
python -m pip install pytest google-genai
```

### 2. Configure the API key

Set your API key as the `GEMINI_API_KEY` environment variable. Keep it private and never commit it to GitHub.

### 3. Run the deterministic demo

```bash
python -m src.agent_demo
```

### 4. Run the LLM-connected agent

```bash
python -m src.llm_agent
```

This requires valid API credentials, an available Gemini model, and working API access.

### 5. Run the project tests

```bash
python -m pytest -v tests/
```

---

## Design Principles

- **Separation of proposal and authorization:** An LLM proposing an action does not automatically authorize it.
- **Argument-level checks:** The gateway checks the tool and relevant arguments that will actually be passed for execution.
- **Fail-closed validation:** Malformed actions, missing required fields, and values outside configured allowlists are rejected.
- **Testable decisions:** Authorization logic can be tested independently of the language model.

---

## Limitations

Barrier is an early-stage research prototype, not a production-ready security product.

- The current workflow uses a simulated tool rather than a real enterprise integration.
- Authorization relies on explicitly configured policy fields and allowlists.
- Comprehensive protection against prompt injection, compromised tools, and all forms of malicious actions has not been established.
- The prototype has not yet been comprehensively evaluated across the full CrossMCP-Bench dataset.


### Current Focus

Barrier is an experimental authorization layer for AI agents. It intercepts proposed tool calls and checks them against explicit permissions before allowing execution.

**Current capability (v0.3):**
- Accepts tool-call proposals from an LLM.
- Validates action structure and checks tool, destination, data domain, and destination class against configured allowlists.
- Blocks unauthorized actions before the registered tool executes.
- Demonstrates the flow using a simulated report-sending tool.

**Planned research direction (v0.4): Content-Aware Authorization**

The current policy evaluates action metadata; it does not inspect report contents. The next research stage will investigate whether payload inspection can prevent sensitive or prohibited information from being transferred to an otherwise approved destination.

Planned work:
- Define explicit content-handling policies.
- Build labelled test cases for permitted and prohibited payloads.
- Evaluate content inspection approaches.
- Measure false positives and false negatives.
- Document limitations and test results.

**Scope and limitations:** Barrier is a research prototype, not a production-ready security product. Content-aware authorization is planned work and is not yet implemented.

## Roadmap

- [ ] Expand realistic toy-agent workflows.
- [ ] Evaluate authorization decisions across a broader set of benchmark scenarios.
- [ ] Explore context-sensitive policies based on action risk and data sensitivity.
- [ ] Investigate integration with real agent frameworks and tool interfaces.

---

## Project Status

Barrier is an evolving engineering and research project focused on making AI-agent authorization explicit, testable, and independent of the model's own decisions.

Each version builds on the previous one: from preparing benchmark data, to implementing deterministic authorization, to connecting a language model to the gateway.

The goal is to build and evaluate the security layer incrementally—not to claim a complete solution prematurely.
