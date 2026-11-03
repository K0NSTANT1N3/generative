# Research report: choosing a measurement-bound generative modeling project

Literature and dataset screening · October 19, 2026

## 1. Short answer

My top recommendation is property-conditioned molecular graph generation for experimentally measured aqueous solubility, using the AqSolDB dataset. It has an unusually clean combination of genuinely scarce experimental labels, a confirmed CC0 dataset of 9,982 compounds, graph-structured outputs, and fast chemical-validity checking with RDKit. The research opportunity is to develop a small-data generative method that combines chemical constraints, uncertainty-aware property guidance, and rigorous structural novelty evaluation. This is not necessarily the most exciting engineering application among your preferences, but it currently offers the most defensible route to a reproducible research paper under your compute and schedule constraints.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Scientific Data

+3



One essential distinction drives my assessment: a simulator can verify some properties of a generated artifact without producing new real-world measurements of that artifact. Your 100×-compute gate concerns the second problem, not just the computational difficulty of generating examples.

## 2. Screening: eight concrete candidate problems

The gates are G1 structured output, G2 real-world measurement scarcity, G3 natural generation, G4 automatic validity checking, G5 at least two research levers, G6 immediately usable open data or simulator, G7 compute feasibility, and G8 memorization testing.

A pass in the compute column is an engineering feasibility judgment, not a verified T4 benchmark. I have not trained these models in Colab. For G4, I distinguish structural validity from measured-property correctness; a surrogate prediction does not constitute an experimental measurement.

P = pass · F = fail · \* = restricted, small-model implementation only

| Concrete generative problem                                                                           | G1 | G2 | G3 | G4 | G5 | G6 | G7  | G8 |
| ----------------------------------------------------------------------------------------------------- | -- | -- | -- | -- | -- | -- | --- | -- |
| A. Generate op-amp device-topology graphs conditioned on gain and bandwidth, using CktBench           | P  | F  | P  | P  | P  | P  | P\* | P  |
| B. Generate distribution-grid connectivity graphs conditioned on bus counts and loads, using SimBench | P  | F  | P  | P  | P  | P  | P\* | P  |
| C. Generate human-style CAD sketch constraint graphs from SketchGraphs construction sequences         | P  | P  | P  | P  | P  | F  | F   | P  |
| D. Generate room-adjacency graphs and boundary polygons conditioned on RPLAN room types               | P  | P  | P  | P  | P  | F  | P\* | P  |
| E. Generate measured-room polygons and assembly layouts from MagicPlan/PuzzleFusion                   | P  | P  | P  | P  | P  | F  | P\* | P  |
| F. Generate molecular graphs conditioned on experimentally measured aqueous solubility, AqSolDB       | P  | P  | P  | P  | P  | P  | P\* | P  |
| G. Generate molecular graphs conditioned on experimental flash point, Sun et al. dataset              | P  | P  | P  | P  | P  | P  | P\* | P  |
| H. Generate molecular graphs from measured MS/MS peak sets and chemical formulas, MassSpecGym         | P  | P  | P  | P  | P  | P  | P\* | P  |

### Why the five engineering candidates fail

