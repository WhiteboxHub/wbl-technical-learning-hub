# PowerShell Smoke Test Suite for Windows
$baseUrl = "http://localhost:8000"
Write-Host "=== ClaimFlow AI PowerShell Smoke Test Suite ===" -ForegroundColor Cyan

# 1. Health check
Write-Host -NoNewline "1. Checking API Health... "
try {
    $res = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get
    if ($res.status -eq "healthy") { Write-Host "[PASS]" -ForegroundColor Green } else { Write-Host "[FAIL]" -ForegroundColor Red; exit 1 }
} catch {
    Write-Host "[FAIL] - Could not connect to $baseUrl. Ensure server is running." -ForegroundColor Red
    exit 1
}

# 2. Patient Roster
Write-Host -NoNewline "2. Querying Patient Roster... "
$patients = Invoke-RestMethod -Uri "$baseUrl/api/v1/patients" -Method Get
if ($patients.Count -gt 0) { Write-Host "[PASS]" -ForegroundColor Green } else { Write-Host "[FAIL]" -ForegroundColor Red; exit 1 }

# 3. MCP Tools
Write-Host -NoNewline "3. Inspecting MCP Tool Schemas... "
$tools = Invoke-RestMethod -Uri "$baseUrl/api/v1/mcp/tools" -Method Get
if ($tools.Count -ge 3) { Write-Host "[PASS]" -ForegroundColor Green } else { Write-Host "[FAIL]" -ForegroundColor Red; exit 1 }

# 4. Low-dollar Auto Approval
Write-Host -NoNewline "4. Submitting Low-Dollar Claim (Auto-Approval Expected)... "
$bodyAuto = @{
    claim_id = "SMOKE-PS-AUTO"
    patient_id = "PAT-901"
    patient_name = "John Doe"
    provider_id = "PRV-501"
    diagnosis_code = "M17.11"
    procedure_code = "27447"
    requested_amount = 900.0
    clinical_notes = "Documented severe osteoarthritis failing conservative therapy"
    tenant_id = "tenant-health-corp"
} | ConvertTo-Json

$resAuto = Invoke-RestMethod -Uri "$baseUrl/api/v1/claims" -Method Post -Body $bodyAuto -ContentType "application/json"
if ($resAuto.status -eq "approved") { Write-Host "[PASS]" -ForegroundColor Green } else { Write-Host "[FAIL]" -ForegroundColor Red; exit 1 }

# 5. Ineligible Patient
Write-Host -NoNewline "5. Submitting Ineligible Patient Claim (Denial Expected)... "
$bodyDeny = @{
    claim_id = "SMOKE-PS-DENY"
    patient_id = "PAT-903"
    patient_name = "Robert Miller"
    provider_id = "PRV-501"
    diagnosis_code = "M17.11"
    procedure_code = "27447"
    requested_amount = 500.0
    clinical_notes = "Routine checkup"
    tenant_id = "tenant-health-corp"
} | ConvertTo-Json

$resDeny = Invoke-RestMethod -Uri "$baseUrl/api/v1/claims" -Method Post -Body $bodyDeny -ContentType "application/json"
if ($resDeny.status -eq "denied") { Write-Host "[PASS]" -ForegroundColor Green } else { Write-Host "[FAIL]" -ForegroundColor Red; exit 1 }

# 6. High Dollar HITL Gate
Write-Host -NoNewline "6. Submitting High-Dollar Claim (HITL Approval Gate Expected)... "
$bodyHitl = @{
    claim_id = "SMOKE-PS-HITL"
    patient_id = "PAT-901"
    patient_name = "John Doe"
    provider_id = "PRV-501"
    diagnosis_code = "M17.11"
    procedure_code = "27447"
    requested_amount = 15000.0
    clinical_notes = "Complete joint arthroplasty"
    tenant_id = "tenant-health-corp"
} | ConvertTo-Json

$resHitl = Invoke-RestMethod -Uri "$baseUrl/api/v1/claims" -Method Post -Body $bodyHitl -ContentType "application/json"
if ($resHitl.status -eq "pending_human_approval") { Write-Host "[PASS]" -ForegroundColor Green } else { Write-Host "[FAIL]" -ForegroundColor Red; exit 1 }

# 7. Resolve HITL Gate
Write-Host -NoNewline "7. Resolving HITL Review Gate... "
$bodyResolve = @{
    decision = "approve"
    human_notes = "Clinically validated by orthopedic board"
    approved_amount = 15000.0
} | ConvertTo-Json

$resResolve = Invoke-RestMethod -Uri "$baseUrl/api/v1/claims/SMOKE-PS-HITL/human-review" -Method Post -Body $bodyResolve -ContentType "application/json"
if ($resResolve.status -eq "approved") { Write-Host "[PASS]" -ForegroundColor Green } else { Write-Host "[FAIL]" -ForegroundColor Red; exit 1 }

Write-Host "All Windows smoke tests passed successfully." -ForegroundColor Green
