"""A simple search tool.

This is a stand-in that returns canned notes so the project runs without any
external service. Replace the body of `search` with a real web search or your
own data source to make the researcher pull live information.
"""


def search(query: str) -> str:
    """Return a short snippet of reference text for a query."""
    snippets = {
        "state graph": (
            "A state graph is a computation expressed as nodes connected by edges, "
            "where a shared state object is passed from node to node. Each node reads "
            "the state, does some work, and returns an update. Edges (which can be "
            "conditional) decide which node runs next."
        ),
        "supervisor": (
            "In a multi-agent system, a supervisor is a controller that inspects the "
            "current state and decides which specialist agent should act next, or that "
            "the task is finished."
        ),
    }
    q = query.lower()
    for key, text in snippets.items():
        if key in q:
            return text
    return (
        f"No specific reference found for '{query}'. In general, break the task into "
        "smaller steps and reason about each one."
    )
