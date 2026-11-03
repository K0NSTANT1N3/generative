# Project idea: constrained generation of glycans with desired properties

Prepared: **26 October 2026**, using the primary-source research saved in the [glycan audit](glycan_np_audit.md). This is a focused project brief, dataset list and reading guide, matching the bee-project brief.

## 1. What the project is about

**Generate new, chemically consistent branched glycan structures, optionally conditioned on a desired motif or predicted binding to a selected lectin.** Glycans are carbohydrates built from sugar units connected into branched structures. Lectins are proteins that recognize particular carbohydrate features.

The research question is:

> Can a small generator produce diverse, structurally valid glycans that satisfy a requested condition, while avoiding copies and near-copies of its training structures?

Compare a small unconditional generator, a conditional generator, and conditional generation with explicit structural constraints. The contribution would be **reliable constrained generation and evaluation**, especially structural-family generalization, near-duplicate detection and resistance to exploiting a property predictor's mistakes.

There are two sensible scopes:

- **Simpler starting scope:** condition on an explicitly defined structural motif, such as a chosen sugar/linkage pattern. These labels can be computed from structures, so experimental binding data are unnecessary. This tests structural control, not biological function.
- **Functional extension:** condition on predicted binding to one selected lectin, or preference for it over another lectin. This requires measured binding data and a validated predictor. Improved predicted binding is not experimental proof of binding.

**Glycan generation is not an empty research area.** Existing work includes spectra-to-glycan generation, inference from lectin fingerprints, masked structure completion and historical predictor-guided mutation search. A broad “first glycan generator” claim would be wrong. The potential gap is a carefully evaluated, small-compute approach to controlled whole-structure generation; its exact novelty must be compared with those precedents.

## 2. Public datasets and download links

**Use GlyCosmos or the processed GlycanGT data first for structure training.** Add a binding dataset only if you pursue the functional extension.

Counts below distinguish unique structures from interaction measurements, spectra and dataset collections. Values come from the saved primary-source audit; they are not all independently recounted here. Sources overlap, so their counts must not be added together.

### Structure data: usable without a binding predictor

