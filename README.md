# Multi-Agent Lab

A small, readable **multi-agent system** built with **LangGraph**: a supervisor agent routes a task between two specialists — a **researcher** and a **writer** — and returns a final answer. The supervisor uses **deterministic guardrails** so the graph always makes progress, even when the LLM's routing is unreliable.

## The problem it addresses
Single-prompt LLM calls fall over on multi-step tasks — they mix "gather information" and "compose the answer" into one messy step, and they're hard to steer or debug. Multi-agent routing splits the work into roles with a coordinator, which is the pattern behind most production agent systems. This project is a clean, minimal reference implementation of that pattern — small enough to read in one sitting, structured enough to extend.

## What it demonstrates
- A LangGraph `StateGraph` with shared state passed between nodes
- A supervisor/router that decides which agent acts next
- **Deterministic routing guardrails** — the supervisor advances the graph by rule (no notes → research; notes but no draft → write; draft exists → finish) and only consults the LLM to confirm completion, so a bad model response can't stall or loop the system
- Specialist agents with distinct roles and a simple tool
- Conditional edges and a clean stop condition (with a max-steps safety cap)
- A CLI to run a task end to end

## How it works

```
              ┌─────────────┐
  question ──►│  supervisor │◄─────────────┐
              └──────┬──────┘              │
             route   │                     │ (loop back until done)
        ┌────────────┼────────────┐        │
        ▼                         ▼         │
  ┌───────────┐            ┌───────────┐    │
  │ researcher│            │  writer   │────┘
  └───────────┘            └───────────┘
        │                         │
        └──────────► FINISH ──────┘──► final answer
```

The supervisor inspects the running state and picks the next worker. The researcher gathers notes (via a simple search tool), the writer composes the answer. When a draft exists, the supervisor finishes and the graph ends.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then add your OpenAI API key
```

## Usage

```bash
python -m app.cli "Explain what a state graph is and why it is useful."
```

Or interactively:

```bash
python -m app.cli
```

## Project layout

```
multi-agent-lab/
├── app/
│   ├── config.py          # settings from environment
│   ├── state.py           # shared graph state
│   ├── tools.py           # a simple search tool
│   ├── agents/
│   │   ├── supervisor.py  # routes to the next agent or finishes
│   │   ├── researcher.py  # gathers notes
│   │   └── writer.py      # composes the final answer
│   ├── graph.py           # wires the agents into a LangGraph
│   └── cli.py             # run a task from the terminal
├── requirements.txt
├── .env.example
└── README.md
```

## Design notes
- **Guardrails first, LLM second.** Routing is rule-driven for the common path; the model is only asked to confirm the task is complete. This keeps the system cheap, fast, and predictable.
- **Separation of concerns.** State, tools, and each agent live in their own module, so a new agent or tool is an additive change.

## Limitations & future work
This is a learning/reference implementation, and it deliberately keeps scope small. Known limitations and natural next steps:
- **The search tool is a stub.** Swap `app/tools.py` for a real web search or a private data source to make the researcher pull live information.
- **No evaluation harness yet.** There are no task-success metrics or regression tests on routing decisions — the next step would be a small golden set of tasks with pass/fail checks.
- **No observability.** Adding tracing (e.g. Langfuse/LangSmith) and per-run token/cost logging would make behavior measurable in production.
- **Single-turn, synchronous.** No streaming, no conversation memory across runs, and agents run sequentially rather than in parallel.
- **Minimal guardrails on outputs.** Inputs and tool use aren't validated against misuse; a production version would add input checks and output constraints.

## License
MIT
