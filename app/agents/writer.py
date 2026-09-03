"""Writer node: composes the final answer from the research notes."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..config import settings
from ..state import AgentState

SYSTEM = (
    "You are a writer. Using the research notes, write a clear, well-structured "
    "answer to the task in a short paragraph or two. Do not mention the notes."
)


def writer_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model=settings.chat_model, temperature=0.3)
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM), ("human", "Task: {question}\n\nNotes:\n{notes}")]
    )
    draft = (prompt | llm).invoke(
        {"question": state["question"], "notes": state.get("notes", "")}
    ).content.strip()

    return {"draft": draft, "steps": state.get("steps", 0) + 1}
