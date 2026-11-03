# Project idea: generating pesticide-like molecules with lower predicted honey-bee toxicity

Prepared and expanded: **26 October 2026**. This brief explains the proposed project, links to original modelling studies, and includes a focused public training-data inventory in **Section 5**. It distinguishes **toxicity prediction** from **molecular generation**.

## 1. The idea

Train a small molecular generator to propose structures conditioned on the **lower acute honey-bee-toxicity class** in the ApisTox dataset. The input condition would be a toxicity class; the output would be a molecular graph or SMILES string describing a candidate molecule.

The research question is:

> With only about 1,000 experimentally labelled molecules, can a conditional generator produce chemically valid, diverse candidates aligned with the requested toxicity class, while avoiding copies and near-copies of its training molecules?

A practical comparison would include a small unconditional generator followed by filtering, a conditional generator, and the same conditional generator with chemical constraints. A fingerprint-based toxicity classifier would provide an inexpensive baseline for scoring candidates. Keep its test set separate from model fitting and generator optimization.

The most useful contribution would be a careful evaluation of **validity, conditional control, diversity and memorization**. Simply obtaining a high score from the same predictor used to guide generation is insufficient: a generator can exploit that predictor's errors. Report uncertainty and similarity to known training structures, and test whether apparent gains survive an independently trained evaluator.

This is an **in-silico candidate-design project**. ApisTox's lower-toxicity label concerns its acute-toxicity definition; it does not establish safety at every exposure, chronic effects, or pesticide effectiveness. Those outcomes require additional measurements. The small dataset makes a compact model worth testing, but fitting the complete experiment into four T4 GPU-hours and a five-minute setup remains **unbenchmarked**.

## 2. Dataset and download links

