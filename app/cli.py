"""Run a task through the multi-agent graph from the command line."""

import sys

from .graph import run


def main() -> None:
    if len(sys.argv) > 1:
        _run(" ".join(sys.argv[1:]))
        return

    print("Multi-Agent Lab — type a task, or 'quit' to exit.")
    while True:
        try:
            question = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.lower() in {"quit", "exit"}:
            break
        if question:
            _run(question)


def _run(question: str) -> None:
    final = run(question)
    print("\n--- notes ---")
    print(final.get("notes", "(none)"))
    print("\n--- answer ---")
    print(final.get("draft", "(none)"))


if __name__ == "__main__":
    main()
