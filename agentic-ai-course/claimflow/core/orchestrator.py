"""Orchestrator Workflow assembling LangGraph for ClaimFlow AI."""
from claimflow.core.graph import StateGraph, END
from claimflow.core.models import ClaimState, ClaimStatus
from claimflow.agents.multi_agent import (
    triage_agent_node,
    policy_verifier_agent_node,
    claims_auditor_agent_node,
    decision_engine_node
)

def route_after_triage(state: ClaimState) -> str:
    """Conditional Edge: routes directly to denial if triage fails, else policy verification."""
    if state.status == ClaimStatus.DENIED:
        return "decision"
    return "verify_policy"

def route_after_verification(state: ClaimState) -> str:
    """Conditional Edge: routes to decision if policy verifier denied or abstained, else audit."""
    if state.status in (ClaimStatus.DENIED, ClaimStatus.PENDING_HUMAN_APPROVAL):
        return "decision"
    return "audit_claim"

def route_after_audit(state: ClaimState) -> str:
    """Conditional Edge: routes to decision engine."""
    return "decision"

def build_claimflow_workflow():
    """Builds and compiles the complete LangGraph workflow."""
    workflow = StateGraph(ClaimState)
    
    # 1. Register Nodes
    workflow.add_node("triage", triage_agent_node)
    workflow.add_node("verify_policy", policy_verifier_agent_node)
    workflow.add_node("audit_claim", claims_auditor_agent_node)
    workflow.add_node("decision", decision_engine_node)
    
    # 2. Set Entry Point
    workflow.set_entry_point("triage")
    
    # 3. Add Edges & Conditional Routing
    workflow.add_conditional_edges(
        "triage",
        route_after_triage,
        {"verify_policy": "verify_policy", "decision": "decision"}
    )
    workflow.add_conditional_edges(
        "verify_policy",
        route_after_verification,
        {"audit_claim": "audit_claim", "decision": "decision"}
    )
    workflow.add_conditional_edges(
        "audit_claim",
        route_after_audit,
        {"decision": "decision"}
    )
    workflow.add_edge("decision", END)
    
    return workflow.compile()

# Global compiled instance
_compiled_app = None

def get_claimflow_app():
    global _compiled_app
    if _compiled_app is None:
        _compiled_app = build_claimflow_workflow()
    return _compiled_app
