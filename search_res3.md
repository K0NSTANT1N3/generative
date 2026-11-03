# Research report: generative modeling problems where nearly all existing data is public and will stay scarce

Prepared against `prompt2.md` · 2026-10-21 · searched by Claude Code (Opus 5)

## 0. Verification status — read this first

This report is the output of roughly 13 web searches plus 2 direct page fetches. **Almost nothing here is confirmed at the primary source.** Two facts only were read off the hosting page directly:

| Fact | Status |
| --- | --- |
| ApisTox: CC BY 4.0, 1,035 instances, 13 features, CSV, 40.9 KB zip (131.9 KB raw), donated 2024-04-23 | **Confirmed** at the UCI dataset page |
| IZA Database of Zeolite Structures: 270 framework-type codes listed (including 20 interrupted frameworks); **no license or terms-of-use statement**, only "Copyright © 2017 Structure Commission of the International Zeolite Association" | **Confirmed** at the IZA framework-type table page |

Everything else — sample counts, growth rates, model sizes, runtimes, registration costs — is either a search-engine summary of a source I did not open, or my own estimate. Each claim is tagged. Section 6 lists what to audit first.

---

## 1. Short answer

**Generate pesticide-like molecular graphs conditioned on measured honey-bee toxicity, using ApisTox.** It is the only candidate I found that passes your three new criteria *and* all 8 course gates with a confirmed open license. The label is a live-bee laboratory assay, so no amount of compute creates more of it; the 1,035 molecules were compiled from public regulatory databases (US EPA ECOTOX, PPDB, BPDB), because pesticide registration is a public legal process; and the agrochemical generative-ML field is small, active (Pesti-Gen 2025, Mos-Gen 2026), and explicitly low-data — Mos-Gen reports working from about 200 labeled samples.

Runner-up is **zeolite framework-type generation** (IZA), which has the single best permanent-scarcity story of anything I found: 270 framework codes in total, worldwide, after 70 years of synthesis. It is ranked second only because **the IZA data carries no open license**, which fails course gate 6 as written. Third is **superconductor composition inverse design** (NIMS SuperCon, CC BY 4.0), which is weaker on your permanent-scarcity criterion.

I rejected chemical process flowsheets, metro networks, mineral species, approved drugs, quasicrystals and MOFs, each for a specific reason given below.

---

## 2. Screening table

**A** = public completeness (≈90%+ of all existing data is public, no much larger private holding)
**B** = permanent scarcity (cannot grow much in 5–10 years)
**C** = active research 2022–2026 (named lab + paper)
**G1–G8** = the course's 8 gates.

| # | Concrete problem | A | B | C | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **P1** | Generate pesticide-like molecular graphs conditioned on measured honey-bee toxicity class (ApisTox), checked with RDKit | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Pass | **Pass** | Pass | Pass | **Passes all** |
| **P2** | Generate novel zeolite framework topologies / pure-silica crystal structures matching the IZA framework distribution | Pass | **Pass (strongest)** | Pass | Pass | Pass | Pass | Cond. | Pass | **Fail** | Pass | Pass | Fails G6 |
| **P3** | Inverse design of superconductor compositions conditioned on target critical temperature (NIMS SuperCon) | Cond. | **Fail** | Pass | Cond. | Pass | Pass | **Fail** | Pass | Pass | Pass | Pass | Fails B, G4 |
| P4 | Generate chemical process flowsheets (SFILES 2.0 strings) conditioned on feed/product | **Fail** | Pass | Pass | Pass | Pass | Pass | Cond. | **Fail** | Pass | Pass | Fails A, G6 |
| P5 | Generate metro / subway network graphs conditioned on city geography | Pass | Pass | **Fail** | Pass | Cond. | Pass | Cond. | Pass | Pass | Pass | Pass | Fails C |
| P6 | Generate candidate new mineral species / crystal structures against the IMA approved list | Pass | Pass | **Fail** | Pass | Pass | Pass | Cond. | Pass | Cond. | Pass | Pass | Fails C |
| P7 | Generate molecules resembling the set of FDA/EMA-approved drugs | Cond. | Pass | **Fail** | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Fails C |
| P8 | Generate quasicrystal structures / compositions from the known quasicrystal inventory | Pass | Pass | **Fail** | Pass | Pass | Pass | Cond. | Pass | **Fail** | Pass | Pass | Fails C, G6 |
| P9 | Generate experimentally synthesizable MOFs (CoRE MOF) | **Fail** | **Fail** | Pass | Pass | Pass | Pass | Pass | Pass | Cond. | Cond. | Pass | Fails A, B |
| P10 | Generate analog circuit topologies (AnalogGenie) — *your earlier pick, re-screened* | **Fail** | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Fails A |

### One-line reason for every fail or conditional

