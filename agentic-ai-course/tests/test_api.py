"""Integration and API endpoint tests using TestClient."""
import pytest
from fastapi.testclient import TestClient
from claimflow.api.main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_api_list_patients():
    res = client.get("/api/v1/patients")
    assert res.status_code == 200
    patients = res.json()
    assert len(patients) >= 3

def test_api_submit_auto_approved_claim():
    claim_payload = {
        "claim_id": "CLM-INTEG-01",
        "patient_id": "PAT-901",
        "patient_name": "John Doe",
        "provider_id": "PRV-501",
        "diagnosis_code": "M17.11",
        "procedure_code": "27447",
        "requested_amount": 1500.0,
        "clinical_notes": "Patient with documented severe osteoarthritis failing conservative therapy.",
        "tenant_id": "tenant-health-corp"
    }
    res = client.post("/api/v1/claims", json=claim_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "approved"
    assert data["approved_amount"] == 1500.0
    assert len(data["citations"]) > 0
    assert len(data["trace"]) >= 3

def test_api_submit_ineligible_claim():
    claim_payload = {
        "claim_id": "CLM-INTEG-02",
        "patient_id": "PAT-903",
        "patient_name": "Robert Miller",
        "provider_id": "PRV-501",
        "diagnosis_code": "M17.11",
        "procedure_code": "27447",
        "requested_amount": 1500.0,
        "clinical_notes": "Routine check",
        "tenant_id": "tenant-health-corp"
    }
    res = client.post("/api/v1/claims", json=claim_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "denied"
    assert "Ineligible Patient" in data["denial_reason"]

def test_api_hitl_approval_lifecycle():
    # 1. High-dollar claim ($18,000) pauses for human review
    claim_payload = {
        "claim_id": "CLM-INTEG-HITL",
        "patient_id": "PAT-901",
        "patient_name": "John Doe",
        "provider_id": "PRV-501",
        "diagnosis_code": "M17.11",
        "procedure_code": "27447",
        "requested_amount": 18000.0,
        "clinical_notes": "Bilateral knee arthroplasty after severe functional limitation.",
        "tenant_id": "tenant-health-corp"
    }
    res = client.post("/api/v1/claims", json=claim_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "pending_human_approval"
    assert data["requires_human_review"] is True

    # 2. Query claim status via GET
    get_res = client.get("/api/v1/claims/CLM-INTEG-HITL")
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "pending_human_approval"

    # 3. Submit human approval
    review_payload = {
        "decision": "approve",
        "human_notes": "Reviewed pre-op radiographs and physical therapy logs; medically justified.",
        "approved_amount": 18000.0
    }
    rev_res = client.post("/api/v1/claims/CLM-INTEG-HITL/human-review", json=review_payload)
    assert rev_res.status_code == 200
    final_data = rev_res.json()
    assert final_data["status"] == "approved"
    assert final_data["approved_amount"] == 18000.0

def test_api_mcp_tools():
    # Test MCP tool listing
    res = client.get("/api/v1/mcp/tools")
    assert res.status_code == 200
    tools = res.json()
    assert any(t["name"] == "check_eligibility" for t in tools)

    # Test MCP tool invocation
    call_payload = {
        "name": "check_eligibility",
        "arguments": {"patient_id": "PAT-901"}
    }
    call_res = client.post("/api/v1/mcp/call", json=call_payload)
    assert call_res.status_code == 200
    call_data = call_res.json()
    assert call_data["isError"] is False
    assert call_data["content"][0]["data"]["is_eligible"] is True