| Dataset/source | What you get | Access, license and caveat |
|---|---|---|
| **[GlyCosmos](https://glycosmos.org/download)**; [direct glycan CSV](https://download.glycosmos.org/glycosmos_glycans_list.csv) | Glycan accessions, structural representations including IUPAC/WURCS, and annotations. The October 2026 download listing checked in the audit showed **79.71 MB** for the full CSV. | **CC BY 4.0**, [official license](https://glycosmos.org/license). Public download without an application. Filter ambiguous, disconnected or unsupported structures; the number of fully specified usable trees must be counted after filtering. |
| **[GlyTouCan](https://glytoucan.org/)**; [terms](https://doc.glytoucan.org/en/Terms-and-Conditions) | International registry of glycan structures and identifiers; includes partially specified entries. | **CC0** according to its terms. Public reading is separate from account-based deposition. GlyCosmos provides a convenient bulk route for related registered structures; these are overlapping resources, not independent datasets. Exact standalone bulk size was not established in the audit. |
| **[GlycanGT processed data](https://github.com/matsui-lab/GlycanGT/tree/main/data/clean)**; [versioned source archive](https://zenodo.org/records/18636040) | The paper reports **83,739** processed glycan graphs; the repository reports **83,740**. GlyCosmos-derived, filtered for complete structural information. Public clean-data files and preprocessing code. | GlyCosmos source **CC BY 4.0**; Zenodo archive **CC BY 4.0 in API metadata**; repository code **Apache-2.0**. Source ZIP **7,688,791 bytes** in the audit. Pretrained Hugging Face weights were gated; that does not gate the public training data. |
| **[SweetTalk released structures](https://github.com/midas-wyss/sweettalk)**; [direct CSV](https://raw.githubusercontent.com/midas-wyss/sweettalk/master/datasets/combined_database_long.csv) | Historical sequence/label dataset. The downloaded CSV had **21,296 records and 13,541 distinct literal target strings**, rather than the final paper's **19,299 unique glycans**. | Immediate CSV, approximately **1.56 MB**. Repository **Apache-2.0**; separate upstream source rights were not comprehensively established. Useful historical baseline, with a paper-versus-release version mismatch. |

### Binding and labelled benchmark data

| Dataset/source | What it contains | Access, license and fit |
|---|---|---|
| **[GlyGen Glycan Array Data Repository](https://glygen.ccrc.uga.edu/ggarray/)** | Public glycan-array studies with binding measurements. The checked portal listed **989 datasets and 533 glycans**. “Dataset” here means an array/study collection, not one molecule or measurement. | Portal explicitly states **CC BY 4.0**. Promising source for functional labels, but a complete bulk training-table download was **not verified**. Check individual downloadable studies and select a consistent assay context before committing to binding-conditioned generation. |
| **[LectinOracle released data](https://github.com/BojarLab/LectinOracle/tree/main/data)** | **564,647 unique protein–glycan interactions** reported by the project, with array data, metadata, protein embeddings and a pretrained predictor. | Public CSV/PKL/PT files. The audited main array CSV was approximately **12.76 MB**, stored embeddings approximately **16.64 MB**. Code **MIT**; separate reuse terms for every underlying CFG/Imperial measurement were **not established**. Legacy repository points to the maintained glycowork implementation. |
| **[SweetNet task data](https://github.com/BojarLab/SweetNet)** | Glycan taxonomy/property tasks and a viral-binding task with **126,894 HA–glycan interactions** from 587 arrays. This is not one uniformly labelled dataset. | Public CSVs; code **MIT**. Separate original measurement-data license not fully established. Useful predictor baselines; viral binding is a different target from an arbitrary lectin. |
| **[GlycanML benchmark](https://github.com/GlycanML/GlycanML)**; [project page](https://glycanml.github.io/project/) | Official splits and data for **11 prediction tasks**, including taxonomy, immunogenicity, glycosylation and affinity. | Public repository, code **Apache-2.0**. Task-specific sample counts, aggregate bytes and separate data licenses were not fully verified. Choose one task and inspect its labels; class counts are not sample counts. |

### Alternative task: generate structures from spectra

| Dataset | What you get | Access and caveat |
|---|---|---|
| **[GlycoBART training release](https://zenodo.org/records/15741423)**; [spectrum XLSX](https://zenodo.org/records/15741423/files/dataset.xlsx?download=1); [glycan CSV](https://zenodo.org/records/15741423/files/glycans_antennae.csv?download=1) | Paper describes CandyCrunch v2 with **510,160 spectra and 3,590 glycan identities** before its described filtering. Released XLSX **1,509,745,314 bytes** and glycan CSV **807,866 bytes**. | **CC BY 4.0**, confirmed in Zenodo API metadata. Public downloads. Suitable for spectrum-conditioned identification, which is a different project from designing a new glycan for desired binding. Full GlycoBART retraining is a poor fit for the four-hour budget. |

**Practical selection:** begin with a filtered GlyCosmos export or GlycanGT's processed structures. Do not collect every source before implementing a baseline. A binding table should preserve the glycan identity, lectin identity, measured response and assay context. Array RFU values are not automatically interchangeable across studies or equivalent to solution-phase affinity.

## 3. Papers by researchers who trained relevant models

| Paper, authors and year | What they trained/generated | Why it matters; paper and code |
|---|---|---|
| **LectinOracle: A Generalizable Deep Learning Model for Lectin–Glycan Binding Prediction** — Jon Lundstrøm, Emma Korhonen, Frédérique Lisacek, Daniel Bojar; Gothenburg/Geneva/SIB; **Advanced Science, 2022**. | Binding predictor combining a glycan graph network with fixed protein-language-model embeddings. **Does not generate glycans.** | Closest starting point for a binding surrogate. [Paper](https://doi.org/10.1002/advs.202103807); [code/data](https://github.com/BojarLab/LectinOracle); maintained models in [glycowork](https://github.com/BojarLab/glycowork). |
| **A Boltzmann model predicts glycan structures from lectin binding** — Aria Yom, Austin Chiang, Nathan E. Lewis; UC San Diego/Augusta; **Analytical Chemistry, 2024**. | Second-order Markov glycan sampling with a Boltzmann motif model, ranking candidate structures given observed lectin/antibody fingerprints. | **Actual inverse structure inference already exists.** It infers an unknown structure from observations, rather than designing a new selective binder. [Paper](https://doi.org/10.1021/acs.analchem.3c04992); [free full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11162346/). No official implementation located in the audit. |
| **Transformer-based Deep Learning for Glycan Structure Inference from Tandem Mass Spectrometry** — Ejas Althaf Abtheen, Arun Singh, Shyam Sriram, Changyou Chen, Sriram Neelamegham, Rudiyanto Gunawan; Buffalo; **2025 preprint**. | **GlycoBART generates glycan sequences conditioned on MS/MS spectra**; companion GlycoBERT classifies known structures. | Direct sequence-generation precedent, but analytical identification rather than functional design. [Paper](https://doi.org/10.1101/2025.07.02.662857); [code](https://github.com/CABSEL/glycotrans); [weights](https://huggingface.co/CABSEL/glycobart). |
| **Modeling All-Atom Glycan Structures via Hierarchical Message Passing and Multi-Scale Pre-training** — Minghao Xu, Jiaze Song, Keming Wu, Xiangxin Zhou, Bin Cui, Wentao Zhang; Peking; **ICML 2025**. | GlycanAA learns atom/sugar representations using masked recovery, then predicts properties. | Representation/pretraining reference; **not demonstrated whole-tree or coordinate generation**. [Paper](https://arxiv.org/abs/2506.01376); [code](https://github.com/kasawa1234/GlycanAA). |
| **GlycanGT: a pretrained graph transformer framework for glycan graph representation and generative learning** — Akihiro Kitani, Bingyuan Zhang, Koichi Himori, Yusuke Matsui; Nagoya/iGCORE; **Bioinformatics, 2026**. | Graph-transformer masked recovery of sugars and linkages in supplied graph connectivity, plus property prediction. | Strong completion baseline. Completion on a given topology differs from generating a new branching topology. [Paper](https://doi.org/10.1093/bioinformatics/btag147); [code/data](https://github.com/matsui-lab/GlycanGT). |
| **GlycanML: A Multi-Task and Multi-Structure Benchmark for Glycan Machine Learning** — Minghao Xu, Yunteng Geng, Yihang Zhang, Ling Yang, Jian Tang, Wentao Zhang; Peking/Mila and collaborators; **ICLR 2025**. | Multiple supervised sequence/graph prediction baselines across 11 tasks. | Useful evaluation tasks/splits; **not a generator**. [Paper](https://arxiv.org/abs/2405.16206); [code/data](https://github.com/GlycanML/GlycanML). |
| **A Glycan-Aware Diffusion Model for Carbohydrate and Glycoprotein Structure Prediction** — Keshav Sundar, Hyunjun Yang; Brandeis; **2026 preprint**. | SweetFold produces 3D coordinates for a supplied glycan identity/connectivity, optionally with protein context. | Coordinate-generation precedent, **not a new chemical-topology designer**; full training is beyond the intended small baseline. [Paper](https://doi.org/10.64898/2026.07.16.738959); [code](https://github.com/Keshav-Sundar-4/SweetFold). |

Two older papers are essential prior art:

- **SweetTalk:** Daniel Bojar, Riley K. Powers, Diogo M. Camacho and James J. Collins, *Deep-Learning Resources for Studying Glycan-Mediated Host-Microbe Interactions*, **Cell Host & Microbe, 2021**. Includes predictor-guided mutation/ranking for immunogenicity. This prevents claiming the first property-guided glycan design. [Paper](https://doi.org/10.1016/j.chom.2020.10.004), [code](https://github.com/midas-wyss/sweettalk).
- **SweetNet:** Rebekka Burkholz, John Quackenbush and Daniel Bojar, *Using graph convolutional neural networks to learn a representation for glycans*, **Cell Reports, 2021**. A small graph-prediction architecture useful for a surrogate. [Paper](https://doi.org/10.1016/j.celrep.2021.109251), [code/data](https://github.com/BojarLab/SweetNet).

## 4. Training order and implementation steps

**For motif-controlled generation, you do not need a classifier first. For binding-directed design, validate a binding predictor before using it to steer generation.** Binding measurements often call for regression rather than binary classification.

1. **Choose the task and vocabulary.** Start with fully specified, connected glycans and a limited set of supported sugars/linkages. Define whether the condition is a structural motif or a measured binding property.
2. **Prepare the data.** Canonicalize and deduplicate structures, then split by structural family before augmentation. Equivalent branch-order strings must remain in the same split. Compute motif labels directly if using the simpler task.
3. **Establish a cheap baseline.** Implement a tree/Markov sampler or seed-mutation search, then a small autoregressive sequence model with branch/linkage-aware tokenization.
4. **Add conditional generation and constraints.** Enforce valid branching, supported tokens and nonconflicting linkage positions. Compare against unconstrained decoding under the same compute allowance.
5. **If targeting binding:** select one assay context, train/validate a small predictor or assess released weights, then freeze it during generator optimization. Use a separate evaluator where possible and report uncertainty. High surrogate scores alone do not establish binding.
6. **Evaluate:** structural validity, condition satisfaction, diversity, exact training copies, nearest structural neighbours, and performance on held-out families. Report parser coverage separately from chemical/biological validity.

## 5. Free validity and novelty tools

- **[glycowork](https://github.com/BojarLab/glycowork)** — MIT; glycan parsing, graph representations, motifs, canonicalization and prediction utilities. Useful for structure processing and checking requested motifs.
- **[GlyLES](https://github.com/kalininalab/GlyLES)** — MIT; translates supported IUPAC-condensed glycans to atom-level SMILES. [Paper](https://doi.org/10.1186/s13321-023-00704-0).
- **[RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html)** — BSD-3-Clause; parse/sanitize converted molecules and support atom-level comparisons.

Implement explicit tree/linkage rules for the selected vocabulary. **GlyLES is not a complete semantic or biosynthetic validity checker**; unsupported chemistry can fail or be ignored with warnings. Reject or separately report those cases. Successful parsing does not prove that a glycan can be synthesized, biosynthesized or binds a protein.

In the saved local CPU benchmark, GlyLES→RDKit averaged approximately **380 ms per attempted reference glycan**. The GlyLES paper reports approximately **19 ms** on a different supported subset/hardware. Neither is a Colab measurement. [Benchmark results](tasks/validity_benchmark.json).

For novelty, compare labelled glycan trees while preserving sugar identities, linkages and anomers. Report exact isomorphism/canonical matches and near-neighbour tree/motif similarity. Different text strings can represent the same glycan.

## 6. A realistic four-week version

| Week | Deliverable |
|---|---|
| 1 | Frozen dataset and grammar, family-based split, timed setup and short training pilot. |
| 2 | Small generator and simple sampling/mutation baseline. |
| 3 | Motif conditioning and constrained decoding; binding extension only if the data/predictor is ready. |
| 4 | Novelty, generalization and constraint ablations; final reproducible notebook/report. |

Use a small model and measure actual T4 throughput early. **Under four GPU-hours and setup under five minutes are targets, not verified results.** Full retraining of GlycoBART, all GlycanGT variants or SweetFold is not the recommended scope. The easiest defensible version is **small-scale motif-controlled glycan generation with a rigorous validity and memorization audit**; functional binding design is the more demanding extension.

Read **SweetTalk → LectinOracle → the Boltzmann paper → GlycanGT/GlycoBART** first to understand the closest precedents. Detailed compute, access and licensing qualifications remain in [glycan_np_audit.md](glycan_np_audit.md).
