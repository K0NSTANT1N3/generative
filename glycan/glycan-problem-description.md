# Target-Conditioned Glycan Generation: Problem Formulation, Datasets, Prior Art, and Research Landscape

## 1. Biological Foundation & Formal Problem Formulation

### 1.1 Biological Role and Structural Complexity of Glycans
Glycans are complex carbohydrates constructed from individual monosaccharide sugar units linked together through covalent glycosidic bonds. Unlike linear biological polymers such as DNA, RNA, or proteins—which possess fixed directional backbones—glycans form highly non-linear, branched tree structures. The primary monosaccharide building blocks include D-galactose (Gal), D-glucose (Glc), N-acetyl-D-glucosamine (GlcNAc), N-acetyl-D-galactosamine (GalNAc), D-mannose (Man), L-fucose (Fuc), and N-acetylneuraminic acid (Neu5Ac, also known as sialic acid).

The structural diversity of glycans is exponentially larger than that of proteins or nucleic acids due to three distinct stereochemical factors:
1. **Anomeric Configurations**: Each glycosidic bond can adopt either an $\alpha$ or $\beta$ stereochemical orientation at the anomeric carbon center.
2. **Linkage Positions**: Monosaccharides possess multiple hydroxyl ($-\text{OH}$) groups capable of forming glycosidic bonds (e.g., $1\to2$, $1\to3$, $1\to4$, $1\to6$, or $2\to6$ linkages), enabling multiple branching points from a single sugar residue.
3. **Branched Tree Topologies**: A single glycan tree can split into complex bi-antennary, tri-antennary, or tetra-antennary architectures, capped by specific terminal motifs such as sialic acid or fucose.

In biological systems, glycans coat all cell surfaces (the glycocalyx) and are covalently attached to proteins (N-linked and O-linked glycoproteins) and lipids (glycolipids). They serve as primary recognition handles for carbohydrate-binding proteins known as lectins, regulating critical physiological processes including cell-cell signaling, immune cell trafficking, and tissue homeostasis.

### 1.2 Real-World Biomedical Applications
The capacity to design custom, target-conditioned glycan structures addresses three major bottlenecks in biopharmaceuticals and targeted therapeutics:

* **Targeted Cancer Immunotherapy**: Tumor cells frequently overexpress specific sialylated glycan motifs that bind immunosuppressive lectins—such as Sialic acid-binding immunoglobulin-type lectins (Siglec-7, Siglec-9) and Galectin-3—on cytotoxic T cells and Natural Killer (NK) cells. This interaction triggers inhibitory signaling cascades that allow the tumor to evade immune destruction. High-affinity synthetic glycan mimetics can selectively bind and block these lectins, restoring endogenous anti-tumor immune responses.
* **Antiviral Decoys and Receptor Inhibitors**: Respiratory viral surface proteins (such as Influenza Hemagglutinin) attach to host cell-surface glycans (such as $\alpha2\text{-}6$ linked sialic acids) to initiate cellular binding. Engineered soluble glycan decoys with optimized binding kinetics can bind circulating viral proteins prior to cell membrane engagement.
* **Biopharmaceutical Glyco-Engineering**: Over 70% of therapeutic monoclonal antibodies are glycoproteins. The composition of their Fc-region N-linked glycans governs antibody-dependent cellular cytotoxicity (ADCC), serum clearance rates, organ distribution, and conformational stability. Designing specific glycan branch architectures enables precise control over therapeutic efficacy and drug half-life.

### 1.3 The Core Research Gap and Technological Bottlenecks
Despite the critical biological importance of glycans, computational glycobiology lacks de novo generative tools. Existing machine learning models operate under severe functional limitations:
* **Absence of Function-Conditioned De Novo Generators**: Current models perform masked residue filling on pre-existing topological skeletons, generate glycan sequence candidates from mass spectra, or infer structures from lectin binding fingerprints. No published model generates valid, whole-tree glycan topologies from scratch conditioned directly on a target protein sequence.
* **Surrogate Exploitation and Predictor Artifacts**: Optimizing generative models against fixed property predictors (such as neural lectin binding models) frequently causes the generator to discover adversarial topological artifacts—unrealistic sugar patterns that exploit predictor errors to yield artificially high affinity scores without true biological binding.
* **Chemical Grammar Constraints**: Naive graph generative models frequently produce chemically impossible trees containing invalid atomic valences, conflicting linkage positions, or stereochemically impossible sugar rings. Enforcing strict chemical rules during decoding is essential to guarantee structural validity.

