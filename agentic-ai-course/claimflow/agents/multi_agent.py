"""Multi-Agent Specialization: Triage Agent, Policy Verifier Agent, and Claims Auditor Agent."""
import json
from claimflow.core.models import ClaimState, ClaimStatus, AuditTraceEntry
from claimflow.tools.healthcare_tools import check_patient_eligibility, validate_medical_codes
from claimflow.tools.vector_rag import get_vector_store
from claimflow.memory.agent_memory import get_memory_store
from claimflow.guardrails.security import GuardrailsManager
from claimflow.core.llm import get_llm_provider

# Pricing models: token costs
TOKEN_COST_INPUT = 0.00000015
TOKEN_COST_OUTPUT = 0.00000060

def triage_agent_node(state: ClaimState) -> ClaimState:
    """Triage Agent: Checks PII guardrails, verifies patient eligibility, and validates ICD/CPT codes."""
    # 1. Guardrail checks
    clean_notes, pii_found = GuardrailsManager.sanitize_pii(state.clinical_notes)
    state.clinical_notes = clean_notes
    
    has_injection, inj_msg = GuardrailsManager.detect_prompt_injection(clean_notes)
    if has_injection:
        state.status = ClaimStatus.DENIED
        state.denial_reason = f"Security Violation: {inj_msg}"
        state.trace.append(AuditTraceEntry(
            step="Triage",
            agent="TriageAgent",
            action="RejectSecurityViolation",
            details={"violation": inj_msg}
        ))
        return state

    # 2. Check patient eligibility
    eligibility = check_patient_eligibility(state.patient_id, tenant_id=state.tenant_id)
    state.is_eligible = eligibility.is_eligible
    
    if not eligibility.is_eligible:
        state.status = ClaimStatus.DENIED
        state.denial_reason = f"Ineligible Patient: {eligibility.message}"
        state.trace.append(AuditTraceEntry(
            step="Triage",
            agent="TriageAgent",
            action="RejectIneligible",
            details={"message": eligibility.message}
        ))
        return state

    # 3. Code verification
    code_val = validate_medical_codes(state.diagnosis_code, state.procedure_code)
    if not (code_val.is_valid_diagnosis and code_val.is_valid_procedure):
        state.status = ClaimStatus.DENIED
        state.denial_reason = "Invalid diagnostic or billing codes submitted."
        state.trace.append(AuditTraceEntry(
            step="Triage",
            agent="TriageAgent",
            action="RejectInvalidCodes",
            details={"diag_valid": code_val.is_valid_diagnosis, "proc_valid": code_val.is_valid_procedure}
        ))
        return state

    state.is_preauth_required = code_val.preauth_required
    state.status = ClaimStatus.TRIAGED
    state.trace.append(AuditTraceEntry(
        step="Triage",
        agent="TriageAgent",
        action="CompleteTriage",
        details={
            "eligible": True,
            "preauth_required": code_val.preauth_required,
            "pii_redactions": pii_found
        },
        tokens_used=120,
        cost_usd=120 * TOKEN_COST_INPUT
    ))
    state.total_tokens += 120
    state.total_cost_usd += (120 * TOKEN_COST_INPUT)
    return state


def policy_verifier_agent_node(state: ClaimState) -> ClaimState:
    """Policy Verifier Agent: Uses Vector RAG to ground clinical necessity in official insurance policies."""
    if state.status == ClaimStatus.DENIED:
        return state

    vstore = get_vector_store()
    query = f"{state.procedure_code} {state.diagnosis_code} {state.clinical_notes}"
    docs = vstore.search(query, tenant_id=state.tenant_id, top_k=2)

    if not docs:
        # Abstention when no matching guidelines exist
        state.status = ClaimStatus.PENDING_HUMAN_APPROVAL
        state.requires_human_review = True
        state.human_review_reason = "Abstention: No matching policy guidelines found in knowledge base."
        state.trace.append(AuditTraceEntry(
            step="PolicyVerification",
            agent="PolicyVerifierAgent",
            action="AbstainNoCoveragePolicy",
            details={"query": query}
        ))
        return state

    top_doc = docs[0]
    state.policy_matched = top_doc["policy_code"]
    state.citations = [d["citation"] for d in docs]
    
    # LLM Clinical Necessity Assessment
    llm = get_llm_provider()
    eval_prompt = f"Assess medical necessity for {state.diagnosis_code} / {state.procedure_code}. Notes: {state.clinical_notes}. Policy: {top_doc['content']}"
    resp_text = llm.generate(eval_prompt, system_prompt="You are a clinical reviewer.")
    
    try:
        data = json.loads(resp_text)
        state.medical_necessity_score = data.get("necessity_score", 0.5)
    except Exception:
        state.medical_necessity_score = 0.85

    state.status = ClaimStatus.POLICY_VERIFIED
    state.trace.append(AuditTraceEntry(
        step="PolicyVerification",
        agent="PolicyVerifierAgent",
        action="VerifiedPolicyCriteria",
        details={
            "policy": state.policy_matched,
            "necessity_score": state.medical_necessity_score,
            "citations": state.citations
        },
        tokens_used=350,
        cost_usd=350 * TOKEN_COST_OUTPUT
    ))
    state.total_tokens += 350
    state.total_cost_usd += (350 * TOKEN_COST_OUTPUT)
    return state


