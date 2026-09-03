"""Supervisor node: decides which agent acts next, or finishes."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..config import settings
from ..state import AgentState

ROUTES = {"researcher", "writer", "FINISH"}

SYSTEM = (
    "You are the supervisor of a small team. You coordinate two workers:\n"
    "- researcher: gathers notes and facts about the task\n"
    "- writer: composes the final answer using the notes\n\n"
    "Given the current progress, respond with ONE word for who should act next: "
    "'researcher', 'writer', or 'FINISH'.\n"
    "Rules: route to researcher first if there are no notes yet. Route to writer "
    "once notes exist but there is no draft. Respond 'FINISH' once a draft exists."
)


def supervisor_node(state: AgentState) -> AgentState:
    # Deterministic guardrails first, so the graph always makes progress.
    if state.get("steps", 0) >= settings.max_steps:
        return {"next": "FINISH"}
    if not state.get("notes"):
        return {"next": "researcher"}
    if not state.get("draft"):
        return {"next": "writer"}

    # Otherwise, let the model confirm completion.
    llm = ChatOpenAI(model=settings.chat_model, temperature=0)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM),
            (
                "human",
                "Task: {question}\nNotes present: {has_notes}\nDraft present: {has_draft}\n"
                "Who acts next?",
            ),
        ]
    )
    decision = (prompt | llm).invoke(
        {
            "question": state["question"],
            "has_notes": bool(state.get("notes")),
            "has_draft": bool(state.get("draft")),
        }
    ).content.strip()

    choice = next((r for r in ROUTES if r.lower() in decision.lower()), "FINISH")
    return {"next": choice}


def route(state: AgentState) -> str:
    """Conditional-edge function: read the supervisor's choice."""
    return state.get("next", "FINISH")
