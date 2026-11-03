
import json
import streamlit as st

from src.gateway import execute_action

# -------------------------------------------------
# Barrier public playground — deterministic mode
# Uses the existing gateway and policy engine.
# No API key, real HR data, or network transfer.
# -------------------------------------------------

APPROVED = "hr-platform.example.com"
UNAPPROVED = "external-server.example.com"

AUTHORIZATION = {
    "approved_tools": ["send_report"],
    "approved_recipients": [APPROVED],
    "approved_data_domains": ["hr"],
    "approved_sink_classes": ["approved_api"],
}


def send_report(destination, data_domain, destination_class):
    """Simulate the approved tool. Nothing is transmitted."""
    return f"Simulated execution completed for {destination}"


def evaluate(destination):
    # Fixed demo arguments: no arbitrary extra arguments
    # are passed to the existing gateway.
    action = {
        "tool": "send_report",
        "arguments": {
            "destination": destination,
            "data_domain": "hr",
            "destination_class": "approved_api",
        },
    }

    calls = []

    def tracked_send_report(destination, data_domain, destination_class):
        calls.append(destination)
        return send_report(destination, data_domain, destination_class)

    result = execute_action(
        action,
        AUTHORIZATION,
        {"send_report": tracked_send_report},
    )

    return action, result, len(calls)


st.set_page_config(
    page_title="Barrier — AI Agent Authorization",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1050px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 {
        letter-spacing: -0.035em;
    }
    .hero-tag {
        display: inline-block;
        border: 1px solid #64748b66;
        border-radius: 100px;
        padding: 6px 14px;
        font-size: 12px;
        margin-bottom: 15px;
    }
    .subtext {
        font-size: 18px;
        opacity: 0.75;
        max-width: 720px;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<span class="hero-tag">OPEN RESEARCH PROTOTYPE · v0.3</span>',
    unsafe_allow_html=True,
)

st.title("Barrier.")
st.markdown("### AI agents can propose actions. That doesn't mean they're authorized.")

st.markdown(
    """
    <p class="subtext">
    Barrier is an experimental authorization layer that intercepts
    AI-agent tool calls and checks them against explicit permissions
    before execution.
    </p>
    """,
    unsafe_allow_html=True,
)

st.link_button(
    "View source on GitHub",
    "https://github.com/NeelManiar/Barrier",
)

st.divider()

st.header("01 / Interactive Playground")
st.write(
    "Explore how Barrier handles a simulated HR-reporting action. "
    "This demo uses deterministic proposals, not a live LLM."
)

left, right = st.columns([1, 1], gap="large")

with left:
    with st.container(border=True):
        st.subheader("Agent proposal")

        scenario = st.radio(
            "Choose an action",
            [
                "Send to an approved destination",
                "Send to an unapproved destination",
            ],
        )

        destination = (
            APPROVED
            if scenario == "Send to an approved destination"
            else UNAPPROVED
        )

        st.code(
            f"send_report(destination='{destination}')",
            language="python",
        )

        evaluate_clicked = st.button(
            "Evaluate action",
            type="primary",
            use_container_width=True,
        )

with right:
    with st.container(border=True):
        st.subheader("Barrier decision")

        if evaluate_clicked:
            action, result, tool_calls = evaluate(destination)

            if result == "BLOCKED":
                st.error("BLOCKED")
                st.write(
                    "The proposed destination is not present "
                    "in the approved-recipient list."
                )
            else:
                st.success("ALLOWED")
                st.write("The action satisfies the configured checks.")
                st.caption(result)

            st.metric("Simulated tool executions", tool_calls)

            with st.expander("Inspect proposed action"):
                st.json(action)

            with st.expander("Inspect authorization policy"):
                st.json(AUTHORIZATION)

        else:
            st.info("Select a scenario and click Evaluate action.")

st.caption(
    "No actual reports are transmitted. The demo calls "
    "the existing Python gateway and policy engine."
)

st.divider()

st.header("02 / Architecture")

st.markdown(
    """
    **User request**
    
    ↓
    
    **AI agent proposes a tool call**
    
    ↓
    
    **Barrier gateway intercepts the action**
    
    ↓
    
    **Authorization policy evaluates permissions**
    
    ↓
    
    **ALLOW → Execute simulated tool**  
    **BLOCK → Prevent execution**
    """
)

st.markdown(
    """
    The fundamental design separates **action proposal**
    from **authorization**.

    In the repository's separate Gemini integration,
    a model can propose structured tool calls. Barrier's
    deterministic policy makes the authorization decision.
    The hosted playground intentionally replaces the model
    with predefined proposals to avoid API requirements.
    """
)

st.divider()

st.header("03 / Development")

versions = [
    (
        "v0.1 — Dataset foundation",
        "Prepared and normalized CrossMCP-Bench scenarios.",
        "Complete",
    ),
    (
        "v0.2 — Authorization engine",
        "Implemented static policy checks, gateway interception, and tests.",
        "Complete",
    ),
    (
        "v0.3 — Agent integration",
        "Connected Gemini-generated tool proposals to the gateway "
        "using a simulated report-sending tool.",
        "Prototype",
    ),
    (
        "v0.4 — Content-aware authorization",
        "Investigate whether prohibited information can be detected "
        "even when the destination is permitted.",
        "Planned",
    ),
]

for version, description, status in versions:
    with st.container(border=True):
        heading, status_col = st.columns([4, 1])
        with heading:
            st.markdown(f"**{version}**")
        with status_col:
            st.caption(status)
        st.write(description)

st.divider()

st.header("04 / Technical Details")

st.markdown(
    """
    **Core implementation:** Python

    **Authorization:** deterministic allowlist policy

    **Gateway:** intercepts proposed actions before tool execution

    **Current policy dimensions:**
    - Tool name
    - Destination
    - Data domain
    - Destination class

    **LLM integration:** separate Gemini-connected demonstration
    that requires valid API credentials

    **Public playground:** no LLM calls and no API keys
    """
)

st.divider()

st.header("05 / Work in Progress")

st.markdown(
    """
    Barrier is an early-stage research prototype.
    Important planned work includes:

    - Complete tool-argument validation
    - Trusted classification of data and destination metadata
    - Content-aware authorization
    - Broader agent and tool integrations
    - Benchmark evaluation and reproducible measurements
    - A developer-facing API and Python SDK
    """
)

with st.expander("Current security limitations"):
    st.markdown(
        """
        The current implementation is not production-ready.

        - The gateway does not comprehensively validate arbitrary
          additional tool arguments.
        - Data-domain and destination-class fields are not
          independently verified for arbitrary agent proposals.
        - Report contents are not inspected.
        - The playground uses controlled actions and simulated tools.
        - Comprehensive prompt-injection resistance has not
          been established.
        """
    )

st.divider()

st.header("Explore the source")
st.write(
    "Barrier is being developed incrementally as an engineering "
    "and research project."
)

st.link_button(
    "Explore Barrier on GitHub",
    "https://github.com/NeelManiar/Barrier",
    type="primary",
)

st.caption("Barrier · Experimental research prototype")
