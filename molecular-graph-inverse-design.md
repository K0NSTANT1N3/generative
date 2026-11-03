# Quantum-Property-Conditioned Molecular Graph Inverse Design (QM9 Benchmark)

## 1. Executive Overview & Screening Gate Qualification

The inverse design of small organic molecules conditioned on quantum chemical properties represents a hallmark benchmark in scientific generative modeling. Rather than predicting the properties of an existing molecule (the forward problem), this project formulates a conditional generative task: given a desired quantum physical profile—such as a target HOMO–LUMO energy gap ($\Delta \epsilon$) or isotropic polarizability ($\alpha$)—the generative framework must synthesize valid, novel, and synthetically accessible molecular graphs that satisfy the specification.

This candidate proposal explicitly satisfies all eight Pass/Fail Screening Criteria established in the research vetting framework:

*   **Criterion 1 (Non-Grid / Non-Token Structured Output):** The model directly outputs 2D molecular graphs $G = (\mathbf{X}, \mathbf{E})$ represented as discrete node feature matrices $\mathbf{X} \in \mathbb{R}^{N \times d_{\text{node}}}$ (encoding atomic species like C, N, O, F, H) and edge attribute tensors $\mathbf{E} \in \mathbb{R}^{N \times N \times d_{\text{edge}}}$ (encoding bond orders: single, double, triple, aromatic, or unbonded). It avoids string-based SMILES tokenization, ensuring direct structural graph generation.
*   **Criterion 2 (100x Compute Invariance & Ground-Truth Scarcity):** Ground-truth chemical validity and biological toxicity cannot be created or replaced by scaling GPU compute by 100x. Physical wet-lab chemical synthesis, nuclear magnetic resonance (NMR) characterization, and live biological assays ($LD_{50}$, cell viability, metabolic stability) remain strict physical bottlenecks.
*   **Criterion 3 (Natural Inverse Formulation):** The problem is inherently inverse-conditioned: $f_\theta: y^* \to G$, mapping from continuous property vectors $y^* \in \mathbb{R}^k$ to discrete molecular graph topologies $G$.
*   **Criterion 4 (Checkable Machine Validity):** The domain provides an instantaneous, deterministic, open-source Python validation oracle: **RDKit**. RDKit evaluates chemical valence sanity, ring strain, charge balance, and graph connectedness in milliseconds per sample.
*   **Criterion 5 (Open Methodological Levers):** The project tests a controlled 3-way methodological comparison:
    1.  *Constraint-Aware Generation:* Masked diffusion or autoregressive GNNs enforcing valence constraints during sampling.
    2.  *Unconstrained Generation + Rejection:* Raw generative sampling followed by RDKit validity filtering.
    3.  *Post-Hoc Valence Repair:* Generative sampling with deterministic rule-based bond/charge correction post-processing.
*   **Criterion 6 (Instant Open Data & License):** Relies on the canonical **QM9 dataset** (133,885 small organic molecules), which is instantly accessible under a Creative Commons CC BY 4.0 license and loads via a single line of Python (`torch_geometric.datasets.QM9`).
*   **Criterion 7 (Compute Feasibility):** The lightweight graph representation allows full model training within 1.5 to 3 GPU-hours on a single free Google Colab / Kaggle NVIDIA T4 GPU, well within resource constraints.
*   **Criterion 8 (Checkable Memorization Protocol):** Memorization and training set leakage are deterministically auditable using Tanimoto similarity over 2048-bit Morgan structural fingerprints against the training split.

---

## 2. Formal Mathematical Problem Formulation

The objective is to train a conditional generative model $p_\theta(G \mid y^*)$ that parameterizes a distribution over molecular graphs $G$ conditioned on a target physical property vector $y^*$.

### Graph Representation Definition

A molecular graph $G$ is defined as a tuple $(\mathbf{X}, \mathbf{E})$, where:

*   $\mathbf{X} \in \{0, 1\}^{N \times |A|}$ represents the node (atom) feature matrix, where $N \le 29$ is the maximum number of atoms per molecule, and $A = \{\text{H}, \text{C}, \text{N}, \text{O}, \text{F}\}$ is the set of heavy and light atom types.
*   $\mathbf{E} \in \{0, 1\}^{N \times N \times |B|}$ represents the edge (bond) tensor, where $B = \{\text{None}, \text{Single}, \text{Double}, \text{Triple}\}$ defines discrete bond categories.

### Conditioning Property Space

The conditioning vector $y^* \in \mathbb{R}^k$ selects from continuous quantum chemical targets computed at the DFT B3LYP/6-31G(2dp) level of theory, such as:

