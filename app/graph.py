"""Wire the supervisor and specialist agents into a LangGraph state graph."""

from langgraph.graph import StateGraph, END

from .config import require_api_key
from .state import AgentState
from .agents.supervisor import supervisor_node, route
from .agents.researcher import researcher_node
from .agents.writer import writer_node


def build_graph():
    """Compile and return the runnable multi-agent graph."""
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("supervisor")

    # The supervisor routes to a worker or finishes.
    graph.add_conditional_edges(
        "supervisor",
        route,
        {"researcher": "researcher", "writer": "writer", "FINISH": END},
    )

    # After a worker runs, control returns to the supervisor.
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("writer", "supervisor")

    return graph.compile()


def run(question: str) -> AgentState:
    """Run a single task through the graph and return the final state."""
    require_api_key()
    app = build_graph()
    return app.invoke({"question": question, "steps": 0})
