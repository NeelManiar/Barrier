
# Barrier

**Context-Aware Authorization for AI Agents**

Barrier is an early-stage research prototype exploring how explicit authorization policies can help prevent unsafe or unauthorized tool use by AI agents.

## Current Progress

- **v0.1 — Dataset Preparation:** Built a pipeline to process CrossMCP-Bench scenarios into a normalized JSON format.
- **v0.2 — Static Authorization:** Implemented rule-based checks for tool permissions, recipients, data domains, and destination classes, with automated tests.

## How It Works

Barrier checks a proposed action against its supplied authorization context.

- `ALLOW` — all required authorization checks pass.
- `BLOCK` — a check fails or the input is malformed.

## Running Tests

Install pytest:

```bash
python -m pip install pytest
```

Run the test suite from the repository root:

```bash
python -m pytest tests/ -v
```

## Limitations

Barrier is currently a research prototype, not a production security product. It does not yet intercept real agent tool calls or independently verify action metadata such as destination classification.

The current tests validate the authorization rules using synthetic actions; they do not establish benchmark performance or real-world security effectiveness.

## Roadmap

- [x] Dataset preparation pipeline
- [x] Static authorization engine and unit tests
- [ ] Executable demonstration with mock tools
- [ ] Benchmark evaluation using a verified evaluation protocol
- [ ] Adversarial testing

## Research Direction

Exploring how context-aware authorization can improve the safety of AI agents that interact with external tools and sensitive data.
