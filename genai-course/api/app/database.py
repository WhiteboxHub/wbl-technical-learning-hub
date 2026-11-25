"""In-memory session state store for UI and inspection."""

_state = {
    "last_query": None,
    "last_retrieved_chunks": [],
    "last_generated_answer": None,
    "last_sources": [],
    "last_abstained": False,
}

def get_state() -> dict:
    return _state.copy()

def set_state(key: str, value):
    _state[key] = value

def clear_state():
    _state.update({
        "last_query": None,
        "last_retrieved_chunks": [],
        "last_generated_answer": None,
        "last_sources": [],
        "last_abstained": False,
    })
