# Regulatory chemical candidates — evidence notes

Research for `prompt2.md`, 21 October 2026. Two candidates screened. This is evidence for the final report, not the report itself. `P*` below means a pass only for the stated narrow scope; `F/U` means the hard requirement is not established, rather than evidence that no possible dataset could satisfy it. Runtime and training-budget numbers are estimates unless stated otherwise.

## Main conclusion and the definition problem

An approved molecule's **identity and approval status** can be public even while the experimental data needed to design a successful successor are incomplete or confidential. A company cannot secretly own additional FDA approvals, but can have more useful compound–assay observations. These are different units of data. Neither regulatory candidate establishes the user's stronger protection against private-data advantage for practical inverse design. Do not claim that confidential manufacturing information alone proves a much larger private collection of *approved structures*: it does not.

Do not inflate the data by counting salts, products, strengths, formulations, repeated toxicity records, countries approving the same molecule, or randomized SMILES as independent approved molecules. Do not describe FDA/EMA/PMDA coverage as worldwide completeness without a cross-regulator coverage audit.

## Candidate D: conditional small-molecule generation from regulatory-approved active ingredients

**Concrete formulation:** learn `p(G | c)` over molecular graphs `G`, conditional on a coarse therapeutic class or desired calculated properties `c`, using one standardized molecular graph per approved active ingredient. A realistic four-week experiment conditions on *calculated* descriptors or coarse class and tests structural generalization; it cannot validate newly generated drugs as clinically effective or approved. A closed-catalog alternative generates existing approved molecules for repurposing, but then novelty beyond the catalog is impossible and a retrieval baseline is essential.

### A, B, C and gates

| Criterion | Result | Reason / scope |
|---|---|---|
| A | P* for FDA approval identities; F/U for global practical design task | Public approval lists close the narrow regulator-defined identity inventory; no demonstrated ≥90% worldwide union or ≥90% assay/clinical evidence coverage. Private-data-advantage claim is unsupported. |
| B | P* slow regulated additions; F/U if “cannot grow significantly” is literal | Dozens of approvals annually is slow but not a permanent cap, and the relevant small-molecule denominator/current growth must be measured consistently. |
| C | P | University of Pittsburgh's Yanshan Wang, David Oniani, Jordan Hilsman and collaborators directly study indication→molecular-SMILES generation in 2024. |
| 1 | P | Molecules are labeled graphs; SMILES is a serialization of structured chemistry, not ordinary text. |
| 2 | P* | Compute alone cannot manufacture regulatory approval. This does not prevent compute, private assays, or synthesis capacity from improving a model. |
| 3 | P | Descriptor/class-conditioned molecular generation is natural. |
| 4 | P* structural surrogate only | RDKit sanitization checks graph chemistry; no fast checker establishes regulatory approval, safety, clinical efficacy or synthesizability. If approval is the promised validity property, this gate fails. |
| 5 | P | Scaffold-aware evaluation with memorization controls; constrained sampling for valence and property ranges; calibrated uncertainty/abstention with tiny class counts. These are proposed research levers, not verified unsolved theorems. |
| 6 | P* | DrugCentral explicitly licenses its resource CC BY-SA 4.0 and advertises no-form flat structure downloads. Current download endpoints could not be fetched in this research session; actual bytes/current clean subset count need a smoke test. |
| 7 | P* estimated | A small GRU/SELFIES autoregressive model or small graph/sequence VAE on a few thousand graphs should fit 1–3 T4 GPU-hours including a modest evaluation run; not benchmarked. Do not promise the published MolT5 runs fit four hours. |
| 8 | P | Standardize consistently, canonical isomeric SMILES/InChIKey for exact matches; Morgan fingerprint Tanimoto and Bemis–Murcko scaffold overlap for near duplicates. |

**Recommended screening outcome:** reject as a full pass under the user's strongest interpretation of A. Do not spend effort producing a favorable R/H score after this rejection.

### Verified data and growth evidence

