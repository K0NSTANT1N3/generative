# Glycan project presentation — expanded speaker notes

Prepared 4 November 2026. Source proposal preserved; corrections and unverified requirements are explicit.

## 01. Designing glycans for a chosen lectin

A small-compute generative modeling proposal

- **WHOLE TREES:** Generate new monosaccharide connectivity and linkage labels.
- **FUNCTIONAL CONDITION:** Aim for a specified assay response; audit every claim.

This presentation follows the target-conditioned generation problem in the supplied glycan folder, rather than redefining the project as single-token completion. It is a proposal and evidence audit. No generator has been trained for this deck and no improved biological activity is claimed. The course guide requires measured feasibility before final topic acceptance. The full vision uses a target protein representation; the bounded pilot uses a small set of experimentally represented lectin IDs. This distinction is fundamental to keeping the scope honest.

Sources: [DESC](../glycan-problem-description.md), [GUIDE](../../Final Project Guide.pdf)

## 02. The project in one sentence

Generate multiple valid glycan structures under a specified biological condition.

- **INPUT:** Lectin identity + desired response class + optional motif.
- **OUTPUT:** A complete, labelled glycan tree; branching is generated.
- **DELIVERABLE:** A ranked, audited candidate set and a reproducible benchmark.

The intended output is a carbohydrate chemical structure, not a protein binder, a property label or a completed fixed skeleton. A condition can be a target lectin identity with high/low normalized array-response bins. A structural motif can also be requested. New targets are not automatically supported: the small target-ID pilot only addresses lectins represented in the selected data. In a computer-only project, candidates remain hypotheses. Their value is a reproducible generation-and-audit method that could prioritize subsequent experiments.

Sources: [DESC](../glycan-problem-description.md), [BRIEF](../glycan_project.md)

## 03. Glycans are recognition surfaces

Their biological meaning depends on both chemistry and presentation.

- **GLYCOCALYX:** Glycoproteins and glycolipids display diverse glycan epitopes.
- **LECTINS:** Carbohydrate-binding proteins recognize particular glycan contexts.
- **CONTEXT:** Density, scaffold, accessibility and conformation influence recognition.

The cell-surface illustration is schematic. Glycans can be linear or branched; this project restricts its output to connected tree-like structures supported by the chosen grammar. Recognition occurs at a three-dimensional interface even when the model uses a two-dimensional labelled graph. Display on a protein or membrane can make a major contribution. We therefore avoid assuming that a free glycan, an array-immobilized glycan and a densely displayed glycan have interchangeable activities.