**ApisTox** contains **1,035 molecular records and 13 listed fields**, including SMILES, toxicity labels and identifiers. It combines curated information from ECOTOX, PPDB and BPDB. The UCI distribution explicitly states **CC BY 4.0** and offers a public download. These facts were checked at the [official UCI page](https://archive.ics.uci.edu/dataset/995/apistox).

| Resource | Link | What to use it for |
|---|---|---|
| Official dataset page | [ApisTox at UCI](https://archive.ics.uci.edu/dataset/995/apistox) | Description, fields, license and download button. UCI lists a **40.9 KB ZIP** and **131.9 KB CSV**; these are the site's rounded sizes. |
| Versioned dataset archive | [Zenodo v2: record 13350981](https://zenodo.org/records/13350981) | Main CSV, source/cleaning files, and predefined train/test splits. Public files are accessible without an application. |
| Direct main CSV | [Download dataset_final.csv](https://zenodo.org/records/13350981/files/dataset_final.csv?download=1) | Start here for molecular structures and labels. |
| Dataset construction code | [j-adamczyk/ApisTox_dataset](https://github.com/j-adamczyk/ApisTox_dataset) | Inspect cleaning, deduplication, feature definitions and split construction. |
| Dataset paper | [Adamczyk, Poziemski and Siedlecki, Scientific Data, 2025](https://doi.org/10.1038/s41597-024-04232-w) | Understand what the labels measure and how conflicting measurements were handled. [Free 2024 preprint](https://arxiv.org/abs/2404.16196). |

The binary target is `label`: **0 = non-toxic and 1 = toxic under the dataset's acute-toxicity classification**. The alternative `ppdb_level` is an ordered three-level target. Begin with the binary task to keep the experiment manageable. The dataset paper provides random, MaxMin and approximate time splits, with **828 training and 207 test molecules**. These split counts and target definitions are confirmed in the [dataset paper](https://doi.org/10.1038/s41597-024-04232-w).

Use the supplied splits before any SMILES augmentation. Do not feed identifiers, source metadata or toxicity-derived columns into a structure-only toxicity predictor. If a chosen representation requires removing salts, disconnected structures or unsupported elements, document the resulting count and retain the split boundaries.

**License detail:** the later prediction-study repository below labels its bundled data CC BY-NC 4.0, while the original UCI dataset states CC BY 4.0. Download the original dataset from its cited distribution and preserve that license/provenance; do not silently treat all repository copies as having identical terms. [Original UCI license](https://archive.ics.uci.edu/dataset/995/apistox), [prediction repository's statement](https://github.com/j-adamczyk/ApisTox_bee_toxicity_ML_prediction).

## 3. Recent papers by researchers who trained relevant models

The first three papers train **bee-toxicity predictors**. Papers 4–5 train **agrochemical generators**. Paper 6 studies transferable ecotoxicity representations, and paper 7 supplies a general low-data generation method. They are original modelling studies rather than reviews. A linked paper is not automatically an immediately reproducible baseline: code, data and compute availability differ.

### 1. Direct modelling on the exact dataset — start here

**Evaluating machine learning models for predicting pesticide toxicity to honey bees** — **Jakub Adamczyk, Jakub Poziemski and Pawel Siedlecki**. *Ecotoxicology and Environmental Safety* 312, 119869, **2026**; first preprint **2025**.

- **Paper:** [Journal DOI](https://doi.org/10.1016/j.ecoenv.2026.119869), [free arXiv version](https://arxiv.org/abs/2503.24305).
- **Code:** [ApisTox_bee_toxicity_ML_prediction](https://github.com/j-adamczyk/ApisTox_bee_toxicity_ML_prediction).
- **What they trained:** fingerprint/Random Forest models, graph-kernel classifiers and graph neural networks on ApisTox; also evaluated frozen pretrained molecular embeddings with classifiers.
- **Why relevant:** provides the closest predictor baselines and evaluation protocol. Fingerprints and graph kernels performed strongly; a large neural model is not automatically a better toxicity evaluator.
- **Distinction:** predicts toxicity for supplied molecules; it does **not** train a pesticide generator. The public repository states MIT for study code, with separately licensed bundled components/data.

### 2. BeeSafe 2.0 — prediction linked to pesticide discovery

**Deep Learning-Driven Discovery of Bee-Safe Isoxazoline Pesticide Candidates** — **Zhaokai Yang, Hao Wang, Meina Song, Bihong Tian, Wei Sun, Jianze Wei and Jian Wu**; Guizhou University and the Chinese Academy of Sciences. *Journal of Agricultural and Food Chemistry* 73, 31190–31202, **2025**.

- **Paper:** [Journal DOI](https://doi.org/10.1021/acs.jafc.5c12299), [freely readable abstract](https://pubmed.ncbi.nlm.nih.gov/41324313/).
- **What they trained:** BeeSafe 2.0, combining graph neural and residual-network components for bee-toxicity prediction.
- **Why relevant:** connects a trained predictor to identifying an isoxazoline candidate with reduced measured bee toxicity and pest activity. It shows that “bee-aware pesticide discovery” already has experimental precedents.
- **Distinction:** predictor-guided discovery is not proof of a learned de novo generator. Full training code and unrestricted training-data access were **not verified for this brief**; the abstract is available without requiring full-text access.

### 3. BeeEcoTox — a recent graph-based bee-toxicity model

**BeeEcoTox: A Large Language Model-Empowered Graph-Learning Framework for Predicting Ecotoxicity of Agrochemicals to Bees** — **Xuanlin Chen, Lilai Shen, Yizhou Huang, Yuchen Gao, Ke Chen, Dirong Zhang, Jianing Liu, Jinhui Yuan and Shulin Zhuang**; Zhejiang University. *Environmental Science & Technology* 60, 12076–12086, **2026**.

- **Paper:** [Journal DOI](https://doi.org/10.1021/acs.est.5c18162), [abstract and author information](https://pubmed.ncbi.nlm.nih.gov/41982052/).
- **What they trained:** a predictor combining ChemFM-derived molecular features with graph-isomorphism-network features and cost-sensitive learning.
- **Why relevant:** another direct comparator for the toxicity-scoring part of the project, particularly class imbalance and representation choices.
- **Distinction:** a toxicity classifier, **not** a generator. This entry was checked against the public abstract; its complete training assets and compute were not audited.

### 4. Pesti-Gen — the closest toxicity-aware generation precedent

**Pesti-Gen: Unleashing a Generative Molecule Approach for Toxicity Aware Pesticide Design** — **Taehan Kim and Wonduk Seo**. **2025 arXiv preprint**, listed as accepted to the **RECOMB 2025 Poster Track**.

- **Paper:** [arXiv 2501.14469](https://arxiv.org/abs/2501.14469), [full HTML](https://arxiv.org/html/2501.14469v2).
- **What they trained:** a variational-autoencoder-based generator using general chemical pretraining followed by toxicity-aware adaptation.
- **Why relevant:** directly precedes the broad idea of generating pesticide candidates with toxicity objectives.
- **Important difference:** its stated objectives concern **livestock and aquatic toxicity**, not ApisTox honey-bee toxicity.
- **Assets:** an author-associated [Pesti-Gen dataset repository](https://github.com/winterrykim/pesticide_data_Pesti-Gen) is public. This is a **data repository**; a complete generator-training code release and its license were not verified here.

### 5. Mos-Gen — generation followed by insecticide testing

**Mos-Gen: A Generative Molecular Framework for Mosquito Insecticide Design** — **Lina Wang, Yaning Cui, Zhifeng Gao, Ping Xing and Biao Jiang**. **2026 arXiv preprint**, revised August 2026.

- **Paper:** [arXiv 2606.01846](https://arxiv.org/abs/2606.01846), [full HTML](https://arxiv.org/html/2606.01846v2).
- **What they trained:** a motif-aware framework combining pretrained Uni-Mol representations with a VAE to generate disulfide-containing allicin derivatives.
- **Why relevant:** illustrates a specialised agrochemical generator with selected compounds synthesized and tested.
- **Important difference:** the target is **mosquito insecticidal activity**, not low honey-bee toxicity. It does not establish bee safety. A complete public training-code/data release was not verified for this brief.

### 6. PE-GCL — learning ecotoxicity representations from unlabelled molecules

**Advancing ecotoxicity assessment: Leveraging pre-trained model for bee toxicity and compound degradability prediction** — **Xinkang Li, Feng Zhang, Liangzhen Zheng and Jingjing Guo**. *Journal of Hazardous Materials* 475, 134828, **2024**.

- **Paper:** [Journal DOI](https://doi.org/10.1016/j.jhazmat.2024.134828), [publisher abstract](https://www.sciencedirect.com/science/article/pii/S0304389424014079).
- **What they trained:** pesticide-ecotoxicity graph contrastive learning, with unlabelled pretraining and downstream predictive tasks.
- **Why relevant:** a precedent for using larger unlabelled molecular collections when bee-toxicity labels are scarce.
- **Distinction:** representation learning and prediction, not molecular generation. The complete training-code/data release and its suitability for your compute limit were not verified here.

### 7. HI-Mol — a general method for generation with little data

**Data-Efficient Molecular Generation with Hierarchical Textual Inversion** — **Seojin Kim, Jaehyun Nam, Sihyun Yu, Younghoon Shin and Jinwoo Shin**. **ICML 2024**, PMLR 235, 24392–24414.

- **Paper:** [Official proceedings](https://proceedings.mlr.press/v235/kim24z.html), [arXiv 2405.02845](https://arxiv.org/abs/2405.02845).
- **Code:** [Seojin-Kim/HI-Mol](https://github.com/Seojin-Kim/HI-Mol), linked by the proceedings page.
- **What they trained:** hierarchical textual embeddings for low-data molecular generation, with generation using interpolated embeddings.
- **Why relevant:** a methodological reference for the small-data part of your proposal.
- **Important difference:** its published experiments do not establish performance on ApisTox or bee toxicity. Its full pretraining/adaptation cost has not been verified against your four-hour budget.

## 4. Suggested experiment and reading order

Read the **ApisTox dataset paper**, then **paper 1**, then **Pesti-Gen**. Next read **BeeSafe 2.0** and **BeeEcoTox** to understand existing bee-toxicity models; use **Mos-Gen**, **PE-GCL** and **HI-Mol** for generation, pretraining and low-data methods.

For implementation:

1. Download ApisTox and preserve a supplied held-out split. Fit a simple fingerprint-based toxicity classifier before selecting a more complex surrogate.
2. Train one compact conditional generator and compare it against unconditional generation plus filtering, under the same compute allowance.
3. Use [RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html) for parsing, sanitization, exact deduplication and fingerprints. Count unsupported/invalid outputs explicitly.
4. Report exact training matches, nearest-neighbour Tanimoto distributions, diversity, conditional-score changes and evaluator uncertainty. Group all representations of the same molecule together before splitting.
5. Describe the outputs as **candidates with predicted lower acute bee toxicity**. Pest efficacy and experimental bee safety remain separate endpoints.

**Scope of verification:** dataset size/license/download information, paper identities, stated model tasks and listed official links were checked against primary dataset pages, publisher/proceedings pages, author repositories and original-paper abstracts/full text where available. This is a project brief and reading list, not a complete training-compute or reproducibility audit. An earlier working note incorrectly called the ApisTox dataset paper a Journal of Cheminformatics publication; its final venue is **Scientific Data, 2025**.

## 5. Public datasets worth considering for training

**Start with ApisTox. The most useful additions are the harmonized ECOTOX workbooks, Tosi's toxicity tables, and USDA's bee-versus-Varroa assays.** The sources below are a focused selection, not a claim to cover the entire internet.

Counts below are reported by the original source or confirmed in its files/metadata. They refer to different units: chemicals, assay records, or endpoint summaries. **Do not add these counts together:** several datasets reuse ECOTOX, PPDB or the same published experiments. A public file can also have restrictive or unstated reuse terms.

### 5.1 Sources with an explicit public data license

| Dataset and download link | What you get | License and training use |
|---|---|---|
| **[ApisTox](https://archive.ics.uci.edu/dataset/995/apistox)**; [direct CSV](https://zenodo.org/records/13350981/files/dataset_final.csv?download=1) | **1,035 molecules:** 296 toxic and 739 lower-toxicity-class examples; SMILES and acute honey-bee labels. | **CC BY 4.0 at UCI.** Best ready-to-use classifier and conditional-generator baseline. Repository copies carry different license statements; preserve the original distribution's provenance. |
| **[Harmonized ECOTOX Dataset for Honeybee](https://zenodo.org/records/17288507)** | Two XLSX workbooks, approximately **60 MB**. The associated study retains **11,014 honey-bee assay records**, not 11,014 unique chemicals. Includes harmonized acute/chronic endpoints and adult/larval information. | **CC BY 4.0, confirmed in Zenodo API metadata.** Useful for expanding measured-endpoint coverage, but requires identifier resolution and assay harmonization. Some endpoints are converted or extrapolated; keep them separate from directly measured values. |
| **[Tosi et al.: lethal, sublethal and combined pesticide effects on bees](https://doi.org/10.6084/m9.figshare.20208659)** | Four downloadable XLSX tables covering lethal toxicity, sublethal effects, mixtures and monitored pesticides. File inspection found **216 rows with numeric oral/contact LD50 values** in the lethal table. [Associated paper](https://doi.org/10.1016/j.scitotenv.2022.156857). | **CC BY 4.0.** Useful additional endpoint tables. Preserve bee species, exposure route and units; mixture rows are not single-molecule labels. |
| **[EPA acute-to-chronic endpoint table](https://plos.figshare.com/articles/dataset/19541630)** | Small XLSX supplement with **46 pesticides having paired acute/chronic endpoints**, including adult and larval studies. [Associated paper](https://doi.org/10.1371/journal.pone.0265962). | **CC BY 4.0.** Suitable for a small chronic-toxicity extension or endpoint comparison; it overlaps regulatory sources and is not an independent new chemical collection. |
| **[Honey-bee adult acute dermal toxicity values](https://figshare.com/articles/dataset/28074422)** | **185 CSV rows / 184 distinct literal active-ingredient names**, mainly ECOTOX-derived LD50 values for pesticides used in US corn/soybean production. These are name counts, not independently standardized unique structures. | **CC BY 4.0.** Small and convenient for structure mapping and checking contact-toxicity coverage. Retain inequality signs such as “greater than” in censored LD50 values. |
| **[USDA honey-bee and Varroa-mite toxicity trials](https://catalog.data.gov/dataset/honey-bee-apis-mellifera-and-varroa-mite-varroa-destructor-toxicity-data)** | **Five CSV files, about 724 KB total**, with laboratory bee/mite mortality from vial, jar and cage assays. | **US public-domain designation.** Particularly relevant to selectivity: killing a bee parasite while limiting bee mortality. Requires chemical identification and matching dose, exposure and timing; rows can include treatments/formulations rather than one pure molecule. |
| **[Chronic honey-bee ecotoxicity modelling inputs and code](https://data.mendeley.com/datasets/7y27kdw5h2/1)** | Public research release for adult/larval chronic ED10 modelling, with model inputs and Python code. Exact number of independently measured, structure-resolved training compounds was not established here. | **CC BY 4.0.** Relevant if you choose a chronic-toxicity task. The reported predictions for over 300 uncharacterized pesticides are **predictions, not additional experimental training labels**. File-level download sizes were not verified. |

### 5.2 Other public molecular datasets, with access or license qualifications

| Dataset and source | Size / endpoint | What to check before using it |
|---|---|---|
| **[BeeEcoTox data](https://acs.figshare.com/articles/dataset/32019582)** | Paper reports **1,139 agrochemicals** for bee-toxicity prediction. | Public data record; **CC BY-NC 4.0**, so noncommercial restrictions apply. Check overlap with ApisTox before treating it as extra data. |
| **[BeeSafe 2.0 workbooks](https://github.com/sxxyyzk/Bee-Safe-2.0)** | Repository exposes bee-toxicity XLSX workbooks. Exact unique-structure count was not verified. | Public files, but **no explicit dataset license confirmed**. Useful lead for isoxazoline coverage; public availability alone does not establish reuse rights. |
| **[BeeTOX](https://github.com/fwangccnu/beetox)**; [comparison-data mirror](https://github.com/j-adamczyk/ApisTox_dataset/tree/master/other_sources) | ApisTox authors report **876 cleaned unique structures** from 891 input structure records. | Dataset-specific license and live legacy-server downloads remain unverified. This lineage is reused by later predictors, including PE-GCL; avoid counting those as separate data. |
| **[CropCSM bee-toxicity data](https://biosig.lab.uq.edu.au/crop_csm/data)**; [comparison-data mirror](https://github.com/j-adamczyk/ApisTox_dataset/tree/master/other_sources) | **871 cleaned structures** in the ApisTox comparison, from 900 initial records. | Original data license and standalone bee-table download route need checking. Its toxicity definitions must be matched to your chosen endpoint. |
| **[BeeToxAI supplementary CSVs](https://www.sciencedirect.com/science/article/pii/S2667318521000131)**; [public mirror](https://github.com/SimonEnsemble/graph-kernel-SVM-for-toxicity-of-pesticides-to-bees) | Separate contact/oral classification and regression files. ApisTox's comparison reports **472 cleaned structures, 403 with labels** in its examined molecular set. These are not the sizes of every individual task file. | Supplement-level reuse license not independently established. Keep oral/contact tasks separate and deduplicate molecules across files. |
| **[toxCSM honey-bee ZIP](https://biosig.lab.uq.edu.au/toxcsm/static/datasets/smiles_endpoints/honey_bee.zip)**; [endpoint documentation](https://biosig.lab.uq.edu.au/toxcsm/honey_bee) | **195 examples**, an older ECOTOX/admetSAR-derived classification task. | Direct public download; explicit dataset license unconfirmed. The endpoint documentation appears to reverse the usual verbal interpretation of LD50 toxicity: verify label direction before use. |
| **[Deep-PK bee-toxicity ZIP](https://biosig.lab.uq.edu.au/deeppk/static/datasets/smiles_endpoints/bee_tox.zip)**; [data page](https://biosig.lab.uq.edu.au/deeppk/data) | **182 molecules**, classification task. | Direct public download; explicit data license unconfirmed. A derived subset, not necessarily new independent assays. |

The cleaned counts for BeeTOX, CropCSM and BeeToxAI above come from the [ApisTox authors' comparison](https://pmc.ncbi.nlm.nih.gov/articles/PMC11696378/), not a new cleaning run performed for this brief.

### 5.3 Optional data for generator pretraining

These provide chemical structures to help a generator learn molecular syntax and diversity. **They do not provide bee-safety labels.**

| Source | Access and license | Suggested role |
|---|---|---|
| **[ChEMBL](https://www.ebi.ac.uk/chembl/)**; [download instructions](https://chembl.gitbook.io/chembl-interface-documentation/downloads) | Public release/API downloads; **CC BY-SA 3.0**. | Use a modest, deduplicated structure subset for pretraining. Some activity records may support a separate efficacy task, but verify the tested organism and endpoint. |
| **[COCONUT](https://coconut.naturalproducts.net/download)** | Public CSV/SDF downloads; current download page states **CC0**. | Optional natural-product-like structure pretraining. Contains compounds from many organisms, not specifically pesticides or bee-tested chemicals. |

### 5.4 What to actually use in this project

1. **First baseline:** ApisTox alone. It already has both harmful and lower-toxicity examples and a ready-made evaluation protocol.
2. **First expansion:** compare structures and compatible acute endpoints from the harmonized ECOTOX, Tosi and Kniss tables. Add only genuinely new, interpretable records; keep provenance for each label.
3. **If you want pest efficacy as well:** inspect the USDA bee/Varroa trials. This makes a more specific project about parasite-control selectivity, rather than assuming low bee toxicity implies useful pesticide activity.
4. **If the generator memorizes:** consider a small ChEMBL or COCONUT pretraining subset, removing overlaps with all held-out bee-toxicity molecules.

Do not merge binary labels defined at **11 µg/bee** with labels defined at **100 µg/bee**, or pool acute LD50, chronic ED10 and mixture outcomes as one target. Keep species, life stage, route, exposure duration, dose units and measured-versus-predicted status explicit. Downloading more rows does not automatically create more independent training examples.

Supporting source checks are saved in [curated-dataset notes](tasks/bee_curated_datasets.md), [raw-data notes](tasks/bee_raw_datasets.md) and [adjacent-resource notes](tasks/bee_adjacent_datasets.md). The focused list above supersedes the earlier request for an internet-wide inventory; it prioritizes training relevance and openly accessible files, while identifying unresolved reuse terms.
