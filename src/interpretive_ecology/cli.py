"""Command-line entry point for the reproducible experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .experiment import ExperimentConfig, run_experiment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=19)
    parser.add_argument("--steps", type=int, default=180)
    parser.add_argument("--ledger", type=Path, help="write the full causal event ledger")
    args = parser.parse_args()
    report = run_experiment(ExperimentConfig(seed=args.seed, steps=args.steps))
    if args.ledger:
        args.ledger.write_text(report.ledger_json + "\n", encoding="utf-8")
    print(json.dumps(report.as_dict(), indent=2))
    return 0 if report.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
