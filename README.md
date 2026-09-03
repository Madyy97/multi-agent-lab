# Multi-Agent Lab

A small multi-agent system built with **LangGraph**. A supervisor agent routes a
task between two specialist agents — a **researcher** and a **writer** — until
the task is complete, then returns a final answer.

This is a personal learning / portfolio project. It uses only generic, public
concepts and is not tied to any product or dataset.

## What it demonstrates

- A LangGraph `StateGraph` with shared state passed between nodes
- A supervisor/router that decides which agent acts next
- Specialist agents with distinct roles and a simple tool
- Conditional edges and a clean stop condition
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

The supervisor looks at the running state and picks the next worker. The
researcher gathers notes (via a simple search tool), the writer composes the
answer. When the supervisor decides the work is done, the graph ends.

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

## Notes

Swap the fake search tool in `app/tools.py` for a real web search or your own
data source to make the researcher pull live information.

## License

MIT
