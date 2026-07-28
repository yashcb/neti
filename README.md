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
PYTHONPATH=src python -m interpretive_ecology.cli --comprehensive
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

The comprehensive report additionally performs destructive operator ablation,
JSON checkpoint/restart, graph-changing reinterpretation, five-seed robustness,
and a strongest-isolated-instance comparison. The last control is intentionally
falsifying: the present synthetic task reports **no positive ecological
synergy**, because a single local lag learner can solve it. The implementation
does not relabel that scientifically useful negative result as success.

## Executable architecture

Beyond the original decisive experiment, the repository now supplies:

- structurally rewritable relational hypergraphs with motif crystallization and
  lineage-preserving concept splits;
- history-dependent sparse associative fields;
- simultaneously retained, assumption-aware world-models with evidence and
  revision dynamics;
- grounded local symbol systems, composition, negotiated translation, and
  explicit translation residue;
- discriminating investigation selection and consequence-validated sandboxed
  tool composition;
- inquiry metabolism with typed tension lifecycles and resource-bounded
  continuation;
- quality-diversity resource allocation and executable instance birth, split,
  merge, dormancy, decay, archival recovery, and checkpoint/restart.

These are inspectable research primitives rather than a claim that the system
has achieved unrestricted metaphysical self-creation. Their tests establish
software state transitions and behavioral effects; they cannot by themselves
settle whether those effects constitute interpretation in every philosophical
sense.

## Package map

- `worlds.py`: deterministic synthetic worlds and scale-free observations.
- `events.py`: append-only causal ledger and lineage validation.
- `ecology.py`: local traces, resonance, boundary objects, operator discovery.
- `cognition.py`: hypergraphs, associative fields, world-models, local languages.
- `inquiry.py`: tension metabolism, investigation choice, sandboxed tool creation.
- `system.py`: persistence, resource allocation, and ecological lifecycle.
- `evaluation.py`: behavioral ablation, restart, robustness, and synergy controls.
- `models.py`: concepts, tensions, and inquiry lifecycle objects.
- `experiment.py`: treatment, controls, persistence test, and success criteria.
- `cli.py`: reproducible JSON report and optional full-ledger export.

See [`docs/research_decisions.md`](docs/research_decisions.md) for reconciliation,
load-bearing assumptions, limitations, and the implementation decision log.
