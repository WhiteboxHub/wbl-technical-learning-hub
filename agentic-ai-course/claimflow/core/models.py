"""Data models for ClaimFlow AI."""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ClaimStatus(str, Enum):
    RECEIVED = "received"
    TRIAGED = "triaged"
    POLICY_VERIFIED = "policy_verified"
    AUDITED = "audited"
    PENDING_HUMAN_APPROVAL = "pending_human_approval"
    APPROVED = "approved"
    DENIED = "denied"
    FAILED = "failed"

class HumanReviewAction(str, Enum):
    APPROVE = "approve"
    DENY = "deny"
    EDIT_AND_APPROVE = "edit_and_approve"
    ESCALATE = "escalate"

class ClaimRequest(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier, e.g. CLM-1001")
    patient_id: str = Field(..., description="Patient ID, e.g. PAT-901")
    patient_name: str = Field(..., description="Full patient name")
    provider_id: str = Field(..., description="Healthcare provider ID, e.g. PRV-501")
    diagnosis_code: str = Field(..., description="ICD-10 code, e.g. M17.11")
    procedure_code: str = Field(..., description="CPT code, e.g. 27447")
    requested_amount: float = Field(..., description="Total dollar amount requested")
    clinical_notes: str = Field("", description="Clinical summary justifying prior authorization")
    tenant_id: str = Field("tenant-health-corp", description="Multi-tenant identifier for security isolation")

class AuditTraceEntry(BaseModel):
    step: str
    agent: str
    action: str
    details: Dict[str, Any] = Field(default_factory=dict)
    tokens_used: int = 0
    cost_usd: float = 0.0

class ClaimResponse(BaseModel):
    claim_id: str
    status: ClaimStatus
    approved_amount: float = 0.0
    denial_reason: Optional[str] = None
    requires_human_review: bool = False
    human_notes: Optional[str] = None
    citations: List[str] = Field(default_factory=list)
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    trace: List[AuditTraceEntry] = Field(default_factory=list)

class ClaimState(BaseModel):
    """LangGraph compatible State Schema for ClaimFlow AI."""
    claim_id: str
    patient_id: str
    patient_name: str
    provider_id: str
    diagnosis_code: str
    procedure_code: str
    requested_amount: float
    clinical_notes: str
    tenant_id: str = "tenant-health-corp"
    
    # Workflow Progression
    status: ClaimStatus = ClaimStatus.RECEIVED
    is_eligible: Optional[bool] = None
    policy_matched: Optional[str] = None
    is_preauth_required: bool = True
    medical_necessity_score: float = 0.0
    audit_risk_score: float = 0.0
    citations: List[str] = Field(default_factory=list)
    
    # Decisions
    requires_human_review: bool = False
    human_review_reason: Optional[str] = None
    human_decision: Optional[HumanReviewAction] = None
    human_decision_notes: Optional[str] = None
    final_decision: Optional[str] = None
    approved_amount: float = 0.0
    denial_reason: Optional[str] = None
    
    # Memory and Observability
    memory_context: List[str] = Field(default_factory=list)
    trace: List[AuditTraceEntry] = Field(default_factory=list)
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    
    # Fault Injection for Testing
    injected_fault: Optional[str] = None