- **P1** — no fails. G6 confirmed: ApisTox is CC BY 4.0 on UCI and Zenodo, 40.9 KB, instant download.
- **P2, G6 (fail)**: the IZA framework table shows only a 2017 copyright notice and no license or terms-of-use grant. Your gate 6 requires an open license; a bare copyright line is the opposite. **G4 (cond.)**: IZA's own topology check runs the TOTOPOL program as a *web form*, one structure at a time, and I could not confirm TOTOPOL is open source; `zeose` and `pymatgen` exist but I found no ready-made zeolite validity checker, so you would write your own.
- **P3, B (fail)**: SuperCon grows with every published measurement, and a December 2025 preprint reports extracting a *new* 78,203-record database with an LLM, which is the opposite of a frozen inventory. **G4 (fail)**: there is no fast free checker for superconductivity; you would need a surrogate trained on the same data, which is circular. **G1 (cond.)**: a composition is a set/multiset, which the guide allows, but it is the weakest "abstract structure" of the candidates. **A (cond.)**: SuperCon is the main public compilation, but corporate and national-lab measurement archives are not in it.
- **P4, A (fail)**: real flowsheets are proprietary plant designs. The TU Delft group pretrains on *synthetic* topologies and fine-tunes on real ones, and states a larger dataset of real flowsheets is still needed — so the public share is small, not ~90%. **G6 (fail)**: I found no confirmed open-access download for the real-flowsheet data.
- **P5, C (fail)**: I found no deep generative model for metro topologies. The adjacent work is street-network GANs, origin–destination flow diffusion, and ridership forecasting — none of which is your task. **G2 (cond.)**: metro maps are public objects, but a procedural generator can make plausible graphs cheaply, so the scarcity claim is about matching real systems, not validity. **G4 (cond.)**: rule-based geometry/connectivity checks only, no simulator.
- **P6, C (fail)**: the machine learning in this area predicts *where minerals occur* (mineral association analysis on Mindat, Carnegie/RPI, Hazen co-authored), not generative structure design. The only generative-AI mineral item I found is a Sciforum preprint evaluating chatbots, with "widely variable" results and reference problems. **G4/G6 (cond.)**: open crystallography data exists (COD) but the IMA-approved list itself is curated and I did not verify a license.
- **P7, C (fail)**: I searched specifically for generative models trained only on approved drugs (DrugBank, ChEMBL `max_phase 4`) and found none — only general memorization literature on medical imaging and LLMs. No lab to name means R1–R3 collapse. **A (cond.)**: "approved" is public by law, but pharma holds vastly larger private candidate libraries, which is the objection you raised about AqSolDB.
- **P8, C (fail)**: no quasicrystal database and no quasicrystal generative paper surfaced; results were general crystal-structure work (VQCrystal, CCDCGAN). **G6 (fail)**: no open quasicrystal dataset located.
- **P9, A (fail)**: CoRE MOF is curated from the Cambridge Structural Database, which is a licensed commercial product, and hypothetical MOF libraries (e.g. 137,953 combinatorially generated) show compute does make more MOF-like structures. **B (fail)**: the 2025 CoRE MOF update reports over 40,000 experimental MOFs by early 2024 and is growing fast.
- **P10, A (fail)**: re-screened under your new rule and it now fails for exactly the reason you gave — chip companies hold far more topologies, which is why AnalogFed proposes federated training.

---

## 3. Score table (candidates that pass the gates)

Scores are my judgment from search summaries, not bibliometric counts. P2 is scored even though it fails gate 6, because the gate might be rescued (see its deep dive).

| Candidate | R1 Labs | R2 Venues | R3 Growth | R4 Demand | H1 Headroom | H2 Not big-lab | H3 Critiquable | Total /14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **P1 Bee-toxicity-conditioned agrochemicals** | 2 | 1 | 2 | 2 | 2 | 2 | 2 | **13** |
| **P2 Zeolite frameworks** | 2 | 1 | 1 | 2 | 2 | 2 | 2 | **12** |
| P3 Superconductor compositions | 2 | 2 | 2 | 2 | 1 | 1 | 2 | **12** |

### Evidence behind the scores

