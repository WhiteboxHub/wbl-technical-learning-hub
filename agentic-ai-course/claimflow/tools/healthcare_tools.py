"""Healthcare Verification Tools for ClaimFlow AI."""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from claimflow.data.healthcare_kb import PATIENTS_DB, ICD10_DB, CPT_DB

class EligibilityCheckResult(BaseModel):
    is_eligible: bool
    plan_type: str
    deductible_remaining: float
    copay: float
    message: str

class CodeValidationResult(BaseModel):
    is_valid_diagnosis: bool
    diagnosis_desc: str
    is_valid_procedure: bool
    procedure_desc: str
    preauth_required: bool
    max_allowable: float

def check_patient_eligibility(patient_id: str, tenant_id: str = "tenant-health-corp") -> EligibilityCheckResult:
    """Verifies patient coverage, active enrollment and deductible status."""
    patient = PATIENTS_DB.get(patient_id)
    if not patient:
        return EligibilityCheckResult(
            is_eligible=False,
            plan_type="None",
            deductible_remaining=0.0,
            copay=0.0,
            message=f"Patient ID {patient_id} not found in system."
        )
    if patient.get("tenant_id") != tenant_id:
        return EligibilityCheckResult(
            is_eligible=False,
            plan_type="None",
            deductible_remaining=0.0,
            copay=0.0,
            message="Tenant isolation violation: Patient belongs to different healthcare organization."
        )
    if not patient["active"]:
        return EligibilityCheckResult(
            is_eligible=False,
            plan_type=patient["plan_type"],
            deductible_remaining=0.0,
            copay=0.0,
            message="Coverage terminated or inactive."
        )
    return EligibilityCheckResult(
        is_eligible=True,
        plan_type=patient["plan_type"],
        deductible_remaining=patient["deductible_remaining"],
        copay=patient["copay"],
        message="Patient coverage is active and verified."
    )

def validate_medical_codes(diagnosis_code: str, procedure_code: str) -> CodeValidationResult:
    """Validates ICD-10 and CPT codes against standard regulatory databases."""
    icd_info = ICD10_DB.get(diagnosis_code)
    cpt_info = CPT_DB.get(procedure_code)
    
    return CodeValidationResult(
        is_valid_diagnosis=bool(icd_info),
        diagnosis_desc=icd_info["description"] if icd_info else "Invalid ICD-10 Code",
        is_valid_procedure=bool(cpt_info),
        procedure_desc=cpt_info["description"] if cpt_info else "Invalid CPT Code",
        preauth_required=cpt_info.get("preauth_required", True) if cpt_info else True,
        max_allowable=cpt_info.get("max_allowable", 0.0) if cpt_info else 0.0
    )
