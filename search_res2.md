# Generative Modeling Project Scan: Structured Engineering Domains

Oct 19, 2026 · @animenerd9026

## Short answer

Pick **memorization-aware analog circuit topology generation** on the AnalogGenie corpus: 3,350 expert-drawn topologies from textbooks and papers (MIT license), checked with ngspice. It passes all 8 gates, with gate 2 passing only under a strict definition: the scarce ground truth is expert-invented, published topologies, not "simulatable" graphs, which compute can churn out.

The field is publishing fast at ICLR and ICML (2023–2025), the main baseline is an 11.8M-parameter GPT that fits a free T4, and its weak spots — "valid" means it simulates with default sizing, "novel" means not an exact copy — are exactly what a 4-week audit-plus-one-fix project can attack. Runners-up: distribution-grid topology generation with pandapower (best data-scarcity story, mostly synthetic open data) and floor-plan completion on Modified Swiss Dwellings (shortest learning curve, borderline compute).

Four of eight screened candidates pass every gate. No biology or physics problem made the list: I did not find one clearly stronger and did not screen them in depth.

## Screening: 8 candidates against the 8 gates

Four candidates pass all gates (C1, C3, C5, C8); gate 2 is the main killer, as you expected. "Cond." means it passes only under the stricter framing given in the notes; "Not checked" means a gate was moot after an earlier fail.