| Candidate | Labs + one paper each (R1) | Venues (R2) / trend (R3) | Demand (R4) | Headroom + flaws (H1, H3) |
| --- | --- | --- | --- | --- |
| **P1** | Shanghai Institute of Organic Chemistry + DP Technology: Mos-Gen (arXiv 2606.01846, 2026). Adamczyk / Poziemski / Siedlecki (Polish Academy of Sciences, AGH): ApisTox (arXiv 2404.16196). Pesti-Gen authors incl. Taehan Kim (arXiv 2501.14469, 2025). Central China Normal University chemistry group: FungiPAD / PADFrag / Pesti-DGI-Net toolkit (Accounts of Chemical Research, 2026) | R2 = 1: *Journal of Cheminformatics*, *Accounts of Chemical Research*, *Transactions of the CSAE* — credible domain venues, but I found **no NeurIPS/ICML/ICLR agrochemical generation paper**. R3 = 2: 2024 fungicide transformer preprint → ApisTox 2024 → Pesti-Gen Jan 2025 → MHA-RNN 2025 → Mos-Gen 2026 → latent-diffusion agrochemical 2026 | Pollinator decline and pesticide risk assessment are regulated by the US EPA and EFSA; ApisTox standardizes toxicity to µg/bee per US EPA guidance. Bee-safety data requirements are a legal condition of registration | **H1 = 2**: Pesti-Gen reports only ~68% chemical validity — RDKit-valid output is close to a solved problem elsewhere, so the floor is very low. **H3 = 2**: Pesti-Gen fine-tunes on toxicity and then evaluates with its own toxicity model (circular); ApisTox's authors report that methods successful in medicinal chemistry often fail to generalize to agrochemicals; I found no memorization audit anywhere in this literature |
| **P2** | Korean group behind ZeoDiff (*J. Mater. Chem. A*, 2024, DOI 10.1039/d3ta06274k); ZeoNet synthetic-feasibility work (arXiv 2601.17253, 2026); Zeo-1 dataset authors (2022); Deem's Monte Carlo lineage | R2 = 1: *J. Mater. Chem. A*, *Phys. Chem. Chem. Phys.*, *Faraday Discussions*. Strong domain venues, no top-ML venue found. R3 = 1: steady, not fast | Zeolites are the catalyst backbone of petrochemical refining and ion exchange; the IZA Structure Commission is an international standards body | **H1 = 2**: ZeoDiff's own framing is that the prior GAN had catastrophic validity (it reports >2000× improvement), so validity is still the open problem. **H3 = 2**: ZeoDiff trains on **IZA/PCOD mixed** — PCOD is a computationally enumerated hypothetical database, so "novel structure" claims are measured partly against compute-generated data. That conflation is a clean critique and is exactly your objection, in print |
| **P3** | Fujii et al., domain-knowledge-constrained deep generative models for high-Tc (arXiv 2403.13627); LLM-extracted superconductor DB + inverse design (arXiv 2512.10847); Stanev et al. (*npj Computational Materials*, 2018) is the standard reference | R2 = 2: *npj Computational Materials*. R3 = 2: active through 2025 | Superconductors matter for grid transmission, MRI and magnets | **H1 = 1**: Tc prediction is relatively mature. **H3 = 2**: the 2512 preprint reports "28% novel candidates", which is a novelty metric with no memorization audit behind it |

---

## 4. Deep dives

### 4.1 — P1 (recommended): bee-toxicity-conditioned agrochemical generation

**Project title suggestion:** *Memorization-Aware Conditional Generation of Pesticide-Like Molecules Under Measured Honey-Bee Toxicity*

**Problem statement.** Given a target honey-bee toxicity class, generate novel, chemically valid, pesticide-like molecular graphs. The research question is whether constraint-aware decoding and uncertainty-aware conditioning beat a plain conditional generator when only ~1,000 assayed molecules exist — and how much of the reported "novelty" in this young literature survives a proper near-duplicate audit.

