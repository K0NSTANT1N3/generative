# Constraint-Aware Generative Design of Mechanical Metamaterials

> **Research proposal · Generative Models final project · Status: scoping / feasibility not yet verified**
>
> Inspired by **DiffuMeta** (Zheng, Kumar & Kochmann, *Nature Machine Intelligence*, 2026). This repository is an **independent proposed undergraduate research project**, not the authors' original implementation and not a claim that the proposed experiments have been completed.

## Overview

Mechanical metamaterials are engineered structures whose stiffness, deformation, and energy absorption depend strongly on the **geometry of their internal architecture**. Different 3D shell or lattice structures can exhibit very different mechanical behavior even when manufactured from the same base material.

The **inverse-design problem** is to start from a desired mechanical response and generate *multiple distinct geometries* expected to achieve it:

**Target mechanical properties → generative model → candidate 3D structures → geometric and mechanical evaluation**

This project investigates a focused methodological question:

> **Can enforcing geometric constraints during generation produce more valid and diverse mechanical metamaterial geometries than unconstrained generation followed by rejection or repair, without degrading predicted mechanical performance?**

The central contribution would be a **controlled comparison of algorithms**, not a new large-scale foundation model.

## Why this is an interesting research problem

A generator may produce a mathematically expressible surface that is still unsuitable as a metamaterial: it might be disconnected, have tiny isolated parts, possess unwanted topological defects, or violate minimum-feature-size constraints. The obvious solutions—discard invalid samples or repair them afterward—have costs. Rejection wastes sampling effort; repair can alter the geometry and therefore its mechanical properties.

We want to measure the trade-off between:

- **Geometric validity:** Can the sample be converted to a coherent manufacturable-style structure?
- **Conditional accuracy:** Does its predicted stiffness or stress–strain response match the target?
- **Diversity and novelty:** Can the model discover distinct solutions rather than repeat known designs?
- **Efficiency:** How many model samples, seconds, and GPU-hours are needed to obtain useful candidates?

## Relation to DiffuMeta

**DiffuMeta**, developed by researchers at **ETH Zürich and TU Delft**, generates **token sequences encoding algebraic equations** for implicit 3D shell geometries. It conditions generation on desired mechanical responses and demonstrates inverse design, including physical testing of selected fabricated structures.

Its published dataset contains **23,534 unique simulated shell designs** paired with finite-element-derived mechanical responses. The **official ETH Zürich download** for the training data is approximately **25.9 MB** and is listed under **CC BY 4.0**. The authors' code repository is **MIT-licensed**.

DiffuMeta is **prior work and a potential reference baseline**. Our proposed project differs in its interest in **direct geometric representations** (rather than only equation-token outputs), explicit validity constraints, and a matched comparison of constrained vs. unconstrained sampling.

**Important:** It is not yet established that the released symbolic records can be converted into a convenient geometry-native training representation at the required fidelity and runtime. That conversion is the first feasibility milestone.

Sources:

- [DiffuMeta paper — *Nature Machine Intelligence* (2026)](https://doi.org/10.1038/s42256-026-01218-8)
- [Authors' DiffuMeta code and validity checker](https://github.com/li-zhengz/DiffusionMetamaterials)
- [ETH Zürich training dataset and checkpoints](https://www.research-collection.ethz.ch/items/a6cadc6b-a3a6-48f9-b223-88d414524923)

## Formal problem statement

Let:

- \(y\) be a target mechanical response, such as a stiffness value or a sampled stress–strain curve.
- \(G\) be a 3D geometric object, represented as a **surface mesh** (vertices, faces, and connectivity) or another **explicit non-token geometric structure**.
- \(C_i(G)\in\{0,1\}\) be tests for geometric constraints, e.g., connectedness and nondegeneracy.
- \(\hat f(G)\) be an available **mechanical surrogate** or inexpensive physics-based evaluation, not a replacement for physical measurement.

Learn a conditional generator \(p_\theta(G\mid y)\) that produces **diverse** geometries satisfying

\[
C_i(G)=1\quad\text{for relevant }i, \qquad d(\hat f(G),y)\text{ is small}.
\]

The main experiment compares the **number of distinct valid, target-matching geometries** produced under a fixed training and sampling budget.

### Proposed hypotheses

1. **H1 — validity:** Constraint-aware generation increases the proportion of geometrically valid samples over unconstrained generation.
2. **H2 — sample efficiency:** It generates more distinct valid candidates per fixed sampling budget than rejection-only generation.
3. **H3 — trade-off:** Stronger geometric constraints may reduce diversity or disturb target-property matching; the effect should be measured rather than assumed.

## Data

### Primary: DiffuMeta (geometry + simulated responses)

| Property | Verified information |
|---|---|
| Research source | ETH Zürich / TU Delft, 2026 |
| Samples | 23,534 unique shell topologies in the published study |
| Download | 25.9 MB ZIP listed by ETH Zürich |
| Source representation | Tokenized algebraic descriptions of implicit 3D surfaces |
| Property labels | Finite-element simulation results, including mechanical response data |
| Dataset license | CC BY 4.0, as displayed by ETH Zürich |
| Original code license | MIT, as displayed in the authors' GitHub repository |

**Do not call these 23,534 labels physical experiments.** They are primarily simulation-generated labels. Only selected designs in the research were physically fabricated and evaluated.

### Optional, separate physical-data audit

The [University of Bath experimental auxetic structures dataset](https://researchdata.bath.ac.uk/1525/) contains measured responses from **19 physically tested structures**, alongside FE outputs and model files, under **CC BY 4.0**. Its configurations are **not equivalent to the DiffuMeta shell dataset**. It may be useful to demonstrate simulation-to-experiment limitations, but **must not be merged as if both datasets measured the same design family**.

## Proposed methodology

### Step 0 — Dataset/geometry smoke test

1. Download a small subset of the official data and inspect its schema and license.
2. Decode representative equation-token sequences using the authors' utilities.
3. Generate or reconstruct their corresponding geometries.
4. Decide whether a **mesh / geometric graph** representation is reliable and sufficiently compact.
5. Time generation, conversion, rendering, and validity checks on at least 100 structures.

**Go/no-go criterion:** If reliable geometry extraction is prohibitively expensive or loses essential topology, reformulate the representation before training a model.

### Baseline A — Unconstrained geometry-native generation

Train a small conditional generative model (e.g., a compact graph VAE, or a deliberately restricted geometry generator) that produces a non-token geometric object. The precise architecture must follow the geometry representation and the Colab memory test, not be chosen in advance for novelty.

### Baseline B — Generate, then reject or repair

Use **the same generator and training split** as Baseline A. Reject samples failing the geometric checker, or apply an explicitly documented repair operation. Record how much each repair changes the geometry and its predicted mechanics.

### Proposed method — Constraint-aware generation

Enforce selected geometric constraints **inside** the generative process. Candidate techniques include validity-aware action masks for a graph generator, a differentiable geometric penalty, or a projection operation on intermediate geometric states.

To avoid a trivial comparison, keep model capacity, training budget, data splits, and raw sample budget matched wherever possible.

### Scope restriction

The first version should use a **small, coherent family of geometries** and a limited set of target properties. Full nonlinear finite-element analysis for every generated design is **out of scope initially**. Use the original provided evaluation code when compatible and clearly identify learned-surrogate results as predictions.

## Evaluation protocol

| Metric | Interpretation |
|---|---|
| **Validity rate** | Fraction passing all declared geometric constraints |
| **Distinct valid yield** | Number of unique valid geometries per 100 or 1,000 raw samples |
| **Target-property error** | Distance between target and *predicted/simulated* mechanical response |
| **Diversity** | Pairwise distance among valid generated geometries, using a declared structural metric |
| **Novelty / memorization** | Exact and near-duplicate comparisons against the training split, accounting for geometry normalization and symmetries |
| **Repair distortion** | Geometric and predicted-property change caused by post-hoc repair |
| **Runtime / compute** | Time per sample, checker time per sample, peak VRAM, total GPU-hours |

### Memorization protocol

- Normalize geometries for translation, scale, and permitted symmetry transformations.
- Hash canonical graph connectivity where available.
- Use mesh/shape distances (e.g., symmetric Chamfer distance on sampled surfaces) for near-neighbor screening; do not confuse approximate geometric similarity with proof of exact equivalence.
- Report exact-duplicate and nearest-training-neighbor statistics separately.
- Keep a held-out evaluation split and prevent equivalent designs from leaking across splits when possible.

### Ablations

1. Constraint-aware generation **vs.** rejection **vs.** post-hoc repair.
2. Weak **vs.** strong constraint penalties or masks.
3. Optional: 25% **vs.** 50% **vs.** 100% training data.
4. Optional: several geometry representation granularities.

Report conditional-property results only for structures on which the property evaluator is valid and available.

## Eight-condition qualification checklist

The course guide requires every criterion to pass. This is the **current screening status**, not a completed qualification.

| # | Required gate | Current assessment |
|---|---|---|
| 1 | Genuinely non-grid, non-token structured output | **Conditional:** Proposed mesh/graph generator would qualify; simply reusing DiffuMeta's token-sequence output may not. |
| 2 | Real-world ground-truth scarcity / 100× compute invariance | **Conditional:** Physical compression behavior requires fabrication and measurement, but the main available training labels are simulated. Must justify the link to genuinely scarce measurements. |
| 3 | Natural inverse/conditional/multi-valid formulation | **Strong:** Many geometries can have similar mechanical responses. |
| 4 | Free, fast validity checker / solver / surrogate | **Partially verified:** DiffuMeta publishes a validity checker; execution time and coverage remain to be measured. |
| 5 | At least two open methodological levers | **Proposed:** Constraint integration and validity–diversity/performance trade-offs. Literature novelty requires further audit. |
| 6 | Immediate data access and acceptable license | **Verified for primary dataset:** ETH Zürich lists public download and CC BY 4.0. |
| 7 | Free-tier Colab/Kaggle feasibility | **Unverified:** Must run a 50-step / one-epoch micro-batch and measure VRAM and wall time. |
| 8 | Checkable memorization | **Designed, not implemented:** Geometry equivalence and nearest-neighbor audit above. |

**Do not describe the project as passing all eight gates until the unresolved items are verified.**

## Reproducibility and compute plan

The course requires a setup script or notebook cell that installs dependencies and loads a subset quickly, benchmarks the checker on **100+ samples**, and records a **50-step / one-epoch training micro-batch**, VRAM, epoch time, and total GPU-hour budget. These are **planned experiments**, not completed benchmarks.

For reference, the **original** DiffuMeta repository documents:

```bash
# This clones the authors' project, not this proposed project.
git clone https://github.com/li-zhengz/DiffusionMetamaterials.git
cd DiffusionMetamaterials
pip install -r requirements.txt

# Download and place the dataset/checkpoint as directed by its README.
# Then consult the original README and config.yaml before attempting:
# python sample.py
# python dataGeneration/validity_check.py
```

Dependency compatibility and GPU availability vary by environment. No one-command setup for **our proposed method** is provided yet because that implementation does not exist.

## Proposed repository layout (not implemented)

```text
.
├── README.md
├── configs/                   # planned experiment configurations
├── data/                      # external data, excluded from version control
├── notebooks/                 # data inspection and Colab smoke tests
├── src/
│   ├── geometry/              # decoding and geometric representation
│   ├── models/                # baseline and constrained generators
│   ├── constraints/           # validity checking and repair
│   └── evaluation/            # metrics and memorization audit
├── experiments/               # training and ablation entry points
└── reports/                   # figures and W&B report links
```

## Four-week implementation outline (course Phase 2)

| Week | Planned milestone | Evidence to save |
|---|---|---|
| 16 | Reproducible setup, data conversion, W&B artifacts | Data schema, licenses, sample visualizations, benchmark log |
| 17 | Train a compact geometry-native baseline | Loss curves, checkpoint, VRAM and runtime |
| 18 | Implement constraints, checker and memorization audit | Validity table, novelty examples, 100+ sample timings |
| 19 | Compare rejection/repair/constraint-aware variants | Ablation plots, public W&B report, representative 3D structures |

## Risks and limitations

- **Guide fit:** DiffuMeta itself generates equation-token sequences. We must generate genuinely structured geometry if we want to make a strong claim under criterion 1.
- **Measurement scarcity:** Simulated FE responses cannot be presented as physical ground truth. Physical-test scarcity is a legitimate motivation, but our proposed claims must not exceed the evidence.
- **Representation mismatch:** A geometry-native baseline may be harder to train than the original compact symbolic model.
- **Mechanical validation:** Geometric checks do not prove target stiffness, successful 3D printing, or real-world reliability.
- **Repair effects:** Repair may modify important structural features and change predicted mechanical properties.
- **Compute uncertainty:** The official full training schedule should not be assumed to fit free Colab GPU quotas.
- **Prior work:** Geometric constraints and post-hoc filtering are not novel in general; novelty must come from a precise, fairly evaluated method or analysis.

## References and attribution

1. **Zheng, L., Kumar, S., & Kochmann, D. M. (2026).** *Algebraic language models for inverse design of metamaterials via diffusion transformers.* Nature Machine Intelligence. https://doi.org/10.1038/s42256-026-01218-8
2. **Official DiffuMeta code (MIT):** https://github.com/li-zhengz/DiffusionMetamaterials
3. **Official DiffuMeta data (CC BY 4.0):** https://doi.org/10.3929/ethz-b-000746797
4. **Rogers et al. (2025), University of Bath experimental auxetic dataset (CC BY 4.0):** https://doi.org/10.15125/BATH-01525

> **Academic-use note:** Credit the original authors, inspect the exact license terms of every redistributed component, and maintain a primary-source verification log for the course report. This proposal has not been experimentally validated yet.
