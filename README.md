# Evolving Interpretive Ecology: decisive micro-world experiment

This repository implements the smallest falsifiable experiment described by the
two research specifications. It is deliberately **not** a general-purpose
multi-agent assistant. It tests whether partial, surface-distinct histories can
be coordinated by a sparse cue into an unseeded, executable structural concept
that changes later prediction.

## Run

```bash
python -m pip install -e .
eie-experiment --ledger ledger.json
```

For a dependency-free source checkout:

```bash
PYTHONPATH=src python -m interpretive_ecology.cli
```

The command exits non-zero unless every decisive success predicate passes and
prints each predicate separately. The optional ledger contains the causal
parents, evidence, confidence, state delta, dependencies, and reversibility of
every accepted event.

## Experimental flow

1. Three worlds expose different nouns and scales: resource storage, packet
   routing, and an artificial ecosystem. Their shared generating mechanism is
   never supplied to an instance.
2. Five persistent instances, each with a representational bias, receive
   overlapping partial exposure and produce local structural traces.
3. A sparse cue is broadcast. Resonance selects a bias-diverse coalition; it is
   not routed to a predeclared domain expert.
4. The inquiry aligns driving signal, bounded state, and time as a boundary
   object while preserving surface translation residue.
5. Candidate executable lag operators are fit and selected from observed data.
   A concept crystallizes only when it improves prediction across all three
   training surfaces.
6. The operator is evaluated on an unseen thermal-grid surface, ablated back to
   the persistence baseline, invoked from persistent instance state in a later
   inquiry, and compared with a matched irrelevant cue.

The reported aptness profile is a vector, not an optimization scalar. Passing
this controlled experiment demonstrates only the specifications' minimal
operational phenomenon—not general intelligence or unrestricted autonomous
ontology formation.

## Package map

- `worlds.py`: deterministic synthetic worlds and scale-free observations.
- `events.py`: append-only causal ledger and lineage validation.
- `ecology.py`: local traces, resonance, boundary objects, operator discovery.
- `models.py`: concepts, tensions, and inquiry lifecycle objects.
- `experiment.py`: treatment, controls, persistence test, and success criteria.
- `cli.py`: reproducible JSON report and optional full-ledger export.

See [`docs/research_decisions.md`](docs/research_decisions.md) for reconciliation,
load-bearing assumptions, limitations, and the implementation decision log.
