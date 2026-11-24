"""StateGraph Engine.
Implements the core LangGraph mechanics (nodes, edges, conditional routing, state transition, and checkpointing).
"""
import copy
from typing import Callable, Dict, List, Optional, Tuple, Any
from .models import ClaimState

START = "__start__"
END = "__end__"

class StateGraph:
    """StateGraph engine modeling nodes, directed edges, conditional routing, and checkpoints."""
    
    def __init__(self, state_schema=ClaimState):
        self.state_schema = state_schema
        self.nodes: Dict[str, Callable[[ClaimState], ClaimState]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Tuple[Callable[[ClaimState], str], Dict[str, str]]] = {}
        self.entry_point: Optional[str] = None
        self.checkpoints: Dict[str, List[Dict[str, Any]]] = {}

    def add_node(self, name: str, action: Callable[[ClaimState], ClaimState]):
        self.nodes[name] = action
        return self

    def set_entry_point(self, name: str):
        self.entry_point = name
        return self

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node
        return self

    def add_conditional_edges(
        self,
        source: str,
        path: Callable[[ClaimState], str],
        path_map: Dict[str, str]
    ):
        self.conditional_edges[source] = (path, path_map)
        return self

    def compile(self):
        """Validates graph structure and returns executable workflow."""
        if not self.entry_point or self.entry_point not in self.nodes:
            raise ValueError(f"Invalid entry point: {self.entry_point}")
        return CompiledGraph(self)


class CompiledGraph:
    """Executable compiled workflow with step-by-step execution and resume capability."""
    
    def __init__(self, graph: StateGraph):
        self.graph = graph

    def save_checkpoint(self, thread_id: str, current_node: str, state: ClaimState):
        if thread_id not in self.graph.checkpoints:
            self.graph.checkpoints[thread_id] = []
        self.graph.checkpoints[thread_id].append({
            "node": current_node,
            "state": copy.deepcopy(state.model_dump())
        })

    def get_checkpoint(self, thread_id: str) -> Optional[Dict[str, Any]]:
        history = self.graph.checkpoints.get(thread_id, [])
        return history[-1] if history else None

    def invoke(
        self,
        initial_state: ClaimState,
        thread_id: Optional[str] = None,
        max_steps: int = 25
    ) -> ClaimState:
        """Runs the graph from entry point or resumes from checkpoint."""
        state = copy.deepcopy(initial_state)
        current_node = self.graph.entry_point
        step_count = 0
        
        tid = thread_id or state.claim_id

        while current_node and current_node != END and step_count < max_steps:
            step_count += 1
            node_fn = self.graph.nodes[current_node]
            
            # Execute node logic
            state = node_fn(state)
            self.save_checkpoint(tid, current_node, state)
            
            # Check if workflow paused for Human-in-the-Loop
            if state.status.value == "pending_human_approval" and not state.human_decision:
                # Paused at approval gate
                return state

            # Route to next node
            if current_node in self.graph.conditional_edges:
                condition_fn, path_map = self.graph.conditional_edges[current_node]
                route_key = condition_fn(state)
                current_node = path_map.get(route_key, END)
            elif current_node in self.graph.edges:
                current_node = self.graph.edges[current_node]
            else:
                current_node = END

        return state
