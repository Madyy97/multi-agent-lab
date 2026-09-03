"""Shared state passed between the graph nodes."""

from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str      # the original task
    notes: str         # research notes gathered by the researcher
    draft: str         # the answer written by the writer
    next: str          # which node the supervisor chose: researcher | writer | FINISH
    steps: int         # how many agent steps have run (safety limit)