$$y^* = \left[ \Delta \epsilon_{\text{HOMO-LUMO}}, \mu, \alpha, H \right]^\top$$

where $\Delta \epsilon$ represents the orbital energy gap in electron-volts ($\text{eV}$), $\mu$ is the dipole moment in Debye ($\text{D}$), $\alpha$ is the isotropic polarizability in $\text{a}_0^3$, and $H$ is the enthalpy at $298.15\text{ K}$ in Hartree.

### Mathematical Objective

For a conditional graph diffusion model or variational graph autoencoder, the parameters $\theta$ are optimized to maximize the conditional log-likelihood of valid molecular graphs while minimizing conditioning error:

$$\mathcal{L}(\theta) = \mathbb{E}_{(G, y) \sim \mathcal{D}} \left[ -\log p_\theta(G \mid y) \right] + \lambda \mathbb{E}_{\hat{G} \sim p_\theta(\cdot \mid y^*)} \left[ \left\| f_{\text{oracle}}(\hat{G}) - y^* \right\|_2^2 \right]$$

where $f_{\text{oracle}}$ is a pre-trained Graph Neural Network property regressor or DFT surrogate model.

---

## 3. Real-World Usefulness & Downstream Application Workflow

Small-molecule generative modeling underpins modern computer-aided drug discovery (CADD), agrochemical development, and material science for clean energy.

### Primary Application Domains

*   **Targeted Pharmaceutical Discovery:** Designing candidate ligand molecules with specific binding affinities and electronic properties while maintaining high drug-likeness (QED) and synthetic accessibility (SA score).
*   **Eco-Friendly Agrochemicals:** Generating low-toxicity crop protection agents designed to target specific pests while minimizing non-target ecotoxicity (e.g., reducing honeybee toxicity).
*   **Organic Photovoltaics & Energy Storage:** Designing organic semiconductors and redox-flow battery electrolytes with tailored HOMO–LUMO gaps ($\Delta \epsilon$) to optimize light absorption and voltage stability.

### Downstream Deployment Workflow

The following structured workflow illustrates how the generated model is deployed in an industrial computer-aided discovery pipeline:

```
+-----------------------------------------------------------------------+
|  1. Target Specification: Chemist inputs target property vector y*    |
|     e.g., Target HOMO-LUMO Gap = 4.2 eV, Polarizability = 75 a_0^3    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  2. Generative Sampling: Model p_theta(G | y*) generates K candidate  |
|     discrete molecular graph structures G_1, G_2, ..., G_K            |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  3. Automated RDKit Sanity Check: Fast local Python evaluation        |
|     Filters out chemically invalid graphs (valence/charge errors)    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  4. Oracle Property Verification: Pre-trained GNN / DFT Surrogate     |
|     Predicts y_hat for valid graphs and ranks candidates by MAE      |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  5. Wet-Lab Synthesis & Bioassay: High-ranking candidates move to     |
|     robotic chemical synthesis and experimental physical testing      |
+-----------------------------------------------------------------------+
```

---

## 4. Complete Dataset Specification: QM9 Benchmark

The QM9 dataset is the benchmark dataset for quantum-property-conditioned molecular generation.

### Key Dataset Attributes

The table below outlines the core specifications of the QM9 dataset:

| Property Dimension | Specification Detail |
| :--- | :--- |
| **Total Samples** | 133,885 small organic molecules |
| **Constituent Elements** | Carbon (C), Nitrogen (N), Oxygen (O), Fluorine (F), Hydrogen (H) |
| **Molecule Size Limit** | Up to 9 heavy atoms (C, N, O, F); up to 29 total atoms including H |
| **Computation Level** | Density Functional Theory (DFT) B3LYP/6-31G(2dp) |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **Programmatic Access** | Native PyTorch Geometric loader (`torch_geometric.datasets.QM9`) |
| **Storage Memory** | Approximately 85 MB in processed PyTorch Geometric tensor format |

### Property Labels Available in QM9

QM9 provides 19 physical and quantum chemical target properties for each molecule:

1.  **$\mu$:** Dipole moment ($\text{Debye}$)
2.  **$\alpha$:** Isotropic polarizability ($\text{a}_0^3$)
3.  **$\epsilon_{\text{HOMO}}$:** Energy of Highest Occupied Molecular Orbital ($\text{Hartree}$)
4.  **$\epsilon_{\text{LUMO}}$:** Energy of Lowest Unoccupied Molecular Orbital ($\text{Hartree}$)
5.  **$\Delta \epsilon$:** HOMO–LUMO energy gap ($\text{Hartree} \to \text{eV}$)
6.  **$\langle R^2 \rangle$:** Electronic spatial extent ($\text{a}_0^2$)
7.  **$\text{ZPVE}$:** Zero point vibrational energy ($\text{Hartree}$)
8.  **$U_0$:** Internal energy at $0\text{ K}$ ($\text{Hartree}$)
9.  **$U$:** Internal energy at $298.15\text{ K}$ ($\text{Hartree}$)
10. **$H$:** Enthalpy at $298.15\text{ K}$ ($\text{Hartree}$)
11. **$G$:** Free energy at $298.15\text{ K}$ ($\text{Hartree}$)
12. **$C_v$:** Heat capacity at $298.15\text{ K}$ ($\text{cal}/\text{mol}\cdot\text{K}$)

---

## 5. Active Research Landscape & Leading Institutions

Molecular graph generation represents one of the most active subfields of AI for Science, driven by major academic computer science departments and pharmaceutical AI divisions.

### Top Research Institutions & Laboratories

*   **MIT CSAIL (Broad Institute & Jameel Clinic):** Prof. Regina Barzilay and Prof. Tommi Jaakkola lead foundational research in property-conditioned graph generation and active learning for molecular synthesis.
*   **Stanford University (SNAP Lab):** Prof. Jure Leskovec's group develops graph neural network architectures and benchmarking frameworks (Open Graph Benchmark - OGB).
*   **University of Toronto & Vector Institute:** Prof. Alán Aspuru-Guzik's lab pioneer inverse design of materials and organic semiconductors using generative flows and diffusion models.
*   **ETH Zürich (Department of Chemistry and Applied Biosciences):** Focuses on automated synthesis planning and molecular graph generation.

### Leading Research Venues & Benchmark Papers

*   **Venues:** *NeurIPS (Datasets & Benchmarks Track)*, *International Conference on Machine Learning (ICML)*, *International Conference on Learning Representations (ICLR)*, *Journal of Chemical Information and Modeling (JCIM)*.
*   **Key Literature Anchors:**
    *   *DiGress: Discrete Denoising Diffusion for Graph Generation* (Vignac et al., ICLR 2023).
    *   *GraphAF: Flow-Based Autoregressive Graph Generation* (Shi et al., ICLR 2020).
    *   *MoFlow: An Invertible Flow Model for Molecular Graph Generation* (Zang & Wang, KDD 2020).

---

## 6. Four-Week Execution Plan & Empirical Baseline Setup

This project is structured for execution within a 4-week timeline using free GPU resources.

```
+-----------------------------------------------------------------------------------+
| WEEK 1: Data Pipeline & Baseline Integration                                      |
| - Load QM9 dataset via PyTorch Geometric.                                         |
| - Implement RDKit chemical validity checking module.                              |
| - Build baseline conditioning splitter (80% train, 10% val, 10% test).            |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| WEEK 2: Model Training & Algorithmic Comparison                                   |
| - Train conditional Graph VAE / Diffusion model on T4 Colab GPU.                  |
| - Implement 3-way methodological comparison:                                      |
|   (a) Masked constraint-aware sampling vs.                                        |
|   (b) Unconstrained generation + rejection vs.                                    |
|   (c) Post-hoc RDKit valence repair.                                              |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| WEEK 3: Empirical Evaluation & Metric Tracking                                    |
| - Compute Validity %, Uniqueness %, Novelty %, and Property MAE.                 |
| - Run memorization audit: Tanimoto similarity to nearest training neighbors.       |
| - Log metrics to Weights & Biases / TensorBoard.                                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| WEEK 4: Results Synthesis & Paper Completion                                      |
| - Generate comparative outcome tables and property conditioning scatter plots.    |
| - Write final research paper following conference submission guidelines.          |
+-----------------------------------------------------------------------------------+
```

### Core Evaluation Metrics

To evaluate model performance, the final report will measure four standard empirical metrics:

1.  **Validity ($\% \text{Valid}$):** Percentage of generated graphs that form chemically valid molecules according to RDKit valence rules.
2.  **Uniqueness ($\% \text{Unique}$):** Percentage of valid generated molecules that are non-identical to each other in the generated batch.
3.  **Novelty ($\% \text{Novel}$):** Percentage of valid generated molecules that do not appear anywhere in the QM9 training split.
4.  **Conditioning MAE ($\text{MAE}_y$):** Mean Absolute Error between target conditioning values $y^*$ and predicted values $\hat{y} = f_{\text{oracle}}(\hat{G})$.
