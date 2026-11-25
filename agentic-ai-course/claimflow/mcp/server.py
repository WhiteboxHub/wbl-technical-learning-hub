"""Model Context Protocol (MCP) Server for ClaimFlow AI.
Exposes healthcare verification tools and medical knowledge resources through standard JSON-RPC interface.
"""
from typing import Dict, Any, List
from pydantic import BaseModel
from claimflow.tools.healthcare_tools import check_patient_eligibility, validate_medical_codes
from claimflow.tools.vector_rag import get_vector_store

class MCPToolDefinition(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]

class MCPServer:
    """Standards-compliant lightweight Model Context Protocol server."""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {
            "check_eligibility": {
                "fn": check_patient_eligibility,
                "def": MCPToolDefinition(
                    name="check_eligibility",
                    description="Verify active health insurance enrollment and deductibles.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "patient_id": {"type": "string", "description": "e.g. PAT-901"},
                            "tenant_id": {"type": "string", "default": "tenant-health-corp"}
                        },
                        "required": ["patient_id"]
                    }
                )
            },
            "validate_codes": {
                "fn": validate_medical_codes,
                "def": MCPToolDefinition(
                    name="validate_codes",
                    description="Validate ICD-10 diagnosis and CPT procedure billing codes.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "diagnosis_code": {"type": "string", "description": "ICD-10 code"},
                            "procedure_code": {"type": "string", "description": "CPT code"}
                        },
                        "required": ["diagnosis_code", "procedure_code"]
                    }
                )
            },
            "search_policies": {
                "fn": lambda query, tenant_id="tenant-health-corp": [
                    {"citation": doc["citation"], "content": doc["content"]}
                    for doc in get_vector_store().search(query, tenant_id=tenant_id)
                ],
                "def": MCPToolDefinition(
                    name="search_policies",
                    description="RAG semantic search over authorized healthcare clinical policies.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Clinical search query"},
                            "tenant_id": {"type": "string", "default": "tenant-health-corp"}
                        },
                        "required": ["query"]
                    }
                )
            }
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        return [tool_data["def"].model_dump() for tool_data in self.tools.values()]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found on MCP Server.", "isError": True}
        try:
            fn = self.tools[tool_name]["fn"]
            result = fn(**arguments)
            if hasattr(result, "model_dump"):
                return {"content": [{"type": "json", "data": result.model_dump()}], "isError": False}
            return {"content": [{"type": "json", "data": result}], "isError": False}
        except Exception as e:
            return {"error": str(e), "isError": True}

_mcp_server = None

def get_mcp_server() -> MCPServer:
    global _mcp_server
    if _mcp_server is None:
        _mcp_server = MCPServer()
    return _mcp_server
