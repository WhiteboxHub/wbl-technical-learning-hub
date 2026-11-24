"""Tests for LangGraph StateGraph mechanics and checkpointing."""
import pytest
from claimflow.core.models import ClaimState, ClaimStatus
from claimflow.core.graph import StateGraph, END

def test_stategraph_compilation():
    g = StateGraph(ClaimState)
    g.add_node("step1", lambda s: s)
    g.set_entry_point("step1")
    g.add_edge("step1", END)
    compiled = g.compile()
    assert compiled is not None

def test_stategraph_conditional_routing():
    g = StateGraph(ClaimState)
    
    def node_a(s: ClaimState):
        s.requested_amount = 500.0
        return s
        
    def node_high(s: ClaimState):
        s.status = ClaimStatus.PENDING_HUMAN_APPROVAL
        return s
        
    def node_low(s: ClaimState):
        s.status = ClaimStatus.APPROVED
        return s

    g.add_node("start", node_a)
    g.add_node("high", node_high)
    g.add_node("low", node_low)
    g.set_entry_point("start")
    
    g.add_conditional_edges(
        "start",
        lambda s: "is_high" if s.requested_amount > 1000 else "is_low",
        {"is_high": "high", "is_low": "low"}
    )
    g.add_edge("high", END)
    g.add_edge("low", END)
    
    app = g.compile()
    init_state = ClaimState(
        claim_id="TEST-01",
        patient_id="PAT-901",
        patient_name="John Doe",
        provider_id="PRV-501",
        diagnosis_code="M17.11",
        procedure_code="27447",
        requested_amount=0.0,
        clinical_notes="test"
    )
    result = app.invoke(init_state)
    assert result.status == ClaimStatus.APPROVED
