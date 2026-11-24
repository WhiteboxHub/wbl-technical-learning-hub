"""FastAPI REST Service for ClaimFlow AI."""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os

from claimflow.core.models import ClaimRequest, ClaimResponse, ClaimState, ClaimStatus, HumanReviewAction
from claimflow.core.orchestrator import get_claimflow_app
from claimflow.mcp.server import get_mcp_server
from claimflow.data.healthcare_kb import PATIENTS_DB

app = FastAPI(
    title="ClaimFlow AI API",
    description="Enterprise Healthcare Claims & Prior-Authorization Agentic Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for submitted and active claims
ACTIVE_CLAIMS: Dict[str, ClaimState] = {}

class HumanReviewInput(BaseModel):
    decision: HumanReviewAction
    human_notes: str
    approved_amount: Optional[float] = None

@app.get("/health")
def health_check():
    """Liveness probe."""
    return {"status": "healthy", "service": "claimflow-ai", "version": "1.0.0"}

@app.get("/api/v1/patients")
def list_patients():
    """Retrieve sample patient roster for testing."""
    return list(PATIENTS_DB.values())

@app.post("/api/v1/claims", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def submit_claim(request: ClaimRequest):
    """Submits a healthcare prior authorization claim to the Agentic Workflow."""
    workflow = get_claimflow_app()
    initial_state = ClaimState(
        claim_id=request.claim_id,
        patient_id=request.patient_id,
        patient_name=request.patient_name,
        provider_id=request.provider_id,
        diagnosis_code=request.diagnosis_code,
        procedure_code=request.procedure_code,
        requested_amount=request.requested_amount,
        clinical_notes=request.clinical_notes,
        tenant_id=request.tenant_id
    )
    
    final_state = workflow.invoke(initial_state)
    ACTIVE_CLAIMS[request.claim_id] = final_state

    return ClaimResponse(
        claim_id=final_state.claim_id,
        status=final_state.status,
        approved_amount=final_state.approved_amount,
        denial_reason=final_state.denial_reason,
        requires_human_review=final_state.requires_human_review,
        human_notes=final_state.human_decision_notes,
        citations=final_state.citations,
        total_tokens=final_state.total_tokens,
        total_cost_usd=round(final_state.total_cost_usd, 6),
        trace=final_state.trace
    )

@app.get("/api/v1/claims/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: str):
    """Retrieves full claim state and execution trace."""
    state = ACTIVE_CLAIMS.get(claim_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Claim {claim_id} not found.")
    
    return ClaimResponse(
        claim_id=state.claim_id,
        status=state.status,
        approved_amount=state.approved_amount,
        denial_reason=state.denial_reason,
        requires_human_review=state.requires_human_review,
        human_notes=state.human_decision_notes,
        citations=state.citations,
        total_tokens=state.total_tokens,
        total_cost_usd=round(state.total_cost_usd, 6),
        trace=state.trace
    )

@app.post("/api/v1/claims/{claim_id}/human-review", response_model=ClaimResponse)
def human_review_decision(claim_id: str, review: HumanReviewInput):
    """Human-in-the-Loop review endpoint: resolves pending authorization gates."""
    state = ACTIVE_CLAIMS.get(claim_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Claim {claim_id} not found.")
    
    if state.status != ClaimStatus.PENDING_HUMAN_APPROVAL:
        raise HTTPException(status_code=400, detail=f"Claim {claim_id} is not awaiting human review (status: {state.status}).")

    state.human_decision = review.decision
    state.human_decision_notes = review.human_notes
    if review.approved_amount is not None:
        state.approved_amount = review.approved_amount

    workflow = get_claimflow_app()
    resumed_state = workflow.invoke(state)
    ACTIVE_CLAIMS[claim_id] = resumed_state

    return ClaimResponse(
        claim_id=resumed_state.claim_id,
        status=resumed_state.status,
        approved_amount=resumed_state.approved_amount,
        denial_reason=resumed_state.denial_reason,
        requires_human_review=resumed_state.requires_human_review,
        human_notes=resumed_state.human_decision_notes,
        citations=resumed_state.citations,
        total_tokens=resumed_state.total_tokens,
        total_cost_usd=round(resumed_state.total_cost_usd, 6),
        trace=resumed_state.trace
    )

@app.get("/api/v1/mcp/tools")
def list_mcp_tools():
    """Lists tools exposed via the Model Context Protocol."""
    return get_mcp_server().list_tools()

@app.post("/api/v1/mcp/call")
def call_mcp_tool(payload: Dict[str, Any]):
    """Executes a tool call over the Model Context Protocol."""
    name = payload.get("name", "")
    args = payload.get("arguments", {})
    return get_mcp_server().call_tool(name, args)

# Mount Web Directory
web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "web")
if os.path.exists(web_dir):
    app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")