**Formal setup.**
- Molecular graph $G=(V,E,\mathbf{x},\mathbf{e})$: atoms as vertices, bonds as edges.
- Training set $D=\{(G_i,y_i)\}_{i=1}^{N}$, $N\approx 1{,}035$, with $y_i$ the measured honey-bee toxicity class (standardized to µg/bee per US EPA guidance; the dataset ships a toxicity label plus identifiers).
- Condition: target class $y^\ast$ (e.g. non-toxic), optionally a pesticide-likeness band.
- Output: $G\sim p_\theta(G\mid y^\ast)$.
- Hard constraints: allowed elements, valence, connectivity, max heavy-atom count, RDKit sanitization.
- Soft objectives: pesticide-likeness (Avram et al.'s six-property score: MW, logP, HBA, HBD, rotatable bonds, aromatic rings), novelty, diversity, predicted-toxicity alignment.

**Criterion A — public completeness.** ApisTox is a *compilation of three public databases*: US EPA ECOTOX, the Pesticide Properties Database (PPDB) and the Bio-Pesticides Database (BPDB). Honey-bee acute toxicity studies are a legal requirement for pesticide registration in the US and EU, and registration dossiers feed these public databases. So the public share is high by regulatory construction. **Honest caveat, unverified:** companies certainly hold unpublished internal bee assays on compounds they never registered, and I did not quantify that. This is the weakest link in the argument and you should say so in the paper rather than overclaim.

**Criterion B — permanent scarcity.** Each label is an acute toxicity assay on live honey bees under OECD-style test guidelines: real colonies, real exposure periods, real mortality counts. No compute produces one. Growth is bounded by how many new active ingredients get registered per year, which is a handful globally. **Unverified:** I did not find a measured year-by-year growth rate for ApisTox or for its upstream databases; get this from ECOTOX release notes before you cite any number. I previously told you registrations cost "~$300M each" — **I did not verify that and you should not cite it.**

**Dataset.**

| Item | Value | Status |
| --- | --- | --- |
| URL | `archive.ics.uci.edu/dataset/995/apistox`; mirror at `zenodo.org/records/13350981` (v2, 2024-08-20) | **Confirmed** |
| License | **CC BY 4.0** | **Confirmed** |
| Samples | **1,035 instances, 13 features** | **Confirmed** |
| Size | **40.9 KB zip** (`apistox.zip`), 131.9 KB CSV (`dataset_final.csv`) | **Confirmed** |
| Format | CSV | **Confirmed** |
| Creators | Jakub Adamczyk, Jakub Poziemski, Paweł Siedlecki; donated 2024-04-23 | **Confirmed** |
| Paper | arXiv 2404.16196; also PMC11696378 (*Journal of Cheminformatics*) | Not opened |

Supplementary corpora you may want for pretraining (**all unverified**): AgroPAD/FungiPAD is described as covering 512 insecticides, 377 fungicides and 542 herbicides; PADFrag is a pesticide fragment database. Check their licenses before use.

**Validity checker.** RDKit (`rdkit.org`, BSD-3). Checks parseability, valence, sanitization, connectivity; also provides canonical SMILES, InChIKey, Murcko scaffolds and ECFP fingerprints. My estimate: **0.2–5 ms per small molecule on CPU** — this is a planning estimate, not a benchmark; time it yourself in Week 12, which the course requires anyway. Pesticide-likeness via the Avram et al. six-property rule is a few RDKit descriptor calls, so effectively free. **Critical honesty point for your paper:** RDKit verifies *chemistry*, never *bee toxicity*. The toxicity side can only be estimated by a surrogate trained on the same 1,035 points, which is the circularity you must design around, not hide.

**Baselines.**

| Model | Family | Code | Note |
| --- | --- | --- | --- |
| Pesti-Gen (arXiv 2501.14469) | Conditional VAE, pretrain + toxicity fine-tune | **No repo found** | Closest prior work; reports ~68% validity. No code located despite a targeted search |
| Mos-Gen (arXiv 2606.01846) | Uni-Mol encoder + VAE, motif-aware | **No repo found** | Works at ~200 labeled samples; 14 compounds synthesized, 78% hit rate among predicted positives |
| MHA-RNN (*Transactions of the CSAE*, 2025) | Scaffold-based RNN | Not checked | Pesticide-specific generator |
| HI-Mol (ICML 2024, arXiv 2405.02845) | Hierarchical textual inversion | PMLR v235/kim24z | **Data-efficient molecular generation — directly relevant method, top-ML venue** |
| DiGress (ICLR 2023) | Discrete graph diffusion | `github.com/cvignac/DiGress`, MIT | Generic strong baseline; older CUDA stack, budget setup time |
| Graph DiT (NeurIPS 2024) | Graph diffusion transformer, property-conditioned | `github.com/liugangcode/Graph-DiT` | Property conditioning is the matching capability |
| JT-VAE | Junction-tree VAE | `github.com/wengong-jin/icml18-jtnn` | Original repo targets Python 2.7; reimplement rather than resurrect |

That **neither Pesti-Gen nor Mos-Gen has findable code** is simultaneously the biggest risk (nothing to reproduce) and the biggest opening (no public baseline to beat, so a clean public implementation is itself a contribution).

**Open levers (4 weeks, pick two).**
1. **Memorization audit (evaluation).** Nobody in this literature has published one. Report exact-duplicate and near-duplicate rates against training data as a function of training length and sampling temperature. Cheap, certain to produce a result.
2. **Constraint-aware decoding (sampling).** Mask atom/bond actions that would violate valence or connectivity, instead of generating then rejecting. Measure the valid×novel trade-off. Pesti-Gen's ~68% validity means there is enormous room here.
3. **Uncertainty-aware guidance.** Train an ensemble of toxicity regressors/classifiers; during sampling prefer candidates near the target *and* penalize ensemble disagreement. Compare against single-predictor guidance and no guidance.
4. **Leakage-resistant evaluation.** Compare random splits against Bemis–Murcko scaffold splits, and score with a predictor held out from guidance. Tests whether apparent conditioning gains survive.

Best pairing for Phase 2: **lever 1 as the analysis + lever 2 as the one methodological improvement.** Lever 3 if time allows.

**Memorization protocol.**
1. Standardize every training and generated molecule with RDKit: neutralize charges, strip salts, canonicalize tautomers, decide stereochemistry handling once and document it.
2. Exact duplicates: canonical isomeric SMILES or standardized InChIKey, both train-vs-generated and generated-vs-generated.
3. Near duplicates: max ECFP4 Tanimoto similarity to the nearest training molecule, reported at pre-declared thresholds (0.8, 0.9), alongside the **train-to-train** nearest-neighbor distribution as the control.
4. Scaffold overlap: Bemis–Murcko scaffold match rate against training scaffolds.
5. Split before any augmentation, and group all SMILES variants of one molecule together so one molecule cannot appear in both splits.

**GPU-hours on a free T4 (all estimates).**

| Work | GPU-hours |
| --- | --- |
| Compact conditional graph generator, 1,035 molecules (+ optional pretraining on a few thousand agrochemicals) | 0.5–1.5 |
| Guided-generation improvement + evaluation sweeps | 0.5–1.0 |
| Ablations and debugging reserve | 0.5–1.0 |
| **Total** | **1.5–3.5** |

The dataset is 40 KB, so setup is `pip install rdkit torch` plus a trivial download — comfortably inside the 5-minute rule, and the easiest gate-7 and smoke-test story of any candidate here. Most checking is CPU.

**Why a practitioner cares, and how they'd test output.** Agrochemical discovery teams need candidate actives that are effective *and* pollinator-safe, because bee-toxicity data is a registration requirement. They would screen generated structures for synthetic accessibility, synthesize the plausible ones, and run a standard acute contact/oral honey-bee assay. Mos-Gen's authors did exactly this chain — synthesized 14 generated compounds and tested them — which is proof the loop is real.

**Risks and fallback.**
- **~1,035 molecules is very small.** A generator may simply reproduce known pesticides. *That is why the memorization audit is the contribution, not a side-check.* Mos-Gen at ~200 samples and the Nature Machine Intelligence low-data results suggest it is workable; still, pretraining on a larger public molecular corpus is the standard fix, and it does not break criteria A/B as long as the *measured labels* stay the scarce part. Say this explicitly in the paper.
- **No reproducible baseline.** Budget time to implement your own conditional baseline rather than hunting for Pesti-Gen's code.
- **Circular evaluation.** Never score with the same model you guided with.
- **Class imbalance / label semantics.** ApisTox is a classification dataset; verify what the 13 columns actually contain before formalizing $y$.
- **Fallback.** Drop conditioning and publish the evaluation paper: a memorization and leakage audit of low-data molecular generation in agrochemistry, with a clean public baseline. That is defensible on its own and needs no new model.

---

### 4.2 — P2: zeolite framework generation (best scarcity story, licensing problem)

**Problem statement.** Generate novel pure-silica zeolite framework structures that are geometrically and topologically valid and distributionally faithful to the ~270 framework types humanity has actually synthesized, without copying them.

**Formal setup.** Output is a periodic crystal structure: lattice $L\in\mathbb{R}^{3\times3}$ plus T-atom (Si) and O positions in the unit cell, or equivalently the 4-connected T-atom net as a periodic graph. Condition on pore descriptors (void fraction, largest included sphere) or ring-size distribution. Hard constraints: 4-connectivity of every T atom, T–O–T bridging, physical T–O bond lengths and O···O separations, no atom overlap, space-group consistency.

**Criterion A — public completeness: the strongest of any candidate.** A framework type *is* a three-letter code assigned by the IZA Structure Commission, an international standards body whose database is the public record. A private company cannot hold a larger collection of approved framework types, because approval is the public act. **Confirmed:** 270 codes listed (including 20 interrupted frameworks).

**Criterion B — permanent scarcity: also the strongest.** Related work indicates 204 frameworks in the 2014 database version against ~255–270 now, i.e. roughly 4–5 new framework types per year worldwide (**unverified, inferred from two search summaries**). Each requires a successful hydrothermal synthesis plus a solved crystal structure — years of work by specialist groups. After ~70 years of zeolite chemistry, the total inventory is still under 300.

**Dataset.**

| Item | Value | Status |
| --- | --- | --- |
| URL | `europe.iza-structure.org/IZA-SC/ftc_table.php` (per-framework CIF downloads); mirror at `america.iza-structure.org` | **Confirmed** |
| Count | **270 framework-type codes**, 20 of them interrupted | **Confirmed** |
| **License** | **None stated. Only "Copyright © 2017 Structure Commission of the International Zeolite Association"** | **Confirmed — this is the blocker** |
| Format | CIF per framework (plus PDF) | **Confirmed** |
| Size | Tiny; CIFs are a few KB each | Estimate |
| Related open sets | Zeo-1 (Materials Cloud) reports properties for 204 of ~256 framework types; PCOD is a large *hypothetical* enumeration | Unverified |

**Why it fails gate 6, and how you might rescue it.** Your gate requires an open license with instant download. The download is instant; the license is absent, which is not the same as permissive. Three options: (a) email the Structure Commission and ask for written terms — fast, but your gate forbids waiting on anything; (b) use Zeo-1 on Materials Cloud instead, if its license is open — **verify this first, it may be the whole fix**; (c) drop to runner-up status. Do not assume "publicly posted" means "openly licensed" — that distinction is precisely what gate 6 is testing, and your grader will check it.

**Validity checker (you build it).** IZA hosts a topology check powered by **TOTOPOL** (M. M. J. Treacy) that reports coordination sequences and vertex symbols and tells you whether a framework already has a three-letter code — conceptually ideal, but it is a one-structure-at-a-time web form and I could not confirm it is open source. Buildable alternative: `pymatgen` + `zeose` (open-source, ASE-based, NetworkX ring finding) for parsing and ring analysis, plus explicit geometric screens — the literature proposes screening hypothetical zeolites on closest non-adjacent O···O distances. `mofchecker` is a good design template (it accepts a pymatgen structure and checks overlapping atoms). **Estimate: 10–100 ms per structure**, unverified.

**Baselines.** ZeoDiff (*J. Mater. Chem. A* 2024, DOI 10.1039/d3ta06274k): diffusion model for pure-silica zeolites, **5.6M parameters, 1500 diffusion steps, batch size 128** (from a search summary of the SI, not confirmed), does inverse design on void fraction, Henry coefficient and heat of adsorption, and claims >2000× structure-validity improvement over the earlier GAN. Kim et al. (*Science Advances* 2020): GAN trained on 31,713 known zeolites producing 121 porous materials. ZeoNet (arXiv 2601.17253, 2026): synthetic-feasibility classifier, trained on IZA 2014 and refined on IZA 2025 — useful as a *surrogate oracle*.

**Open levers.** (1) **The IZA/PCOD critique**: ZeoDiff's training figure captions "structures in training dataset (IZA/PCOD)", mixing ~270 real frameworks with a large hypothetical enumeration. Separating the two and re-measuring novelty against *real* frameworks only is a sharp, cheap contribution that is also exactly your philosophical objection. (2) Constraint-guided denoising enforcing 4-connectivity and O···O minima during sampling. (3) A validity metric that uses coordination sequences / vertex symbols (topological identity) instead of geometric plausibility alone.

**Memorization protocol.** Canonicalize to the T-atom periodic net; compare with `pymatgen`'s `StructureMatcher` for near-identity, and hash the quotient graph (Weisfeiler–Lehman) with VF2 confirmation for topological identity. Report distance to the nearest *real IZA* framework, never to a hypothetical one.

**GPU-hours.** ~1–2 on a T4 (estimate); ZeoDiff's 5.6M parameters and a sub-300-structure real training set are tiny. Compute is not the constraint here; data volume is.

**Why a practitioner cares.** Zeolites are industrial catalysts and adsorbents; a proposed framework with a target pore geometry is a synthesis target. Testing means attempting hydrothermal synthesis and solving the structure — slow and expensive, which is the whole point of gate 2.

**Risks and fallback.** Licensing (above) is the main one. Second: with <300 real structures, a diffusion model may memorize outright — again, that becomes the finding. Third: crystallography has a steeper learning curve than molecules (space groups, periodic boundary conditions) and you said you prefer a short one. Fallback: keep it as a critique paper on IZA/PCOD conflation in reported zeolite novelty, using the released ZeoDiff setup.

---

### 4.3 — P3: superconductor composition inverse design (fails your criterion B)

**Problem statement.** Given a target critical temperature $T_c$, generate chemical compositions predicted to superconduct at it. Output is a composition vector / multiset over elements with stoichiometric coefficients.

**Criterion A (conditional).** NIMS SuperCon is the field's main public compilation, moved to the Materials Data Repository in December 2022, CC BY 4.0 on the readme-linked files, explicitly intended for machine learning — it even ships a `primary.tsv` with recommended $T_c$ values the maintainers ask you to use for testing. But corporate and national-lab archives are outside it.

**Criterion B (fails).** The record count keeps growing: a Dec 2025 preprint reports an LLM-extracted database of **78,203 records** and fine-tunes LLMs for inverse design, reporting 28% novel candidates. An inventory that a language model can expand by scraping literature is not permanently scarce in your sense.

**Gate 4 (fails).** There is no free fast checker for superconductivity. Validity would mean charge balance and known-phase plausibility; actual $T_c$ requires a surrogate trained on the same data — circular, and much weaker than RDKit or ngspice.

Included because the labs (Fujii et al., arXiv 2403.13627; Stanev et al., *npj Comput. Mater.* 2018) and venues are genuinely strong, so it scores 12/14. But on your own stated rule it is out.

---

## 5. Starter reading list — P1 (bee-toxicity-conditioned agrochemicals)

**Honesty note:** your prompt asked for 15–20 papers. I located **15** relevant items, and I am not padding the list with invented or unchecked citations to reach 20. Items 1–10 are agrochemical-specific; 11–15 are the method/baseline layer. I opened **none** of these PDFs — every venue, year and license below came from a search summary or an aggregator page and must be audited. Read 1, 2, 3 and 4 first.

| # | Title | Venue, year | Link | Code / data | License | Known flaw / limitation to investigate |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ApisTox: a new benchmark dataset for the classification of small molecules toxicity on honey bees | *J. Cheminformatics* (PMC11696378); arXiv 2024 | arXiv 2404.16196 | UCI dataset 995; Zenodo 13350981 | **CC BY 4.0 (confirmed)** | Classification, not regression; compiled from three heterogeneous sources (ECOTOX, PPDB, BPDB) with differing protocols; authors note medicinal-chemistry methods often fail to generalize here |
| 2 | Pesti-Gen: Unleashing a Generative Molecule Approach for Toxicity Aware Pesticide Design | arXiv, Jan 2025 | arXiv 2501.14469 | **No repo found** | Not checked | ~68% chemical validity is very low; fine-tunes on toxicity then evaluates with its own toxicity model (circular); custom dataset, not a public benchmark |
| 3 | Mos-Gen: A Generative Molecular Framework for Mosquito Insecticide Design | arXiv, 2026 | arXiv 2606.01846 | **No repo found** | Not checked | ~200 labeled samples; narrow target class (disulfide allicin derivatives); 78% hit rate is on *predicted positives*, not on all generations |
| 4 | Quantitative estimation of pesticide-likeness for agrochemical discovery | *J. Cheminformatics*, 2014 | PMC4173135 | Not checked | Not checked | Six-property rule-of-thumb validated on patented pesticides; a descriptor filter, not a validity oracle — easy to game |
| 5 | Fragment-based design of pesticide-like molecules: from method development to agrochemical discovery | *Accounts of Chemical Research*, 2026 | doi 10.1021/acs.accounts.6c00580 | HerbiPAD / InsectiPAD / FungiPAD / PADFrag / DigFrag | Not checked | Review; the PAD tools are web services — check batch access and licensing before depending on them |
| 6 | AgroPAD / FungiPAD database of approved pesticides | Web database (CCNU) | chemyang.ccnu.edu.cn/ccb/database/FungiPAD | Web only | **Not checked — likely no open license** | Reported as 512 insecticides / 377 fungicides / 542 herbicides (unverified); web interface may block bulk download, mirroring the IZA problem |
| 7 | PestiGen: RL framework (character-based + fragment-based MCTS) for pesticide design | IBDC summary record 8XLX | ibdc.dbtindia.gov.in/isda/summary/8XLX | Not checked | Not checked | Found only via a database summary page, not the paper; target-protein binding focus; "superior pesticide-likeness" claim unaudited |
| 8 | Design and optimization of novel succinate dehydrogenase inhibitors against agricultural fungi based on Transformer model | bioRxiv, 2024 | 10.1101/2024.02.20.581130 | Not checked | Not checked | Preprint; ~91,961-molecule virtual library then docking — docking scores are a weak oracle; no memorization check |
| 9 | Molecular Design of Novel Herbicide and Insecticide Seed Compounds with Machine Learning | ACS (figshare record 25571745) | acs.figshare.com/articles/journal_contribution/25571745 | figshare | Not checked | Ensemble screening/selection rather than generation; 186 herbicide and 12 insecticide candidates, only 2 active on test |
| 10 | MHA-RNN: scaffold-based pesticide molecule generation | *Transactions of the CSAE*, 2025 | doi 10.11975/j.issn.1002-6819.202409017 | Not checked | Not checked | Chinese-language venue, harder to audit; scaffold-constrained, so novelty is bounded by construction |
| 11 | Data-Efficient Molecular Generation with Hierarchical Textual Inversion (HI-Mol) | **ICML 2024** | arXiv 2405.02845; PMLR v235/kim24z | Check PMLR page | Not checked | Reports 50× less data on QM9 — but QM9 is DFT-labeled and enumerated, so transfer to assay-labeled agrochemicals is unproven. **Your top-ML-venue anchor** |
| 12 | Generative molecular design in low data regimes (Moret et al.) | *Nature Machine Intelligence*, 2020 | ETH research-collection 429159 | Not checked | Not checked | Pre-diffusion era (RNN/transfer learning); no memorization audit |
| 13 | Robust RNN molecular generators trained on few molecules | *Nature Machine Intelligence*, 2021 | doi 10.1038/s42256-021-00368-1 | Not checked | Not checked | "Fewer molecules than assumed" is an empirical claim on drug-like space, not agrochemical space |
| 14 | DiGress: Discrete Denoising Diffusion for Graph Generation | ICLR 2023 | github.com/cvignac/DiGress | GitHub | MIT | Older CUDA/PyTorch stack and compiled deps — a real threat to your 5-minute setup rule; unconditional by default |
| 15 | Graph DiT: Graph Diffusion Transformer for multi-conditional molecular generation | NeurIPS 2024 | github.com/liugangcode/Graph-DiT | GitHub | Not checked | Property conditioning relies on predictor quality; trained on larger datasets than yours |

**Gap to close yourself:** search for (a) a memorization or data-leakage audit in *molecular* generative models (the course's H3 angle — I found this literature only for medical imaging and LLMs), (b) OECD honey-bee acute toxicity test guidelines as the primary source for your gate-2 argument, (c) ECOTOX/PPDB release histories for a real data-growth rate. Those three fill both the reading list and your weakest evidence.

---

## 6. Claims to verify at the primary source, in priority order

**Blocking — verify before you commit to a topic:**
1. **ApisTox's 13 columns.** What exactly is the toxicity label (binary? three classes? units?), and how many molecules fall in each class? Your whole formal setup depends on it. Open `dataset_final.csv`.
2. **Whether ApisTox has enough per-class data to condition on at all.** 1,035 rows split across classes could leave a few hundred in the minority class. This is the single biggest risk to P1.
3. **IZA licensing.** Read the "Terms & Credits" page on `iza-structure.org`. If it grants nothing, P2 fails gate 6 as written. Then check **Zeo-1 on Materials Cloud** for an open license, since that may rescue the candidate.
4. **Whether Pesti-Gen or Mos-Gen released code anywhere** (authors' GitHub, paper appendix, lab pages). I found none; if one exists, your baseline problem gets much easier.

**Important — verify before writing Section 5 of the paper:**
5. **My criterion-A argument for ApisTox**, that registration law pushes bee-toxicity data into public databases. Check EPA/EFSA data requirements, and be upfront that unregistered private assays exist.
6. **Data growth rate** for ECOTOX / PPDB / BPDB. I have no verified number. Do not cite my "handful per year".
7. **The "~$300M per registration" figure I gave you earlier in conversation — unverified, do not use.**
8. **ZeoDiff's actual training set composition** (IZA only vs IZA+PCOD, and counts). My whole proposed critique of it rests on a figure caption seen through a search summary. Open DOI 10.1039/d3ta06274k and its SI.
9. **IZA framework-type growth** (204 in 2014 → 270 now). I inferred this across two unrelated summaries; confirm from IZA's own version history.
10. **AgroPAD/FungiPAD counts and license** (512/377/542) before using it for pretraining.

**Routine — audit during Week 8's literature log:**
11. Every venue and year in Section 5. I opened no PDFs. In particular, confirm items 10 and 5 exist in the venues claimed, and treat item 7 (found only via a database summary page) with suspicion.
12. RDKit per-sample runtime: measure it; my 0.2–5 ms is an estimate.
13. All GPU-hour estimates: mine, untested, on hardware I cannot see.
14. Mos-Gen's "~200 labeled samples" and "78% hit rate", and Pesti-Gen's "~68% validity" — these numbers carry a lot of weight in my H1 argument.
15. That no memorization audit exists in the agrochemical generative literature. This is my *absence-of-evidence* claim, and it is the core of your contribution. Absence found via a handful of searches is weak evidence; search Google Scholar deliberately before claiming novelty in print.

---

## 7. Bottom line

Your added rules knocked out your own two earlier picks and most of the obvious alternatives. What survives is small and specific:

- **P1 (agrochemicals / ApisTox) is the recommendation.** It is the only candidate passing A, B, C and all 8 gates with a *confirmed* open license, and it has the lowest setup and compute risk of anything screened (40 KB of data, RDKit, 1.5–3.5 T4-hours). Its weakness is dataset size, and the honest response is to make memorization the subject of the paper rather than a checkbox.
- **P2 (zeolites) has the better scarcity story and the better ready-made critique** (the IZA/PCOD conflation), but a licensing problem that may be fatal to gate 6 and a steeper learning curve than you asked for. Spend thirty minutes on the IZA terms page and the Zeo-1 license before deciding — that one check could promote it.
- Everything else fails on a criterion you named, most often **C (nobody is researching it)** or **A (a company holds much more)**.

A general caution worth putting in your Limitations section: the stricter your "all public, permanently scarce" rule, the smaller and quieter the field, which pushes R1–R3 down. P1 scores 13/14 only because the agrochemical ML community is active; it is weak precisely on R2, with no top-ML-venue paper in the area. That is a trade you are making deliberately, and saying so explicitly in the paper is stronger than pretending otherwise.