\- A — Analog circuits, G2: The [CktGNN/OCB repository](https://github.com/zehao-dong/CktGNN?utm_source=chatgpt.com) explicitly includes code for generating circuit datasets of arbitrary size. Its 10,000- and 50,000-circuit benchmarks are simulation-derived. Fabricated-and-measured chip results would satisfy the scarcity argument, but they are not what this open benchmark supplies. The simulator checks are excellent; the provenance of the target labels is the problem.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



\- B — Power grids, G2: [SimBench](https://github.com/e2nIEE/simbench?utm_source=chatgpt.com) supplies useful synthetic reference networks under the ODbL 1.0 database license, with BSD-3-Clause software. But passing a power-flow test on additional generated networks is not evidence of learning a scarce corpus of measured real utility networks. Real utility topology and telemetry are a much stronger scarcity case, yet that is a different dataset problem.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+2



\- C — CAD, G6 and G7: [SketchGraphs](https://github.com/PrincetonLIPS/SketchGraphs?utm_source=chatgpt.com) has roughly 15 million real design sketches and is scientifically compelling. Its authors explicitly state that the original CAD creators retain copyright, despite the repository's MIT software license. The full construction-sequence file is 15 GB and raw data roughly 43 GB; reproducing the full benchmark is outside the stated workflow. A smaller, rights-cleared subset could change the assessment.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



\- D — RPLAN floor plans, G6: The [HouseDiffusion repository](https://github.com/aminshabani/house_diffusion?utm_source=chatgpt.com) points to either an RPLAN website or a request form and documents download-access difficulties. I could not verify an immediately obtainable dataset with a clearly stated open data license. Your gate explicitly disallows treating a request workflow as sufficient.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



\- E — MagicPlan floor plans, G6: [PuzzleFusion](https://github.com/sepidsh/PuzzleFussion?utm_source=chatgpt.com) offers a download link and says its MagicPlan dataset follows the code license. That license restricts commercial use and refers to research-specific GPL terms; it is not an unrestricted standard open-data grant. This is promising for academic experimentation, but not a clean pass under your licensing requirement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

sepidsh/PuzzleFussion · GitHub

+1



Three candidates provisionally pass all eight gates: F, G, and H. They all use real experimental observations for conditioning, while validating generated structures computationally. Neither RDKit nor a learned predictor can certify the unmeasured physical property of a new molecule.

There is a useful near-miss outside the five priority domains: real-world street-network graph generation from [OpenStreetMap/Geofabrik](https://download.geofabrik.de/europe/liechtenstein.html?utm_source=chatgpt.com). Its licensing and tiny regional downloads are attractive, but simply extracting many more overlapping neighborhoods from the extensive worldwide map data undermines the intended scarce-example formulation unless the task targets a genuinely rare, measured infrastructure category.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://download.geofabrik.de\&sz=32)

Geofabrik Download Server

+1



## 3. Research-opportunity scores

Scores are my assessments, not measured bibliometric statistics. In particular, R3 has deliberately conservative values: I found papers across 2023–2026, but did not verify a year-by-year publication count for these exact subproblems.

| Passing candidate                           | R1 | R2 | R3 | R4 | H1 | H2 | H3 | Total /14 |
| ------------------------------------------- | -- | -- | -- | -- | -- | -- | -- | --------- |
| F. Solubility-conditioned molecular graphs  | 2  | 2  | 1  | 2  | 2  | 1  | 2  | 12        |
| H. Spectrum-conditioned molecular graphs    | 2  | 2  | 1  | 2  | 2  | 1  | 2  | 12        |
| G. Flash-point-conditioned molecular graphs | 0  | 1  | 0  | 2  | 2  | 2  | 2  | 9         |

For R1 and R2, relevant university research includes the University of Notre Dame's Graph DiT work at NeurIPS 2024, the MIT Coley group's DiffMS at ICML 2025, and Universitat Rovira i Virgili's CoCoGraph in Nature Machine Intelligence in May 2026. These are papers in the surrounding graph-generation field, not necessarily direct AqSolDB or flash-point benchmarks. MassSpecGym also includes contributions from academic mass-spectrometry groups and appeared at NeurIPS 2024.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://papers.nips.cc\&sz=32)

papers.nips.cc

+3



The largest documented H3 opportunity is in spectrum-conditioned generation: a June 2026 audit found evaluation issues in 17 of 26 MassSpecGym papers it reviewed, covering leakage, shortcuts, and metric implementation discrepancies. For solubility, a separate 2024 study describes creating multiple randomized SMILES representations before an 80/20 split, illustrating why molecule-identity-level leakage checks matter.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arxiv.org

+1



The score tie is resolved by feasibility: AqSolDB has the smallest dataset, shortest domain-learning curve, simplest measurement definition, and lowest implementation risk. MassSpecGym has the stronger ready-made benchmark controversy but is considerably harder to reproduce.

## 4. Deep dive: the three strongest candidates

### Candidate F — Solubility-conditioned molecular graph generation

Rank 1

Lowest execution risk · Strong measurement-scarcity argument

Proposed project title: Uncertainty-Aware, Constraint-Guided Molecular Graph Generation from Scarce Experimental Solubility Data

Problem statement. Given a target aqueous solubility, generate multiple novel, chemically valid molecular structures likely to exhibit that solubility. The research question is whether explicit chemical constraints and uncertainty-aware conditioning improve property alignment and structural novelty over a small conditional graph generator trained only on limited experimental measurements.

#### Formal setup

Let \\(G=(V,E,\mathbf{x},\mathbf{e})\\) be a molecular graph, with atoms as vertices and bonds as edges.

- Training inputs: \\(D=\\{(G_i,y_i)\\}\_{i=1}^{N}\\), with \\(y_i=\log\_{10} S_i\\), where \\(S_i\\) is the measured aqueous solubility in mol/L.
- Generation condition: desired solubility \\(y^\ast\\), optionally a heavy-atom-count range.
- Generated output: a labeled molecular graph sampled from \\(p\_\theta(G\mid y^\ast)\\).
- Hard constraints: allowable elements, atom valence, bond types, connectedness, maximum graph size, RDKit sanitization.
- Soft goals: target-property alignment, novelty, diversity, synthetic accessibility, predictive uncertainty.

The practical target is not a claim of discovering experimentally verified high-solubility molecules. It is a ranked virtual set of candidates for subsequent measurement.

#### Dataset

[AqSolDB — Harvard Dataverse](https://doi.org/10.7910/DVN/OVHAW8?utm_source=chatgpt.com)

Measured compounds

# 9,982

Archival download

# 3.7 MB

License

CC0 1.0

Format

TAB / CSV

All four facts confirmed at the official Dataverse record and associated paper. The released TAB file has 26 variables.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://doi.org\&sz=32)

Harvard Dataverse

+1

100×-compute argument: Measurements were assembled from nine existing experimental datasets. Creating another experimentally verified solubility label requires a laboratory measurement or access to an independently existing record; generating more SMILES, running a neural predictor, or computing descriptors does not establish that measurement. The original authors also report that experimental error metadata were unavailable for some source records.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

PMC

+1



Validity checker: [RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html?utm_source=chatgpt.com) checks whether a graph can be interpreted as a chemically consistent molecule, including valence and sanitization; it can also generate canonical SMILES and fingerprints. Estimated CPU runtime is approximately 0.2–5 ms per small molecule, depending on graph size and processing. This is my planning estimate, not a published or measured benchmark. It does not verify aqueous solubility.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.rdkit.org\&sz=32)

The RDKit 2026.09.1 documentation



Baselines and code:

| Baseline                                  | Family                | Public reference                                                                               |
| ----------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------- |
| Small conditional molecular graph VAE     | VAE                   | [JT-VAE](https://github.com/wengong-jin/icml18-jtnn?utm_source=chatgpt.com)                    |
| Small conditional discrete graph denoiser | Diffusion             | [DiGress](https://github.com/cvignac/DiGress?utm_source=chatgpt.com)                           |
| Graph diffusion with property encoding    | Diffusion transformer | [Graph DiT](https://github.com/liugangcode/Graph-DiT?utm_source=chatgpt.com)                   |
| Conditional autoregressive graph decoder  | Autoregressive        | A compact implementation of your own, using graph-generation methods from the references above |

These are research reference implementations, not guaranteed Colab-ready drop-in baselines. In particular, JT-VAE's original repository specifies Python 2.7, while the DiGress repository uses an older CUDA/PyTorch stack and additional compiled dependencies. A small clean PyTorch implementation is much safer for your environment-setup requirement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+1



#### Realistic methodological levers

Lever 1 — Constraint-aware graph decoding

Compare post-hoc rejection of invalid generated graphs with a decoder that masks atom/bond actions violating elementary valence and connectivity constraints. Measure valid unique molecules per 1,000 generation attempts, rejection rate, runtime, novelty, and diversity.

Lever 2 — Uncertainty-aware property guidance

Train a small ensemble of property regressors on experimental labels. During generation, prefer candidates whose predicted solubility is close to the condition while penalizing high model disagreement. Compare to guidance from one predictor and no guidance.

Lever 3 — Leakage-resistant evaluation

Compare identity-disjoint random splits, Bemis–Murcko scaffold splits, and a held-out evaluation predictor. Test whether apparent condition satisfaction survives when the scoring model is independent of the guidance model.

Memorization protocol. Normalize molecular identities using RDKit standardization and canonical isomeric SMILES or standardized InChIKey, consistently handling salts, stereochemistry, charge and tautomers. Report exact matches to training structures, exact duplicates among generated structures, scaffold overlap, and maximum training-neighbor ECFP Tanimoto similarity. Report near-duplicate fractions at predeclared thresholds such as 0.8 and 0.9. Crucially, split before augmentation, and group all alternative SMILES for the same molecule together.

Evaluation: validity, uniqueness, exact/scaffold novelty, ECFP novelty, diversity, property-target error under two independently trained regressors, calibration on held-out real measurements, and validity per CPU/GPU-second. If a predictor is used to guide sampling, evaluating exclusively with that same predictor is circular.

Estimated free-T4 budget — one controlled pilot

| Work                                             | GPU-hours |
| ------------------------------------------------ | --------- |
| Compact graph VAE training                       | 1.0–1.8   |
| One guided-generation improvement and evaluation | 0.5–1.0   |
| Limited ablation and troubleshooting reserve     | 0.5–0.7   |
| Total planned                                    | 2.0–3.5   |

Estimates only. Assumes a small graph vocabulary, modest architecture, restricted atom counts and no large hyperparameter search. Dataset preprocessing and most RDKit checks run on CPU.

Why a practitioner cares: A formulation chemist or materials researcher can use generated molecules as candidates for dissolution screening, subject to feasibility and safety review. An actual practitioner would verify promising candidates using a standardized solubility experiment, not merely a model prediction.

Main risks and fallback: The dataset is noisy and small, meaning a generator may simply memorize common soluble compounds or exploit regressor errors. The fallback is a simpler conditional graph VAE with no sophisticated guidance, plus a rigorous split/novelty audit as the methodological contribution. An evaluation-centered paper demonstrating why certain reported property gains disappear under leakage-resistant testing can be more defensible than an unsupported state-of-the-art claim.

### Candidate H — Mass-spectrum-conditioned molecular generation

Rank 2

Strongest benchmark-critique opportunity · Higher technical risk

Proposed project title: Formula-Constrained De Novo Molecular Graph Generation from Experimental Mass Spectra Under Leakage-Resistant Evaluation

Problem statement. Given an experimentally measured tandem mass spectrum, and optionally the elemental formula of an unknown compound, generate possible molecular graphs that could explain the observation. The central problem is an inverse mapping from measured physical evidence to a structured chemical object.

#### Formal setup

- Input space: a set of observed peaks \\(X=\\{(m_j,I_j)\\}\_{j=1}^{k}\\), with mass-to-charge values and intensities; optional formula \\(F\\).
- Output space: molecular graphs \\(G\\).
- Conditions: \\(X\\) and optionally \\(F\\), including instrument information where consistently available.
- Hard constraints: RDKit validity, atom composition matching \\(F\\), charge and connectivity rules.
- Soft objectives: compatibility between measured peaks and the predicted fragmentation behavior.

Formally, learn \\(p\_\theta(G\mid X,F)\\). The spectrum is the condition, not the generated object. The generated object is a molecular graph.

#### Dataset

[MassSpecGym v1.5 on Hugging Face](https://huggingface.co/datasets/roman-bushuiev/MassSpecGym/tree/main/data?utm_source=chatgpt.com)

| Attribute             | Finding                                                                  |
| --------------------- | ------------------------------------------------------------------------ |
| Spectral observations | 231,104 in the original benchmark                                        |
| Distinct molecules    | 32,010 in the original benchmark                                         |
| Main file             | `MassSpecGym1.5.tsv`                                                     |
| Main-file size        | 261 MB                                                                   |
| Full repository       | About 51.6 GB, mostly unnecessary for the scoped project                 |
| Declared license      | MIT                                                                      |
| Format                | TSV with spectrum information, molecular identity and benchmark metadata |

Counts come from published benchmark statistics; file size and license are confirmed at the hosting source. The exact post-cleaning record count for v1.5 should be checked separately rather than assumed identical to the earlier release.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://academic.oup.com\&sz=32)

Oxford Academic

+2



100×-compute argument: Experimental MS/MS measurements require acquiring samples and instrument readings. One can computationally generate unlimited molecular graphs or predicted spectra, but that does not create more experimentally measured spectrum–molecule pairs. The DiffMS authors explicitly contrast abundant synthetic molecular pretraining pairs with the limited availability of experimental structure–spectrum pairs.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://proceedings.mlr.press\&sz=32)

Proceedings of Machine Learning Research



Validity checker: RDKit chemical sanitization and molecular-formula computation check basic structure and formula consistency, estimated 0.2–5 ms per candidate on CPU. For spectrum agreement, the MassSpecGym framework supplies evaluation infrastructure; [ms-pred/ICEBERG](https://github.com/samgoldman97/ms-pred?utm_source=chatgpt.com) offers a learned spectrum simulator. Inference speed is architecture/hardware-dependent and not verified here; I would reserve approximately 0.1–1 second per candidate as an initial GPU planning allowance, subject to measurement. Predicted-spectrum agreement is only a surrogate for real fragmentation.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+1



Baselines and code:

| Baseline                              | Family                              | Code                                                                                                       |
| ------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| DiffMS                                | Formula-restricted graph diffusion  | [MIT Coley group repository](https://github.com/coleygroup/DiffMS?utm_source=chatgpt.com)                  |
| MassSpecGym official methods          | Benchmark reference implementations | [MassSpecGym](https://github.com/pluskal-lab/MassSpecGym?utm_source=chatgpt.com)                           |
| Compact peak-set encoder + graph CVAE | VAE                                 | Your small implementation, using the MassSpecGym data interface                                            |
| Conditional discrete graph denoiser   | Diffusion                           | Adapt the graph-denoising approach in [DiGress](https://github.com/cvignac/DiGress?utm_source=chatgpt.com) |

The official DiffMS architecture relies on substantial molecular pretraining. Do not use reproduction of full DiffMS as your four-week implementation target. Use it as an upper reference and compare a genuinely small generator against simpler alternatives.

Open levers: (1) hard formula-constrained sampling versus unconstrained generation followed by rejection; (2) peak-set encoding and attention versus simple pooled spectra; (3) consistency between alternative molecule identity standardizations; (4) evaluation that blocks training/test overlap through canonical molecules or structural families.

Memorization check: Standardize each generated and reference molecule, then test exact canonical identity, same chemical formula with distinct connectivity, identical scaffold, and maximum molecular fingerprint similarity. Also test for spectral reuse and cross-split molecule overlap: multiple spectra of one molecule must not masquerade as independent novel molecular structures.

Estimated GPU budget: Approximately 2.5–3.8 T4 GPU-hours for a deliberately small model on a reduced, molecule-disjoint training subset, not for a full DiffMS reproduction. A 261 MB dataset download is plausible on free Colab, but download speed and end-to-end environment setup were not measured. Installing just PyTorch/RDKit and processing the TSV directly is more likely to meet five minutes than reproducing the complete software stack.

Why a practitioner cares: An analytical chemist can use proposed molecular graphs to narrow down candidates for an unknown measured compound and test them against additional fragmentation measurements or authentic reference standards.

Main risks and fallback: This is a harder inverse problem than solubility conditioning. Many molecules share the same molecular formula, some measurements are ambiguous, and evaluation is unusually fragile. The June 2026 benchmark audit found leakage, shortcut learning and implementation issues across many published evaluations; use MassSpecGym v1.5 and its corrected procedures from the start. If conditional graph generation proves too difficult, fall back to a minimal formula-constrained graph VAE—not merely a retrieval system, because retrieval alone would not satisfy your generative-project requirement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arXiv

+1



### Candidate G — Experimentally conditioned flash-point molecular design

Rank 3

Strong industrial motivation · Weaker generative-model literature

Proposed project title: Generating Novel Molecular Structures Under Experimentally Measured Flash-Point Constraints

Problem statement. Given a desired minimum flash point, generate chemically valid molecular graphs that a learned property model predicts will meet that safety-relevant threshold. The objective is not to declare a new chemical safe; it is to create candidate structures that can be further evaluated for formulation and handling requirements.

#### Formal setup

Training examples are \\((G_i,T_i)\\), where \\(T_i\\) is an experimentally reported flash point, generally in kelvin. Generate \\(G\sim p\_\theta(G\mid T\geq T\_{\min})\\), or condition on a continuous target. Include atom and bond constraints, size limitations, structural novelty, and preferably a fixed flash-point measurement protocol.

#### Dataset

[Sun et al. — experimental flash-point dataset and supporting materials](https://doi.org/10.6084/m9.figshare.9275210?utm_source=chatgpt.com)

| Attribute                    | Finding                                                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Published integrated dataset | 10,575 unique compounds                                                                                                        |
| Available Figshare archive   | 170.28 MB                                                                                                                      |
| Archive license              | CC BY 4.0                                                                                                                      |
| Supporting code              | [MoleProp](https://github.com/uw-cmg/MoleProp?utm_source=chatgpt.com) — MIT                                                    |
| File format                  | Published tabular molecular/measurement data plus associated support files; individual archive file formats not fully verified |

The 10,575 count is confirmed by the associated paper, and 170.28 MB and CC BY 4.0 by Figshare. Important qualification: the original integrated work drew partly on proprietary DIPPR data; the authors indicate that proprietary DIPPR records were removed from the publicly shared materials. Therefore 10,575 is not a verified count of redistributable, labeled examples in the public archive. This should be treated as a feasibility-audit risk, not concealed by quoting the publication count.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubmed.ncbi.nlm.nih.gov\&sz=32)

PubMed

+3



100×-compute argument: Flash point is a physical measurement of a liquid's tendency to produce an ignitable vapor under specified test conditions. Running extra models cannot create additional verified experimental flash-point results, and the literature emphasizes that large numbers of chemical substances lack such measurements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubmed.ncbi.nlm.nih.gov\&sz=32)

PubMed



Validity checker: RDKit for atomic/bond validity, valence, connectedness and canonical identities. Estimated 0.2–5 ms per sample on CPU. For property-target alignment, train a regression surrogate; there is no comparable free instantaneous experimental-flash-point checker. The safety interpretation of a predicted value must remain explicitly limited.

Baseline generators: a compact conditional graph VAE based on [JT-VAE](https://github.com/wengong-jin/icml18-jtnn?utm_source=chatgpt.com) ideas, or a compact discrete denoiser based on [DiGress](https://github.com/cvignac/DiGress?utm_source=chatgpt.com). The associated [MoleProp](https://github.com/uw-cmg/MoleProp?utm_source=chatgpt.com) project provides MPNN/GCNN property-prediction references, not a ready-made flash-point graph generator.

Open levers: (1) explicitly condition on the experimental method or restrict the dataset to a comparable testing protocol; (2) generate with property guidance using an ensemble of independent predictors rather than a single model; (3) test chemical-family extrapolation instead of solely random molecule splits.

Memorization check: identical to the AqSolDB graph-identity protocol, with an additional split by chemical family. Report exact identity, scaffold overlap and nearest-neighbor fingerprint similarity, together with the percentage of candidate predictions outside the predictor's reliable domain.

Estimated compute: 2.0–3.5 T4 GPU-hours, assuming a cleaned subset of at most roughly 10,000 small graphs and a modest conditional generator. This estimate excludes potentially time-consuming legal/provenance auditing and harmonization of flash-point measurement protocols.

Why a practitioner cares: Chemical engineers and formulators can use a generated list to explore candidate solvents or intermediates. Testing requires standardized physical flash-point measurement. A predicted flash point must never replace the appropriate laboratory or safety assessment.

Main risks and fallback: Mixing open-cup and closed-cup measurements introduces label inconsistency; chemical class imbalance introduces distribution-shift risk; the accessible public subset needs auditing. If cleaning makes the dataset too small or inconsistent, switch to AqSolDB while retaining the same graph-generation infrastructure.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+1



## 5. Starter reading list for the top recommendation

These 20 works span the measured-solubility problem, molecular graph generation, conditional methods, and evaluation integrity. I included some adjacent domains intentionally: you need a research narrative showing both where the methods came from and why your measurement-limited setting differs from common benchmarks.

License column convention: It records the license of the linked code or data artifact when I could verify it. It does not mean the paper itself has that license. “Not verified” means I found the work but could not verify a suitable license; it is not a declaration that no license exists. Limitations include both author-acknowledged boundaries and research questions I would audit.

| #  | Verified paper, venue/year and DOI/arXiv                                                                                                                                                                       | Code or data                                                                                                                                          | Artifact license                   | Known limitation or issue to investigate                                                                          |
| -- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1  | [ESOL: Estimating Aqueous Solubility Directly from Molecular Structure](https://doi.org/10.1021/ci034243x?utm_source=chatgpt.com) — J. Chem. Inf. Comput. Sci., 2004                                           | [Data](https://acs.figshare.com/articles/dataset/ESOL_Estimating_Aqueous_Solubility_Directly_from_Molecular_Structure/7944677?utm_source=chatgpt.com) | Dataset-specific terms: check      | Descriptor model limits structural expressiveness; small older benchmark                                          |
| 2  | [MoleculeNet: A Benchmark for Molecular Machine Learning](https://doi.org/10.1039/C7SC02664A?utm_source=chatgpt.com) — Chemical Science, 2018                                                                  | [DeepChem](https://github.com/deepchem/deepchem?utm_source=chatgpt.com)                                                                               | Not verified here                  | Property prediction framework, not a generation benchmark                                                         |
| 3  | [Automatic Chemical Design Using a Data-Driven Continuous Representation of Molecules](https://doi.org/10.1021/acscentsci.7b00572?utm_source=chatgpt.com) — ACS Central Science, 2018                          | [Chemical VAE](https://github.com/the-matter-lab/chemical_vae?utm_source=chatgpt.com)                                                                 | Not verified here                  | SMILES-based generation can produce invalid molecular representations                                             |
| 4  | [Junction Tree Variational Autoencoder for Molecular Graph Generation](https://arxiv.org/abs/1802.04364?utm_source=chatgpt.com) — ICML, 2018                                                                   | [JT-VAE](https://github.com/wengong-jin/icml18-jtnn?utm_source=chatgpt.com)                                                                           | MIT                                | Old Python/PyTorch dependencies; not directly a small-data solubility benchmark                                   |
| 5  | [AqSolDB, a Curated Reference Set of Aqueous Solubility and 2D Descriptors for a Diverse Set of Compounds](https://doi.org/10.1038/s41597-019-0151-1?utm_source=chatgpt.com) — Scientific Data, 2019           | [AqSolDB](https://doi.org/10.7910/DVN/OVHAW8?utm_source=chatgpt.com)                                                                                  | CC0 data                           | Experimental provenance, heterogeneity and uncertain reliability of singleton observations                        |
| 6  | [GuacaMol: Benchmarking Models for de Novo Molecular Design](https://doi.org/10.1021/acs.jcim.8b00839?utm_source=chatgpt.com) — J. Chem. Inf. Model., 2019                                                     | [GuacaMol](https://github.com/BenevolentAI/guacamol?utm_source=chatgpt.com)                                                                           | Repository license: verify         | Optimization against benchmark scores need not imply real experimental improvement                                |
| 7  | [Molecular Sets (MOSES): A Benchmarking Platform for Molecular Generation Models](https://doi.org/10.3389/fphar.2020.565644?utm_source=chatgpt.com) — Frontiers in Pharmacology, 2020                          | [MOSES](https://github.com/molecularsets/moses?utm_source=chatgpt.com)                                                                                | Repository license: verify         | Distributional similarity and uniqueness do not verify target measured properties                                 |
| 8  | [GraphAF: A Flow-based Autoregressive Model for Molecular Graph Generation](https://arxiv.org/abs/2001.09382?utm_source=chatgpt.com) — ICLR, 2020                                                              | [GraphAF](https://github.com/DeepGraphLearning/GraphAF?utm_source=chatgpt.com)                                                                        | Not verified                       | Sequential graph construction; limited direct measurement-conditioned validation                                  |
| 9  | [MoFlow: An Invertible Flow Model for Generating Molecular Graphs](https://arxiv.org/abs/2006.10137?utm_source=chatgpt.com) — KDD, 2020                                                                        | [MoFlow](https://github.com/calvin-zcx/moflow?utm_source=chatgpt.com)                                                                                 | Not verified                       | Post-generation valence corrections complicate exact modeling claims                                              |
| 10 | [Assessing Graph-based Deep Learning Models for Predicting Flash Point](https://doi.org/10.1002/minf.201900101?utm_source=chatgpt.com) — Molecular Informatics, 2020                                           | [Code/data links](https://github.com/uw-cmg/MoleProp?utm_source=chatgpt.com)                                                                          | MIT code; CC BY 4.0 public archive | Nonuniform experimental protocols; proprietary-source exclusion in shared dataset                                 |
| 11 | [Score-based Generative Modeling of Graphs via the System of Stochastic Differential Equations](https://arxiv.org/abs/2202.02514?utm_source=chatgpt.com) — ICML, 2022                                          | [GDSS](https://github.com/harryjo97/GDSS?utm_source=chatgpt.com)                                                                                      | Not verified                       | Sampling cost; generic graph scores do not test experimentally measured properties                                |
| 12 | [DiGress: Discrete Denoising Diffusion for Graph Generation](https://arxiv.org/abs/2209.14734?utm_source=chatgpt.com) — ICLR, 2023                                                                             | [DiGress](https://github.com/cvignac/DiGress?utm_source=chatgpt.com)                                                                                  | MIT                                | Authors report a September 2026 implementation discrepancy affecting the feed-forward dimension                   |
| 13 | [Conditional Diffusion Based on Discrete Graph Structures for Molecular Graph Generation](https://doi.org/10.1609/aaai.v37i4.25549?utm_source=chatgpt.com) — AAAI, 2023                                        | Official implementation not verified                                                                                                                  | Not verified                       | Conditioning/evaluation may depend on imperfect property surrogates                                               |
| 14 | [Graph Diffusion Transformers for Multi-Conditional Molecular Generation](https://arxiv.org/abs/2401.13858?utm_source=chatgpt.com) — NeurIPS, 2024                                                             | [Graph DiT](https://github.com/liugangcode/Graph-DiT?utm_source=chatgpt.com)                                                                          | Not verified                       | Larger model/benchmark tasks; target-property metrics are not new laboratory measurements                         |
| 15 | [Predicting Small Molecules Solubility on Endpoint Devices Using Deep Ensemble Neural Networks](https://doi.org/10.1039/D3DD00217A?utm_source=chatgpt.com) — Digital Discovery, 2024                           | AqSolDB; official implementation not verified                                                                                                         | AqSolDB: CC0                       | Multiple randomized SMILES are created before an 80/20 data split; molecule-level leakage deserves inspection     |
| 16 | [MassSpecGym: A Benchmark for the Discovery and Identification of Molecules](https://arxiv.org/abs/2410.23326?utm_source=chatgpt.com) — NeurIPS Datasets & Benchmarks, 2024                                    | [MassSpecGym](https://github.com/pluskal-lab/MassSpecGym?utm_source=chatgpt.com)                                                                      | MIT                                | Multiple spectra per structure; original evaluation procedures subsequently audited                               |
| 17 | [DiffMS: Diffusion Generation of Molecules Conditioned on Mass Spectra](https://proceedings.mlr.press/v267/bohde25a.html?utm_source=chatgpt.com) — ICML, 2025                                                  | [DiffMS](https://github.com/coleygroup/DiffMS?utm_source=chatgpt.com)                                                                                 | MIT                                | Depends on extensive pretraining, beyond a tiny Colab reproduction                                                |
| 18 | [A Collaborative Constrained Graph Diffusion Model for the Generation of Realistic Synthetic Molecules](https://doi.org/10.1038/s42256-026-01229-5?utm_source=chatgpt.com) — Nature Machine Intelligence, 2026 | [CoCoGraph](https://github.com/manurubo/CoCoGraph?utm_source=chatgpt.com)                                                                             | MIT                                | Chemical validity is not experimental property verification; large synthetic libraries still lack measured labels |
| 19 | [Invariant Conditional Molecular Generation Under Distribution Shift](https://doi.org/10.1609/aaai.v40i26.39334?utm_source=chatgpt.com) — AAAI, 2026                                                           | Official code not verified                                                                                                                            | Not verified                       | Stronger distribution-shift results still require checking transfer to experimental solubility labels             |
| 20 | [MassSpecGym in the Wild: Uncovering and Correcting Evaluation Pitfalls in AI-Driven Molecule Discovery](https://arxiv.org/abs/2606.19624?utm_source=chatgpt.com) — arXiv preprint, 2026                       | [Corrected benchmark](https://github.com/pluskal-lab/MassSpecGym?utm_source=chatgpt.com)                                                              | MIT code                           | Audit rather than generative model; demonstrates leakage, shortcuts and metric divergence in prior work           |

Several especially consequential details are documented at primary sources: the DiGress implementation discrepancy is disclosed in its own repository; the solubility augmentation sequence appears in the 2024 paper; the benchmark audit explicitly reports its 17-of-26 finding; and CoCoGraph's May 2026 publication and released training/sampling code are confirmed.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+3



For your immediate research preparation, the highest-priority reading sequence is AqSolDB → JT-VAE → DiGress → Graph DiT → the 2024 solubility ensemble paper → CoCoGraph → the 2026 distribution-shift paper. GuacaMol and MOSES establish useful evaluation conventions, while MassSpecGym's audit is valuable for learning how a seemingly strong experiment can be misleading.

## 6. Recommended four-week experimental design

I would narrow the actual research contribution to one controlled question:

> Can constraint-aware generation and uncertainty-aware guidance produce a larger fraction of valid, structurally novel molecules matching a requested solubility range than a small conditional graph VAE, when evaluation uses scaffold-disjoint experimental data and an independent property predictor?

That is sufficiently specific for a conference-style paper and does not require competing directly against enormous pretrained models.

| Week | Goal                                                                                             | Mandatory deliverable                                              |
| ---- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| 16   | Audit AqSolDB, standardize molecules, establish splits and train the plain conditional graph VAE | Reproducible data pipeline, first valid samples, W&B baseline      |
| 17   | Implement constraint-aware generation, run matched-budget comparison                             | Baseline vs constrained generation with fixed sampling count       |
| 18   | Add uncertainty-aware guidance and limited ablations                                             | No-guidance/single-predictor/ensemble-guidance comparison          |
| 19   | Independent evaluation, memorization audit, manuscript and public repository                     | Tables, plots, examples, reproducibility instructions, paper draft |

A practical experiment matrix could look like this:

| Method                                       | Chemical constraints    | Property guidance        | Primary hypothesis                     |
| -------------------------------------------- | ----------------------- | ------------------------ | -------------------------------------- |
| Baseline conditional VAE                     | Post-hoc validity check | None beyond conditioning | Reference                              |
| VAE + constrained decoder                    | During generation       | None beyond conditioning | Higher valid-sample yield              |
| VAE + constrained decoder + single predictor | During generation       | Point estimate           | Better apparent target matching        |
| VAE + constrained decoder + ensemble         | During generation       | Penalize uncertainty     | Better independent-evaluator agreement |

Keep the architecture, training data, optimization budget, candidate count, and evaluation splits consistent. Do not report an apparent improvement without showing its cost in diversity and near-duplicate frequency.

A defensible final result could be a negative one. For example, if property guidance raises the score from the guidance model but fails on an independent evaluator, while also increasing near-memorization, documenting that failure carefully is a meaningful methodological outcome.

## 7. Claims to verify at the primary source first

These are ordered by how seriously an incorrect assumption could derail your project.

0 of 12 verification tasks checked

Reset

AqSolDB's exact released molecular identities: remove invalid, duplicate, disconnected, charged or otherwise incompatible records; record the usable count.

Whether AqSolDB labels are adequately comparable across temperatures, pH, crystalline states and source measurement protocols.

Whether the 2024 augmented-solubility study kept alternate SMILES of the same compound together across train/test splits; do not infer actual leakage from the methods paragraph alone.

Whether each selected molecular generator can run on the current free-Colab Python/CUDA environment within five minutes of setup.

One T4 smoke test: 100–500 training steps, peak VRAM, step time, sample validity and projected full-run duration.

Whether the public flash-point archive excludes proprietary DIPPR records, and the exact number of legal, usable labeled samples remaining.

Whether public flash-point observations identify open-cup versus closed-cup methodology, with enough usable data after separation.

The exact column schema and standardized identity rules of MassSpecGym v1.5, including corrected train/validation/test partitions.

CPU runtime of the chosen RDKit validation, graph canonicalization, nearest-neighbor and optional spectrum-checking procedures on your sample sizes.

Code and data licenses separately: do not assume a repository's MIT license transfers to third-party source datasets.

The specific R3 paper counts for 2023, 2024, 2025 and January–October 2026, using a reproducible scholarly search query.

Whether claimed target-property gains remain when the evaluator is independently trained, chemically scaffold-disjoint and well calibrated.

## Final decision

Choose AqSolDB + a compact conditional graph VAE + chemical constraints + uncertainty-aware property guidance as the proposal topic, with leakage-resistant evaluation as an essential research contribution rather than an afterthought.

Keep MassSpecGym v1.5 as your alternative if the literature audit reveals that solubility-conditioned generation is too well explored for a useful contribution. I would not choose the open CktBench or SimBench benchmarks for this particular course specification, despite their superior engineering-simulator appeal, because their freely generated simulated labels undermine the exact scarcity argument your course is asking you to defend.

The main unresolved issue is not whether this topic has enough mathematics or model complexity—it does. It is whether your solubility-guided generator can demonstrate useful, independently evaluated improvements with only 9,982 experimental records. That is the question I would make central to your Week 6–15 feasibility and proposal work.