Sources: [LO](https://doi.org/10.1002/advs.202103807), [CONTACT](https://doi.org/10.1038/s41467-025-67590-y)

## 04. The structure is more than a sugar list

Node identity, bond chemistry and branching all carry information.

- **NODES:** Gal, GlcNAc, Man, Fuc, Neu5Ac and other supported sugars.
- **EDGES:** Anomeric configuration plus donor/acceptor carbon positions.
- **TOPOLOGY:** The reducing-end root and nonreducing branches define the tree.

Conventional SNFG-style icons are used throughout the deck: galactose is a yellow circle; mannose a green circle; GlcNAc a blue square; fucose a red triangle; Neu5Ac a purple diamond. A monosaccharide count cannot distinguish linkage isomers. Anomeric information is most naturally an edge/donor attribute; terminal reducing residues may have an unspecified anomeric state. The representation must preserve stereo- and linkage labels during canonicalization and comparison.

Sources: [GLYLES](https://doi.org/10.1186/s13321-023-00704-0), [DESC](../glycan-problem-description.md)

## 05. One linkage can change recognition

A useful pilot contrasts related epitopes rather than arbitrary molecules.

- **MOTIF A:** Neu5Ac(α2–6)Gal(β1–4)GlcNAc
- **MOTIF B:** Neu5Ac(α2–3)Gal(β1–4)GlcNAc
- **PILOT TARGETS:** SNA and a specified MAL-I preparation, subject to data coverage.

These are illustrative sialyllactosamine motifs, not generated results. Primary experimental studies show different recognition by SNA and MAL-I. Their preferences are context-dependent; the motif is not a sufficient universal binding rule. Maackia preparations and names vary, so match the precise reagent and metadata instead of merging every MAA/MAL label. The proposed target pair must be confirmed to have adequate overlapping glycans, usable assay metadata and suitable measurement-data reuse terms.

Sources: [SNA](https://doi.org/10.1039/D1SC05435J), [PLATFORM](https://pubmed.ncbi.nlm.nih.gov/24658466/)

## 06. Why design new glycan candidates?

Potential users need selectivity, interpretable probes and useful presentation.

- **RECOGNITION PROBES:** Help experimentalists discriminate related lectin preferences.
- **DECOY CANDIDATES:** Explore ligands that might compete with pathogen attachment.
- **IMMUNE GLYCOBIOLOGY:** Investigate interactions involving Siglecs or galectins in later studies.

These applications motivate the field, but the proposed student study is not a therapeutic development program. Siglecs bind sialylated glycans; galectins recognize beta-galactoside contexts and should not be described as equivalent sialic-acid receptors. Binding may activate, cluster, inhibit or have no useful functional consequence depending on context. Antibody Fc engineering is also a meaningful glycan application, but it is a different design problem and is excluded from this pilot. The immediate output is an assay-aware candidate shortlist.

Sources: [SIGLEC](https://doi.org/10.1038/s41467-026-71086-8), [GALECTIN](https://pubmed.ncbi.nlm.nih.gov/18216021/), [ERC](https://www.gu.se/en/news/erc-grant-for-bojars-research-on-glycans)

## 07. Three tasks that must stay separate

Only the final column is this proposal’s central generative task.

- **COMPLETION:** Recover missing sugar or linkage labels on a supplied structure.
- **IDENTIFICATION:** Infer a glycan from spectra or an experimental binding fingerprint.
- **INVERSE DESIGN:** Generate a whole structure for a requested target/property.

Masked prediction can be a generative training objective, but recovering one class label is not the same research question as designing whole new glycan topologies. Spectral generation is a genuine conditional-generation task whose condition is analytical evidence. A Boltzmann sampler that reconstructs structures from a binding fingerprint is relevant inverse-inference prior art. Neither should be presented as proof that protein-sequence-conditioned ligand design is already solved. This proposal trains a probability distribution over entire structure-building trajectories.

Sources: [GT](https://doi.org/10.1093/bioinformatics/btag147), [BART](https://doi.org/10.1101/2025.07.02.662857), [BOLTZ](https://doi.org/10.1021/acs.analchem.3c04992)

## 08. A bounded, testable research question

Can constrained conditioning improve valid, novel yield at equal compute?

- **MAIN QUESTION:** Does grammar-masked conditional generation outperform filtering?
- **BIOLOGICAL PILOT:** One or two named lectins; assay-aware high/low response conditions.
- **SCOPE LIMIT:** Small sugar vocabulary; bounded tree size; no new-target claim.

The proposed bound is 3–15 sugar residues for an initial pilot; these are design choices rather than dataset statistics. Start with common supported monosaccharides and explicitly listed linkages. The study compares a small conditional autoregressive generator, an unconditional generator followed by selection, and simple statistical/mutation baselines. If functional labels cannot be licensed, downloaded and validated, a motif-only task may remain possible but must be renamed and must not be represented as solved binding design.

Sources: [DESC](../glycan-problem-description.md), [BRIEF](../glycan_project.md)

## 09. Formal problem: a distribution over trees

Learn a generator; use property scores as fallible evidence.

- **STRUCTURE:** G = (V, E, sugar labels, linkage labels), rooted at the reducing end.
- **CONDITION:** c = (lectin ID, response bin, optional motif).
- **GENERATOR:** pθ(G | c) = ∏t pθ(action t | earlier actions, c).

A deterministic traversal gives each labelled tree a reproducible construction sequence. The decoder chooses sugar identity, parent attachment site, anomer and linkage, then branch/stop actions. Hard masks restrict the support of the distribution. The initial loss is conditional negative log-likelihood on eligible structures and measured-response bins. A guidance score can later combine predicted response, size and novelty penalties. A score threshold does not ensure experimental affinity, and ensemble variance is not a validity proof. No binding predictor needs to be differentiated through for the basic comparison.

Sources: [DESC](../glycan-problem-description.md)

## 10. What does one training example mean?

Structure records and functional measurements are different data units.

- **STRUCTURE CORPUS:** One canonical glycan tree; useful for learning chemical syntax.
- **FUNCTION TABLE:** Glycan + lectin + response + assay/context metadata.
- **CRITICAL DISTINCTION:** Many interaction rows can share the same small glycan library.

Keep glycan identifiers, reagent/preparation, concentration, platform, linker, replicate and normalization information where available. The paper’s interaction count is not the number of independent molecules or independent wet-lab discoveries. An array records fluorescence or a normalized assay response; it is not automatically a dissociation constant. Treat high/low classes as within-context labels and retain continuous values. Every table needs explicit units, censoring and missing-value policies. Repeats must not leak across train and test.

Sources: [LO](https://doi.org/10.1002/advs.202103807), [PLATFORM](https://pubmed.ncbi.nlm.nih.gov/24658466/)

## 11. Structural data are small enough to inspect

A practical starting corpus is publicly available; usable counts require filtering.

- **GLYCANGT:** 83,739 pretraining glycans in the paper; 83,740 in the repository.
- **GLYCOSMOS:** Public structures; source data CC BY 4.0.
- **DOWNLOAD SIZE:** GlycanGT source archive ≈7.7 MB, including more than just training data.

The count discrepancy is one record and should be reported rather than hidden. These are source-release counts, not the count after our restricted grammar, size bounds, canonical deduplication and structural-family splitting. The October audit listed a GlyCosmos bulk CSV around 79.71 MB, but release sizes change. Registry resources overlap, so do not add counts from GlyTouCan and GlyCosmos. Download public training files rather than relying on gated model weights. Record exact bytes, release, checksum, schema and license at execution time.

Sources: [GT](https://doi.org/10.1093/bioinformatics/btag147), [GTCODE](https://github.com/matsui-lab/GlycanGT), [GTARCH](https://zenodo.org/records/18636040), [COSLICENSE](https://glycosmos.org/license)

## 12. Binding data are the real bottleneck

Public files exist; reuse rights and target-specific coverage still decide feasibility.

- **LECTINORACLE:** Paper reports 564,647 unique protein–glycan interactions.
- **GLYGEN ARRAY:** An explicitly licensed portal is an alternative; bulk assembly remains to verify.
- **STOP CONDITION:** No functional training until measurement-data rights and splits are settled.

The legacy LectinOracle repository is archived and points users to glycowork. MIT applies to code; it is not sufficient evidence that every original CFG/Imperial measurement has the same license. The previous workspace audit recorded around 12.76 MB for the main CSV, but that is not a newly downloaded verified file in this presentation. GlyGen portal counts refer to dataset collections, not individual measurements, and the full bulk export was not executed. These unresolved checks prevent an all-pass screening claim.

Sources: [LO](https://doi.org/10.1002/advs.202103807), [LOCODE](https://github.com/BojarLab/LectinOracle), [ARRAY](https://glygen.ccrc.uga.edu/ggarray/)

## 13. Split by structure before any training

A random interaction-row split can make generalization look easier than it is.

- **CANONICALIZE:** Unify branch order, sugar names, anomers and linkage labels.
- **GROUP:** Put isomorphic glycans and close structural families in one group.
- **FREEZE:** Use the same train/validation/test boundaries for predictors and generators.

Hashing can efficiently bucket candidates, but exact labelled isomorphism resolves potential collisions. A four-iteration Weisfeiler–Lehman hash is not a family-distance metric. Family grouping needs a declared similarity such as common labelled subtree or motif similarity, with threshold sensitivity reported. No structure from an evaluation family should occur in unsupervised pretraining if the claim is generalization to unseen glycan families. For transfer to new lectins, add a separate protein-family holdout; this pilot does not make that claim.

Sources: [BRIEF](../glycan_project.md), [GUIDE](../../Final Project Guide.pdf)

## 14. Why 100× compute cannot buy the labels

More sampled structures do not create new experimental interaction evidence.

- **CHEAP:** Generate millions of plausible sequences or pseudo-labels.
- **EXPENSIVE:** Measure binding under controlled presentation and assay conditions.
- **ARGUMENT:** Compute can improve inference, but cannot establish unmeasured ground truth.

The course’s compute-invariance argument should be framed around functional measurements, not around the existence of glycan strings. A large structural corpus and synthetic examples can improve representation learning, so it would be wrong to claim that compute cannot help at all. The invariant is epistemic: predictions and simulations are not additional measured binding labels. If the final project becomes only a motif-label task where labels are computable, this particular scarcity argument weakens and topic qualification must be reconsidered.

Sources: [GUIDE](../../Final Project Guide.pdf), [LO](https://doi.org/10.1002/advs.202103807), [PLATFORM](https://pubmed.ncbi.nlm.nih.gov/24658466/)

## 15. Prior work solves neighboring tasks

No “first glycan generator” claim is needed.

- **SweetTalk · 2021:** Language modeling and property-guided local editing.
- **Boltzmann model · 2024:** Candidate structures from measured lectin fingerprints.
- **GlycoBART · 2025:** Glycan strings generated from MS/MS spectra.

These are direct reasons to avoid saying the generative side is empty. The distinction is the condition, the output space and the evaluation protocol. SweetTalk is important historical prior art even though it predates the main 2022–2026 window. The Boltzmann approach uses experimental fingerprints to infer identities. GlycoBART performs analytical sequencing. None of these distinctions guarantees novelty of our entire proposed combination. A narrow reproducible gap must survive a full paper/config/code audit before being claimed.

Sources: [SWEETTALK](https://doi.org/10.1016/j.chom.2020.10.004), [BOLTZ](https://doi.org/10.1021/acs.analchem.3c04992), [BART](https://doi.org/10.1101/2025.07.02.662857)

## 16. Predictors and completion models are tools

They support the pipeline but are not interchangeable with a whole-tree generator.

- **LectinOracle / SweetNet:** Predict binding or learn glycan representations.
- **GlycanGT / GlycanAA:** Masked recovery and representation/property learning.
- **GlycanML / GlyContact:** Prediction benchmarks and structural analysis resources.

Predictive models can supply frozen scorers, encoders or diagnostic tests. Their performance does not certify a generator, and their training budgets are not automatically feasible student baselines. Do not fully retrain large models merely to claim a precedent. The selected generator is deliberately compact and new as an implementation; the course allows a new baseline if the pipeline is measured. A full literature log must identify data, code, compute, metrics and limitations for each relevant study, distinguishing paper verification from repository-only inference.

Sources: [LO](https://doi.org/10.1002/advs.202103807), [SWEETNET](https://doi.org/10.1016/j.celrep.2021.109251), [GT](https://doi.org/10.1093/bioinformatics/btag147), [AA](https://arxiv.org/abs/2506.01376), [ML](https://arxiv.org/abs/2405.16206), [CONTACT](https://doi.org/10.1038/s41467-025-67590-y)

## 17. The contribution is controlled generation

Two methodological levers, plus an audit that can falsify apparent gains.

- **LEVER 1:** Mask chemically impossible actions during tree construction.
- **LEVER 2:** Condition generation on target-specific response or motif requests.
- **AUDIT:** Check whether gains survive independent scoring and near-neighbor analysis.

The empirical claim is modest: an improvement in valid, condition-compliant and non-memorized candidates at an equal compute and sampling budget. It does not require a state-of-the-art biological discovery claim. Independent scorers should differ in model family and ideally assay source; changing only random seeds yields correlated errors. The experiment can also be informative if scores fail to generalize: demonstrating failure under a stronger split is a valid critique when methods and evidence are documented.

Sources: [DESC](../glycan-problem-description.md), [GUIDE](../../Final Project Guide.pdf)

## 18. A small autoregressive tree generator

Train the generator; keep large protein encoders out of the critical path.

- **CONDITION ENCODER:** A learned lectin-ID embedding plus response/motif flags.
- **DECODER:** Proposed 2-layer GRU, hidden size 128; small action vocabulary.
- **STATE:** Track open branches and occupied attachment positions.

This is a proposed architecture, not a published timing result. A deterministic depth-first linearization still represents a non-grid chemical graph; the grammar operates on tree state rather than plain text syntax. A graph generator could be substituted later, but a compact GRU makes a low-compute baseline easier to implement. Parameter count depends on the final vocabulary and condition dimensions and must be measured. Protein-sequence conditioning is a later extension with cached embeddings; ESM-2 dimensions depend on the chosen variant and are not universally 1,280.

Sources: [DESC](../glycan-problem-description.md), [BRIEF](../glycan_project.md)

## 19. Generation is a sequence of chemical decisions

The topology is built, not supplied as a fixed skeleton.

- **START:** Choose a reducing-end residue and initialize the tree state.
- **GROW:** Select parent/site, sugar, anomer and a compatible linkage.
- **BRANCH / STOP:** Open or close a branch; stop within the size bound.

Every training glycan is serialized into an action sequence after canonicalization. Teacher forcing trains the decoder to assign probability to valid construction steps. During sampling, available actions depend on the state. A typical mask prevents a second attachment to an already occupied acceptor position, forbids a Neu5Ac donor linkage from carbon 1 and prevents syntactic branch mismatches. The initial grammar handles a restricted chemistry. Excluded modifications are a stated scope choice rather than evidence that the molecules are invalid in biology.

Sources: [DESC](../glycan-problem-description.md)

## 20. Training does not require reinforcement learning

Establish conditional likelihood first; add guidance only if the scorer is credible.

- **PHASE A:** Learn the structure distribution on the canonical corpus.
- **PHASE B:** Fine-tune on eligible target/response-labelled examples.
- **PHASE C:** Sample under constraints; compare simple reranking with conditioning.

A neural binding predictor is not a prerequisite for structural pretraining or motif conditioning. Functional guidance, however, requires a predictor that first passes its own held-out test. Use measured labels for fine-tuning rather than pretending millions of pseudo-labelled glycans are new ground truth. For a fair baseline, include the same decoder trained without conditions, followed by the same selection budget. Reinforcement learning is optional and outside the minimum scope; it could add instability and consume the entire budget before basic comparisons are established.

Sources: [BRIEF](../glycan_project.md)

## 21. Validate the binding evaluator before guiding

A strong self-score is insufficient evidence of a useful generated structure.

- **FIT:** Train a small motif/fingerprint or graph predictor on training families.
- **CHECK:** Evaluate held-out ranking, calibration and simple motif baselines.
- **FREEZE:** Use a separate locked evaluator to audit generator-selected candidates.

The scorer predicts normalized assay response, not necessarily affinity. Establish whether the task is regression, within-array ranking or high/low classification before selecting metrics. Score all generator variants with the same evaluators. A model used to choose candidates is not an independent test of those candidates. Avoid tuning the generator on the test evaluator. A released LectinOracle checkpoint may include our evaluation glycans and therefore cannot be called independent without a training-provenance audit. If evaluator validity fails, stop functional claims.

Sources: [LO](https://doi.org/10.1002/advs.202103807), [PLATFORM](https://pubmed.ncbi.nlm.nih.gov/24658466/), [GUIDE](../../Final Project Guide.pdf)

## 22. Uncertainty filters are useful, not proofs

Low disagreement can coexist with shared bias.

- **USEFUL SIGNAL:** Flag candidates far from measured chemistry or with scorer disagreement.
- **FAILURE MODE:** Several models may confidently share the same extrapolation error.
- **REPORT:** Separate in-domain, uncertain and unsupported candidates.

The supplied description said an ensemble variance threshold eliminates adversarial out-of-distribution artifacts. That guarantee is not justified. Ensembles may share data, architecture, featurization and errors. Use uncertainty to prioritize or abstain, inspect the effect of thresholds and report accepted yield as well as scores. A deliberately different evaluator and similarity-stratified analysis can expose some failures but do not substitute for measurements. It is also invalid to claim that high predicted binding ensures efficacy, therapeutic safety or biological selectivity.

Sources: [DESC](../glycan-problem-description.md), [BRIEF](../glycan_project.md)

## 23. Validity has four distinct layers

Every accepted structure must pass the declared scope checks.

- **TREE + GRAMMAR:** Connected, acyclic, supported sugar/linkage labels; no occupied-site conflict.
- **ATOM-LEVEL CHECK:** Faithful GlyLES conversion followed by RDKit sanitization.
- **BIOLOGY + FUNCTION:** Biosynthesis, synthesis and binding require additional evidence.

Layer one is the project-specific structural checker. Layer two includes conversion coverage, warnings and atom-level checks. GlyLES explicitly does not perform semantic glycan validation, so a successful translation is not a complete biochemical certificate. Treat ignored modifications as unsupported rather than silently deleting them. A grammar can enforce a restricted structural language, but it cannot guarantee that a glycosyltransferase pathway or synthetic route exists. Layer four is functional confirmation; a binding surrogate only supplies a proxy. Report each layer separately, not one ambiguous validity percentage.

Sources: [GLYLES](https://doi.org/10.1186/s13321-023-00704-0), [WORK](https://github.com/BojarLab/glycowork), [RDKIT](https://www.rdkit.org/docs/GettingStartedInPython.html)

## 24. Novelty must survive structural comparison

A new string can encode an old glycan—or a one-step copy.

- **EXACT COPIES:** Canonical labelled-tree identity; hash buckets plus isomorphism.
- **NEAR COPIES:** Nearest labelled subtree/motif similarity and edit-distance diagnostics.
- **DISCLOSURE:** Publish the nearest training neighbors for selected candidates.

Use graph attributes for sugar identity, anomer, donor/acceptor sites and modifications. Branch reordering must not count as novelty. Hash inequality or equality alone is not a universal chemical proof: verify the canonicalization implementation and handle collisions. For near-duplicate analysis, state the chosen distance, normalization and threshold. A small subset can use exact tree-edit distances; a scalable motif/subtree index can screen the full corpus. Visual nearest-neighbor tables make copying easy to inspect. Separately check overlap with predictor training data.

Sources: [GUIDE](../../Final Project Guide.pdf), [BRIEF](../glycan_project.md)

## 25. Evaluate joint success, not a single score

A useful candidate must clear several tests simultaneously.

- **STRUCTURE:** Grammar pass, conversion coverage, uniqueness and size distribution.
- **CONTROL:** Requested motif rate and held-out response-ranking performance.
- **GENERALIZATION:** Exact-copy rate, nearest-neighbor distance and evaluator agreement.

Define audited yield as the number of generated samples that are structurally valid, condition-compliant, unique and outside a predeclared near-copy threshold, divided by the number sampled. Functional criteria remain proxy criteria unless measured. For prediction use metrics appropriate to the label, such as Spearman ranking or AUPRC for imbalanced classes; estimate uncertainty with family-level resampling. Count invalid and rejected outputs rather than dropping them from every denominator. Match number of samples and oracle calls between methods. Report distributions, not only best examples.

Sources: [GUIDE](../../Final Project Guide.pdf), [BRIEF](../glycan_project.md)

## 26. A small experiment matrix isolates the levers

Use the same decoder, split, sampling budget and evaluation procedure.

- **B0 · SIMPLE:** Markov/tree sampler and seed-mutation search.
- **B1 · NEURAL:** Unconditional GRU + post-filtering / reranking.
- **B2–B4 · ABLATIONS:** Conditional; grammar-masked; conditional + grammar-masked.

B0 is a conceptual baseline inspired by historical statistical/editing methods, not a claim of exact paper reproduction without source code. The 2×2 neural design crosses conditioning on/off with grammar masking on/off. The unconditional row still has access to the same reranker when the comparison is filter versus condition. This separates conditioning benefit from the benefit of rejection. Use paired seeds where budget permits. If the four-hour envelope cannot cover the required comparisons, reduce corpus size, epochs and sample count uniformly before expanding to additional methods.

Sources: [GUIDE](../../Final Project Guide.pdf), [SWEETTALK](https://doi.org/10.1016/j.chom.2020.10.004), [BOLTZ](https://doi.org/10.1021/acs.analchem.3c04992)

## 27. What would count as a good result?

Pre-register the decision rules; do not invent success percentages.

- **MODEL RESULT:** Higher audited yield than equal-budget baselines, with uncertainty.
- **SCIENTIFIC RESULT:** Explain whether improvements survive stronger splits and independent scoring.
- **NEGATIVE RESULT:** Document when high self-scores disappear under the audit.

No result bars appear here because experiments have not been run. The presentation is a Phase 1 proposal. Pre-register any minimum practical improvement and near-copy threshold after inspecting validation data, before opening the test set. A negative outcome can be useful: for example, the generator increases its own binding predictor’s score but loses that gain on a separate evaluator. Biological claims remain limited to the evidence available. The goal is a defensible empirical paper, not a promise of a new drug or a universal glycan designer.

Sources: [GUIDE](../../Final Project Guide.pdf)

## 28. The smoke test is the admission ticket

The course requires measurements on the intended student platform.

- **SETUP:** Fresh Colab/Kaggle session; install + fetch + load in under 5 minutes.
- **TRAIN:** 50 steps / one epoch; record hardware, VRAM and step time.
- **CHECK:** 100+ structures; time parser, semantic checks, conversion and scorer.

A small dataset and model are not enough to assert feasibility. The guide requires a fresh-session setup measurement, a 12–16 GB memory micro-batch test and a training-time projection. Exclude notebook warmup and include data loading transparently. Time at least 100 samples for checkers and report mean, median, p95 and failure counts, because unsupported candidates can dominate cost. No Colab smoke test has been run in preparing this deck. Admission remains pending until these measurements and data-rights checks are complete.

Sources: [GUIDE](../../Final Project Guide.pdf)

## 29. A four-GPU-hour envelope—not a benchmark

Proposed allocation; update it using measured throughput.

- **TRAIN + COMPARE:** 2.0 h generator comparisons + 0.5 h predictor fitting.
- **EVALUATE:** 0.5 h sampling/evaluation + 1.0 h contingency.
- **CPU WORK:** Parsing and conversion also consume session wall time.

These are proposed allocations summing to four GPU-hours, not measured or paper-reported runtimes. CPU-only work may use no GPU time while still keeping a Colab session busy. The saved local checker benchmark measured 200 GlyLES-to-RDKit attempts, mean about 380 ms and 182 parseable conversions, on an Intel i3 laptop. Some failures were compatibility/coverage issues and some warnings indicated ignored modifications; conversion success is not full semantic validity. This evidence does not establish training time, setup time or fresh Colab speed. Use a small corpus and low sampling count if projections exceed the envelope.

Sources: [GUIDE](../../Final Project Guide.pdf), [BENCH](../../tasks/validity_benchmark.json)

## 30. Four weeks, with a decision at each boundary

Every week produces a reviewable artifact.

- **WEEK 1:** Freeze data, licenses, grammar and split; pass the smoke test.
- **WEEKS 2–3:** Train baselines; integrate conditions, masks and audit tables.
- **WEEK 4:** Run bounded ablations; publish reproducible results and limitations.

Map the implementation to course Weeks 16–19: Week 16 produces the setup and W&B artifacts; Week 17 trains the baseline and records convergence/system logs; Week 18 integrates checkers and memorization tables; Week 19 adds the extension, completes ablations and publishes the interactive report. Stop expanding scope if Week 1 cannot establish the functional data pipeline. A motif-only fallback is technically possible but changes the scientific claim and may weaken the measurement-scarcity argument. Do not quietly relabel it as binding design.

Sources: [GUIDE](../../Final Project Guide.pdf)

## 31. W&B records evidence, not just loss curves

The guide requires artifacts, system logs and a public interactive report.

- **ARTIFACTS:** Raw snapshot, preprocessing manifest, split IDs and checkpoints.
- **RUN LOGS:** Seed/config, loss, wall time, VRAM and validity metrics.
- **SAMPLE TABLE:** Generated tree, condition, scores, rejection reason and nearest neighbor.

The sample table must make a generated candidate traceable to its model version, training split and evaluation procedure. Keep failures and rejected candidates. Logs should distinguish training scorer, independent evaluator and structural checker. Version dataset licenses and any filtering policy alongside data artifacts. The course expects an interactive W&B Report and a live ten-minute code/dashboard defense. Access to W&B is experiment tracking infrastructure, not a hidden prerequisite for downloading the scientific dataset. Never upload tokens or original restricted data to public reports.

Sources: [GUIDE](../../Final Project Guide.pdf)

## 32. Relevance in 2026: active, specialized research

The application is credible; publication growth needs a separate count audit.

- **GOTHENBURG:** Bojar Lab: glycan ML, interactions and structural analysis.
- **NAGOYA / iGCORE:** Matsui Lab: graph representations and completion.
- **RECENT TRAJECTORY:** CandyCrunch 2024 → GlyContact 2025 → GlycanGT 2026.

These are examples of continuing methodological development, not counts showing annual growth in a single narrowly defined literature. R1 is supported by official institutional pages, and R2 by the cited venues. R4 is supported by biological questions and funded glycoscience programs. R3 remains partially established because a screened, deduplicated publication corpus for 2023–2026 has not been assembled. H2 is also uncertain: academic concentration does not prove low crowding or eliminate commercial interest. Large generative chemistry models are not the intended competitive benchmark for this four-week study.

Sources: [BOJAR](https://www.gu.se/index.php/en/research/daniel-bojar), [MATSUI](https://www.nagoya-u.ac.jp/researchinfo/result/2026/04/ai-108.html), [CANDY](https://doi.org/10.1038/s41592-024-02314-6), [CONTACT](https://doi.org/10.1038/s41467-025-67590-y), [GT](https://doi.org/10.1093/bioinformatics/btag147), [ERC](https://www.gu.se/en/news/erc-grant-for-bojars-research-on-glycans)

## 33. Headroom: constraint control and evaluation

The strongest gap is a bounded empirical question, not an absence claim.

- **H1 · HEADROOM:** Quantify validity/control trade-offs rather than assuming unsaturated SOTA.
- **H2 · CROWDING:** Specialized academic work is visible; low scooping risk is unproven.
- **H3 · AUDIT:** Test proxy exploitation and near-copy dependence explicitly.

There is no verified universal claim that no whole-tree protein-conditioned generator exists. The narrow proposal may still be useful if it measures a poorly characterized trade-off at student compute scale. Treat hypotheses about predictor exploitation as things to test, not accusations against papers that were not fully audited. Good critique is operational: define the condition, build leakage-resistant splits, use independently trained evaluators, publish nearest neighbors, and reveal how much apparently strong performance comes from memorization or familiar motifs.

Sources: [GUIDE](../../Final Project Guide.pdf), [BRIEF](../glycan_project.md)

## 34. All eight course gates: a candid status

The topic is not fully qualified until the pending evidence is measured.

- **SUPPORTED:** Structured output; natural conditional generation; two methodological levers.
- **CONDITIONAL:** Scarcity argument; validity implementation; licensed functional data; copy audit.
- **PENDING:** Fresh-platform setup, end-to-end timing and memory test.

Gate 1 passes in formulation because the output is a labelled tree. Gate 2 is supported only if functional measurement scarcity remains central. Gate 3 passes as a conditional generative formulation. Gate 4 requires implementing and benchmarking a composite checker rather than merely naming libraries. Gate 5 has at least conditioning and grammar constraints. Gate 6 passes for a structural corpus but the functional-label license/export is unresolved. Gate 7 is not measured. Gate 8 has an algorithmic plan but no executed audit. Since the guide requires all eight, do not describe the project as fully accepted yet.

Sources: [GUIDE](../../Final Project Guide.pdf), [BRIEF](../glycan_project.md)

## 35. The five risks that can change the project

Each has an explicit action rather than a hidden assumption.

- **DATA / PREDICTOR:** Unclear rights or weak held-out predictor → stop functional guidance.
- **COMPUTE / COVERAGE:** Over budget or unsupported chemistry → shrink scope and remeasure.
- **MEMORIZATION:** Near-copy dependence → stronger splits, simple baselines and revised claims.

Additional biological risks include array-to-solution transfer, effects of multivalency, unknown synthesis feasibility and target-context mismatch. Removing unsupported sugars changes the domain and should be quantified. An unreliable predictor cannot be rescued merely by a more powerful generator. A training model that fits in memory may still be too slow end-to-end. The fallback motif task is a distinct claim and should be requalified against the course’s measurement-bound focus. These are limitations of the proposed evidence, not reasons to imply that glycan research lacks real-world importance.

Sources: [BRIEF](../glycan_project.md), [GUIDE](../../Final Project Guide.pdf)

## 36. The full vision is larger than the pilot

Keep target-sequence conditioning as a separately tested extension.

- **PILOT:** Target ID + response class; generate whole trees in a narrow domain.
- **EXTENSION:** Cache protein embeddings; condition across sufficiently sampled targets.
- **NEW CLAIM:** Unseen-lectin transfer requires protein-family holdout and enough labels.

The original description assumes a 200-amino-acid lectin domain and 1,280-dimensional ESM-2 embedding. Neither is universal: lectin architectures vary and embeddings depend on the encoder variant. In the pilot there is no expensive end-to-end protein-model training. If cached embeddings are added, count their extraction/setup costs and confirm rights and split boundaries. Conditioning on a sequence does not demonstrate generalization to a new target. This extension is excluded unless the core model, data and budget tests are already complete.

Sources: [DESC](../glycan-problem-description.md), [LO](https://doi.org/10.1002/advs.202103807)

## 37. The decision to defend

Proceed with functional generation only after the first-week evidence gates pass.

- **WHAT WE BUILD:** A small, conditional whole-tree generator with chemical action masks.
- **WHAT WE TEST:** Valid, controlled, novel yield under stronger splits and independent scoring.
- **WHAT WE CLAIM:** Computational candidate-design evidence; biological function remains unverified.

The project is worth pursuing if a suitable measured functional table can be licensed and assembled, a simple evaluator generalizes beyond trivial motif recognition, and the smoke test fits the compute envelope. Otherwise, redesign the scientific task explicitly rather than forcing a falsely qualified result. The contribution is a reproducible constrained generative-modeling study. The final research package should include source audits, honest negative results, all baselines and a readable candidate table. No generated structure is a validated ligand merely because it passes grammar checks.

Sources: [DESC](../glycan-problem-description.md), [GUIDE](../../Final Project Guide.pdf)

## 38. Appendix A · Guide-to-deck mapping

This presentation explains the plan; it does not replace the required report.

- **PHASE 1 · 60%:** 8–10 page two-column proposal; formalism, qualification and peer response.
- **PHASE 2 · 40%:** Code, trained baselines, checker/memorization audit, W&B report and defense.
- **STILL REQUIRED:** 15+ audited papers; empirical smoke test; appendices A–D and AI audit log.

Course sections map to this deck as follows: domain mechanics and introduction are slides 3–6; formalism slides 8–10 and 18–20; related work slides 15–16; qualification/scarcity slides 14 and 34; evaluation slides 21–27; smoke test and execution slides 28–31; risks and limitations slides 33–36. Slide positions may be read from the generated notes. The supplied guide also specifies peer review with at least three citation/link spot checks, an author response, a 15+ paper log and a separate AI usage/verification appendix. None of those is marked complete merely because the presentation exists.

Sources: [GUIDE](../../Final Project Guide.pdf)

## 39. Appendix B · Corrections to the source draft

Preserve the idea; remove guarantees the evidence does not support.

- **NO UNIVERSAL FIRST:** Replace “no glycan generators” with a narrow audited gap.
- **NO FUNCTION GUARANTEE:** Array score ≠ affinity; ensemble agreement ≠ binding proof.
- **NO HASH GUARANTEE:** WL hashing helps deduplication; it does not certify family novelty.

Other corrections: not all glycans are branched; tree-only topology is a chosen scope. Do not present the average of 7.1 residues or 91 heavy atoms as universal facts without its original dataset. Galectin-3 is not a Siglec-like sialic-acid receptor. Omit the unsupported percentage of therapeutic monoclonal antibodies. A 7.7 MB repository archive is not a pure training-data file. Code licenses do not automatically cover source measurements. The published GlyLES timing is not the workspace’s measured timing. Hardware performance targets and method improvements are proposals, not results.

Sources: [DESC](../glycan-problem-description.md), [BRIEF](../glycan_project.md), [GLYLES](https://doi.org/10.1186/s13321-023-00704-0), [LO](https://doi.org/10.1002/advs.202103807)

## 40. Appendix C · Data and checker ledger

Provenance matters more than a large headline row count.

- **CONFIRMED SOURCE CLAIMS:** 83,739 glycans in GlycanGT; 564,647 interactions in LectinOracle.
- **HISTORICAL LOCAL MEASUREMENT:** 200 conversion attempts: mean ≈380 ms on an Intel i3 CPU.
- **NOT YET MEASURED:** Eligible target rows; clean split sizes; setup; T4 training and evaluator speed.

The local benchmark succeeded in producing parseable molecules for 182 of 200 attempts. The remaining cases cannot be equated with invalid biology because notation/version compatibility contributes. Some conversions issued ignored-modification warnings, so success does not imply faithful full chemistry. The original GlyLES benchmark reported about 19 ms per supported glycan on different hardware. The raw file-size figures in the workspace brief are snapshots; the plan requires fresh exact bytes and checksums. Record source data rights, source URL, retrieval date, filtering code and a reproducible count at every stage.

Sources: [GT](https://doi.org/10.1093/bioinformatics/btag147), [LO](https://doi.org/10.1002/advs.202103807), [BENCH](../../tasks/validity_benchmark.json), [BRIEF](../glycan_project.md)

## 41. Appendix D · Glossary and claim boundaries

Definitions used consistently throughout the proposal.

- **GLYCAN / LECTIN:** A carbohydrate structure / a carbohydrate-binding protein.
- **RFU / AFFINITY:** Assay fluorescence / a thermodynamic binding quantity; not interchangeable.
- **NOVEL / FUNCTIONAL:** Structurally distinct / experimentally active; separate claims.

Other useful definitions: anomer describes configuration at the anomeric center; linkage specifies donor and acceptor positions; motif is a labelled substructure; glycoform is a particular glycosylated molecular form; canonicalization maps equivalent representations to a consistent representation; conditional generation samples structures given a requested context; a surrogate is a model predicting a measured quantity; a held-out family is a predeclared structural group excluded from fitting; abstention means refusing to trust a proxy outside its supported domain. These definitions prevent the scientific claim from expanding beyond available evidence.

Sources: [LO](https://doi.org/10.1002/advs.202103807), [GLYLES](https://doi.org/10.1186/s13321-023-00704-0), [PLATFORM](https://pubmed.ncbi.nlm.nih.gov/24658466/)

## 42. Primary sources · 1/5

Clickable citations; full URLs and qualifications are in sources.md.

- **GT:** Kitani et al. GlycanGT. Bioinformatics (2026)
- **LO:** Lundstrøm et al. LectinOracle. Advanced Science (2022)
- **SWEETTALK:** Bojar et al. Deep-Learning Resources for Studying Glycan-Mediated Host-Microbe Interactions. Cell Host & Microbe (2021)
- **SWEETNET:** Burkholz et al. Using graph convolutional neural networks to learn a representation for glycans. Cell Reports (2021)
- **BOLTZ:** Yom et al. A Boltzmann model predicts glycan structures from lectin binding. Analytical Chemistry (2024)

These references are a reading and citation register, not a claim that the course’s full Appendix B audit has been completed. Older papers are retained when they establish essential prior art or measurement context. In each formal paper-log row, still record model/data versions, licenses, training compute, evaluation and limitations at the primary source. The bibliography includes resources as well as papers; resources must not be counted as trained-generative-model precedents.

Sources: [GT](https://doi.org/10.1093/bioinformatics/btag147), [LO](https://doi.org/10.1002/advs.202103807), [SWEETTALK](https://doi.org/10.1016/j.chom.2020.10.004), [SWEETNET](https://doi.org/10.1016/j.celrep.2021.109251), [BOLTZ](https://doi.org/10.1021/acs.analchem.3c04992)

## 43. Primary sources · 2/5

Clickable citations; full URLs and qualifications are in sources.md.

- **BART:** Abtheen et al. Transformer-based Deep Learning for Glycan Structure Inference from Tandem Mass Spectrometry (2025 preprint)
- **AA:** Xu et al. Modeling All-Atom Glycan Structures via Hierarchical Message Passing and Multi-Scale Pre-training (ICML 2025)
- **ML:** Xu et al. GlycanML: A Multi-Task and Multi-Structure Benchmark for Glycan Machine Learning (ICLR 2025)
- **CONTACT:** Thomès et al. GlyContact analyzes glycan 3D structures at scale. Nature Communications (2025)
- **CANDY:** Urban et al. Predicting glycan structure from tandem mass spectrometry via deep learning. Nature Methods (2024)

These references are a reading and citation register, not a claim that the course’s full Appendix B audit has been completed. Older papers are retained when they establish essential prior art or measurement context. In each formal paper-log row, still record model/data versions, licenses, training compute, evaluation and limitations at the primary source. The bibliography includes resources as well as papers; resources must not be counted as trained-generative-model precedents.

Sources: [BART](https://doi.org/10.1101/2025.07.02.662857), [AA](https://arxiv.org/abs/2506.01376), [ML](https://arxiv.org/abs/2405.16206), [CONTACT](https://doi.org/10.1038/s41467-025-67590-y), [CANDY](https://doi.org/10.1038/s41592-024-02314-6)

## 44. Primary sources · 3/5

Clickable citations; full URLs and qualifications are in sources.md.

- **GLYLES:** Joeres et al. GlyLES. Journal of Cheminformatics (2023)
- **SNA:** Systematic synthesis of bisected N-glycans and unique recognitions by glycan-binding proteins. Chemical Science (2022)
- **PLATFORM:** Cross-platform comparison of glycan microarray formats (2014)
- **SIGLEC:** An atlas of human siglecs integrates expression, affinity, and cis/trans sialoglycan recognition profiles. Nature Communications (2026)
- **GALECTIN:** Galectin-1, -2, and -3 exhibit differential recognition of sialylated glycans and blood group antigens (2008)

These references are a reading and citation register, not a claim that the course’s full Appendix B audit has been completed. Older papers are retained when they establish essential prior art or measurement context. In each formal paper-log row, still record model/data versions, licenses, training compute, evaluation and limitations at the primary source. The bibliography includes resources as well as papers; resources must not be counted as trained-generative-model precedents.

Sources: [GLYLES](https://doi.org/10.1186/s13321-023-00704-0), [SNA](https://doi.org/10.1039/D1SC05435J), [PLATFORM](https://pubmed.ncbi.nlm.nih.gov/24658466/), [SIGLEC](https://doi.org/10.1038/s41467-026-71086-8), [GALECTIN](https://pubmed.ncbi.nlm.nih.gov/18216021/)

## 45. Primary sources · 4/5

Clickable citations; full URLs and qualifications are in sources.md.

- **COSMOS:** GlyCosmos downloads
- **COSLICENSE:** GlyCosmos official data license
- **GTCODE:** GlycanGT source and public processed data
- **GTARCH:** GlycanGT versioned source archive
- **ARRAY:** GlyGen Glycan Array Data Repository

These references are a reading and citation register, not a claim that the course’s full Appendix B audit has been completed. Older papers are retained when they establish essential prior art or measurement context. In each formal paper-log row, still record model/data versions, licenses, training compute, evaluation and limitations at the primary source. The bibliography includes resources as well as papers; resources must not be counted as trained-generative-model precedents.

Sources: [COSMOS](https://glycosmos.org/download), [COSLICENSE](https://glycosmos.org/license), [GTCODE](https://github.com/matsui-lab/GlycanGT), [GTARCH](https://zenodo.org/records/18636040), [ARRAY](https://glygen.ccrc.uga.edu/ggarray/)

## 46. Primary sources · 5/5

Clickable citations; full URLs and qualifications are in sources.md.

- **WORK:** glycowork maintained repository
- **RDKIT:** RDKit getting started and sanitization
- **BOJAR:** Daniel Bojar Group, University of Gothenburg
- **MATSUI:** Nagoya University: GlycanGT announcement (2026)
- **ERC:** University of Gothenburg: ERC grant for glycan research (2025)

These references are a reading and citation register, not a claim that the course’s full Appendix B audit has been completed. Older papers are retained when they establish essential prior art or measurement context. In each formal paper-log row, still record model/data versions, licenses, training compute, evaluation and limitations at the primary source. The bibliography includes resources as well as papers; resources must not be counted as trained-generative-model precedents.

Sources: [WORK](https://github.com/BojarLab/glycowork), [RDKIT](https://www.rdkit.org/docs/GettingStartedInPython.html), [BOJAR](https://www.gu.se/index.php/en/research/daniel-bojar), [MATSUI](https://www.nagoya-u.ac.jp/researchinfo/result/2026/04/ai-108.html), [ERC](https://www.gu.se/en/news/erc-grant-for-bojars-research-on-glycans)