| # | Concrete problem | G1 Structure | G2 100x | G3 Formulation | G4 Checker | G5 Levers | G6 Open data | G7 Compute | G8 Memorization | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Circuit-type-conditioned generation of pin-level analog topologies from the [AnalogGenie](https://github.com/xz-group/AnalogGenie) expert corpus, checked in ngspice | Pass | Cond. | Pass | Pass | Pass | Pass | Pass | Pass | **Passes** |
| C2 | Spec-conditioned power-converter topology generation (target voltage ratio, efficiency) on [LaMAGIC](https://arxiv.org/abs/2407.18269)-style data | Pass | **Fail** | Pass | Pass | Pass | Not checked | Pass | Pass | Fails G2 |
| C3 | Generation of LV/MV distribution feeders (topology + impedances + bus types) that converge in AC power flow, from [SimBench](https://pypi.org/project/simbench/) / [ENGAGE](https://zenodo.org/records/15464235) | Pass | Cond. | Pass | Pass | Pass | Pass | Pass | Pass | **Passes** |
| C4 | Constraint-graph CAD sketch generation on [SketchGraphs](https://github.com/PrincetonLIPS/SketchGraphs) | Pass | **Fail** | Pass | Not checked | Pass | **Fail** | Pass | Pass | Fails G2, G6 |
| C5 | Floor-plan completion: building structure + zoning graph → typed room polygons, on [Modified Swiss Dwellings](https://data.4tu.nl/datasets/e1d89cb5-6872-48fc-be63-aadd687ee6f9) | Pass (vector output only) | Pass | Pass | Pass | Pass | Pass | Borderline | Pass | **Passes** |
| C6 | Fuel-molecule inverse design conditioned on measured cetane number, from the [NREL compendium](https://www.osti.gov/biblio/1345058) (496 compounds) | Pass | Pass | Pass | Cond. | Pass | **Fail (unclear)** | Pass | Pass | Fails G6 |
| C7 | Unconditional drug-like molecule generation on ZINC / MOSES / QM9-style libraries | Pass | **Fail** | Pass | Pass | Pass | Not checked | Pass | Pass | Fails G2 |
| C8 | Water-distribution network generation with hydraulic feasibility, from public EPANET networks ([WNTR](https://pypi.org/project/wntr/), [DiTEC-WDN](https://arxiv.org/abs/2503.17167)) | Pass | Cond. | Pass | Pass | Pass | Pass | Pass | Pass | **Passes** |

**Why each fail or conditional pass**

- **C1, G2 (cond.)**: expert topologies are scarce because they come from decades of textbooks and papers, and industrial netlists sit behind IP and foundry NDAs ([AnalogFed](https://arxiv.org/abs/2507.15104) exists for this reason). But random graphs that simulate are free to make, so ground truth must be the expert corpus, not "simulatable".
- **C2, G2**: the converter datasets come from enumerating small topologies and simulating each one. [AnalogGenie's paper](https://arxiv.org/html/2503.00205v1) says LaMAGIC and CktGNN use permutation-synthesized data; [AutoCircuit-RL](https://arxiv.org/html/2506.03122v1) built its 4–10-component set with ngspice. More compute means more data. The OCB op-amp benchmark fails for the same reason: its [repo](https://github.com/zehao-dong/CktGNN) ships a generator script.
- **C3, G2 (cond.)**: real feeders are withheld for security ([CEII](https://electricgrids.engr.tamu.edu/electric-grid-test-cases); utilities refuse to share, per [TUM's VGAE paper](https://arxiv.org/abs/2509.02469)). Yet the open data is mostly synthetic: ENGAGE is 300 perturbations of each of 10 SimBench grids. Only those \~10 expert-built base grids are compute-invariant.
- **C4, G2**: 15 million public Onshape sketches is not scarce. **G6**: the repo says the original creators hold copyright under Onshape's terms; there is no open data license. G4 not checked: the paper's constraint solving used Onshape's API.
- **C5, G7 (borderline)**: polygon diffusion on 4,167 plans likely needs 3–6 T4-hours (estimate), and the training zip is 4.76 GB. The cheap raster U-Net baseline would fail G1, so the project must output polygons.
- **C6, G6**: the cetane compendium is a PDF report with no explicit data license, so numbers must be scraped from tables. The larger 615-molecule [fuel database](https://doaj.org/article/75ad5f22388240918e69fbeb4d5b6046) fills gaps with model estimates, which breaks G2. **G4 (cond.)**: RDKit checks structure, but the property check needs a surrogate fit on the same \~500 points.
- **C7, G2**: ZINC- and GDB-style molecules come from enumerated virtual libraries and QM9 labels are DFT calculations, so compute makes more.
- **C8, G2 (cond.)**: real water networks are withheld for security and privacy, per the [DiTEC-WDN paper](https://arxiv.org/pdf/2503.17167). But some public benchmarks are fictional, and only a few dozen networks exist in total.

## Scores for the passing candidates

Circuits (C1) and grids (C3) tie at 13 of 14; circuits win the tie because their training data are real expert designs, while the grid candidate's open data are mostly synthetic. Scores are my judgment from the papers I opened, not a bibliometric count.

| Candidate | R1 Labs | R2 Venues | R3 Growth | R4 Demand | H1 Headroom | H2 Not big-lab | H3 Critiquable | Total /14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 Analog topologies | 2 | 2 | 2 | 1 | 2 | 2 | 2 | **13** |
| C3 Distribution grids | 2 | 2 | 1 | 2 | 2 | 2 | 2 | **13** |
| C5 Floor plans (MSD) | 1 | 1 | 1 | 1 | 2 | 2 | 2 | **10** |
| C8 Water networks | 1 | 0 | 0 | 1 | 2 | 2 | 1 | **7** |

**Evidence behind the scores**

| Candidate | Labs and one recent paper each (R1) | Venues (R2) and trend (R3) | Demand (R4) | Headroom and flaws (H1, H3) |
| --- | --- | --- | --- | --- |
| C1 | Xuan Zhang, Northeastern: [AnalogGenie](https://proceedings.iclr.cc/paper_files/paper/2025/hash/f0552f14388d95b19740dee809f5cad1-Abstract-Conference.html), ICLR 2025. Weidong Cao, George Washington U.: [AnalogFed](https://arxiv.org/abs/2507.15104), 2025. Yiran Chen, Duke: [LaMAGIC2](https://icml.cc/virtual/2025/poster/44935), ICML 2025. David Z. Pan (UT Austin) and Ping Luo (HKU): [AnalogCoder](https://ojs.aaai.org/index.php/AAAI/article/view/32016), AAAI 2025 | ICLR 2023, ICML 2024, ICLR 2025, two ICML 2025 papers, AAAI 2025, DATE 2026. I found 1 paper from 2023, 4 from 2024, 8+ from 2025 and 4+ from 2026 | Proprietary designs and manual design flow, stated by the papers themselves; NSF award acknowledged in AnalogGenie. No independent industry report found, hence 1 | Validity means "simulates with default sizing"; novelty means "not in dataset". [AnalogToBi](https://arxiv.org/abs/2603.08720) reports severe memorization in sequence models. Baseline validity 73.5% before fine-tuning |
| C3 | Hanghang Tong, UIUC: [PowerGrow](https://arxiv.org/abs/2509.12212), 2025. TUM (Okoyomon): [VGAE grid generation](https://arxiv.org/abs/2509.02469), 2025, and ENGAGE, e-Energy 2025. Zhaoyu Wang group: [DeepGDL](https://arxiv.org/abs/1901.09674) and an IEEE TPWRS 2022 graph-GAN paper. Thomas Overbye, Texas A&M: the [synthetic grid repository](https://electricgrids.engr.tamu.edu/electric-grid-test-cases) | IEEE Trans. Smart Grid (FeederGAN 2021, Graph-CPS 2023), IEEE TPWRS 2022, PRX Energy 2024. Steady rather than fast growth | ARPA-E funded the GRID DATA program because real grid data is CEII-restricted | FeederGAN reached 27% power-flow feasibility (per the VGAE paper). VGAE ran no power-flow check. PowerGrow trains on perturbations of one 36-bus grid and scores MMD against its own training set |
| C5 | Jan van Gemert and Seyran Khademi, TU Delft: [MSD](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/7514_ECCV_2024_paper.php), ECCV 2024. Other labs not verified in this scan | ECCV 2024 (a top vision venue, outside your list); 2025–2026 datasets such as ResPlan | Stated by papers only | MSD's baselines drop sharply versus RPLAN. MIoU against one ground truth punishes valid alternatives. The MSD paper found 70% near-duplicates in RPLAN |
| C8 | Lazovik and Degeler, Groningen: [DiTEC-WDN](https://arxiv.org/abs/2503.17167), Sci. Data 2025. No deep generative model for network topology found | Sci. Data, Water Resources Management; mostly non-neural generators (HydroGen, SyNF) | Utilities' unwillingness to share is stated by the papers | Wide open but nothing to beat, so little to critique |

## Deep dive 1 (recommended): analog circuit topology generation

The project in one line: audit whether autoregressive circuit generators copy their training set, replace "simulatable" with a tiered validity check, and add one fix (constraint-guided decoding) that raises valid-and-novel output.

### Problem and formal setup

Learn a distribution over transistor-level circuit topologies from 3,350 expert designs, conditioned on circuit type, and sample topologies that are electrically valid, not copies of training circuits, and functional once sized. The test set is the held-out 10% of expert topologies; success is measured against that expert distribution, not against raw simulatability.

- **Output space**: a typed bipartite device–net graph G = (D ∪ N, E). Devices D have types {NMOS, PMOS, NPN, PNP, R, C, L, diode, …}; each edge carries a pin role (D, G, S, B for MOSFETs). AnalogGenie's equivalent is a pin-level graph serialized as an Eulerian circuit.
- **Condition**: circuit type c ∈ {op-amp, LDO, bandgap, comparator, PLL, LNA, PA, mixer, VCO, power converter, SC sampler}.
- **Hard constraints (ERC)**: every pin on exactly one net; every internal net touches ≥ 2 pins; VDD and VSS present; no device with all pins on one net; graph connected.
- **Functional constraint**: some sizing x (W/L, R, C values) exists so ngspice converges and the spec holds, e.g. op-amp DC gain ≥ 40 dB.

```latex
\max_\theta \; \mathbb{E}_{c}\,\Pr_{G\sim p_\theta(\cdot\mid c)}\big[\mathrm{ERC}(G)\wedge \exists x:\ \mathrm{spec}_c(G,x)\wedge G\not\cong G_i\ \forall G_i\in\mathcal{D}_{\text{train}}\big]
```

### The 100x compute argument

It holds, but only if ground truth means "topologies human experts invented and published". The corpus was hand-redrawn in Cadence from Razavi, Gray, Johns and Martin, Allen and Holberg, Camenzind and papers; more GPUs do not add textbook chapters. Industrial topologies are confidential along with the foundry process data needed to evaluate them, which is why [AnalogFed](https://arxiv.org/abs/2507.15104) proposes federated training.

What compute *can* make is random graphs that pass ERC and simulate. That is the honest weakness of the current "validity" metric, and it is the hook for your paper: report fidelity to held-out expert topologies and functional pass rates, not simulatability.

### Dataset

| Item | Value | Status |
| --- | --- | --- |
| URL | Raw: [github.com/xz-group/AnalogGenie](https://github.com/xz-group/AnalogGenie) (Dataset/). Processed: [huggingface.co/datasets/JianGao666/AnalogGenie](https://huggingface.co/datasets/JianGao666/AnalogGenie) | Confirmed |
| License | MIT on both the repo and the HF card. The raw folder also holds textbook-page screenshots, which MIT cannot relicense; use the netlists only | Confirmed |
| Samples | 3,350 topology folders; 802 also contain an auxiliary sub-block netlist (e.g. Opamp1463.cir), 4,152 .cir files in all. Devices per circuit: min 1, median 21, max 72 | Confirmed by my clone and parse |
| Size | Raw Dataset/ 493 MB on disk (mostly PNGs); processed HF set 222 MB | Confirmed |
| Format | Spectre-style, unsized netlists (`M1 (d g s b) nmos4`), port lists, page references; processed set is NumPy token arrays | Confirmed |
| Access | Instant download, no form | Confirmed |

### Validity checker (tiered)

| Tier | Tool | What it checks | Speed per sample |
| --- | --- | --- | --- |
| 0. ERC | Your own networkx code | Floating pins and nets, shorted devices, connectivity, supply nets | Under 1 ms (estimate) |
| 1. Simulatable | [ngspice](https://ngspice.sourceforge.net/) 42, BSD-3, via subprocess or PySpice | Operating point converges with default sizes and generic level-1 models; this is AnalogGenie's definition of valid | **15 ms** measured: 8-transistor op-amp, OP + AC sweep, process spawn included |
| 2. Functional | ngspice plus quick sizing (random search or small GA, 50–200 simulations) | Per-type spec, e.g. gain ≥ 40 dB and phase margin ≥ 45° for op-amps | About 1–3 s per topology (estimate from tier 1) |

The netlists carry no sizes and use Spectre syntax, so you need a small converter to ngspice syntax plus a generic model card. Generic models give relative comparisons, not silicon truth.

### Baselines

| Model | Family | Code | Note |
| --- | --- | --- | --- |
| [AnalogGenie](https://arxiv.org/abs/2503.00205), ICLR 2025 | Autoregressive GPT, 11.8M parameters, Eulerian-circuit tokens | [repo](https://github.com/xz-group/AnalogGenie), MIT; checkpoint on HF | Main baseline; 73.5% valid after pretraining, 93.2% after fine-tuning |
| [AnalogGenie-Lite](https://proceedings.mlr.press/v267/gao25a.html), ICML 2025 | Autoregressive with subgraph compression | [repo](https://github.com/xz-group/AnalogGenie-Lite), MIT | Compression pipeline only; motifs hard-coded to their data |
| [AnalogToBi](https://arxiv.org/abs/2603.08720), 2026 | Autoregressive over a bipartite graph, grammar-guided decoding | [repo](https://github.com/Seungmin0825/AnalogToBi), no license shown | Closest competitor: targets memorization directly |
| [CktGNN](https://arxiv.org/abs/2308.16406), ICLR 2023 | Graph VAE | [repo](https://github.com/zehao-dong/CktGNN), MIT | Op-amps only, generated data |
| [DiGress](https://github.com/cvignac/DiGress), ICLR 2023 | Discrete graph diffusion | MIT | Generic; adapt to the bipartite graph if you test a second family |
| [ARCS](https://arxiv.org/abs/2603.29068), 2026 | Graph VAE + flow matching | No code found | Limited to 32 templates |

### Open levers you can finish in 4 weeks

1. **Memorization audit (evaluation)**: exact and near-duplicate rates of samples versus train, as a function of augmentation (1×, 10×, 70× Eulerian sequences) and sampling temperature. Cheap, and nobody has published it independently.
2. **Constraint-guided decoding (sampling)**: mask tokens that would break ERC given the partial pin graph, then measure the valid × novel trade-off against plain sampling.
3. **Tiered validity metric (evaluation)**: re-score released baselines with tier 2 and report how much "validity" survives.
4. **Representation (riskier)**: bipartite graph with discrete diffusion versus Eulerian sequences; keep this for the proposal's future work.

A good Phase 2 plan is lever 1 as the analysis and lever 2 as the one methodological improvement.

### Memorization protocol

1. Canonicalize each netlist as the typed device–net graph above. Keep VDD and VSS; keep port names (strict) or collapse them to PORT (loose); anonymize internal nets.
2. Hash with Weisfeiler–Lehman (4 iterations, node and edge labels), then confirm collisions with VF2 isomorphism in networkx. Measured: 0.8 ms per hash, 1–13 ms per VF2 check.
3. Report the exact-copy rate of valid samples against train and against validation, under both strict and loose canonicalization.
4. For near-duplicates, compare WL feature vectors (cosine) or graph edit distance on small circuits, against the train-to-train nearest-neighbour baseline.

Smoke test already run on the full corpus: with strict canonicalization the 3,350 main netlists contain **0** isomorphic duplicates; with ports collapsed there are **20** groups and **25** redundant copies (0.7%). One trap: my first pass read the auxiliary sub-block file in 802 folders and wrongly found about 6% duplicates, so always parse `<id>.cir`.

### Compute on a free T4

About 2–3 GPU-hours in total (estimate). The full augmented set is 227,766 sequences of up to 1,024 tokens, about 2.3 × 10^8 tokens and 1.7 × 10^16 FLOPs per epoch at 11.8M parameters. At an effective 15 TFLOPS that is roughly 20–30 minutes per epoch, so 3–5 epochs, or a 10–20× augmentation subset, fits. Sampling 2,000 circuits takes minutes, ngspice tier 1 about 30 s of CPU, and hashing about 2 s. Setup is `apt-get install ngspice`, a git clone and a 222 MB download; ngspice installed here in one apt step, but time the full setup on Colab.

### Why a practitioner cares, and how they would test it

Topology choice is the creative, manual step in analog design, per the AnalogGenie paper. A designer would take a generated netlist, size it with an optimizer, and simulate it in ngspice or a commercial simulator with their process models; a topology that meets spec after sizing is directly usable.

### Main risks and fallback

- **Learning curve**: MOSFET pins and op-amp basics. Limit the functional tier to op-amps and OTAs; Razavi's op-amp chapters cover it.
- **Plumbing**: Spectre-to-ngspice conversion and default sizing take one or two days.
- **Fast-moving field**: AnalogToBi already targets memorization, so frame your paper as an independent audit plus metric, and check arXiv weekly.
- **Validity gap**: generic models are not silicon; say so in the paper.
- **Fallback**: if training stalls, use the released checkpoint and study decoding and evaluation only (zero training). If tier 2 is too slow, report tiers 0–1 plus the memorization audit.

## Deep dive 2: distribution-grid topology generation

The strongest scarcity story of the four, with the weakest open data: real feeders are security-restricted, so almost everything public is synthetic.

### Problem and formal setup

Generate low- and medium-voltage distribution feeders (topology, line impedances, bus types and loads) that converge in AC power flow, look like realistic feeders, and are not near-copies of the few expert-built base grids. Condition on voltage level and area class.

- **Output**: attributed graph G = (V, E, X, W). Buses V carry type {slack, PV, PQ} and load P, Q; branches E carry r, x in per-unit and a rating.
- **Condition**: c = (LV or MV, rural / semi-urban / urban / commercial, number of buses).
- **Hard constraints**: connected; radial (LV) or ring with an open point (MV); exactly one slack bus.
- **Physical constraints**: Newton–Raphson converges; 0.9 ≤ |V\_i| ≤ 1.1 p.u.; line loading ≤ 100%; optionally N-1 secure.

### The 100x compute argument

The target passes cleanly: real feeder models are withheld for security and privacy, and the US treats grid data as CEII, which is why [ARPA-E funded synthetic grids](https://electricgrids.engr.tamu.edu/electric-grid-test-cases). No amount of compute produces a utility's real feeder.

The training data does not pass cleanly. [ENGAGE](https://zenodo.org/records/15464235) is 300 generated perturbations of each of 10 SimBench base grids, and DINGO is a rule-based generator; a model trained on either learns the generator. The compute-invariant core is about 10 expert-built SimBench grids, plus PGLib transmission cases and the OSM-derived European high-voltage grid. Frame the project as few-shot generation from that core, with synthetic grids only for pretraining.

### Dataset

| Source | License | Samples | Size | Format | Status |
| --- | --- | --- | --- | --- | --- |
| [ENGAGE](https://zenodo.org/records/15464235) (TUM, 2025) | CC BY 4.0 | 3,000 grids (10 base × 300) | Graphs-only 8.2 MB; complete 11.6 GB | PyTorch Geometric `dataset.pt`; pandapower JSON in the complete set | Confirmed |
| [SimBench](https://pypi.org/project/simbench/) | Data ODbL 1.0, code BSD-3 | LV to EHV base grids; the four I loaded had 15–144 buses | 91 MB wheel | pandapower networks via `pip install simbench` | Confirmed |
| [PGLib-OPF](https://github.com/power-grid-lib/pglib-opf) | Creative Commons Attribution | Transmission benchmark cases (count not checked) | Small | MATPOWER `.m` | License confirmed |
| [OSM European HV grid](https://zenodo.org/records/14144752) | ODbL 1.0 | One continental 220–750 kV network; split it into regions | Not checked | CSV | License confirmed |

### Validity checker

[pandapower](https://www.pandapower.org/) (BSD-3) `runpp`: Newton–Raphson AC power flow. It checks convergence, voltage limits and line loading. **Measured: 63–74 ms per grid** on SimBench grids of 15–144 buses on CPU without numba (numba makes it faster). An N-1 check costs one power flow per line. Structural checks in networkx take under 1 ms.

### Baselines

| Model | Family | Code | Note |
| --- | --- | --- | --- |
| [PowerGrow](https://arxiv.org/abs/2509.12212), UIUC 2025 | Hierarchical graph beta diffusion | Paper says code is on GitHub; link not found | 98.9% convergence, but trained on perturbations of one grid |
| [VGAE grid generation](https://arxiv.org/abs/2509.02469), TUM 2025 | Graph VAE, four decoders | [GridGEN](https://github.com/SyedZainAbbas/GridGEN) (license not checked) | No power-flow check; trained on ENGAGE and DINGO |
| [DiGress](https://github.com/cvignac/DiGress) | Discrete graph diffusion | MIT | Generic baseline; PowerGrow compared other graph diffusion models |
| FeederGAN, IEEE TSG 2021 | Wasserstein GAN | Not released (per the VGAE paper) | 27% feasibility |
| [DeepGDL](https://arxiv.org/abs/1901.09674) | GRU autoregressive | Not released | Topology metrics only |

### Open levers you can finish in 4 weeks

1. **Feasibility-guided sampling**: use the power-flow mismatch as a guidance or rejection signal during diffusion sampling, and compare convergence against unguided sampling on honest data.
2. **Evaluation**: replace MMD-to-training-set with fidelity to held-out base grids plus a copy rate. PowerGrow's own random-walk baseline wins MMD by construction, which shows the metric's weakness.
3. **Few-shot transfer**: pretrain on synthetic ENGAGE or DINGO, fine-tune on the \~10 SimBench base grids, and measure how much the model copies them.

### Memorization protocol

Hash topology with bus-type labels using Weisfeiler–Lehman (measured 0.25–2.6 ms per SimBench grid), confirm with VF2, and add relative L2 distance on sorted impedance vectors for near-duplicates. The key number is distance to the nearest of the 10 base grids, not to the training perturbations.

### Compute on a free T4

About 1–2 GPU-hours (estimate) for a small discrete-diffusion model on 3,000 graphs of at most \~150 nodes. Power-flow evaluation of 1,000 samples takes about 70 s of CPU. Setup is `pip install pandapower simbench` plus an 8.2 MB download; both installed here without trouble (not timed).

### Why a practitioner cares, and how they would test it

Distribution operators and researchers need realistic test feeders for hosting-capacity and DER-integration studies. They would load a generated feeder into pandapower or OpenDSS and run power flow, N-1 and hosting-capacity analysis.

### Main risks and fallback

- **Tiny real data**: about 10 compute-invariant grids; results may say more about the synthetic generators than about real grids.
- **Learning curve**: per-unit systems, slack buses and radial operation take about a week.
- **Nonphysical parameters**: generated impedances can be absurd. Fallback: generate topology only and assign standard line types by rule, then check feasibility.
- **Fallback paper**: an evaluation audit of existing grid generators on ENGAGE, with no new model.

## Deep dive 3: floor-plan completion on Modified Swiss Dwellings

The easiest domain to learn and the cleanest dataset, but the heaviest compute and the weakest validity checker (geometry rules, no physics).

### Problem and formal setup

Given a multi-apartment building's structural elements and a zoning access graph, generate typed room polygons whose adjacencies match the graph, that do not overlap, and that fill the footprint. Outputs must be vector polygons; a raster segmentation would fail gate 1.

- **Input**: structure S (load-bearing walls and columns, as polygons or a mask) and zoning graph Z = (V, E), nodes labelled zone 1–4 (private, public, service, outside), edges labelled passage, door or front door.
- **Output**: P = {(polygon\_i, roomtype\_i) : i ∈ V}.
- **Constraints**: polygons inside the boundary; interiors pairwise disjoint; their union covers the usable area; rooms joined by an edge lie within MSD's 0.04 m adjacency buffer; structure not crossed.

### The 100x compute argument

The plans are real Swiss buildings, digitized by Archilyse with a manual quality check. Compute cannot create more real dwellings or architects' decisions. This pass is weaker than for circuits or grids: plans are not secret, and procedural generators can make valid-looking layouts, so the claim is about matching the real-dwelling distribution, not about validity.

### Dataset

| Item | Value | Status |
| --- | --- | --- |
| URL | [data.4tu.nl, doi 10.4121/e1d89cb5-6872-48fc-be63-aadd687ee6f9](https://data.4tu.nl/datasets/e1d89cb5-6872-48fc-be63-aadd687ee6f9) | Confirmed |
| License | CC BY 4.0 | Confirmed (dataset citation file) |
| Samples | 4,167 training plans; 5,372 in the full benchmark, covering 18.9K apartments | Confirmed |
| Size | Train zip 4.76 GB, test zip 787 MB, 5.54 GB unzipped | Confirmed |
| Format | `graph_in` / `graph_out` networkx pickles, `struct_in` / `full_out` NumPy arrays | Confirmed |
| Access | Direct download, no form. RPLAN, the usual alternative, requires a request form ([HouseDiffusion repo](https://github.com/blase3/house_diffusion), [DS2D repo](https://github.com/plstory/ds2d)), so it is excluded | Confirmed |

### Validity checker

Your own Shapely and networkx rules: overlap, containment, coverage, adjacency versus the input graph, plus MSD's graph-compatibility metric. **Measured: about 2 ms per 30-room plan** on a synthetic test. There is no physics simulator; daylight or egress checks would be extra work.

### Baselines

| Model | Family | Code | Note |
| --- | --- | --- | --- |
| Modified HouseDiffusion (MHD), [MSD paper](https://arxiv.org/abs/2407.10121), ECCV 2024 | Diffusion over polygon corners, with wall cross-attention and a GAT | Paper says code is open; repo link not verified | Approximates rooms as rotated rectangles |
| [HouseDiffusion](https://arxiv.org/abs/2211.13287) | Diffusion over corners | Repo exists; trained on RPLAN | Upstream of MHD |
| [Kuhn's MSD adaptation](https://arxiv.org/abs/2312.03938), 2023 | Diffusion over corners | Code "later" | Found rectangles beat true polygons |
| Graph-informed U-Net, MSD paper | Segmentation (raster) | [Unofficial Colab version](https://github.com/craked-code/MSD_implementation) | Reference only; fails gate 1 |

### Open levers you can finish in 4 weeks

1. **Representation**: variable-length polygons instead of rectangles, which Kuhn's report left open.
2. **Constraint-guided sampling**: non-overlap and coverage penalties applied during denoising.
3. **Evaluation**: MIoU against a single ground truth penalizes valid alternatives; propose constraint-satisfaction plus distributional metrics.

### Memorization protocol

Hash each room graph with Weisfeiler–Lehman over room types, then compute the rasterized IoU to the nearest training plan with the same hash bucket. MSD itself flagged near-duplicates at MIoU above 0.87; reuse that threshold.

### Compute on a free T4

Borderline: an MHD-style model likely needs 3–6 GPU-hours (estimate), and downloading 4.76 GB may break your 5-minute setup rule. Restricting to rectangles or smaller plans would bring it under 4 hours.

### Why a practitioner cares, and how they would test it

Architects and developers want early-stage layout options that respect fixed structure. They would test outputs with code checks, area schedules and daylight simulation; the parent Swiss Dwellings dataset already ships simulated daylight and noise features.

### Main risks and fallback

- **Compute** is the main risk; fall back to single-apartment sub-plans or rectangles.
- **MHD code availability** is unverified; check before committing.
- **Validity is rule-based**, so a reviewer may call it weaker than a simulator.
- **Fallback paper**: a metric study showing how MIoU and compatibility rank models differently from constraint satisfaction.

## Starter reading list for the analog-topology project

Read 1, 9, 3 and 17 first: the main baseline, its closest critic, the original graph benchmark, and the standard warning about graph-generation metrics. "Not checked" means I did not open the code page; licenses are for code or data, not the paper.

| # | Title | Venue, year | Link | Code or data | License | Known flaw or limitation |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AnalogGenie: A Generative Engine for Automatic Discovery of Analog Circuit Topologies | ICLR 2025 | [arXiv 2503.00205](https://arxiv.org/abs/2503.00205) | [code](https://github.com/xz-group/AnalogGenie), [data](https://huggingface.co/datasets/JianGao666/AnalogGenie) | MIT | "Valid" = simulates with default sizing; "novel" = not identical to a dataset topology |
| 2 | AnalogGenie-Lite: Enhancing Scalability and Precision in Circuit Topology Discovery through Lightweight Graph Modeling | ICML 2025 | [PMLR v267](https://proceedings.mlr.press/v267/gao25a.html) | [code](https://github.com/xz-group/AnalogGenie-Lite) | MIT | Motif compression is hard-coded to their dataset |
| 3 | CktGNN: Circuit Graph Neural Network for Electronic Design Automation | ICLR 2023 | [arXiv 2308.16406](https://arxiv.org/abs/2308.16406) | [code + OCB](https://github.com/zehao-dong/CktGNN) | MIT | Op-amps only; benchmark circuits come from a generator script |
| 4 | LaMAGIC: Language-Model-based Topology Generation for Analog Integrated Circuits | ICML 2024 | [arXiv 2407.18269](https://arxiv.org/abs/2407.18269) | Not checked | Not checked | Power converters with few devices (≤ 4 in AnalogGenie's comparison); 12.7% novel |
| 5 | LaMAGIC2: Advanced Circuit Formulations for Language Model-Based Analog Topology Generation | ICML 2025 | [arXiv 2506.10235](https://arxiv.org/abs/2506.10235) | Not checked | Not checked | Reuses LaMAGIC's converter dataset |
| 6 | AnalogCoder: Analog Circuit Design via Training-Free Code Generation | AAAI 2025 | [doi 10.1609/aaai.v39i1.32016](https://doi.org/10.1609/aaai.v39i1.32016) | [code](https://github.com/laiyao1/AnalogCoder) | MIT | Prompted LLM; circuits up to about 10 devices and 8.9% novel (per AnalogGenie) |
| 7 | AnalogCoder-Pro: Unifying Analog Circuit Generation and Optimization via Multi-modal LLMs | arXiv 2025 | [arXiv 2508.02518](https://arxiv.org/abs/2508.02518) | Announced, not checked | Not checked | Depends on large multimodal LLMs; not reproducible on a T4 |
| 8 | AnalogFed: Federated Discovery of Analog Circuit Topologies with Generative AI | arXiv 2025 | [arXiv 2507.15104](https://arxiv.org/abs/2507.15104) | No code link | — | No code and no venue listed on arXiv; a federated setup is overkill for a single-student project |
| 9 | AnalogToBi: Device-Level Analog Circuit Topology Generation via Bipartite Graph and Grammar Guided Decoding | arXiv 2026 | [arXiv 2603.08720](https://arxiv.org/abs/2603.08720) | [code](https://github.com/Seungmin0825/AnalogToBi) | None shown | Preprint; its memorization claims need an independent check |
| 10 | ARCS: Autoregressive Circuit Synthesis with Topology-Aware Graph Attention and Spec Conditioning | arXiv 2026 | [arXiv 2603.29068](https://arxiv.org/abs/2603.29068) | No code found | — | Limited to 32 predefined templates, by its own account |
| 11 | From Generation to Discovery: Diffusion Mutation Kernels for Circuit and Physical Design | arXiv 2026 | [arXiv 2608.27649](https://arxiv.org/abs/2608.27649) | Not checked | Not checked | I could not read the full text; novelty is WL similarity, which ignores sizing |
| 12 | DiffCkt: A Diffusion Model-Based Hybrid Neural Network Framework for Automatic Transistor-Level Generation of Analog Circuits | arXiv 2025 | [arXiv 2507.00444](https://arxiv.org/abs/2507.00444) | Not checked | Not checked | Trained on synthetic data, per ARCS's comparison table |
| 13 | AutoCircuit-RL: Reinforcement Learning-Driven LLM for Automated Circuit Topology Generation | arXiv 2025 | [arXiv 2506.03122](https://arxiv.org/abs/2506.03122) | Not checked | Not checked | Dataset built by enumeration plus ngspice, so compute-generated |
| 14 | AnalogSeeker: An Open-Source Foundation Language Model for Analog Circuit Design | arXiv 2025 | [arXiv 2508.10409](https://arxiv.org/abs/2508.10409) | Not checked | Not checked | Found only via AnalogToBi's references; not read |
| 15 | AMSNet: Netlist Dataset for AMS Circuits | IEEE LAD workshop 2024 | [arXiv 2405.09045](https://arxiv.org/abs/2405.09045) | [project page](https://ams-net.github.io/) | Not checked | Initially two textbooks, partial release |
| 16 | DiGress: Discrete Denoising Diffusion for Graph Generation | ICLR 2023 | [code page with citation](https://github.com/cvignac/DiGress) | [code](https://github.com/cvignac/DiGress) | MIT | No mixed discrete-continuous outputs or spec conditioning, per ARCS |
| 17 | Evaluation Metrics for Graph Generative Models: Problems, Pitfalls, and Practical Solutions (O'Bray et al.) | ICLR 2022 | [OpenReview](https://openreview.net/forum?id=tBtoZYKd9n) | Not checked | Not checked | Generic graphs; says nothing about domain validity |
| 18 | SynCircuit: Automated Generation of New Synthetic RTL Circuits Can Enable Big Data in Circuits | arXiv 2025 | [arXiv 2509.00071](https://arxiv.org/abs/2509.00071) | Not checked | Not checked | Digital RTL, not analog; useful for its diffusion-plus-validity-repair pipeline |

## Claims to verify before you commit

Check the first five before your proposal: each one could change the recommendation.

1. **AnalogGenie data license scope**: MIT is stated on the repo and HF card, but the raw folder includes textbook screenshots. Confirm you may redistribute derived netlists, and never redistribute the PNGs.
2. **AnalogToBi's overlap with your idea**: read it in full; if it already reports the memorization audit you plan, shift your contribution to the tiered validity metric.
3. **Spectre-to-ngspice conversion**: confirm the AnalogGenie repo's ngspice infrastructure (mentioned in the paper's reproducibility statement) is in the public code, or budget two days to write it.
4. **T4 training time**: my 20–30 minutes per epoch is arithmetic, not a run. Time one epoch on Colab in your feasibility smoke test.
5. **MHD code for floor plans**: the MSD paper says code is open; I did not find the repo link.
6. PowerGrow's code link ("on GitHub" per the paper) and the GridGEN license.
7. PGLib-OPF case count and the exact Creative Commons version.
8. Affiliations I took from author pages or logos rather than papers: Pan at UT Austin, Luo at HKU, Chen at Duke, Overbye at Texas A&M.
9. DiGress's arXiv ID; I linked its repo, which states ICLR 2023.
10. DiTEC-WDN's license: the paper says CC BY-NC 4.0, but a Hugging Face copy says CC BY 4.0.
11. Whether the MSD Kaggle mirror is official (it would shorten setup).
12. LaMAGIC and LaMAGIC2 code and data availability (not checked because they failed gate 2).

**What I measured versus estimated**

| Figure | Value | How |
| --- | --- | --- |
| ngspice per sample | 15 ms (8-transistor op-amp, OP + AC sweep) | Measured, ngspice 42, CPU, process spawn included |
| pandapower `runpp` | 63–74 ms (SimBench, 15–144 buses) | Measured, pandapower 3.5.6, CPU, no numba |
| WNTR / EPANET snapshot | 15–22 ms (Net1, Net3) | Measured, WNTR 1.5.0 |
| Shapely floor-plan rules | \~2 ms per 30-room plan | Measured on a synthetic plan |
| RDKit canonicalization | 0.36 ms per molecule | Measured |
| WL hash, circuits | 0.8 ms per graph | Measured on all 3,350 AnalogGenie netlists |
| AnalogGenie duplicates | 0 strict; 25 copies in 20 groups loose | Measured (my canonicalization choices) |
| All GPU-hours, setup times on Colab, sizing time per topology | See each deep dive | Estimated |
| Dataset sizes, licenses, sample counts | See each dataset table | Confirmed at source unless marked |

**Sources (pages opened)**

- AnalogGenie: [paper](https://arxiv.org/html/2503.00205v1), [repo](https://github.com/xz-group/AnalogGenie), [HF dataset](https://huggingface.co/datasets/JianGao666/AnalogGenie); [AnalogGenie-Lite repo](https://github.com/xz-group/AnalogGenie-Lite)
- [AnalogToBi](https://arxiv.org/abs/2603.08720) and [repo](https://github.com/Seungmin0825/AnalogToBi); [AnalogFed](https://arxiv.org/abs/2507.15104); [CktGNN repo](https://github.com/zehao-dong/CktGNN); [AnalogCoder repo](https://github.com/laiyao1/AnalogCoder); [DiGress repo](https://github.com/cvignac/DiGress); [ARCS](https://arxiv.org/abs/2603.29068)
- Grids: [PowerGrow](https://arxiv.org/pdf/2509.12212), [VGAE grid generation](https://arxiv.org/pdf/2509.02469), [ENGAGE](https://zenodo.org/records/15464235), [SimBench](https://pypi.org/project/simbench/), [PGLib-OPF](https://github.com/kyribaker/pglib-opf), [TAMU test cases](https://electricgrids.engr.tamu.edu/electric-grid-test-cases), [OSM HV grid](https://zenodo.org/records/14144752)
- Floor plans: [MSD paper](https://arxiv.org/html/2407.10121v3), [MSD data](https://data.4tu.nl/datasets/e1d89cb5-6872-48fc-be63-aadd687ee6f9), [Swiss Dwellings](https://zenodo.org/records/7070952), [Kuhn report](https://arxiv.org/html/2312.03938v1)
- Other screens: [SketchGraphs](https://github.com/lxuechen/SketchGraphs), [DiTEC-WDN](https://arxiv.org/pdf/2503.17167), [NREL cetane compendium](https://www.osti.gov/biblio/1345058), [AutoCircuit-RL](https://arxiv.org/html/2506.03122v1)
