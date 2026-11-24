"""Tests for medical validation and patient eligibility tools."""
import pytest
from claimflow.tools.healthcare_tools import check_patient_eligibility, validate_medical_codes

def test_eligibility_active_patient():
    res = check_patient_eligibility("PAT-901", tenant_id="tenant-health-corp")
    assert res.is_eligible is True
    assert res.copay == 50.0

def test_eligibility_inactive_patient():
    res = check_patient_eligibility("PAT-903", tenant_id="tenant-health-corp")
    assert res.is_eligible is False
    assert "terminated or inactive" in res.message

def test_eligibility_tenant_isolation():
    res = check_patient_eligibility("PAT-901", tenant_id="foreign-tenant")
    assert res.is_eligible is False
    assert "Tenant isolation violation" in res.message

def test_code_validation_valid():
    res = validate_medical_codes("M17.11", "27447")
    assert res.is_valid_diagnosis is True
    assert res.is_valid_procedure is True
    assert res.preauth_required is True

def test_code_validation_invalid():
    res = validate_medical_codes("UNKNOWN-ICD", "UNKNOWN-CPT")
    assert res.is_valid_diagnosis is False
    assert res.is_valid_procedure is False
