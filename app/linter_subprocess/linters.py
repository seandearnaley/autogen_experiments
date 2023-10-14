"""Run pylint, flake8, and black on a given Python script."""
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import List


def run_linters(script_path: Path) -> str:
    """Run pylint, flake8, and black on a given Python script and return a string of errors or output."""  # noqa: E501 pylint: disable=line-too-long
    linters = ["pylint", "flake8", "black --check --diff"]
    results: List[str] = []

    for linter in linters:
        try:
            result = run(
                f"{linter} {script_path}",
                check=True,
                shell=True,
                capture_output=True,
                text=True,
            )
            results.append(f"{linter} output: {result.stdout}")
        except CalledProcessError as e:
            results.append(f"{linter} failed with error: {e.output}")

    return "\n".join(results)


def main() -> None:
    """Run linters on a script."""
    script_path = Path(
        "/Users/seandearnaley/Documents/GitHub/autogen_docsearch/work_dir/mermaid_delegator/mermaid_diagram.py"  # noqa: E501 pylint: disable=line-too-long
    )
    lint_results = run_linters(script_path)
    print(lint_results)


if __name__ == "__main__":
    main()