### 1.4 Formal Mathematical Problem Setup

#### Output Space ($\mathcal{G}$)
A glycan structure is formally represented as a rooted, directed, acyclic branched graph $G = (V, E, \mathbf{X}_V, \mathbf{X}_E) \in \mathcal{G}$, where:
* $V$ is the set of monosaccharide nodes, with average node count $|V| \approx 7.1$ (corresponding to approximately 91 heavy atoms).
* $E \subset V \times V$ is the set of directed glycosidic linkage edges directed from child residues to parent residues toward the reducing end root.
* $\mathbf{X}_V = \{x_v \mid v \in V\}$ defines monosaccharide identities and anomeric configurations ($x_v \in \{\text{Gal}, \text{Glc}, \text{GlcNAc}, \text{Neu5Ac}, \text{Fuc}, \text{Man}, \dots\} \times \{\alpha, \beta\}$).
* $\mathbf{X}_E = \{x_e \mid e \in E\}$ defines linkage positions ($x_e \in \{1\to2, 1\to3, 1\to4, 1\to6, 2\to3, 2\to6\}$).

#### Input Conditioning Space ($\mathcal{C}$)
The generative model is conditioned on a context vector $c = (\mathbf{p}, m) \in \mathcal{C}$, where:
1. $\mathbf{p} = \text{ESM-2}(S_{\text{lectin}}) \in \mathbb{R}^{1280}$ represents a continuous protein language model embedding derived from the 200-amino-acid binding domain sequence $S_{\text{lectin}}$ of the target lectin.
2. $m \in \mathcal{M}$ represents an optional hard or soft structural motif constraint (e.g., specifying a required terminal $\alpha2\text{-}6$ sialic acid cap or core $\alpha1\text{-}6$ fucose).

#### Objective Function and Loss Formulation
We learn the conditional distribution $p_\theta(G \mid c)$ by maximizing the joint objective:

$$\max_\theta \; \mathbb{E}_{(c, G) \sim \mathcal{D}} \left[ \log p_\theta(G \mid c) \right] - \lambda \mathcal{L}_{\text{grammar}}(G)$$

subject to four mandatory operational constraints:
1. **Hard Grammar Constraints**: $\text{GrammarPass}(G) = 1$, enforced via valid mask filtering during autoregressive decoding to prevent valence violations and conflicting linkage positions.
2. **Target Affinity Optimization**: $\hat{y}_{\text{binding}} = \text{LectinOracle}(G, \mathbf{p}) \ge \tau$, ensuring predicted binding affinity exceeds threshold $\tau$.
3. **Surrogate Exploitation Defense**: $\text{Var}_{\text{ensemble}}(\hat{y}) \le \delta$, penalizing candidates where independent secondary binding predictors disagree, eliminating adversarial out-of-distribution artifacts.
4. **Novelty and Non-Memorization Audit**: $D_{\text{WL}}(G, G_i) > 0 \quad \forall G_i \in \mathcal{D}_{\text{train}}$, verified using Weisfeiler-Lehman 4th-order (WL-4) graph hashing against held-out structural training families.

### 1.5 End-to-End System Architecture and Inference Workflow

1. **Input Processing**: The user inputs a target lectin amino acid sequence (e.g., Siglec-7) and an optional structural constraint. ESM-2 computes the target embedding vector $\mathbf{p}$.
2. **Grammar-Masked Generation**: The autoregressive graph generator samples candidate IUPAC-condensed glycan trees, applying valid token masks at each decoding step to enforce valid monosaccharide valences and linkage positions.
3. **Chemical Sanitization**: GlyLES converts candidate IUPAC strings into atomic SMILES representations, and RDKit sanitizes ring structures and verifies valence consistency.
4. **Surrogate Binding Evaluation**: LectinOracle predicts binding affinity for the target lectin embedding, while an ensemble of secondary predictors calculates variance $\text{Var}_{\text{ensemble}}(\hat{y})$ to filter out adversarial artifacts.
5. **Memorization Audit**: Generated candidates are evaluated using WL-4 graph hashing against training set structures to confirm structural novelty beyond training set duplication.

---

## 2. Complete Inventory of Training and Benchmark Datasets

