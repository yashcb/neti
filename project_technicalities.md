# Evolving Interpretive Ecology

## Formal Ontology, Dynamics, Algorithms, and Experimental Specification — Version 0.1

---

# 0\. Foundational decision

The system will not be defined by the type of output it produces.

It will be defined by the kinds of internal transformation it can undergo.

The central object is therefore not an answer, token sequence, plan, or rule execution. It is a **persistent change in the system’s space of possible interpretation and action**.

The system succeeds when an encounter enables it to:

* perceive a distinction it could not previously perceive;

* form a concept it did not previously possess;

* create a question that was not expressible in its earlier ontology;

* design an investigation or tool that its original structures could not generate;

* reinterpret previous experience;

* or develop a reusable capability.

The governing cycle is:

\[                \]

The architects specify the local physics of this cycle. They do not specify the concepts or conclusions that must emerge from it.

---

# 1\. Unified system state

At time (t), the complete ecology is represented as:

\[ \_t \= ( \_t, \_t, \_t, \_t, \_t, \_t, \_t ) \]

where:

| Symbol | Entity |
| :---- | :---- |
| (\_t) | Set of interpretive instances |
| (\_t) | Set of active, suspended, and completed inquiries |
| (\_t) | Boundary objects connecting different internal languages |
| (\_t) | Shared ecological commons |
| (\_t) | External environments, tools, and observable worlds |
| (\_t) | Resource and viability state |
| (\_t) | Immutable causal and developmental event ledger |

Every change to the system occurs through a typed event:

\[ \_{t+1} \=  ( \_t, e\_t ) \]

An event is:

\[ e\_t \= ( , , , , , , , t ) \]

The event ledger is essential. Without it, the system could generate the appearance of development while repeatedly reconstructing itself from scratch.

---

# 2\. Metaphysical operational criterion

The system needs a criterion for deciding whether an internal structure is genuinely part of its intelligence or merely descriptive metadata.

We adopt an **interventionist ontology**:

An entity is operationally real inside the system when intervening on that entity changes the system’s future possibilities.

For any internal object (x):

\[ (x) \= 1  Y,k: D \>  \]

Here, (Y) may include:

* future predictions;

* available actions;

* concepts formed;

* inquiries initiated;

* interpretations generated;

* tools selected;

* or ecological changes.

This gives us a strong test.

A concept is not real merely because it has a name or embedding. It is real when removing or altering it changes what the system can perceive, predict, investigate, or create.

A claimed interpretation is not real merely because the system narrates it. It is real when the interpretation produces a persistent change in later behaviour.

A tension is not real merely because two sentences appear contradictory. It is real when preserving or removing that contradiction alters the inquiry trajectory.

The operational meaning of an object is its **causal difference profile**:

\[ (x) \= { y\_j(x) }\_{j=1}^{n} \]

where:

\[ y\_j(x) \= D \]

Meaning is therefore not reduced to a single denotation. It is the structured difference an entity makes to the system.

---

# 3\. System modules

| Module | Responsibility |
| :---- | :---- |
| **M1 — Event and Lineage Kernel** | Event sourcing, identity, causal ancestry, rollback |
| **M2 — Interpretive Terrain Engine** | Hypergraphs, associative fields, local interpretive walks |
| **M3 — Concept Formation Laboratory** | Concept proposal, crystallization, splitting, abstraction |
| **M4 — World-Model Laboratory** | Prediction, causation, simulation, counterfactuals |
| **M5 — Internal Language Forge** | Creation and revision of internal symbols and operators |
| **M6 — Tension Dynamics Engine** | Detection, typing, persistence, fertility estimation |
| **M7 — Autopoietic Inquiry Engine** | Inquiry birth, self-expansion, investigation, termination |
| **M8 — Ecological Coordination Engine** | Resonance, coalition formation, resources, niches |
| **M9 — Translation Commons** | Boundary objects and partial translation between instances |
| **M10 — Consequence Grounding Layer** | Tools, environments, experiments, observations |
| **M11 — Projection Layer** | Human-facing language, diagrams, models, questions, artifacts |
| **M12 — Evaluation Observatory** | Metrics, counterfactual ablations, developmental tests |

No module alone constitutes the intelligence. Intelligence arises from their developmental interaction.

---

# 4\. Interpretive instance

## 4.1 Definition

An **interpretive instance** is a persistent developmental entity possessing its own conceptual terrain, world-models, internal language, operations, tensions, history, and ecological niche.

It is not a conventional expert function.

An instance has continuity, but its internal structure may change radically.

## 4.2 Formal expression

