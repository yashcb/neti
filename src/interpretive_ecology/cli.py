"""Command-line entry point for the reproducible experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .experiment import ExperimentConfig, run_experiment
from .evaluation import evaluate_behavior
from .phases import run_all_phases
from .advanced_phases import run_advanced_phases
from .readiness import run_readiness_controls
from .phase7 import phase_seven_as_dict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=19)
    parser.add_argument("--steps", type=int, default=180)
    parser.add_argument("--ledger", type=Path, help="write the full causal event ledger")
    parser.add_argument(
        "--comprehensive", action="store_true", help="also run ablation, restart, isolation, and seed controls"
    )
    parser.add_argument(
        "--phases", action="store_true", help="run the preregistered Phase 1--4 research programme"
    )
    parser.add_argument(
        "--advanced-phases", action="store_true", help="run Phase 1--4 falsifiers and integrated Phases 5--6"
    )
    parser.add_argument(
        "--readiness-controls", action="store_true", help="run the adversarial controls required before Phase 7"
    )
    parser.add_argument(
        "--phase-seven", action="store_true", help="run the Phase 7.0 episode kernel and Phase 7.1 synthetic pilot"
    )
    args = parser.parse_args()
    if args.phase_seven:
        report = phase_seven_as_dict()
        print(json.dumps(report, indent=2))
        return 0 if report["ready_for_phase_7_2"] else 1
    if args.readiness_controls:
        report = run_readiness_controls()
        print(json.dumps(report, indent=2))
        return 0 if all(report["predicates"].values()) else 1
    if args.advanced_phases:
        reports = run_advanced_phases()
        print(json.dumps(reports, indent=2))
        return 0 if all(all(report["predicates"].values()) for report in reports.values()) else 1
    if args.phases:
        reports = run_all_phases()
        print(json.dumps(reports, indent=2))
        return 0 if all(all(report["predicates"].values()) for report in reports.values()) else 1
    report = run_experiment(ExperimentConfig(seed=args.seed, steps=args.steps))
    if args.ledger:
        args.ledger.write_text(report.ledger_json + "\n", encoding="utf-8")
    output = report.as_dict()
    if args.comprehensive:
        from dataclasses import asdict

        output["behavioral_evaluation"] = asdict(
            evaluate_behavior(ExperimentConfig(seed=args.seed, steps=args.steps))
        )
    print(json.dumps(output, indent=2))
    return 0 if report.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
