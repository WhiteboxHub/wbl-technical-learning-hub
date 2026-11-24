"""Tests for Multi-Agent coordination and workflows."""
import pytest
from claimflow.core.models import ClaimState, ClaimStatus
from claimflow.core.orchestrator import get_claimflow_app

def test_multi_agent_clean_approval():
    app = get_claimflow_app()
    state = ClaimState(
        claim_id="TEST-AUTO-100",
        patient_id="PAT-901",
        patient_name="John Doe",
        provider_id="PRV-501",
        diagnosis_code="M17.11",
        procedure_code="27447",
        requested_amount=1200.0,
        clinical_notes="Documented primary osteoarthritis right knee failed conservative therapy",
        tenant_id="tenant-health-corp"
    )
    result = app.invoke(state)
    assert result.status == ClaimStatus.APPROVED
    assert len(result.trace) >= 3
    assert result.total_tokens > 0

def test_multi_agent_ineligible_patient():
    app = get_claimflow_app()
    state = ClaimState(
        claim_id="TEST-DENY-101",
        patient_id="PAT-903",
        patient_name="Robert Miller",
        provider_id="PRV-501",
        diagnosis_code="M17.11",
        procedure_code="27447",
        requested_amount=1200.0,
        clinical_notes="Routine checkup",
        tenant_id="tenant-health-corp"
    )
    result = app.invoke(state)
    assert result.status == ClaimStatus.DENIED
    assert "Ineligible Patient" in (result.denial_reason or "")