### 2.1 Structural Datasets for Generative Grammar Training

#### GlyCosmos Bulk Glycan Export
* **Access Location**: GlyCosmos Portal (glycosmos.org/download; direct CSV download at download.glycosmos.org/glycosmos_glycans_list.csv)
* **Dataset Characteristics**: Contains GlyCosmos accessions, IUPAC-condensed strings, WURCS representations, and species annotations (~79.71 MB bulk CSV). Released under Creative Commons Attribution 4.0 International (CC BY 4.0).
* **Preprocessing Protocol**: Raw files contain ambiguous linkage positions, unassigned sugar residues, and disconnected fragments. Preprocessing filters entries to retain only fully specified, connected monosaccharide trees.
* **Role in Pipeline**: Provides the foundational structural corpus for learning carbohydrate grammar, monosaccharide co-occurrence distributions, and autoregressive branching patterns.

#### GlyTouCan International Registry
* **Access Location**: GlyTouCan Registry Portal (glytoucan.org; terms at doc.glytoucan.org/en/Terms-and-Conditions)
* **Dataset Characteristics**: The primary international glycan repository providing unique accession identifiers (e.g., G12345AB) for registered carbohydrate structures under Creative Commons Zero (CC0).
* **Preprocessing Protocol**: Cross-referenced with GlyCosmos to extract standardized WURCS strings and filter out incomplete entries lacking linkage specificity.
* **Role in Pipeline**: Serves as the authoritative accession reference for structure canonicalization and mapping across external databases.

#### GlycanGT Processed Clean Dataset
* **Access Location**: Matsui Lab Repository (matsui-lab/GlycanGT on GitHub; Zenodo Archive ID 18636040)
* **Dataset Characteristics**: Contains 83,739 (repository lists 83,740) pre-filtered, fully specified glycan network graphs derived from GlyCosmos (~7.69 MB compressed ZIP archive). Source data CC BY 4.0; repository code Apache-2.0.
* **Preprocessing Protocol**: Already parsed into node-and-edge graph representations. Requires partition into structural-family held-out splits using WL-4 graph isomorphism clustering to prevent data leakage between training and evaluation sets.
* **Role in Pipeline**: Primary clean dataset for training baseline graph transformers and autoregressive tree generators without raw WURCS string parsing overhead.

#### SweetTalk Historical Structure Corpus
* **Access Location**: Wyss Institute Repository (midas-wyss/sweettalk on GitHub)
* **Dataset Characteristics**: Historical dataset containing 21,296 records and 13,541 distinct literal target strings (~1.56 MB CSV file; final paper uses 19,299 unique glycans). Code released under Apache-2.0.
* **Preprocessing Protocol**: Requires deduplication of literal strings and standardization of IUPAC nomenclature to align with modern glycowork conventions.
* **Role in Pipeline**: Used as an auxiliary structural dataset for baseline sequence models and historical comparison with early mutation-search algorithms.

### 2.2 Functional Binding and Interaction Datasets

#### LectinOracle Array Interaction Dataset
* **Access Location**: Bojar Lab Repository (BojarLab/LectinOracle on GitHub)
* **Dataset Characteristics**: Curated dataset reporting 564,647 unique protein-glycan interaction pairs derived from 3,228 Consortium for Functional Glycomics (CFG) and 100 Imperial College microarrays (~12.76 MB main array CSV, ~16.64 MB protein embedding PKL file). Code released under MIT license.
* **Preprocessing Protocol**: Raw Relative Fluorescence Unit (RFU) values vary across microarray platforms. Preprocessing normalizes RFU values into non-linear percentile ranks per array and extracts 200-amino-acid lectin binding domains for ESM-2 embedding generation.
* **Role in Pipeline**: Primary dataset used to train the frozen LectinOracle surrogate predictor and evaluate target-conditioned generation affinity.

#### GlyGen Glycan Array Repository
* **Access Location**: GlyGen Array Portal (glygen.ccrc.uga.edu/ggarray/)
* **Dataset Characteristics**: Portal hosting 989 array study collections across 533 unique glycans, providing raw binding measurements under CC BY 4.0.
* **Preprocessing Protocol**: Requires filtering by specific lectin families (e.g., Siglecs, Galectins) and converting study-specific RFU values into standardized binding classifications.
* **Role in Pipeline**: Auxiliary validation dataset for secondary binding predictors in the surrogate exploitation defense ensemble.