1. [DrugCentral download page](https://www.drugcentral.org/download), **opened successfully**. Advertises PostgreSQL dump dated **2026-09-25**, separate FDA/EMA/PMDA approval downloads, SDF V2000/V3000 and SMILES/InChI flat files. It labels the site “DrugCentral 2027” while the dump date is in 2026; use the dump date, not the marketing version as a future observation. The full dump requires PostgreSQL + RDKit cartridge and is unsuitable for a five-minute setup; prefer flat files.
2. [DrugCentral resource license](https://www.drugcentral.org/privacy), **opened successfully**; its license link resolves to [CC BY-SA 4.0 legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode), **opened successfully**. This is a resource license, not merely the journal article's license. Attribution and share-alike apply. This does not establish rights to unrelated external linked datasets or proprietary medical vocabularies; keep the experiment on structure/approval fields and check licenses for extra conditions.
3. [2023 SDF download directory](https://unmtid-shinyapps.net/download/DrugCentral/2023/), **opened successfully**: `structures.molV2.sdf.gz`, **1.3M** as displayed by server; `structures.molV3.sdf.gz`, **705K**; both modified **2023-06-12**. These sizes are source-confirmed rounded server sizes, not measured exact byte counts. Files were not downloaded and parsed. They are not proven to contain exactly the count from the 2022 paper below.
4. [Halip et al., “Exploring DrugCentral: from molecular structures to clinical effects,” JCAMD 2023, DOI 10.1007/s10822-023-00529-x](https://link.springer.com/content/pdf/10.1007/s10822-023-00529-x.pdf), **opened successfully**. Its **2022 release** has **4,959 active drug substances**, including **4,108 small organic molecules**; **4,288 drug structures** entered/validated. Human and veterinary categories overlap. These are DrugCentral counts, **not a current FDA-only count**. The reported first-approval range across its regulator coverage is **29–70/year in 2013–2022**, and the figure's 2022 trailing ten-year average is **54/year, all drug types**. Small molecules approved since 2020: **93** through the 2022 release; roughly **31/year** is a division-based historical estimate, not a 2026 measured rate. Salt removal/standardization means formulation counts are not molecular counts.
5. [DrugCentral current statistics page](https://drugcentral.org/static/drugcentral2026.html): search index exposes a source-dated **2026-09-04** table with **5,116 active ingredients / 4,175 small molecules**. **Full page open failed because it exceeds the web tool's content limit**, so label this **index-observed, not independently verified by direct page read/download** or omit from final report. Categories visible in index sum to 5,115, another reason to verify. Do not infer growth by subtracting this changing classification from the historical small-organic count.
6. [FDA novel approvals 2025](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2025), **opened successfully**: **46 CDER novel drugs in calendar 2025**. This mixes small molecules and biologics; it is not “46 new small molecules”. Do not count its combination products or ingredients without an explicit rule.
7. [European Commission Union Register](https://health.ec.europa.eu/medicinal-products/union-register_en), **opened successfully**: centralised approvals, with separate mutual-recognition/national registers. Thus EMA/Union Register alone is not every EU authorization and FDA+EMA is not every world approval.

**Forecast:** 31/year against 4,108 implies about 7.5% additions over ten years if unchanged (**estimate**, historical classification, not a prediction); 54/year counts all modalities and must not be used as a small-molecule rate. No validated global unique-molecule annual rate was established.

### Active research and baselines

- **University of Pittsburgh / PittNAIL**, Yanshan Wang, David Oniani, Jordan Hilsman; collaborators include Chengxi Zang (Weill Cornell) and Junmei Wang (Pittsburgh). [“Emerging Opportunities of Using Large Language Models for Translation Between Drug Molecules and Indications”](https://arxiv.org/abs/2402.09588), **arXiv 2024**, [full HTML v1](https://arxiv.org/html/2402.09588v1), both opened successfully. Direct indication→SMILES task, T5/MolT5 encoder–decoder family, ChEMBL/DrugBank examples. The paper reports poor performance and inconsistent gains from fine-tuning; clinical validity is not established. [Code URL cited by paper](https://github.com/PittNAIL/drug-to-indication) was found in the paper but opening the repo returned cache miss; code license not checked. It is **not evidence of a top-ML-venue publication** and its DrugBank data cannot simply be assumed open-license.
- Small autoregressive baseline proposed here: train a compact GRU on canonical/randomized SMILES or SELFIES from the licensed flat structure set; fit train-only vocabulary; compare against scaffold/fragment recombination and training-set retrieval. Proposed design, not a claim about a specific verified repository.
- More data via public molecule pretraining is a methodologically reasonable ablation but does **not** rescue the stronger A claim: it demonstrates that additional non-approved molecular data can matter. Keep pretraining and scarce approved labels distinct.

### Authoritative confidentiality evidence

[FDA, July 10, 2025 CRL disclosure announcement](https://www.fda.gov/news-events/press-announcements/fda-embraces-radical-transparency-publishing-complete-response-letters), **opened successfully**, says the first release included over 200 previously nonpublic decision letters and redacted trade secrets/confidential commercial information. [openFDA CRL API description](https://open.fda.gov/apis/transparency/completeresponseletters/), **opened successfully**, cites FOIA, FDCA and FDA disclosure regulations and states confidential information is redacted. This supports “approval status is not all supporting data”; it does not quantify a 90% public fraction or private assay advantage.

## Candidate P: generate pesticide-like molecular graphs conditional on use class and toxicity surrogate

**Concrete formulation:** `p(G | use class, desired descriptor/toxicity range)` using registered conventional chemical active ingredients, with graph validity and property surrogates at evaluation. Separate active ingredients from products/mixtures/microbial pesticides. Strong practical utility requires external bioassay and ecotoxicity evidence that is not supplied by mere registration lists.

### A, B, C and gates

| Criterion | Result | Reason / scope |
|---|---|---|
| A | P* for one regulator's registered identities; F/U globally and for useful design measurements | Public label/approval lists are not a demonstrated ≥90% worldwide molecule+assay dataset; unsubmitted/private R&D is outside the inventory. |
| B | F/U strict | Legal gating makes additions slow; current deduplicated conventional-molecule count and same-unit annual growth were not established, so do not declare permanent scarcity proved. |
| C | P | Central China Normal University's State Key Laboratory of Green Pesticide, Guangfu Yang / Fan Wang group, published pesticide-likeness ML in 2024; Berkeley/Peking authors have a 2025 generative paper. |
| 1 | P | Molecular graphs, with mixtures explicitly treated as sets if included. |
| 2 | P* | Additional compute cannot issue registration or generate measured ecological outcomes. |
| 3 | P | Use/property-conditioned candidate generation is natural. |
| 4 | P* structural surrogate only | RDKit checks valence/aromaticity; predicted toxicity is an uncertain surrogate and cannot certify safe or effective pesticides. If proven efficacy/safety is required, fail. |
| 5 | P | Mixture-aware representations; scaffold/identity leakage controls; calibrated toxicity conditioning. Proposed levers. |
| 6 | F/U | Public regulator identity tables were found, but no verified immediately downloadable openly licensed complete structure+registration+condition dataset. Publication open access is not a dataset license. |
| 7 | P* estimated | Small GRU/VAE on hundreds–thousands of distinct structures: approximately 1–3 T4 hours, unbenchmarked; sparse labels may make meaningful training impossible without pretraining. |
| 8 | P | Canonicalize each constituent, sort constituents for mixtures; scaffold and Tanimoto checks after splitting on unique active ingredient rather than product rows. |

**Recommended screening outcome:** reject as strict pass; explicit failures are A (strong/global definition), B not demonstrated, G6 unverified. Avoid declaring the entire industry lacks public structures.

### Counts, growth, access and licensing

1. [EPA FY2023 Congressional Justification, April 2022](https://www.epa.gov/system/files/documents/2022-04/fy-2023-congressional-justification-all-tabs.pdf), **opened successfully**, PDF page 13 / printed context: approximately **1,200 active ingredients** in over **17,000 products**. **Source-confirmed estimate from 2022**, U.S. EPA scope, includes more than conventional small molecules. This is not a 2026 global total or current downloadable sample count.
2. [EPA FY2024 Annual Performance Report](https://www.epa.gov/system/files/documents/2025-01/fy24-annual-performance-report.pdf), **opened successfully**, PDF pages 83–84: **12** and **26 risk assessments supporting new-active registration decisions** in FY2023 and FY2024; majority in FY2024 involved biopesticides. These are **risk-assessment counts**, not proven unique small-molecule additions. They suggest order-of-tens regulated events/year but cannot serve as a correctly denominated small-molecule growth series. Current unique-molecule growth remains **unverified**.
3. [EPA pesticide information access page](https://www.epa.gov/ingredients-used-pesticide-products/how-search-information-about-pesticide-ingredients-and-labels), **opened successfully**, last updated 2026-10-08: APPRIL exposes active/cancelled products, PC/CAS ingredient IDs, proportions and pest/use categories; PPIS is described as ASCII files for all U.S.-registered products. It does not itself provide a clean molecular graph dataset. Join to an independently licensed structure source, then validate CAS/parent/salt mapping, before claiming G6.
4. [EU Pesticides Database official description](https://food.ec.europa.eu/plants/pesticides/eu-pesticides-database_en), **opened successfully**: active/non-approved/basic substances, APIs and downloads; explicitly says its information may be incomplete/outdated and the Official Journal is authoritative. The description is not a worldwide completeness certificate. A ready structure export, license for joined structures, current count, and bytes were **not verified**.
5. **Do not use a publication's CC license as the license of linked government/private data.** No PPDB/Pesticide Properties Database open-data license was verified in this search. No claim is made that PubChem automatically licenses every depositor's data identically.

### Active research

- **Central China Normal University, State Key Laboratory of Green Pesticide**, **Guangfu Yang, Fan Wang; first author Ruoqi Yang**. [University announcement, January 28, 2024](https://kjc.ccnu.edu.cn/info/1009/3802.htm?item=2), **opened successfully**. Paper **“Pesti-DGI-Net: A multi-modal deep learning architecture based on dual interpretability for pesticide-likeness prediction,” Computers and Electronics in Agriculture (2024), DOI [10.1016/j.compag.2024.108660](https://doi.org/10.1016/j.compag.2024.108660)**. University page supplies title, DOI, group and authors. Prediction, not generative design; qualifies as closely related ML. Uses graph/descriptors/image modalities; proposed project can retain graph outputs.
- **Taehan Kim (UC Berkeley), Wonduk Seo (Peking University)**. [“Pesti-Gen: Unleashing a Generative Molecule Approach for Toxicity Aware Pesticide Design”](https://arxiv.org/abs/2501.14469), **arXiv 2025 / RECOMB 2025 Poster Track**, [HTML](https://arxiv.org/html/2501.14469v2), both **opened successfully**. VAE with pretraining then toxicity fine-tuning; paper reports **56,360 rows but only 520 unique pesticides**, with mixtures included, and about **68% structural validity**. It is not 56,360 independent molecules. Paper CC BY-NC-SA 4.0 does not establish a separate open dataset license. Author affiliations establish university work, not an identified standing lab. Limitation to investigate: mixture identity/row leakage and consistency of ordinal toxicity mapping; avoid alleging misconduct.
- A separate **PestiGen** (without hyphen), **“Reinforcement learning-based generative artificial intelligence for novel pesticide design” (2025)** by CCNU's Fan Wang / Guangfu Yang team was found at [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12685504/). Search result exposed details, but full-page opening hit a CAPTCHA; **not relied on as a directly read source**. Do not conflate it with Kim/Seo's Pesti-Gen.

### Legal/public-data nuance

[EPA Registration Manual Chapter 15](https://www.epa.gov/pesticide-registration/pesticide-registration-manual-chapter-15-submitting-data-and-confidential), **opened successfully**, explains FIFRA section 10: safety/efficacy information for registered or formerly registered pesticides generally must be public, while specified manufacturing, testing of inert ingredients and other confidential details have exceptions. This is stronger public-disclosure support than a casual “all pesticide data are secret” claim. It still does not establish immediate bulk access/open licensing to all underlying records, all world regulators, or disclosure of an industry's never-submitted screening library. Keep those distinctions explicit.

## Shared structural verification protocol (proposed, not benchmarked)

[RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html), **opened successfully**, documents aromaticity/sanitization/valence handling. For conventional molecules under roughly 100 heavy atoms, budget **1–10 ms/sample CPU** for parsing, sanitization, basic descriptors and canonicalization (**engineering estimate**; machine and structures matter). Do not fold docking into this time. A successful RDKit parse cannot prove stability, synthesis, potency, toxicology, or regulatory eligibility.

Split deduplicated parent molecules before augmentation; hold out scaffolds and a recent approval-time cohort; preserve stereochemical distinctions; report exact train-hit rate plus nearest-neighbor Tanimoto distribution, scaffold overlaps and diversity at fixed sample budget. Flag stereoisomers, salt/tautomer variants and near-exact analogs separately. Add a train-set-resampling baseline so “drug-like” scores cannot reward memorization. Save the normalization rules, dataset version, hashes, and every exclusion.

## Claims the final report should ask the user to verify first

1. DrugCentral current FDA-only/EMA-union small-molecule count after a declared salt/stereo/classification rule; current flat-file bytes and actual accessibility.
2. Global approval-list coverage versus FDA/EMA/PMDA-only coverage, including national European and non-US/EU regulators.
3. A matched-year, same-unit growth series; never mix biologic approvals, products, and unique conventional molecules.
4. Separate licenses for molecular structures, clinical vocabularies, approvals, assay labels and code.
5. Scope of a structural validity surrogate versus the intended practitioner outcome.
6. Real Colab installation time and a one-epoch timing before making any ≤4-hour promise.
