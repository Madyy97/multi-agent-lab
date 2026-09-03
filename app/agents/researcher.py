"""Researcher node: gathers notes for the task using the search tool."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..config import settings
from ..state import AgentState
from ..tools import search

SYSTEM = (
    "You are a researcher. Using the reference material provided, write 3-5 concise "
    "bullet notes that a writer could use to answer the task. Notes only, no prose."
)


def researcher_node(state: AgentState) -> AgentState:
    question = state["question"]
    reference = search(question)

    llm = ChatOpenAI(model=settings.chat_model, temperature=0)
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM), ("human", "Task: {question}\n\nReference:\n{reference}")]
    )
    notes = (prompt | llm).invoke(
        {"question": question, "reference": reference}
    ).content.strip()

    return {"notes": notes, "steps": state.get("steps", 0) + 1}
