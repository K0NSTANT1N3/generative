# Audit of existing generative-model work: glycans and microbial natural products

Prepared against `prompt3.md` · 2026-10-23 · Claude Code (Sonnet 5.5)

## How to read the evidence tags

| Tag | Meaning |
| --- | --- |
| **[C]** | Confirmed: I read it in the paper PDF, the official repo, or the dataset's own page during this session |
| **[S]** | Seen only in a search-result snippet or an aggregator page. Not opened at the source. Treat as unverified |
| **[E]** | My own estimate, with reasoning given |
| **[NR]** | Not reported by the authors, in the parts I could read |

Sources I could **not** read, so their rows contain gaps: the *Cell* 2025 paper (HTTP 403 from Cell; the MIT-hosted copy returned an HTML page, not a PDF), the GlycanGT supplementary tables S2 and S3 (parameter counts and epochs live there), the NP-VAE methods section (the fetch covered only the first ~100k of ~395k characters), and the GlyTouCan terms page (it did not render; its CC0 wording comes from a search snippet).

---

## 1. Short answer

1. **No de novo glycan generator exists in what I could find.** The paper whose title says "Generative Learning" (GlycanGT) does masked completion: it fills in missing monosaccharides and linkages in a partly known glycan. It does not sample new glycans from scratch. The only glycan models that produce structures are GlycoBART (spectrum in, glycan out) and a 2024 Boltzmann model (lectin-binding fingerprint in, ranked candidate glycans out). Neither is function-conditioned design of new glycans, and the Boltzmann model has no released code. That gap is real, but see the data risk below before you build on it.
2. **Natural-product generation is crowded and mostly unconditional.** Every generator I found imitates the distribution of known natural products. Only the antibiotic papers (*Cell* 2025, *JACS Au* 2025) aim at a function, and they do it with large labs, wet-lab synthesis and licensed or non-public training data.
3. **Nobody ran a real memorization audit in either field.** "Novelty" always means "not an exact copy of a database entry". This is the common opening in both domains.
4. **Glycans fit your T4 budget much better than natural products.** Glycan graphs are tiny (about 7 monosaccharides on average) and the usable set is about 84k structures. The recent natural-product models were trained on 4 GPUs or A100s for hours to a week.
5. **Biggest risk for glycans is function labels, not structures.** GlyTouCan's site content is stated as CC0 (via snippet), but I found **no license** for the lectin-binding data that would give a glycan model a goal. Without a goal you are back to unconditional generation, which you already rejected as "no problem being solved".

---

## 2. Glycans

### 2.1 Papers table