### 2.3 Analytical and Benchmark Datasets

#### GlycoBART / CandyCrunch Mass Spectrometry Release
* **Access Location**: SUNY Buffalo Release (Zenodo Archive ID 15741423; repository CABSEL/glycotrans on GitHub)
* **Dataset Characteristics**: Contains 510,160 tandem MS/MS spectra paired with 3,590 glycan identities (~1.51 GB XLSX file, ~808 KB glycan CSV). Released under CC BY 4.0.
* **Preprocessing Protocol**: Spectral peaks require intensity normalization and precursor mass matching.
* **Role in Pipeline**: Analytical reference dataset used strictly to evaluate spectrum-based structure identification baselines; not used for target-conditioned de novo generation.

#### GlycanML Multi-Task Benchmark
* **Access Location**: GlycanML Repository (GlycanML/GlycanML on GitHub; project page at glycanml.github.io/project/)
* **Dataset Characteristics**: Multi-task benchmark suite standardizing official splits across 11 prediction tasks, including immunogenicity, tissue glycosylation, and lectin affinity. Released under Apache-2.0.
* **Preprocessing Protocol**: Requires task-specific label filtering and conversion to graph network objects.
* **Role in Pipeline**: Standardized evaluation suite for multi-task property control and cross-dataset generalization benchmarks.

### 2.4 Summary Table of Dataset Provenance and Preprocessing Protocols

Prior to training, all raw structural inputs undergo a unified canonicalization pipeline:
1. **Filtering**: Removal of ambiguous linkage notations (e.g., `?1-?`) and disconnected fragments.
2. **Parsing**: Translation from raw WURCS/IUPAC strings into monosaccharide node graphs using `glycowork`.
3. **Partitioning**: Structural family clustering via WL-4 graph hashing to construct strict held-out evaluation splits.

| Dataset Name | Access Location | Size / Count | Open License | Required Preprocessing | Pipeline Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GlyCosmos Bulk Export** | GlyCosmos Portal (glycosmos.org) | 79.71 MB CSV (~244k entries) | CC BY 4.0 | Filter ambiguous linkages & unassigned monosaccharides | Core structural grammar pretraining |
| **GlyTouCan Registry** | GlyTouCan Portal (glytoucan.org) | Registry database | CC0 | Canonical accession mapping & WURCS extraction | Standard accession cross-referencing |
| **GlycanGT Clean Data** | GitHub (matsui-lab/GlycanGT) | 7.69 MB ZIP (83,739 graphs) | CC BY 4.0 | WL-4 graph hashing & family held-out splitting | Graph generator pretraining baseline |
| **SweetTalk Corpus** | GitHub (midas-wyss/sweettalk) | 1.56 MB CSV (21,296 rows) | Apache-2.0 | Deduplicate literal strings & normalize IUPAC names | Auxiliary sequence training baseline |
| **LectinOracle Dataset** | GitHub (BojarLab/LectinOracle) | 12.76 MB CSV (564,647 pairs) | MIT | RFU percentile ranking & ESM-2 protein embedding | Surrogate predictor training & evaluation |
| **GlyGen Array Portal** | GlyGen Portal (glygen.ccrc.uga.edu) | 989 studies (533 glycans) | CC BY 4.0 | Standardize study RFUs per lectin family | Secondary ensemble predictor training |
| **GlycoBART Release** | Zenodo ID 15741423 | 1.51 GB XLSX (510k spectra) | CC BY 4.0 | Peak intensity normalization & precursor matching | Analytical MS identification benchmark |
| **GlycanML Benchmark** | GitHub (GlycanML/GlycanML) | Multi-task corpus (11 tasks) | Apache-2.0 | Task-specific label extraction & graph formatting | Multi-objective control evaluation |

---

## 3. Prior Art, Similar Projects, and Comparative Analysis

### 3.1 Precedent Generative and Predictive Models