def claims_auditor_agent_node(state: ClaimState) -> ClaimState:
    """Claims Auditor Agent: Inspects provider trust history, checks financial risk thresholds and routes to HITL."""
    if state.status == ClaimStatus.DENIED:
        return state

    mem = get_memory_store()
    provider_profile = mem.lookup_provider_profile(state.provider_id)
    
    # Check simulated fault injection
    if state.injected_fault == "tool_failure":
        state.status = ClaimStatus.PENDING_HUMAN_APPROVAL
        state.requires_human_review = True
        state.human_review_reason = "Escalated: External audit database connection timed out (resilient recovery)."
        state.trace.append(AuditTraceEntry(
            step="Auditing",
            agent="ClaimsAuditorAgent",
            action="RecoverToolFailure",
            details={"error": "Database timeout handled gracefully as observation."}
        ))
        return state

    risk_score = 0.10
    reasons = []

    # High Dollar Trigger: > $10,000 must pause for human approval
    if state.requested_amount >= 10000.00:
        risk_score += 0.50
        reasons.append("High dollar threshold: requested amount >= $10,000.00")

    # High Scrutiny Provider Trigger
    if provider_profile and provider_profile.get("status") == "high_scrutiny":
        risk_score += 0.40
        reasons.append("Provider flagged for high past audit violation rate")

    # Low medical necessity
    if state.medical_necessity_score < 0.60:
        risk_score += 0.35
        reasons.append("Clinical necessity score below 0.60 threshold")

    state.audit_risk_score = min(1.0, risk_score)
    state.status = ClaimStatus.AUDITED
    
    if state.audit_risk_score >= 0.50 or state.requested_amount >= 10000.00:
        state.requires_human_review = True
        state.status = ClaimStatus.PENDING_HUMAN_APPROVAL
        state.human_review_reason = "; ".join(reasons)
        action_name = "TriggerHumanApprovalGate"
    else:
        state.requires_human_review = False
        action_name = "AutoApprovalRecommended"

    state.trace.append(AuditTraceEntry(
        step="Auditing",
        agent="ClaimsAuditorAgent",
        action=action_name,
        details={
            "risk_score": state.audit_risk_score,
            "reasons": reasons,
            "requires_human": state.requires_human_review
        },
        tokens_used=180,
        cost_usd=180 * TOKEN_COST_INPUT
    ))
    state.total_tokens += 180
    state.total_cost_usd += (180 * TOKEN_COST_INPUT)
    return state


def decision_engine_node(state: ClaimState) -> ClaimState:
    """Final Decision Node: Resolves approvals or records finalized human action."""
    if state.status == ClaimStatus.DENIED:
        state.final_decision = "DENIED"
        state.approved_amount = 0.0
        return state

    if state.requires_human_review and not state.human_decision:
        # Remains in pending state
        return state

    # If Human review was submitted
    if state.human_decision:
        if state.human_decision == "approve":
            state.status = ClaimStatus.APPROVED
            state.final_decision = "APPROVED_BY_HUMAN"
            state.approved_amount = state.requested_amount
        elif state.human_decision == "deny":
            state.status = ClaimStatus.DENIED
            state.final_decision = "DENIED_BY_HUMAN"
            state.approved_amount = 0.0
            state.denial_reason = state.human_decision_notes or "Denied during human clinical audit."
        elif state.human_decision == "edit_and_approve":
            state.status = ClaimStatus.APPROVED
            state.final_decision = "MODIFIED_AND_APPROVED_BY_HUMAN"
        state.trace.append(AuditTraceEntry(
            step="Decision",
            agent="HumanInTheLoopGate",
            action="ApplyHumanDecision",
            details={
                "decision": str(state.human_decision),
                "notes": state.human_decision_notes
            }
        ))
    else:
        # Clean automated approval
        state.status = ClaimStatus.APPROVED
        state.final_decision = "AUTO_APPROVED"
        state.approved_amount = state.requested_amount
        state.trace.append(AuditTraceEntry(
            step="Decision",
            agent="DecisionEngine",
            action="AutoApproveClaim",
            details={"approved_amount": state.approved_amount}
        ))

    # Update provider memory
    get_memory_store().update_provider_record(state.provider_id, state.status == ClaimStatus.APPROVED)
    return state