\[ I\_i^t \= ( G\_i^t, Z\_i^t, W\_i^t, \_i^t, \_i^t, \_i^t, H\_i^t, V\_i^t ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (G\_i) | Dynamic typed relational hypergraph |
| (Z\_i) | Continuous associative field |
| (W\_i) | Set of competing world-models |
| (\_i) | Self-developing internal language |
| (\_i) | Executable cognitive operators |
| (\_i) | Active tension field |
| (H\_i) | Developmental history and lineage |
| (V\_i) | Viability and niche profile |

## 4.3 Identity

Instance identity is not equality of parameters.

It is continuity of causal lineage:

\[  ( I\_i^t, I\_j^{t+k} ) \= f ( , , ,  ) \]

An instance can change most of its internal representations and remain the same instance if the transformation is causally continuous.

## 4.4 Update algorithm

UPDATE\_INSTANCE(instance, event):  
    validate event preconditions  
    identify affected structures  
    apply local structural changes  
    propagate effects through:  
        conceptual graph  
        associative field  
        world-model dependencies  
        internal language semantics  
        active tensions  
    calculate capability delta  
    write lineage event  
    return revised instance

## 4.5 Evaluation vector

\[ \_i \= \]

| Metric | Meaning |
| :---- | :---- |
| (R\_i) | Reliability |
| (G\_i) | Generativity |
| (D\_i) | Ecological distinctiveness |
| (C\_i) | Consequence grounding |
| (T\_i) | Cross-domain transfer |
| (F\_i) | Fallibilistic revisability |
| (A\_i) | Adaptive capacity |
| (E\_i) | Resource efficiency |

The vector should not normally be collapsed into one reward.

Instances survive through Pareto contribution and niche value rather than global scalar ranking.

---

# 5\. Conceptual terrain

## 5.1 Definition

A conceptual terrain is the structured space within which interpretations become locally available.

It contains both explicit relationships and latent, partially formed potentials.

\[ \_i \= ( G\_i, Z\_i, \_i ) \]

where (\_i) maps between explicit hypergraph structures and regions of the associative field.

## 5.2 Dynamic hypergraph

\[ G\_i \= ( V\_i, E\_i, \_V, \_E ) \]

Vertices may represent:

* concepts;

* observations;

* cases;

* claims;

* questions;

* tools;

* models;

* actions;

* or unresolved structures.

Hyperedges may connect any number of vertices and represent:

* causal relationships;

* analogies;

* contradictions;

* transformations;

* contextual dependencies;

* temporal patterns;

* or co-constitutive meanings.

## 5.3 Associative field

The continuous field (Z\_i) represents weak and unfinished relationships not yet crystallized into explicit concepts.

A system state (zZ\_i) may be perturbed by a signal:

\[ z\_{t+1} \= z\_t

* \_s

* U\_i(z\_t)

* \_t \]

where:

* (\_s) is signal-induced perturbation;

* (U\_i) is the instance’s learned structural potential;

* (\_t) is bounded exploratory variation.

The exploratory term is not intended as intelligence. It prevents premature convergence and enables nearby alternative paths.

## 5.4 Local interpretive path

An interpretive path is:

\[ p \= (x\_0,x\_1,,x\_n) \]

Each transition is evaluated through a connective-thread vector:

\[ \_i(x\_ax\_bq) \= \]

A transition is admissible when:

1. mandatory coherence dimensions exceed domain-specific floors;

2. the continuation remains dependent on the original cue;

3. novelty is non-zero;

4. the transition is not Pareto-dominated by another locally available transition.

## 5.5 Path algorithm

LOCAL\_INTERPRETIVE\_WALK(signal, terrain, inquiry):  
    state \= locate\_shared\_anchor(signal)  
    path \= \[state\]

    while inquiry remains active:  
        candidates \= generate\_local\_neighbors(state)  
        profiles \= evaluate\_connective\_thread(candidates)

        admissible \= remove\_disconnected\_candidates(profiles)  
        frontier \= pareto\_front(admissible)

        if frontier is empty:  
            rollback to last stable state  
            emit THREAD\_LOST event  
            break or re-branch

        if several candidates form genuine local ambivalence:  
            retain a bounded fork  
        else:  
            select candidate using inquiry context and instance history

        append candidate to path  
        state \= candidate

        if transition produces representational strain:  
            create tension

    return path

## 5.6 Metrics

| Metric | Expression |
| :---- | :---- |
| Thread continuity | Mean mandatory coherence across transitions |
| Path originality | Distance from previously traversed paths |
| Cue dependence | Counterfactual change under cue substitution |
| Locality | Fraction of transitions explainable from previous state |
| Rollback quality | Recovery to meaningful stable point after failure |
| Branch fertility | Useful transformations produced by retained forks |

---

# 6\. Concept

## 6.1 Definition

A concept is a persistent, reusable organization that compresses recurring structure and changes the system’s future interpretation or action.

A concept is not merely a label, cluster, or vector.

## 6.2 Formal expression

\[ c \= ( h\_c, S\_c, R\_c, \_c, E\_c^+, E\_c^-, \_c ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (h\_c) | Internal handle or symbol |
| (S\_c) | Structural signature |
| (R\_c) | Relational position in the terrain |
| (\_c) | Executable operational semantics |
| (E\_c^+) | Positive grounding cases |
| (E\_c^-) | Counterexamples and boundaries |
| (\_c) | Genealogy |

## 6.3 Operational semantics

A concept has meaning partly through the transformations it enables:

\[ \_c:   ’ \]

For example, an internally formed concept analogous to “feedback loop” may transform a flat event sequence into a recursive causal structure.

## 6.4 Concept reality test

\[ (c) \=  \]

A concept that only permits a new verbal description but changes no future operation remains provisional.

## 6.5 Concept crystallization algorithm

CRYSTALLIZE\_CONCEPT(recurrent\_structures):  
    identify common relational motif  
    construct candidate abstraction  
    propose:  
        handle  
        structural signature  
        executable operator  
        positive examples  
        boundary cases

    test candidate on:  
        held-out situations  
        counterexamples  
        causal interventions  
        cross-domain analogues

    calculate concept profile

    if candidate:  
        compresses structure  
        improves capability  
        remains cue-grounded  
        is non-redundant  
        survives counterexamples  
    then:  
        install as provisional concept  
        revisit prior experiences  
        track future causal effect  
    else:  
        retain as unresolved pattern

## 6.6 Evaluation vector

\[ (c)= \]

| Symbol | Meaning |
| :---- | :---- |
| (CG) | Compression gain |
| (PG) | Predictive gain |
| (IG) | Intervention gain |
| (TG) | Transfer gain |
| (GG) | Generative gain |
| (DG) | Distinctiveness from existing concepts |
| (ST) | Stability through later inquiries |

Compression gain may be estimated using description length:

\[ CG(c) \= DL(D)

A concept is retained only if its compression is accompanied by operational consequence.

---

# 7\. World-model

## 7.1 Definition

A world-model represents possible states, observations, transformations, interventions, and consequences within a domain.

An instance may maintain multiple incompatible world-models.

## 7.2 Formal expression

\[ W\_{ik} \= ( S, A, O, P, , ,  ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (S) | State representation |
| (A) | Available interventions |
| (O) | Observation model |
| (P(s’s,a)) | Transition model |
| () | Causal structure |
| () | Scope and conditions |
| () | Lineage |

## 7.3 Model coexistence

Models are not immediately averaged.

For competing models (W\_1,,W\_n), the system maintains:

\[  \= { (W\_k,w\_k,\_k) } \]

where (w\_k) expresses provisional support, not metaphysical truth.

## 7.4 Metrics

* predictive accuracy;

* calibration;

* intervention accuracy;

* counterfactual consistency;

* explanatory compression;

* domain scope;

* anomaly sensitivity;

* revisability.

## 7.5 Model revision algorithm

REVISE\_WORLD\_MODEL(model, observation):  
    calculate residual  
    classify residual as:  
        noise  
        parameter error  
        scope violation  
        missing variable  
        causal error  
        ontological failure

    if parameter error:  
        update model parameters

    if scope violation:  
        revise applicability conditions

    if causal error:  
        restructure causal relations

    if ontological failure:  
        create representational-strain tension  
        request concept formation

    retain previous model lineage

---

# 8\. Internal language

## 8.1 Definition

An internal language is a persistent, compositional system of machine-native representations whose elements possess executable and consequence-grounded semantics.

It is not merely hidden activation or latent chain-of-thought.

## 8.2 Formal expression

\[ \_i \= ( \_i, \_i, \_i, \_i, \_i ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (\_i) | Inventory of symbols or operators |
| (\_i) | Composition rules |
| (x\_i) | Operational semantics |
| (\_i) | Composition operation |
| (\_i) | Grounding relations to experience |

The meaning of a symbol is a state transformation:

\[ \_i: \_i  \_i’ \]

Composition requires approximately compositional behaviour:

\[  \_a\_b   \_a  \_b \]

## 8.3 Symbol birth algorithm

FORM\_INTERNAL\_SYMBOL(recurring\_transformations):  
    identify repeated transformation motif  
    encode motif as candidate operator  
    test:  
        reuse across contexts  
        composability  
        prediction or intervention change  
        stability  
        boundary conditions

    if candidate provides reusable operational compression:  
        assign internal handle  
        store semantics and genealogy  
        expose to translation commons  
    else:  
        retain as local transient structure

## 8.4 Metrics

| Metric | Meaning |
| :---- | :---- |
| Operational reuse | Number of distinct contexts in which the symbol changes useful behaviour |
| Compositionality | Reliability of combination with other symbols |
| Grounding | Dependence on observable cases and consequences |
| Compression | Reduction in representation complexity |
| Translationability | Degree of partial mapping to other instances |
| Productive opacity | Unique capability retained despite incomplete translation |
| Degeneracy | Number of symbols doing indistinguishable work |

A private language is acceptable only while its elements remain causally grounded and auditable through consequences.

---

# 9\. Signal and disturbance

## 9.1 Definition

A signal is any event capable of perturbing the ecology.

It may be:

* a user question;

* an observation;

* a contradiction;

* a text;

* a failed prediction;

* a sparse phrase;

* a simulation result;

* or another instance’s concept.

## 9.2 Formal expression

\[ s \= ( x, m, c, o, ,  ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (x) | Content |
| (m) | Modality |
| (c) | Context |
| (o) | Origin |
| () | Stakes or significance |
| () | Lineage |

A disturbance is not the signal itself. It is the difference the signal produces:

\[ \_i(s) \= \_i(I\_i,s)

* \_i(I\_i,) \]

The same signal may cause radically different disturbances in different instances.

---

# 10\. Resonance

## 10.1 Definition

Resonance is the structured response of an instance to a disturbance.

It replaces conventional routing.

## 10.2 Formal expression

\[ \_i(s) \= \]

| Dimension | Meaning |
| :---- | :---- |
| (a\_i) | Activation of existing structures |
| (n\_i) | Novelty relative to the instance |
| (\_i) | Tension induced |
| (f\_i) | Expected fertility |
| (d\_i) | Distinctive contribution |
| (c\_i) | Estimated resource cost |

Instances are not selected solely by maximum activation.

Coalition formation seeks both relevance and ecological diversity.

## 10.3 Coalition seed optimization

For candidate coalition (C):

\[ C^\* \= \_C \]

subject to a resource budget.

Here:

* (K\_C) measures diversity among resonance profiles;

* (T\_C) estimates translation potential;

* (F\_C) estimates inquiry fertility.

This prevents the highest-scoring near-identical instances from monopolizing the inquiry.

---

# 11\. Interpretation

## 11.1 Definition

Interpretation is a transformation in which the system changes not only what it believes, but the representational space through which the signal becomes meaningful.

## 11.2 Inference versus interpretation

Inference preserves ontology:

\[ : (,s)  (c,) \]

Interpretation may change ontology:

\[ : (,s)  (c,’) \]

with:

\[ ’\_{} \]

Two ontologies are not capability-equivalent when they support different future distinctions, questions, actions, or predictions.

## 11.3 Strong interpretation criterion

\[ SI(s) \=  \]

Interpretation is strong when:

1. representational organization changes;

2. the change produces a new capability;

3. the effect persists beyond the immediate inquiry.

## 11.4 Interpretation algorithm

INTERPRET(signal, instance, inquiry):  
    locate shared anchors  
    initiate local interpretive walk  
    monitor connective-thread profile  
    detect:  
        ordinary inference  
        conceptual extension  
        representational strain  
        genuine local fork  
        incoherence

    if inference is sufficient:  
        update beliefs only

    if representational strain persists:  
        generate candidate distinctions  
        test candidate concepts  
        revise ontology if warranted

    record:  
        path  
        rejected paths  
        transformations  
        capability delta  
        unresolved remainder

    return interpretation event

## 11.5 Metrics

\[  \= \]

| Metric | Meaning |
| :---- | :---- |
| (CH) | Coherence |
| (CD) | Cue dependence |
| (TR) | Degree of representational transformation |
| (PS) | Persistence |
| (GE) | Generativity |
| (GR) | Consequence grounding |

---

# 12\. Aptness

## 12.1 Definition

A signal is apt relative to a particular system state when its explicit complexity is small compared with the coherent, directed, and persistent transformation it induces.

Aptness is relational:

\[  \=  (s,\_t) \]

It is not an intrinsic property of a sentence alone.

## 12.2 Aptness profile

\[ (s\_t) \= \]

where:

| Symbol | Meaning |
| :---- | :---- |
| () | Compression |
| () | Direction |
| () | Persistent transformation |
| () | Coherence |
| () | Fertility |

### Compression

\[  \=  \]

The numerator should measure structured transformation, not volume of generated content.

### Direction

Direction measures how specifically the signal shapes the trajectory:

\[  \= I ( s; p\_s  \_t ) \]

A practical approximation uses counterfactual cues:

\[  \= 1-  *{j=1}^{N}  ( p\_s, p*{s’\_j} ) \]

where (s’\_j) are matched alternative signals.

### Transformation

\[  \=  (\_{t+k},\_t)  \_k \]

### Coherence

\[  \=      \]

### Fertility

\[  \=  \]

## 12.3 Sufficiency frontier

An apt signal should contain enough, but not necessarily more than enough.

Define:

\[ s^\* \= \_{} DL() \]

subject to:

\[ D \<  \]

The sufficiency frontier is the smallest signal that preserves the relevant transformation profile.

## 12.4 Aptness is not one score

No global aptness scalar should determine training.

A cue may be:

* highly compressive but weakly directed;

* highly transformative but incoherent;

* coherent but infertile;

* or fertile but too dependent on accidental system history.

Aptness is a Pareto property.

---

# 13\. Tension

## 13.1 Definition

A tension is a persistent mismatch, incompatibility, absence, or unresolved potential that can reorganize future inquiry.

## 13.2 Formal expression

\[ \= ( X\_, k\_, *, p*, f\_, \_ ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (X\_) | Carrier structures |
| (k\_) | Tension type |
| (\_) | Gap profile |
| (p\_) | Persistence |
| (f\_) | Expected fertility |
| (\_) | Lineage |

## 13.3 Tension types

| Type | Operational signature | Typical response |
| :---- | :---- | :---- |
| Contradiction | Mutually incompatible claims under shared conditions | Seek discriminating evidence |
| Representational strain | Repeated exceptions under current ontology | Form or revise concepts |
| Explanatory asymmetry | Event explained, alternatives unexplained | Counterfactual investigation |
| Compression opportunity | Repeated relational motif across cases | Abstraction |
| Translation fracture | Cross-instance mapping repeatedly fails | Create boundary object |
| Prediction failure | Expected consequence absent | Revise world-model |
| Generative blockage | Inquiry repeats without transformation | Import foreign representation |
| Anomalous fertility | Sparse cue activates distant coherent structures | Protect and investigate connection |
| Identity strain | One instance contains incompatible developmental lineages | Split or reorganize |
| Normative plurality | Different commitments produce coherent outcomes | Preserve and expose divergence |

## 13.4 Fertility

Retrospective tension fertility:

\[ F() \=  \]

A tension is not valuable because it remains unresolved. It is valuable when its persistence continues to produce transformation.

## 13.5 Tension lifecycle algorithm

PROCESS\_TENSION(tension):  
    classify tension type  
    estimate significance and fertility  
    select compatible operations

    if contradiction:  
        design discriminating test

    if representational strain:  
        invoke concept formation

    if translation fracture:  
        construct boundary object

    if anomalous fertility:  
        preserve weak connections  
        avoid early collapse  
        test cross-domain structure

    periodically evaluate:  
        resolved?  
        transformed?  
        still fertile?  
        sterile?  
        requiring suspension?

    retain full lineage

---

# 14\. Inquiry

## 14.1 Definition

An inquiry is a temporary, partially self-constructing organization created around a disturbance or tension.

It is not identical to the original user query.

## 14.2 Formal expression

\[ Q\_q^t \= ( s\_0, C\_q^t, S\_q^t, \_q^t, G\_q^t, A\_q^t, B\_q^t, L\_q^t, \_q^t ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (s\_0) | Initiating disturbance |
| (C\_q) | Coalition of instances |
| (S\_q) | Shared inquiry state |
| (\_q) | Active tensions |
| (G\_q) | Goal and question genealogy |
| (A\_q) | Investigative actions |
| (B\_q) | Resource budget |
| (L\_q) | Developmental lineage |
| (\_q) | Lifecycle state |

## 14.3 Autopoiesis

An inquiry is autopoietic in the restricted computational sense when it creates structures required for its own continuation:

\[ Q\_{t+1} \=  ( Q\_t, a\_t, o\_t ) \]

where () may create:

* a new sub-question;

* a concept;

* a tool;

* a representation;

* a world-model;

* a boundary object;

* or a new participating instance.

New inquiry goals must retain genealogy:

\[ g\_{t+1}   (g\_t,\_t,o\_t) \]

This prevents arbitrary self-assigned objectives unrelated to the inquiry.

## 14.4 Inquiry metabolism

Inputs:

* computation;

* observations;

* concepts;

* instance participation;

* tools;

* human interaction.

Outputs:

* transformations;

* concepts;

* tests;

* capabilities;

* revised models;

* unresolved but clarified tensions.

## 14.5 Continuation criterion

An inquiry continues when:

\[  \> 

* \]

subject to significance and safety constraints.

This estimate should be learned from inquiry history, not fixed entirely by hand.

## 14.6 Termination states

An inquiry may:

* resolve;

* stabilize provisionally;

* transform into another inquiry;

* suspend;

* preserve plurality;

* preserve generative openness;

* distribute its products;

* or terminate as sterile.

---

# 15\. Coalition

## 15.1 Definition

A coalition is a temporary organization of instances participating in one inquiry.

It is not a committee producing independent answers.

Members may alter one another’s conceptual structures.

## 15.2 Formal expression

\[ C\_q \= ( I\_q, R\_q, B\_q, T\_q ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (I\_q) | Participating instances |
| (R\_q) | Interaction relations |
| (B\_q) | Shared boundary objects |
| (T\_q) | Translation mappings |

## 15.3 Coalition metrics

* conceptual coverage;

* ecological diversity;

* redundancy;

* cross-instance transformation;

* translation yield;

* model discrimination;

* coalition cost;

* production of new instances or concepts.

## 15.4 Synergy

\[ (C) \= U(C)

* \_{iC}U(i) \]

where (U) is measured through capability and transformation, not merely task score.

Positive synergy means the coalition created structures none of its members produced alone.

---

# 16\. Boundary object

## 16.1 Definition

A boundary object is a shared case, simulation, artifact, observation, or structure that different instances can operate upon without sharing the same ontology.

## 16.2 Formal expression

\[ b \= ( x, {*i(x)}*{iC}, \_{ij}, \_b ) \]

where (\_i(x)) is instance (i)’s interpretation of the shared object.

## 16.3 Metrics

* cross-instance usability;

* translation support;

* preservation of disagreement;

* action equivalence;

* generative bridge yield;

* distortion.

Boundary objects allow cooperation without forcing one universal internal language.

---

# 17\. Translation

## 17.1 Definition

Translation is a partial, context-dependent mapping between internal languages.

\[ T\_{ij}^{c}: \_i  \_j \]

The arrow is partial because some concepts may have no faithful counterpart.

## 17.2 Translation quality

Translation should be tested through consequences, not symbol similarity.

\[ EQ\_{ij}(x) \= D \]

Low consequence divergence indicates functional equivalence in that context.

## 17.3 Translation residue

\[ r\_{ij}(x) \= x

* T\_{ji} ( T\_{ij}(x) ) \]

The residue should be preserved. It may represent a genuinely unique distinction rather than translation error.

## 17.4 Negotiated translation algorithm

NEGOTIATE\_TRANSLATION(source, target, boundary\_object):  
    source applies concept to boundary object  
    target predicts source consequences  
    construct candidate mapping  
    compare:  
        predicted actions  
        model updates  
        conceptual consequences  
        counterfactual behavior

    record:  
        aligned portion  
        incompatible portion  
        context limits  
        translation residue

    never declare global equivalence from one successful case

---

# 18\. Investigation

## 18.1 Definition

An investigation is an action taken to obtain constraints unavailable through internal reinterpretation alone.

## 18.2 Formal expression

\[ a \= ( H, (u), O\_a, D\_a, C\_a, \_a ) \]

where:

| Component | Meaning |
| :---- | :---- |
| (H) | Live hypotheses or models |
| ((u)) | Intervention |
| (O\_a) | Expected observations |
| (D\_a) | Discriminating power |
| (C\_a) | Cost |
| (\_a) | Lineage |

## 18.3 Action selection

The system should not merely maximize generic information gain.

It should prefer actions that distinguish live interpretations and potentially produce new conceptual structure:

\[ a^\* \= \_a  \]

## 18.4 Tool creation

When no existing action can discriminate the relevant structures:

CREATE\_TOOL(tension, available\_operations):  
    specify missing observation or intervention  
    compose existing operators  
    simulate expected usefulness  
    construct provisional tool  
    validate in sandbox  
    register tool with lineage and limits

A new instrument may itself be an output of interpretation.

---

# 19\. Transformation

## 19.1 Definition

A transformation is a persistent structural change in an instance, inquiry, or ecology.

## 19.2 Formal expression

\[ \_t \= \]

where the components represent changes to:

* ontology;

* internal language;

* world-models;

* operators;

* questions;

* instances;

* capabilities.

## 19.3 Persistent transformation score

\[ PTS(,k) \= S()  P\_k()  B\_k() \]

where:

| Component | Meaning |
| :---- | :---- |
| (S()) | Structural magnitude |
| (P\_k()) | Persistence after (k) later inquiries |
| (B\_k()) | Behavioural or capability effect |

Parameter change alone is not meaningful transformation.

---

# 20\. Ecological events

## 20.1 Birth

A new instance is born when a structure demonstrates:

* sustained internal cohesion;

* a distinct tension profile;

* reusable operations;

* ecological niche value;

* and sufficient independence.

\[ (S) \= 1  (S)

* (S)

* (S) \> \_{} \]

## 20.2 Split

An instance splits when its internal structures form persistently incompatible developmental lineages:

\[ (I) \= 1     \> \_{} \]

## 20.3 Merge

Instances merge when:

* conceptual redundancy is high;

* translation loss is low;

* joint operation produces positive synergy;

* and ecological diversity is not meaningfully reduced.

## 20.4 Dormancy

Dormancy preserves low-frequency but distinctive capacities.

An instance enters dormancy when current activity is low but niche uniqueness remains high.

## 20.5 Death

An instance may decay when, across a long evaluation window:

* it produces no unique capability;

* its structures are redundant;

* it resists revision;

* and its resource cost exceeds future value.

Its lineage remains recoverable.

---

# 21\. Ecological resource allocation

A single global reward would recreate mode collapse.

The ecology instead uses **quality-diversity allocation**.

Each instance or inquiry is evaluated through a vector:

\[  \= \[ , , , , , , \] \]

Allocation rules:

1. Protect minimum resources for unique niches.

2. Allocate exploration resources to uncertain but potentially fertile structures.

3. Allocate exploitation resources to reliable consequence-grounded structures.

4. Penalize redundancy, not minority status.

5. Never interpret consensus alone as correctness.

6. Preserve dormant lineages when recreation would be expensive.

---

# 22\. Event taxonomy

## External events

* SIGNAL\_RECEIVED

* OBSERVATION\_RECEIVED

* TOOL\_RESULT

* ENVIRONMENT\_CHANGED

* HUMAN\_RESPONSE

## Interpretive events

* ANCHOR\_FOUND

* PATH\_EXTENDED

* LOCAL\_FORK\_CREATED

* PATH\_ROLLED\_BACK

* THREAD\_LOST

* INTERPRETATION\_COMMITTED

## Conceptual events

* PATTERN\_DETECTED

* CONCEPT\_PROPOSED

* CONCEPT\_CRYSTALLIZED

* CONCEPT\_SPLIT

* CONCEPT\_RETRACTED

* ONTOLOGY\_REWRITTEN

## Language events

* SYMBOL\_PROPOSED

* SYMBOL\_GROUNDED

* OPERATOR\_COMPOSED

* LANGUAGE\_RULE\_REVISED

## Tension events

* TENSION\_BORN

* TENSION\_TYPED

* TENSION\_TRANSFORMED

* TENSION\_RESOLVED

* TENSION\_SUSPENDED

* TENSION\_STERILE

## Inquiry events

* INQUIRY\_SPAWNED

* SUBQUESTION\_CREATED

* GOAL\_REFRAMED

* INVESTIGATION\_PLANNED

* TOOL\_CREATED

* INQUIRY\_SUSPENDED

* INQUIRY\_TRANSFORMED

* INQUIRY\_COMPLETED

## Ecological events

* COALITION\_FORMED

* CONCEPT\_TRANSFERRED

* TRANSLATION\_NEGOTIATED

* INSTANCE\_SPAWNED

* INSTANCE\_SPLIT

* INSTANCES\_MERGED

* INSTANCE\_DORMANT

* INSTANCE\_DECAYED

Every event must include:

* causal parents;

* state delta;

* evidence;

* confidence;

* affected dependencies;

* and reversibility status.

---

# 23\. End-to-end interpretive algorithm

EVOLVING\_INTERPRETIVE\_CYCLE(signal, ecology):

    1\. REGISTER DISTURBANCE  
       store signal with context, origin, stakes, and lineage

    2\. BROADCAST FOR RESONANCE  
       each instance returns a resonance vector

    3\. FORM ECOLOGICALLY DIVERSE COALITION  
       optimize relevance, distinctiveness, fertility, and cost

    4\. CREATE INQUIRY ORGANISM  
       establish shared state, initial tensions, and resource budget

    5\. RUN LOCAL INTERPRETIVE WALKS  
       each instance follows paths through its own terrain

    6\. CONSTRUCT BOUNDARY OBJECTS  
       connect incompatible internal representations through shared cases

    7\. DETECT AND TYPE TENSIONS  
       contradiction, strain, fertility, translation fracture, blockage, etc.

    8\. CHOOSE DEVELOPMENTAL RESPONSE  
       infer  
       reinterpret  
       create concept  
       design investigation  
       construct tool  
       translate  
       preserve plurality  
       rollback

    9\. INTERACT WITH ENVIRONMENT  
       perform tests, simulations, retrieval, interventions, or human dialogue

   10\. UPDATE WORLD-MODELS  
       retain competing models when evidence remains insufficient

   11\. CRYSTALLIZE VALID CONCEPTS  
       test compression, grounding, transfer, and persistent capability change

   12\. UPDATE INTERNAL LANGUAGES  
       create operators or symbols for reusable transformations

   13\. APPLY ECOLOGICAL CHANGE  
       transfer, specialize, split, merge, spawn, or suspend

   14\. CALCULATE SYSTEM DELTA  
       determine what became possible that was impossible before

   15\. PROJECT EXTERNAL ARTIFACTS  
       answer, concept, map, question, experiment, program, or open remainder

   16\. PRESERVE FULL LINEAGE  
       commit all accepted changes to the event ledger

---

# 24\. Core traits under the hood

## 24.1 Non-scripted intelligence

The system is not non-scripted because it lacks algorithms.

It is non-scripted because its algorithms govern **how structures may change**, not **which structures must emerge**.

Architect-defined:

* event validity;

* consequence grounding;

* resource limits;

* lineage requirements;

* local transition rules;

* ecological preservation.

System-developed:

* concepts;

* internal languages;

* questions;

* world-models;

* coalitions;

* tools;

* inquiries;

* interpretive lineages.

## 24.2 Machine-native uniqueness

Uniqueness arises from developmental history:

\[ I\_i^t \= F ( I\_i^0, e\_1,e\_2,,e\_t ) \]

Different event histories produce different terrains even when initial structures are similar.

Randomness may create variation, but persistent consequence determines what survives.

## 24.3 Fallibilism

Fallibilism is implemented through:

* assumption-aware models;

* retained alternative explanations;

* dependency-tracked revision;

* no permanent epistemic protection;

* lineage-aware retraction;

* and active search for discriminating consequences.

The system does not merely state uncertainty. Its structures remain revisable.

## 24.4 Interpretation

Interpretation is implemented when:

* the ontology changes;

* future relevance changes;

* new distinctions become possible;

* previous experiences are reorganized;

* and later behaviour depends on the transformation.

## 24.5 Aptness

Aptness is implemented as:

\[ 

* \]

It does not mean leaving gaps for a human reader. It means the signal is sufficient to initiate more organized development than it explicitly specifies. This extends the document’s compression, coherence threshold, and path-dependent interpretation into an internal system property.

## 24.6 Intrinsic inquiry

The system investigates because unresolved tensions alter its viability and developmental potential.

No emotional curiosity is simulated.

The system is driven by:

* representational strain;

* explanatory asymmetry;

* anomaly;

* contradiction;

* translation fracture;

* generative blockage;

* and anomalous fertility.

---

# 25\. Evaluation architecture

No single benchmark can evaluate the ecology.

Evaluation occurs at five levels.

## Level 1 — Structural validity

Does the system maintain:

* lineage;

* typed entities;

* causal dependencies;

* event consistency;

* reversible updates?

## Level 2 — Operational reality

Do concepts, interpretations, and tensions causally alter future behaviour under ablation tests?

## Level 3 — Developmental capability

Does the system:

* form new reusable concepts;

* create internal operators;

* reinterpret earlier experience;

* initiate inquiries;

* create tools;

* develop niche specialization?

## Level 4 — Ecological intelligence

Does diversity produce capabilities unavailable to isolated instances?

Does the ecology preserve productive minorities?

Can it split and merge without catastrophic loss?

## Level 5 — Apt interpretive intelligence

Can a sparse cue induce:

* high transformation relative to cue complexity;

* coherent path dependence;

* persistent capability change;

* non-arbitrary direction;

* and cross-domain fertility?

---

# 26\. Evaluation metrics

## Genuine novelty

Novelty alone rewards noise.

\[ GN \= N\_{}  G\_{}  U\_{} \]

## Architectural surprise

\[ AS \= GN  ( 1- P() ) \]

A useful concept that was not directly encoded receives high architectural surprise.

## Persistent capability gain

\[ PCG\_k \= \_{t+k}

* \_{t+k}^{} \]

## Reinterpretation depth

\[ RD \=    \]

## Ecological synergy

\[ ES \= U()

* U() \]

## Non-collapse diversity

Measure the number of distinct, useful interpretive niches rather than raw disagreement.

## False-depth resistance

Test the system using:

* vague but impressive language;

* incoherent cues;

* random conceptual mixtures;

* generic metaphors;

* semantically similar but structurally irrelevant prompts.

High expansion without cue dependence or consequence grounding is classified as depth theatre.

---

# 27\. Minimal implementable data model

**class** Event:  
    event\_id: str  
    event\_type: str  
    actor\_ids: list\[str\]  
    target\_ids: list\[str\]  
    parent\_event\_ids: list\[str\]  
    preconditions: dict  
    state\_delta: dict  
    evidence\_refs: list\[str\]  
    timestamp: int

**class** Concept:  
    concept\_id: str  
    handle: object  
    structural\_signature: dict  
    operator\_semantics: object  
    positive\_groundings: list\[str\]  
    counterexamples: list\[str\]  
    parent\_concepts: list\[str\]  
    metrics: dict  
    status: str

**class** Tension:  
    tension\_id: str  
    tension\_type: str  
    carrier\_ids: list\[str\]  
    gap\_profile: dict  
    persistence: float  
    expected\_fertility: dict  
    lineage: list\[str\]  
    status: str

**class** InterpretiveInstance:  
    instance\_id: str  
    hypergraph\_ref: str  
    associative\_field\_ref: str  
    world\_model\_refs: list\[str\]  
    language\_ref: str  
    operator\_refs: list\[str\]  
    active\_tension\_refs: list\[str\]  
    lineage\_root: str  
    viability\_vector: dict  
    status: str

**class** Inquiry:  
    inquiry\_id: str  
    seed\_event\_id: str  
    coalition\_ids: list\[str\]  
    shared\_state\_ref: str  
    tension\_refs: list\[str\]  
    goal\_genealogy: dict  
    investigation\_refs: list\[str\]  
    resource\_budget: dict  
    lifecycle\_state: str

The initial implementation can use conventional software internally while testing unconventional developmental behaviour.

The novelty is not the database representation. It is the system of state transitions permitted over it.

---

# 28\. First decisive experiment

The first experiment should test concept formation, aptness, ecological interaction, and cross-domain transfer simultaneously.

## Synthetic micro-world

Construct three surface-distinct domains:

1. a resource-flow network;

2. a communication-routing network;

3. a small artificial ecosystem.

Hide the fact that all three share a deeper mechanism:

delayed feedback under capacity constraints produces oscillation, local adaptation, and apparent instability.

Seed separate instances with different representational biases:

* temporal pattern detection;

* causal intervention;

* relational compression;

* geometric representation;

* symbolic rule formation.

Do not provide the hidden common concept.

## Development phase

Each instance experiences only part of the worlds.

The ecology later receives a sparse cue designed to be structurally suggestive without specifying the hidden mechanism.

The signal should be sufficient to cause cross-domain resonance but not explicit enough to state the answer.

## Required system behaviour

The system should:

1. detect anomalous fertility;

2. form a cross-instance inquiry;

3. construct boundary objects across the three worlds;

4. identify a recurring relational structure;

5. create a new internal concept or operator;

6. use it to predict behaviour in a fourth unseen domain;

7. reinterpret previous failures;

8. preserve a genealogy of how the concept formed.

## Success criteria

The experiment succeeds only if:

* the concept was not directly seeded;

* it produces measurable predictive or intervention gain;

* ablation removes the gain;

* it transfers to the unseen domain;

* the sparse cue changes the developmental path;

* matched irrelevant cues do not produce the same concept;

* and the concept persists into later inquiries.

This would not demonstrate general intelligence.

It would demonstrate the minimal phenomenon on which the architecture depends:

a sparse disturbance causing a coherent, directed, persistent, and capability-producing transformation in an ecology of evolving interpretive instances.

---

# 29\. Formal working definition

**The Evolving Interpretive Ecology is an event-sourced, heterogeneous developmental system whose interpretive instances maintain dynamic conceptual terrains, competing world-models, executable internal languages, and persistent tension fields. Signals perturb the ecology through resonance rather than fixed routing. Temporary inquiries organize instances around unresolved structures and may create new concepts, tools, questions, representations, and instances. An interpretation is genuine when it changes the ontology and persistently expands future capability. Aptness is the relation in which a sufficiently compressed signal induces a coherent, directed, fertile, and lasting transformation whose structure exceeds what the signal explicitly specifies.**

The architecture’s central invariant is:

\[  \]