#### GlycanGT (Nagoya University / iGCORE, 2026)
* **Citation & Access**: Akihiro Kitani, Bingyuan Zhang, Koichi Himori, Yusuke Matsui. *Bioinformatics*, 42(4), btag147, 2026. DOI: 10.1093/bioinformatics/btag147 | Code: matsui-lab/GlycanGT on GitHub
* **Model Architecture & Function**: TokenGT-based graph transformer framework trained on 83,739 graphs. Performs masked monosaccharide and glycosidic bond recovery on a supplied graph topology.
* **Similarities**: Utilizes clean GlyCosmos graph representations and monosaccharide/linkage tokenization.
* **Differences & Crucial Gap**: GlycanGT is a masked completion model operating on a fixed, pre-existing graph skeleton. It cannot generate new branching topologies from scratch or condition generation on target protein binding.

#### Boltzmann Lectin Model (UC San Diego / Augusta University, 2024)
* **Citation & Access**: Aria Yom, Austin Chiang, Nathan E. Lewis. *Analytical Chemistry*, 96, 8332–8341, 2024. DOI: 10.1021/acs.analchem.3c04992 | Full Text: PMC11162346
* **Model Architecture & Function**: Second-order Markov tree sampler coupled with a Boltzmann motif model. Infers unknown glycan structures by sampling candidates that match an observed 64-lectin/9-antibody binding fingerprint.
* **Similarities**: Performs inverse mapping between lectin binding profiles and glycan tree structures.
* **Differences & Crucial Gap**: Performs inverse *identification* of existing natural glycans from wet-lab binding fingerprints. It cannot design *novel synthetic binders* from scratch conditioned on protein sequences without prior experimental array data.

#### GlycoBART & GlycoBERT (SUNY Buffalo, 2025)
* **Citation & Access**: Ejas Althaf Abtheen et al. *bioRxiv preprint*, 2025. DOI: 10.1101/2025.07.02.662857 | Code: CABSEL/glycotrans on GitHub | Weights: CABSEL/glycobart on HuggingFace
* **Model Architecture & Function**: 207M-parameter BART sequence-to-sequence model generating glycan IUPAC sequences conditioned on tandem MS/MS mass spectra and metadata.
* **Similarities**: Uses conditional autoregressive sequence generation for carbohydrate structures.
* **Differences & Crucial Gap**: GlycoBART is an analytical sequencing tool for identifying known biological samples from mass spectra. It does not perform target-conditioned functional design for therapeutic applications.

#### SweetTalk (Wyss Institute / Harvard / MIT, 2021)
* **Citation & Access**: Daniel Bojar, Riley K. Powers, Diogo M. Camacho, James J. Collins. *Cell Host & Microbe*, 29, 132–144, 2021. DOI: 10.1016/j.chom.2020.10.004 | Code: midas-wyss/sweettalk on GitHub
* **Model Architecture & Function**: Bidirectional LSTM language model that proposes single-residue or linkage mutations on seed glycans to optimize a predicted property score.
* **Similarities**: Early pioneer in property-guided glycan modification and language modeling.
* **Differences & Crucial Gap**: Performs local mutation search around pre-existing seed structures (editing 1 residue at a time). It lacks whole-tree de novo generation, target protein sequence conditioning, and surrogate exploitation defenses.

#### LectinOracle (University of Gothenburg / SIB Geneva, 2022)
* **Citation & Access**: Jon Lundstrøm, Emma Korhonen, Frédérique Lisacek, Daniel Bojar. *Advanced Science*, 9, 2103807, 2022. DOI: 10.1002/advs.202103807 | Code: BojarLab/LectinOracle on GitHub
* **Model Architecture & Function**: Hybrid GNN combining a SweetNet glycan graph encoder with frozen ESM-1b/ESM-2 protein embeddings to predict relative binding affinity.
* **Similarities**: Combines protein language model embeddings with glycan graph representations.
* **Differences & Crucial Gap**: LectinOracle is strictly a discriminative predictor and cannot generate glycans. Our project leverages LectinOracle as a frozen surrogate evaluator within a generative loop.

#### SweetFold (Brandeis University, 2026)
* **Citation & Access**: Keshav Sundar, Hyunjun Yang. *bioRxiv preprint*, 2026. DOI: 10.64898/2026.07.16.738959 | Code: Keshav-Sundar-4/SweetFold on GitHub
* **Model Architecture & Function**: All-atom 3D diffusion model predicting 3D spatial coordinates for a supplied, fixed glycan topology and sequence.
* **Similarities**: Applies deep generative models (diffusion) to carbohydrate structures.
* **Differences & Crucial Gap**: SweetFold generates 3D spatial conformations for a pre-specified chemical graph. It does not design the 2D topological graph structure itself.