| # | Paper (lab, venue, year, link) | What it generates, and for what | Cond.? | Model, size | Training data | Free now? | Compute | Code | Memorization check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G1 | **GlycanGT**: Kitani, Zhang, Himori, Matsui. Nagoya University (Graduate School of Medicine; iGCORE). bioRxiv 2025-12, DOI 10.64898/2025.12.14.694171; the paper itself says CC-BY 4.0. A model card cites *Bioinformatics* 2026 [S] | Fills in missing monosaccharides and linkages in partly known glycans, to help curate databases. Also gives embeddings for classification **[C]** | Unconditional completion; **not de novo generation** | Graph transformer (TokenGT), four scales ss/small/medium/large. Param counts in Supp. Table S2, which I could not read **[NR]** | 244,842 GlyTouCan entries via GlyCosmos (as of 2025-06-17), minus ambiguous ones and downstream-task overlaps, leaving **83,739** (the README says 83,740) **[C]** | Data: yes (see §4). **Weights are gated on Hugging Face** (click-through contact-info form) **[S]** | NVIDIA **L40, 46 GB** **[C]**. AdamW lr 1e-6, early stopping (patience 15 epochs for ss/small, 30 for medium/large). **Hours, epochs and batch size [NR]** in main text | github.com/matsui-lab/GlycanGT, **Apache-2.0** **[C]** | None. Leakage handled only by removing downstream-task glycans from pretraining |
| G2 | **GlycoBART**: bioRxiv 2025-07, DOI 10.1101/2025.07.02.662857. Group not named in what I read | Glycan structure from an MS/MS spectrum (spectrum to glycan "sentence"), including structures absent from training **[C]** | Conditional on the spectrum | BART seq2seq, 12+12 layers, 768-dim, 16 heads, **~207M params** **[C]** | CandyCrunch v2: 510,160 spectra, 3,590 glycans; **503,446** spectra kept. Zenodo doi 10.5281/zenodo.15741423 **[C]** | Zenodo data: **license not stated** | **4x RTX A5000**, 30 epochs, batch 80, AdamW lr 1e-5. **Hours [NR]** | github.com/cabsel/glycotrans; license **not stated** | None. Authors note spectra from one MS run can land in both train and test, which may inflate accuracy. Two de novo structures were not confirmed experimentally |
| G3 | **Boltzmann model of glycan structure from lectin binding**: Yom, Chiang, Lewis. UC San Diego and Augusta University. *Analytical Chemistry* 96(21):8332 (2024-05) **[C]** | Ranked candidate glycans whose composition and approximate structure match a lectin-binding fingerprint. Candidates = CFG glycans + about 10^4 glycans sampled from a Markov model **[C]** | Conditional on binary lectin fingerprint (64 lectins, 9 antibodies) | Two-layer fully visible Boltzmann model; Markov generator (entropy 12.3 bits). **Size [NR]** | CFG Mammalian Glycan Array + 25 CHOGlycoNET glycans. Glycan count **[NR]**; license **not stated** | Supplementary files only | **[NR]**; plain gradient descent (step 0.1) | **No code repository mentioned** | Exact structure 61 +/- 10% (N-glycans); top-3 88 +/- 7%. No train-set similarity audit |
| G4 | **GIFFLAR**: Joeres, Bojar. U. Gothenburg + Saarland U. **NeurIPS 2024**, arXiv 2409.13467 **[C]** | Representation learning (predicts glycan properties). **Not generative** | n/a | Higher-order message passing, **35.1M params** | Extended GlycanML tasks. Taxonomy: 11,378 / 3,170 / 1,579 train/val/test glycans. Immunogenicity: 825 / 230 / 113. Lectin-glycan interaction: **388,731** / 110,885 / 55,593 rows **[C]** | Data and splits in the repo's `datasets` folder; **license not confirmed** | **RTX 3090 (24 GB): 45.0 min** (Domain task) **[C]** | github.com/BojarLab/GIFFLAR; license not checked | n/a |
| G5 | **SweetNet**: Burkholz, Bojar et al. U. Gothenburg. PMC9208909 | Property and species prediction. **Not generative** | n/a | GCN, 128-dim nodes, 3 graph conv layers. Params **[NR]** (GIFFLAR's table lists **37.2M**) **[C]** | Glycan table from glycowork (~50.5k unique glycans **[S]**) | Via glycowork | **Tesla K80** (original), up to 100 epochs, batch 32. On an RTX 3090 SweetNet took **22.7 min** (GIFFLAR Table A1) **[C]** | github.com/BojarLab/SweetNet. glycowork itself: **MIT** **[C]** | n/a |
| G6 | **GlycanML**: Xu, Geng, Zhang, Yang, Tang, Zhang. arXiv 2405.16206 (2024), no venue named **[C]** | Benchmark for property prediction. **Not generative** | n/a | Many baselines | Four task types: taxonomy, immunogenicity, glycosylation type, protein-glycan interaction **[C]** | github.com/GlycanML/GlycanML; **license not stated** | GPU **[NR]** | Same repo | n/a |
| G7 | **LectinOracle**: Lundstrom, Korhonen, Lisacek, Bojar. *Advanced Science* 2022 | Predicts lectin to glycan binding. **Not generative** | n/a | Transformer protein encoder + glycan GNN | **564,647** protein-glycan interactions **[S]** | Not checked | **[NR]** | Not checked | n/a |

### 2.2 Notes on the cramped cells

- **G1 is the most important correction to what I told you earlier.** I described GlycanGT as a "generative" model. It is pretrained with masked language modeling and its only generative-style output is completing ambiguous entries: top-5 accuracy above 80% even when high fractions are masked **[C]**. That is a useful base for a generator, but it is not one.
- **GlyTouCan is mostly unusable for training as it stands.** As of June 2025, **more than half of the registered glycans have no defined IUPAC-condensed name, and about 60% of those that do contain ambiguity symbols** **[C]**. From 244,842 entries, about 83.7k remain. The authors list this as a limitation: "the number of fully defined glycan structures remains limited".
- **Glycans are tiny graphs.** In GIFFLAR's tables the average glycan has about **7.1 monosaccharides** and about **91 atoms** **[C]**. That is why classifier training takes minutes on a single consumer GPU.
- **G3 is the only function-conditioned glycan generator I found**, and it is old (2024) and solves glycan *sequencing* from a lectin fingerprint, not design of a glycan to hit a target. It is a different task, but it shows the task framing exists.

### 2.3 Labs working on glycan ML (verified by the papers above)

- **Bojar lab, University of Gothenburg**: glycowork, SweetNet, GIFFLAR, LectinOracle. Its fellowship profile states an intent to "design glycan-based antibiotics and antivirals" **[S]**. I found **no published generator** from this lab.
- **Matsui lab, Nagoya University**: GlycanGT **[C]**.
- **Lewis lab, UC San Diego**: Boltzmann lectin model **[C]**.
- **Jian Tang group** (last-but-one author on GlycanML): GlycanML benchmark **[C]**.

---

## 3. Microbial natural products

### 3.1 Papers table

| # | Paper (lab, venue, year, link) | What it generates, and for what | Cond.? | Model, size | Training data | Free now? | Compute | Code | Memorization check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | **Tay et al., "67 million natural product-like compound database"**. A*STAR / SIBER. *Scientific Data*, 2023-05, DOI 10.1038/s41597-023-02207-x **[S for venue]** | 67,064,204 natural-product-like SMILES, to enlarge the searchable space of NP-like chemistry | Unconditional | 3-layer LSTM, 512 hidden, no dropout. Params **[NR]** | COCONUT: **325,535** unique SMILES used (80% of 406,919): 292,981 train, 32,554 val. **81,384** held out **[C]** | Data and model on figshare (doi 10.6084/m9.figshare.c.6482266.v1). **License of files not stated** (article is CC BY 4.0) | **1x V100 32 GB**. **Training + sampling < 24 h**; training alone **[NR]**. Batch 128, Adam lr 1e-3, early-stopping patience 10,000 minibatches **[C]** | github.com/SIBERanalytics/Natural-Product-Generator **[C]** | **Partial.** No novelty metric. 37% of 81,384 held-out known NPs were reproduced by the generated set. Stereochemistry removed |
| N2 | **NPGPT**: Ohue lab, Tokyo Institute of Technology. arXiv 2411.12886 (2024); a Springer version is cited [S] | NP-like molecules, to produce a library of drug-candidate starting points; also docked 1,000 molecules to EGFR | Unconditional | Fine-tuned **smiles-gpt (GPT-2, 24.8M)** and **ChemGPT (GPT-Neo, 19M)** **[C]** | COCONUT (~400k NPs) filtered to <=150 atoms and <=10 rings, then 9x SMILES-randomization augmentation to **~3.6M entries** **[C]** | COCONUT is **CC0** **[C]** | **4x GeForce RTX 3090**. Batch size 256 (smiles-gpt) and 32 (ChemGPT). **Hours, epochs [NR]** | github.com/ohuelab/npgpt, **MIT** **[C]** | **No.** Novelty = "not in COCONUT": 0.996 (smiles-gpt) and 0.999 (ChemGPT); uniqueness 0.663 and 0.939. The authors note ChemGPT's high novelty looks like "nearly random" molecules (FCD 14.28) |
| N3 | **NP-VAE**: Ochiai et al. *Communications Chemistry*, 2023-11, DOI 10.1038/s42004-023-01054-6 **[S for authors/venue]** | Latent space for large natural-product-like molecules with 3D chirality; reconstruction and generation | Unconditional | Graph/tree VAE (Tree-LSTM + ECFP), **~12M params** **[C]** | ~30,000 compounds (DrugBank ~10k + in-house ~20k) for the generative comparison; 76k/5k/5k for the generalization set **[C]** | The in-house part is **not public** | **[NR]** in the part I read | **Not found** in the part I read | **No.** Novelty 0.983 +/- 0.002. The authors say low novelty may indicate overfitting but run no separate audit |
| N4 | **Chemical Language Models for Natural Products: A State-Space Model Approach**: Wang, Sultan, Volkamer, Klakow. Saarland University. arXiv 2602.13958 (2026-02) **[C]** | Pre-trained NP molecule generators (Mamba, Mamba-2, GPT) + property prediction; compares 8 tokenizers | Unconditional (generation); fine-tuned for properties | **8.96M to 69.7M params** (48 pre-trained models) **[C]** | **1,030,273** NP SMILES merged from SuperNatural 3.0, COCONUT and LOTUS **[C]** | Components are open but **merged-set license not stated** | **A100 GPUs; "hours to a week" per model; <=150 epochs** **[C]** | github.com/rozariwang/CLMs-for-NPs; license **not stated** | **No.** Novelty = "not in the 1M NP set". Mamba is 1-2% better on validity/uniqueness; GPT gives ~2% more novel structures |
| N5 | **Generative Deep Learning Pipeline Yields Potent Gram-Negative Antibiotics**: Kollen, Schuh, ... Sieber. Technical University of Munich. *JACS Au* 2025;5(9):4249 **[C]** | Antibiotic candidates active against MRSA and *E. coli*; 11 synthesized, 45 SAR compounds tested | Not conditional: SMILES LSTM pretrained, then 2-step transfer learning on 131 antibiotic scaffolds; scored afterwards by separate predictors | LSTM on one-hot SMILES. Params **[NR]** | ChEMBL 24 (~365k), **MEGx** natural-product collection (Analyticon, **commercial**), PubChem "antibiotic" subset (2,239 molecules; 131 scaffolds) **[C]** | **Partly no**: MEGx is licensed | **RTX 4090 (24 GB)** + 64-core Threadripper, 1 TB RAM. 40 epochs of transfer learning. **Hours [NR]** | github.com/sieber-lab/AIbiotics; **license not stated** | **"No dedicated analysis"** **[C]**. 177 of 3,553 generated molecules matched known PubChem compounds. Only 1 of 11 synthesized candidates was active |
| N6 | **A generative deep learning approach to de novo antibiotic design**: Krishnan et al.; senior author Collins (MIT / Broad Institute) [S]. *Cell* 188(21), 2025, DOI 10.1016/j.cell.2025.07.033 **[C for citation]** | New antibiotics against *N. gonorrhoeae* and *S. aureus*: fragment-based and unconstrained VAE + genetic algorithm. **24 compounds synthesized, 7 active, 2 leads effective in mouse models** **[C]** | Conditional on predicted antibacterial activity | VAE + genetic algorithm + GNN. Params **[NR]** | **Not readable** (403) | **[NR]** | **[NR]** | **No code/data statement found** | **[NR]** |
| N7 | **SyntheMol**: Swanson, Liu, Catacutan, Arnold, Zou, Stokes. McMaster / Stanford. *Nature Machine Intelligence*, 2024-03, DOI 10.1038/s42256-024-00809-7 **[S]** | Easily synthesizable antibiotic candidates for *A. baumannii* from a 30-billion-molecule building-block space, with synthesis recipes. 58 synthesized, 6 novel and potent | Conditional on predicted activity | Search over reaction space guided by a property model | Antibacterial activity data **[NR]** | **[NR]** | **[NR]** | **Not found** | **[NR]** |

### 3.2 Notes on the cramped cells

- **N1 is the only paper with a held-out recall number**, and it measures something different from memorization: the generator re-found 37% of molecules it never saw. That shows it is learning the distribution, not that it avoids copying. Nobody checks *how close* generated molecules are to training molecules (fingerprint similarity, scaffold overlap).
- **N2's own numbers show the metric's weakness.** ChemGPT has the best validity (0.999), uniqueness (0.939) and novelty (0.999) and the worst FCD (14.28 vs 1.29), and the authors say it produces compounds that "appear to be nearly random". High novelty is a bad sign there.
- **N5 is the clearest "goal-directed" example**, but the goal is a post-hoc screen, not a conditioning input.
- **N6 and N7 get the headlines** (real synthesized compounds, mouse data). They are also the hardest to reproduce: wet lab, large compound libraries, and for N6 I could not confirm code or data are public.

### 3.3 Labs and trajectory

- **Collins (MIT / Broad)**, **Stokes (McMaster)** with **Zou (Stanford)**, **Sieber (TU Munich)**, **Ohue (Tokyo Tech)**, **A*STAR SIBER**, **Saarland (Klakow / Volkamer)**. Output is steady from 2023 to 2026.

---

## 4. Data: can you get it for free, right now?

| Dataset | What it is | Size | License | Status |
| --- | --- | --- | --- | --- |
| **GlyTouCan** (via GlyCosmos) | Glycan structure registry | 244,842 entries (as of 2025-06-17), ~83.7k usable after dropping ambiguous ones **[C]** | Terms page states **CC0 1.0**, no attribution, but the page did not render; I saw this only in a search snippet **[S]**. The page also says terms can change without notice | **Mostly open.** Verify the terms page and which download route (GlyCosmos / SPARQL) needs no login |
| **GNOme** (glycan ontology derived from GlyTouCan) | Naming ontology | n/a | CC BY 4.0 **[S]** | Open, but not the structures themselves |
| **CFG glycan array data** (lectin-glycan binding) | The function labels a conditional glycan model needs | 5,203 samples reused by GlyMDB **[S]** | **No license or data-use agreement found** **[S]**. CFG array access is "request reviewed by steering committee" for new arrays | **Unclear. Do not assume open.** Contact `cfgservice@bidmc.harvard.edu` **[S]** |
| **glycowork bundled data** (glycan table, lectin-glycan interactions) | Used by SweetNet, GIFFLAR, LectinOracle | ~50.5k glycans **[S]**; ~388k interactions in GIFFLAR split **[C]** | Code is **MIT** **[C]**; data license inherits from upstream sources, **not stated** | Downloads instantly via `pip`/GitHub, but license of the underlying data is unresolved |
| **COCONUT** | Natural products | Count not on the download page; ~400k referenced by NPGPT, 406,919 by Tay et al. **[C]**. Files: CSV **207.9 MB** (full), 191 MB (lite); SDF 2D **691.7 MB**; SQL dump 31.91 GB **[C]** | **CC0**, stated on the download page **[C]** | **Open.** Registration status not stated on the page; the site shows Log in / Register options |
| **NP Atlas** (microbial NPs) | Curated microbial natural products, MW <= 3000 Da | Count not on the pages I read **[NR]** | **CC BY-NC 4.0** **[C]** (not plain CC BY) | Direct file links for TSV, XLSX, JSON, SDF; version 2024_09 **[C]**. **Non-commercial license: fine for a student paper, but it is not the permissive open license your gate asks for. Decide that consciously** |
| **CO-ADD / SPARK** (open antibacterial screens) | Possible activity labels for NPs | >340,000 compounds screened; SPARK ~160,000 compounds, 120,000+ data points **[S]** | **No named license found** **[S]** | **Unverified.** Contact and terms pages need checking |
| **ChEMBL 24, PubChem antibiotic subset** | Used by N5 | 365k; 2,239 | Not checked | n/a |

---

## 5. Validity checkers

| Domain | Tool | What it checks | Speed per sample |
| --- | --- | --- | --- |
| Natural products | **RDKit** (rdkit.org) | Parses SMILES, valence, sanitization, canonical form, scaffolds, fingerprints. NPGPT and NPCLM both define validity as "parseable by RDKit" **[C]** | Not measured. **[E]** 0.2-5 ms per small molecule, more for large NPs. Measure it in Week 12 |
| Natural products | NP-likeness score / NPClassifier | Resemblance to NP space; used by N1 and N2 | **[NR]** |
| Glycans | **glycowork** (MIT) parsing and `canonicalize_iupac` | Converts IUPAC-condensed to a canonical string or graph; invalid input raises an error. GlycanGT builds graphs with `glycan_to_nxGraph` **[C]** | **[NR]. I found no benchmark and no dedicated "is this a valid glycan" function.** You would likely need your own biosynthetic rules (allowed linkages per monosaccharide) |

Glycans have **no RDKit-equivalent checker I could confirm**. That matters for your gate 4.

---

## 6. Your four questions

### 6.1 Which sub-problems are solved and which are open?

**Glycans**
- Solved or well covered: property prediction (taxonomy, immunogenicity, glycosylation type, lectin binding) with SweetNet, GIFFLAR, LectinOracle, GlycanGT.
- Partly done: structure from spectrum (GlycoBART), structure from lectin fingerprint (G3), completing ambiguous entries (GlycanGT).
- **Open:** sampling new valid glycans at all; conditioning on a function; any validity rules for generated glycans; any memorization or novelty audit.

**Natural products**
- Solved or crowded: unconditional NP-like generation (N1-N4), with ever-larger models.
- Partly done: antibiotic design with synthesized validation (N5-N7).
- **Open:** memorization audits; conditional NP generation using open activity data; evaluation that does not equate "not in COCONUT" with "novel".

### 6.2 Has anyone published a generative glycan model, or only binding prediction?

I found **no de novo glycan generator** with validity and novelty metrics. I ran several searches, one of them a thorough one, and the closest hits are G1 (completion), G2 and G3 (conditional on spectra or lectin fingerprints). A 2021 bioRxiv paper (glyBERT) is described in a snippet as including a "proof of principle" generative exploration **[S]**; I did not open it, so I cannot rule it out. **Treat "the generative side is empty" as likely but unproven** until you search Google Scholar yourself.

**Caveat on why it may be empty:** the usable training data is small (~84k) and ambiguous, and there is no easy validity checker and no clearly open label set. The gap may exist partly because it is hard, not only because nobody tried.

### 6.3 Which domain is more crowded with well-funded labs?

**Natural products.** Collins (MIT/Broad), Stokes (McMaster) and Zou (Stanford), Sieber (TU Munich), plus several smaller groups, all publish generators and the antibiotic papers include synthesis and mouse work you cannot match. **Glycans** has about four active groups, of which Bojar's is the only one that appears to treat design as a stated goal. Glycans score better on your H2 criterion.

### 6.4 Reproducibility ranking on a free T4 (16 GB, <4 GPU-hours)

Hours below are **[E]** unless tagged. T4 is roughly 2-3x slower than the RTX 3090 used in GIFFLAR (my estimate).

| Rank | Project | Reproducible on a T4? | Why |
| --- | --- | --- | --- |
| 1 | **GIFFLAR / SweetNet-style glycan models (G4, G5)** | **Yes** | Measured 22.7-45 min on an RTX 3090 for the Domain task **[C]**; roughly 1-2 h on a T4 **[E]**. Classifiers, not generators |
| 2 | **Glycan sequence/graph generator you build yourself, trained on ~84k GlyTouCan glycans** | **Likely yes** | Tiny graphs (~7 monosaccharides) and a small dataset. **[E]** 0.5-2 GPU-hours, same estimate as before. No baseline to reproduce, so this is your own build |
| 3 | **Tay et al. LSTM (N1)** | **Likely, with a reduced run** | 293k training SMILES, ~3 LSTM layers. Original was a V100, training + sampling < 24 h **[C]**. **[E]** a reduced schedule fits ~1-3 T4-hours |
| 4 | **NPGPT, smiles-gpt 24.8M (N2)** | **Only on a subset** | Original used 4x RTX 3090 and ~3.6M augmented sequences. **[E]** one pass over all of them is roughly 2 T4-hours (≈ 6 x 24.8M params x ~290M tokens ≈ 4.3e16 FLOPs at ~8 TFLOPS effective); train on the unaugmented ~400k set instead, which is ~10 minutes per epoch |
| 5 | **GlycanGT (G1)** | **Probably, but unverified** | 83.7k tiny graphs and an L40 in the paper, but training time is **[NR]**, and weights are gated. Retraining small variants from scratch is plausible |
| 6 | **NP-VAE (N3)** | **Doubtful** | The authors report JT-VAE did not finish even on a reduced library, and I found no code or GPU time |
| 7 | **JACS Au pipeline (N5)** | **Computation maybe; the project no** | LSTM on an RTX 4090 with a 64-core CPU and 1 TB RAM; the value is the synthesis and assays |
| 8 | **NPCLM (N4)** | **No** | "Hours to a week" on A100s, up to 69.7M params |
| 9 | **GlycoBART (G2)** | **No** | ~207M params, 4x A5000, 30 epochs |
| 10 | **Cell (N6), SyntheMol (N7)** | **Unknown** | I could not read their compute or code sections |

---

## 7. What this means for your choice

- **Glycans pass the "avoid industrial compute" and "T4 budget" tests clearly.** They fail on **function labels** (lectin-binding data has no license I could find) and **validity checking** (no confirmed checker). A glycan project is only a *problem-solving* project if you resolve those two.
- **Natural products pass the checker and data tests easily** (RDKit; COCONUT is CC0), but the field is crowded and the headline problem (new antibiotics) overlaps with your classmate's AMP topic at the goal level.
- **The memorization audit is a safe contribution in both domains.** Nobody did one.

Two concrete project shapes that fall out of this, both for you to judge rather than assume:
1. **Glycan generator + audit**: train a small graph/sequence generator on the ~84k defined GlyTouCan glycans, add biosynthesis-rule validity, and audit near-duplicates (monosaccharide-sequence or WL-hash similarity). Goal conditioning only if the label question below resolves.
2. **NP generator audit**: take N1's released LSTM or N2's released smiles-gpt, and measure how far generated molecules sit from COCONUT with fingerprint and scaffold distance, not only exact match. Lowest risk, least novel framing.

---

## 8. Corrections to things I said earlier in this conversation

1. I called GlycanGT "generative". Its generative part is masked completion, not de novo sampling.
2. I said NP Atlas was open. It is **CC BY-NC 4.0**.
3. I said CO-ADD had "tens of thousands" of compounds. A snippet says more than 340,000 screened **[S]**.
4. I credited the Collins lab for the *Cell* paper without a source in hand. The Broad page names only Aarti Krishnan; a search snippet gives Collins as senior author **[S]**.
5. I estimated glycan generator training at 0.5-2 GPU-hours. That is still my estimate **[E]**; the only measured numbers are for classifiers (22.7 min SweetNet, 45.0 min GIFFLAR on an RTX 3090).
6. I said the Gram-negative antibiotics paper came from an unnamed lab. It is from **Sieber's group at TU Munich** **[C]**.
7. The GlycanGT README says 83,740 pretraining glycans; the paper says 83,739. The one-glycan gap is minor but cite the paper.

---

## 9. Claims to verify at the primary source, most important first

**Blocking**
1. **Is there any open, licensed lectin-glycan binding dataset?** Check the NCFG data pages, the glycowork data files' provenance, and the GIFFLAR/GlycanML repos. Without one, a conditional glycan project has no goal.
2. **GlyTouCan's CC0 statement** at `doc.glytoucan.org/en/Terms-and-Conditions`, and which bulk download route needs no login.
3. **GlycanGT's Supplementary Tables S2/S3**: parameter counts and epochs per scale. They would turn my glycan compute estimate into a measured number.
4. **Whether a de novo glycan generator exists** (search Google Scholar and bioRxiv for glyBERT and its successors; try "glycan" with "autoregressive", "diffusion", "graph generation").

**Important**
5. **GlycanGT weights on Hugging Face**: is the gate a simple click-through or an approval wait?
6. **COCONUT**: record count (Statistics page) and whether bulk download needs an account.
7. **NP Atlas**: compound count and whether CC BY-NC is acceptable to your course's "open license" gate.
8. **The *Cell* 2025 paper's data and code availability statement and STAR Methods** (I could not read them).
9. **CO-ADD terms of use** and whether structures are downloadable in bulk.

**Routine**
10. Every venue/year tagged **[S]**: Tay et al. in *Scientific Data*, NP-VAE authors and venue, SyntheMol, GlycanGT in *Bioinformatics* 2026, the 2021 glyBERT claim.
11. RDKit and glycowork runtimes per sample (I measured neither).
12. All **[E]** GPU-hour figures. The course's Week 12 smoke test is the place to measure them.
