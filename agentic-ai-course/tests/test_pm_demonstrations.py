"""Verification tests for all PM Practical Demonstrations (Days 1 to 5)."""
import pytest
import importlib
from langgraph.checkpoint.memory import MemorySaver

m1 = importlib.import_module("examples.pm.01_langgraph_deep_dive")
m2 = importlib.import_module("examples.pm.02_react_tools_deep_dive")
m3 = importlib.import_module("examples.pm.03_mcp_memory_deep_dive")
m4 = importlib.import_module("examples.pm.04_multi_agent_deep_dive")
m5 = importlib.import_module("examples.pm.05_hitl_evaluation_deep_dive")

def test_pm_day1_demo_execution():
    """Validates that Day 1 LangGraph demonstration executes cleanly."""
    m1.run_day1_pm_demo()

def test_pm_day1_graph_retry_cycle():
    """Validates that LangGraph state graph cycles and hits retry logic."""
    saver = MemorySaver()
    app = m1.build_demo_graph(checkpointer=saver)
    init_state = {
        "claim_id": "TEST-CYC",
        "procedure_code": "27447",
        "attempts": 0,
        "audit_log": [],
        "status": "received",
        "error": None
    }
    res = app.invoke(init_state, config={"configurable": {"thread_id": "test-thread"}})
    assert res["status"] == "adjudicated"
    assert res["attempts"] == 2
    assert len(res["audit_log"]) >= 3

def test_pm_day2_demo_execution():
    """Validates that Day 2 ReAct tools demo executes cleanly."""
    m2.run_day2_pm_demo()

def test_pm_day3_demo_execution():
    """Validates that Day 3 MCP & Memory demo executes cleanly."""
    m3.run_day3_pm_demo()

def test_pm_day4_demo_execution():
    """Validates that Day 4 Multi-Agent demo executes cleanly."""
    m4.run_day4_pm_demo()

def test_pm_day5_demo_execution():
    """Validates that Day 5 HITL & RAGAS Evaluation demo executes cleanly."""
    m5.run_day5_pm_demo()
