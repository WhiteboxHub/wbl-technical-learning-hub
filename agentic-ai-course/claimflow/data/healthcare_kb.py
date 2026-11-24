"""Diagnostic and Procedure Code Catalog, Patient Eligibility, and Medical Policies Database."""
from typing import Dict, Any, List

PATIENTS_DB: Dict[str, Dict[str, Any]] = {
    "PAT-901": {
        "id": "PAT-901",
        "name": "John Doe",
        "dob": "1968-04-12",
        "policy_id": "POL-GOLD-99",
        "plan_type": "Commercial Comprehensive",
        "active": True,
        "deductible_remaining": 350.00,
        "copay": 50.00,
        "tenant_id": "tenant-health-corp"
    },
    "PAT-902": {
        "id": "PAT-902",
        "name": "Jane Smith",
        "dob": "1982-11-23",
        "policy_id": "POL-SILVER-12",
        "plan_type": "HMO Standard",
        "active": True,
        "deductible_remaining": 1200.00,
        "copay": 75.00,
        "tenant_id": "tenant-health-corp"
    },
    "PAT-903": {
        "id": "PAT-903",
        "name": "Robert Miller",
        "dob": "1955-09-08",
        "policy_id": "POL-MEDICAID-01",
        "plan_type": "Medicaid Managed",
        "active": False,  # Inactive coverage
        "deductible_remaining": 0.00,
        "copay": 0.00,
        "tenant_id": "tenant-health-corp"
    }
}

ICD10_DB: Dict[str, Dict[str, Any]] = {
    "M17.11": {"description": "Unilateral primary osteoarthritis, right knee", "valid": True},
    "M17.12": {"description": "Unilateral primary osteoarthritis, left knee", "valid": True},
    "I25.10": {"description": "Atherosclerotic heart disease of native coronary artery", "valid": True},
    "R51.9":  {"description": "Headache, unspecified", "valid": True},
    "Z00.00": {"description": "Encounter for general adult medical examination", "valid": True}
}

CPT_DB: Dict[str, Dict[str, Any]] = {
    "27447": {
        "description": "Total knee arthroplasty (replacement)",
        "preauth_required": True,
        "max_allowable": 14500.00,
        "category": "Orthopedics"
    },
    "33533": {
        "description": "Coronary artery bypass, single arterial graft",
        "preauth_required": True,
        "max_allowable": 28000.00,
        "category": "Cardiovascular"
    },
    "70553": {
        "description": "MRI brain without and with contrast",
        "preauth_required": True,
        "max_allowable": 1850.00,
        "category": "Radiology"
    },
    "99213": {
        "description": "Office or other outpatient visit, low complexity",
        "preauth_required": False,
        "max_allowable": 150.00,
        "category": "Evaluation and Management"
    }
}

POLICY_GUIDELINES: List[Dict[str, Any]] = [
    {
        "id": "DOC-POL-01",
        "policy_code": "POL-ORTHO-2026",
        "title": "Clinical Criteria for Total Knee Arthroplasty (CPT 27447)",
        "category": "Orthopedics",
        "content": (
            "Total Knee Arthroplasty (CPT 27447) requires documented failure of at least 6 months "
            "of conservative medical therapy including physical therapy, NSAIDs, or intra-articular injections. "
            "Diagnostic confirmation of grade III or IV osteoarthritis (ICD-10 M17.11, M17.12) via radiograph is mandatory. "
            "Prior authorization approval is granted when functional impairment restricts activities of daily living."
        ),
        "citation": "POL-ORTHO-2026: Section 4.2 - Total Knee Replacement",
        "tenant_id": "tenant-health-corp"
    },
    {
        "id": "DOC-POL-02",
        "policy_code": "POL-CARDIO-2026",
        "title": "Clinical Coverage for Coronary Artery Bypass Graft (CPT 33533)",
        "category": "Cardiovascular",
        "content": (
            "CABG surgery (CPT 33533) requires documented angiographic evidence of multi-vessel coronary artery disease "
            "or left main stenosis > 50%. Associated with diagnosis ICD-10 I25.10. Patient must have documented cardiology evaluation."
        ),
        "citation": "POL-CARDIO-2026: Section 2.1 - Surgical Revascularization",
        "tenant_id": "tenant-health-corp"
    },
    {
        "id": "DOC-POL-03",
        "policy_code": "POL-RAD-2026",
        "title": "Clinical Criteria for Brain MRI (CPT 70553)",
        "category": "Radiology",
        "content": (
            "Brain MRI with/without contrast (CPT 70553) for unspecified headache (R51.9) is NOT authorized unless "
            "accompanied by abnormal neurological examination findings, sudden severe onset (thunderclap headache), or failure of medical management."
        ),
        "citation": "POL-RAD-2026: Section 5.3 - Advanced Neuroimaging Guidelines",
        "tenant_id": "tenant-health-corp"
    }
]
