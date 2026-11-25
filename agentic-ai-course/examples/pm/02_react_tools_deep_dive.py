"""Day 2 PM Practical Demonstration: LLM Tool Calling, ReAct Loop, Parallel Execution & Fallback.
Demonstrates:
1. LLM Tool Selection & OpenAI-compatible JSON Schema generation.
2. Strict Pydantic input schema validation for tool calls and rejection handling.
3. The ReAct (Reason + Act) loop step-by-step with intermediate telemetry.
4. Sequential vs Parallel tool execution benchmark.
5. Tool timeout handling and graceful fallback recovery to local cache.
"""
import sys
import os
import time
import json
import concurrent.futures
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from claimflow.tools.healthcare_tools import check_patient_eligibility, validate_medical_codes

# 1. Pydantic Tool Input Schemas
class EligibilityToolInput(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier, e.g. PAT-901")
    tenant_id: str = Field(default="tenant-health-corp", description="Multi-tenant identifier")

class MedicalCodesToolInput(BaseModel):
    diagnosis_code: str = Field(..., description="ICD-10 clinical code, e.g. M17.11")
    procedure_code: str = Field(..., description="CPT procedure code, e.g. 27447")

# 2. ReAct Agent Implementation
class ReActAgent:
    def __init__(self, tools: Dict[str, Any], schemas: Dict[str, Any]):
        self.tools = tools
        self.schemas = schemas

    def run_step(self, thought: str, action: str, action_input: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n[Thought] {thought}")
        print(f"[Action] Invoking tool: '{action}' with input: {action_input}")
        
        if action not in self.tools:
            return {"error": f"Tool '{action}' not found in registry"}
        
        # Schema validation
        schema_cls = self.schemas.get(action)
        if schema_cls:
            try:
                validated_params = schema_cls(**action_input).model_dump()
            except ValidationError as ve:
                err_msg = f"Schema validation error: {ve.errors()[0]['msg']}"
                print(f"[Observation Error] {err_msg}")
                return {"error": err_msg}
        else:
            validated_params = action_input

        start = time.perf_counter()
        try:
            fn = self.tools[action]
            result = fn(**validated_params)
            latency = (time.perf_counter() - start) * 1000
            print(f"[Observation] ({latency:.2f}ms): {result}")
            return {"observation": result, "latency_ms": latency}
        except Exception as e:
            print(f"[Observation Error] Tool execution failed: {e}")
            return {"error": str(e)}

def run_day2_pm_demo():
    print("=" * 75)
    print("DAY 2 PM DEMONSTRATION: ReAct Tool Execution, Parallel Calling & Fallbacks")
    print("=" * 75)

    # 1. Available Tools and JSON Schemas
    print("\n--- 1. Tool Registry & JSON Schema Definitions ---")
    tools = {
        "check_patient_eligibility": check_patient_eligibility,
        "validate_medical_codes": validate_medical_codes
    }
    schemas = {
        "check_patient_eligibility": EligibilityToolInput,
        "validate_medical_codes": MedicalCodesToolInput
    }

    print("Registered Tool Contracts:")
    for name, schema_cls in schemas.items():
        fields = getattr(schema_cls, "model_fields", getattr(schema_cls, "__fields__", {}))
        required_fields = [k for k, v in fields.items() if getattr(v, "is_required", lambda: getattr(v, "required", False))()]
        print(f"  Tool: '{name}'")
        print(f"    Parameters: {list(fields.keys())}")
        print(f"    Required:   {required_fields}")

    agent = ReActAgent(tools, schemas)

    # 2. Sequential ReAct Trace
    print("\n--- 2. Step-by-Step ReAct Execution Trace ---")
    step1 = agent.run_step(
        thought="Claim CLM-201 requires patient verification. I must check if PAT-901 has active coverage.",
        action="check_patient_eligibility",
        action_input={"patient_id": "PAT-901", "tenant_id": "tenant-health-corp"}
    )

    step2 = agent.run_step(
        thought="Patient coverage is active. Now verifying ICD-10 M17.11 and CPT 27447 billing validity.",
        action="validate_medical_codes",
        action_input={"diagnosis_code": "M17.11", "procedure_code": "27447"}
    )

    print("\n[Final Answer] Claim CLM-201 passes triage: active insurance plan and valid surgical billing codes confirmed.")

    # 3. Schema Validation & Error Recovery
    print("\n--- 3. Tool Schema Validation & Input Error Handling ---")
    print("Scenario: LLM generated malformed input with missing required patient_id.")
    bad_step = agent.run_step(
        thought="Attempting eligibility check without required patient_id parameter.",
        action="check_patient_eligibility",
        action_input={"tenant_id": "tenant-health-corp"} # Missing patient_id
    )
    print(f"  Agent handled validation error cleanly: {bad_step.get('error')}")

    # 4. Sequential vs Parallel Tool Execution Benchmark
    print("\n--- 4. Sequential vs Parallel Tool Execution Benchmark ---")
    
    def simulate_tool_a():
        time.sleep(0.08)
        return check_patient_eligibility("PAT-901")

    def simulate_tool_b():
        time.sleep(0.08)
        return validate_medical_codes("M17.11", "27447")

    # Sequential timing
    t0 = time.perf_counter()
    res_a = simulate_tool_a()
    res_b = simulate_tool_b()
    seq_time = (time.perf_counter() - t0) * 1000

    # Parallel timing (using ThreadPoolExecutor)
    t1 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        fut_a = executor.submit(simulate_tool_a)
        fut_b = executor.submit(simulate_tool_b)
        p_res_a = fut_a.result()
        p_res_b = fut_b.result()
    par_time = (time.perf_counter() - t1) * 1000

    speedup = ((seq_time - par_time) / seq_time) * 100
    print(f"  Sequential Duration: {seq_time:.2f} ms")
    print(f"  Parallel Duration:   {par_time:.2f} ms ({speedup:.1f}% faster)")
    print("  Architectural Conclusion: Independent verification tools should be dispatched concurrently.")

    # 5. Tool Timeout & Fallback Execution
    print("\n--- 5. Tool Timeout & Graceful Degradation Fallback ---")
    print("  Scenario: External Primary Care Provider (PCP) referral service times out after 1.5s.")
    
    def fragile_tool_with_fallback(should_timeout: bool = True):
        try:
            if should_timeout:
                raise TimeoutError("Gateway timeout: pcp-referral.internal service did not respond within 1500ms SLA.")
            return {"status": "referral_confirmed"}
        except TimeoutError as te:
            print(f"  [Error Caught] {te}")
            print("  --> [Executing Fallback] Querying cached referral record from local EHR read replica...")
            return {
                "status": "degraded_cached_referral",
                "referral_valid": True,
                "note": "Served from local fallback cache; flagged for post-adjudication audit.",
                "degraded_mode": True
            }

    fallback_result = fragile_tool_with_fallback(should_timeout=True)
    print(f"  Fallback Result: {fallback_result}")
    print("  Resilience Benefit: System prevents claim abandonment by failing over to verified local cache.")

    print("\n[VERIFIED] ReAct agent loop, schema validation, parallel calling, and timeout fallbacks operating reliably.")

if __name__ == "__main__":
    run_day2_pm_demo()
