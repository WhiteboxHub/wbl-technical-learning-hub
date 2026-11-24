"""Tests for Model Context Protocol (MCP) server and Agent Memory."""
import pytest
from claimflow.mcp.server import get_mcp_server
from claimflow.memory.agent_memory import get_memory_store

def test_mcp_list_tools():
    server = get_mcp_server()
    tools = server.list_tools()
    tool_names = [t["name"] for t in tools]
    assert "check_eligibility" in tool_names
    assert "validate_codes" in tool_names
    assert "search_policies" in tool_names

def test_mcp_call_tool_success():
    server = get_mcp_server()
    resp = server.call_tool("validate_codes", {"diagnosis_code": "M17.11", "procedure_code": "27447"})
    assert resp["isError"] is False
    assert resp["content"][0]["data"]["is_valid_diagnosis"] is True

def test_mcp_call_tool_unknown():
    server = get_mcp_server()
    resp = server.call_tool("unknown_tool", {})
    assert resp["isError"] is True

def test_agent_memory_provider_profile():
    mem = get_memory_store()
    trusted = mem.lookup_provider_profile("PRV-501")
    assert trusted["status"] == "trusted"
    scrutiny = mem.lookup_provider_profile("PRV-999")
    assert scrutiny["status"] == "high_scrutiny"