#### GlycanAA (Peking University / Mila, 2025)
* **Citation & Access**: Minghao Xu et al. *ICML*, 2025. arXiv: 2506.01376 | Code: kasawa1234/GlycanAA on GitHub
* **Model Architecture & Function**: Hierarchical all-atom message-passing network for representation learning and multi-scale property prediction.
* **Similarities**: Hierarchical graph representation of monosaccharide topologies.
* **Differences & Crucial Gap**: Representation learning baseline; does not possess generative capabilities.

#### GlycanML Benchmark Suite (Peking University / Mila, 2025)
* **Citation & Access**: Minghao Xu et al. *ICLR*, 2025. arXiv: 2405.16206 | Code: GlycanML/GlycanML on GitHub
* **Model Architecture & Function**: Benchmark framework standardizing 11 supervised prediction tasks across sequence and graph architectures.
* **Similarities**: Evaluates property prediction accuracy across glycan datasets.
* **Differences & Crucial Gap**: Diagnostic benchmark suite; contains no generative modeling components.

#### SweetNet (Harvard / Wyss Institute, 2021)
* **Citation & Access**: Rebekka Burkholz, John Quackenbush, Daniel Bojar. *Cell Reports*, 35, 109251, 2021. DOI: 10.1016/j.celrep.2021.109251 | Code: BojarLab/SweetNet on GitHub
* **Model Architecture & Function**: Graph convolutional neural network for predicting glycan taxonomy and binding from graph structures.
* **Similarities**: Early baseline for graph neural network representations of carbohydrates.
* **Differences & Crucial Gap**: Purely predictive model; cannot generate glycan structures.

### 3.2 Detailed Comparative Matrix: Proposed Model vs. Prior Art

| Project / Model | Generative Task Type | Input Conditioning Signal | Output Space | Chemical Validity Enforcement | Surrogate Defense |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GlycanGT** | Masked Graph Completion | Partial graph & mask positions | Monosaccharide / edge labels | Soft topological loss | None |
| **Boltzmann Model** | Inverse Structure Inference | 64-lectin binding fingerprint | Ranked candidate trees | Second-order Markov rules | None |
| **GlycoBART** | Sequence Generation | MS/MS spectra & metadata | IUPAC sequence strings | None (post-hoc filter) | None |
| **SweetTalk** | Seed Mutation Search | Seed glycan & property score | Mutated sequence strings | Local glycoword filter | None |
| **LectinOracle** | Property Prediction (*Non-Gen*) | Protein sequence & glycan graph | Binding affinity score | N/A (Predictor) | N/A |
| **SweetFold** | 3D Conformation Prediction | Fixed glycan topology | 3D Atomic coordinates | Stereochemical loss | None |
| **GlycanAA** | Representation Learning (*Non-Gen*) | Glycan graph / atoms | Property predictions | N/A (Predictor) | N/A |
| **GlycanML** | Multi-Task Benchmark (*Non-Gen*) | Glycan sequence / graph | Benchmark evaluation | N/A (Benchmark) | N/A |
| **SweetNet** | Property Prediction (*Non-Gen*) | Glycan graph topology | Property classification | N/A (Predictor) | N/A |
| **Proposed Model** | **De Novo Target Generation** | **ESM-2 Lectin Vector & Motif** | **Branched Graph Topology** | **Grammar-Masked Decoding** | **Ensemble Variance Penalty** |

### 3.3 Validity, Parsing, and Verification Infrastructure

The verification pipeline relies on three open-source software libraries:
1. **glycowork** (MIT License; repository BojarLab/glycowork on GitHub): Maintained Python package developed by the Bojar Lab. Handles IUPAC-condensed string parsing, graph conversions, motif extraction, and canonicalization.
2. **GlyLES** (MIT License; repository kalininalab/GlyLES on GitHub): Translator developed by the Kalinina Lab (*Journal of Cheminformatics*, 2023). Converts IUPAC-condensed glycan trees into atom-level SMILES strings in ~19 ms per molecule.
3. **RDKit** (BSD-3-Clause License): Cheminformatics toolkit used to parse converted SMILES strings, sanitize atomic valences, and verify chemical validity.

---

## 4. Global Research Landscape: Active Universities and Specialized Labs

Research in machine learning for glycobiology is concentrated across a small network of specialized academic laboratories:

### 1. University of Gothenburg (Sweden) – Bojar Lab
* **Principal Investigator**: Dr. Daniel Bojar (Department of Chemistry and Molecular Biology).
* **Core Focus**: Pioneering machine learning applications in glycobiology, glycan language modeling, and host-microbe interaction prediction.
* **Key Projects & Software**: `glycowork` (foundational glycan processing library), `SweetTalk` (mutation search), `SweetNet` (glycan GNN), `LectinOracle` (protein-glycan binding predictor), `GIFFLAR` (NeurIPS 2024), `GlyContact` (Nature Comms 2025), and `GlycoForge` (glycomics data simulator).

### 2. Nagoya University / iGCORE (Japan) – Matsui Lab
* **Principal Investigator**: Dr. Yusuke Matsui (Institute for Glyco-core Research / iGCORE).
* **Core Focus**: Graph neural networks and transformer architectures for carbohydrate structure completion and property representation.
* **Key Projects & Software**: `GlycanGT` (*Bioinformatics*, 2026), a graph transformer trained on 83,739 GlyCosmos graphs for masked monosaccharide and linkage recovery.

### 3. University of California San Diego & Augusta University (USA) – Lewis Lab
* **Principal Investigator**: Dr. Nathan E. Lewis (Departments of Pediatrics and Bioengineering, UCSD).
* **Core Focus**: Systems glycobiology, cell engineering, and probabilistic models for glycan structure inference from experimental binding data.
* **Key Projects & Software**: `Boltzmann Lectin Model` (*Analytical Chemistry*, 2024), a second-order Markov tree sampler for inverse structure inference from lectin binding fingerprints.

### 4. State University of New York (SUNY) at Buffalo (USA) – Gunawan & Neelamegham Labs
* **Principal Investigators**: Dr. Rudiyanto Gunawan (Chemical and Biological Engineering) and Dr. Sriram Neelamegham (Biomedical Engineering).
* **Core Focus**: Deep learning pipelines for mass spectrometry interpretation, glycan structure sequencing, and automated annotation.
* **Key Projects & Software**: `GlycoBART` and `GlycoBERT` (*bioRxiv*, 2025), a 207M-parameter BART model for generating glycan sequence strings from tandem MS/MS mass spectra.

### 5. Peking University & Mila - Québec AI Institute (China / Canada) – Tang & Zhang Groups
* **Principal Investigators**: Dr. Jian Tang (Mila / HEC Montréal) and Dr. Wentao Zhang (Peking University).
* **Core Focus**: Multi-scale representation learning, hierarchical message-passing neural networks, and benchmark standardization for molecular AI.
* **Key Projects & Software**: `GlycanAA` (*ICML*, 2025; all-atom message-passing network) and `GlycanML` (*ICLR*, 2025; multi-task benchmark suite across 11 glycan prediction tasks).

### 6. Brandeis University (USA) – Yang Lab
* **Principal Investigator**: Dr. Hyunjun Yang (Department of Biochemistry).
* **Core Focus**: 3D generative modeling, diffusion architectures, and structural biophysics of carbohydrates and glycoproteins.
* **Key Projects & Software**: `SweetFold` (*bioRxiv*, 2026), an all-atom 3D diffusion model for predicting 3D spatial conformations of glycans and glycoproteins.

### 7. Saarland University (Germany) – Kalinina Lab
* **Principal Investigator**: Dr. Olga Kalinina (Helmholtz Institute for Pharmaceutical Research Saarland / HIPS).
* **Core Focus**: Computational drug design, chemical grammar parsing, and structural bioinformatics.
* **Key Projects & Software**: `GlyLES` (*Journal of Cheminformatics*, 2023), the standard grammar-based parser translating IUPAC-condensed glycan strings into SMILES representations.

### 8. University of Alberta & National Tsing Hua University (Canada / Taiwan) – Derda & Greiner Labs
* **Principal Investigators**: Dr. Ratmir Derda (Chemistry, Univ. of Alberta) and Dr. Russell Greiner (Computing Science, Univ. of Alberta / NTHU).
* **Core Focus**: Machine learning for chemical biology, peptide-carbohydrate interaction profiling, and enantiomer-aware graph networks.
* **Key Projects & Software**: `MCNet` (*bioRxiv*, 2025), an atom-level multi-channel neural network predicting lectin binding across D- and L-glycan enantiomers.
