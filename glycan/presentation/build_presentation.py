"""Build the project proposal deck. All scientific diagrams are editable shapes."""
from pathlib import Path
import json
import zipfile
from xml.etree import ElementTree as ET
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

OUT = Path(__file__).resolve().parent
SOURCES = {
 'GUIDE': ('Course final-project guide', '../../Final Project Guide.pdf', 'Local supplied PDF; pp. 3–12 and appendices. Requirements, not empirical results.'),
 'DESC': ('Project problem description', '../glycan-problem-description.md', 'User-supplied proposal. Claims are qualified or corrected in the deck.'),
 'BRIEF': ('Glycan project brief', '../glycan_project.md', 'Workspace literature/data audit, 26 October 2026; historical file sizes are snapshot-specific.'),
 'GT': ('Kitani et al. GlycanGT. Bioinformatics (2026)', 'https://doi.org/10.1093/bioinformatics/btag147', 'Masked graph representation/completion; paper reports 83,739 pretraining glycans.'),
 'GTCODE': ('GlycanGT source and public processed data', 'https://github.com/matsui-lab/GlycanGT', 'Repository count 83,740; Apache-2.0 code. Data rights inherit their sources.'),
 'GTARCH': ('GlycanGT versioned source archive', 'https://zenodo.org/records/18636040', 'About 7.7 MB source ZIP, not a standalone training-data-size claim. Archived metadata previously audited as CC BY 4.0.'),
 'COSMOS': ('GlyCosmos downloads', 'https://glycosmos.org/download', 'Structure corpus; includes ambiguous records. October audit listing approximately 79.71 MB CSV; freeze exact release before training.'),
 'COSLICENSE': ('GlyCosmos official data license', 'https://glycosmos.org/license', 'CC BY 4.0 for copyrightable dataset content; checked at the primary page.'),
 'TOUCAN': ('GlyTouCan terms', 'https://doc.glytoucan.org/en/Terms-and-Conditions', 'CC0 registry; includes incompletely specified structures and overlaps GlyCosmos.'),
 'LO': ('Lundstrøm et al. LectinOracle. Advanced Science (2022)', 'https://doi.org/10.1002/advs.202103807', 'Binding prediction, not generation. Reports 564,647 protein–glycan interactions; not 564,647 unique glycans.'),
 'LOCODE': ('LectinOracle legacy repository', 'https://github.com/BojarLab/LectinOracle', 'Archived; points to maintained glycowork. MIT code does not settle all original measurement-data rights.'),
 'ARRAY': ('GlyGen Glycan Array Data Repository', 'https://glygen.ccrc.uga.edu/ggarray/', 'October workspace audit: 989 study/dataset collections, 533 glycans, CC BY 4.0. Full bulk export not verified; not used as a confirmed downloaded training table.'),
 'SWEETTALK': ('Bojar et al. Deep-Learning Resources for Studying Glycan-Mediated Host-Microbe Interactions. Cell Host & Microbe (2021)', 'https://doi.org/10.1016/j.chom.2020.10.004', 'Historical language modeling and property-guided local editing; no broad first-generator claim is warranted.'),
 'SWEETNET': ('Burkholz et al. Using graph convolutional neural networks to learn a representation for glycans. Cell Reports (2021)', 'https://doi.org/10.1016/j.celrep.2021.109251', 'Graph predictor and representation baseline, not a whole-tree generator.'),
 'BOLTZ': ('Yom et al. A Boltzmann model predicts glycan structures from lectin binding. Analytical Chemistry (2024)', 'https://doi.org/10.1021/acs.analchem.3c04992', 'Inverse identification from an experimental binding fingerprint; distinguish from designing new ligands for target sequences.'),
 'BART': ('Abtheen et al. Transformer-based Deep Learning for Glycan Structure Inference from Tandem Mass Spectrometry (2025 preprint)', 'https://doi.org/10.1101/2025.07.02.662857', 'Spectra-conditioned sequence generation; not a training baseline within the proposed budget.'),
 'BARTDATA': ('GlycoBART data release', 'https://zenodo.org/records/15741423', 'CC BY 4.0 release; paper describes 510,160 spectra and 3,590 identities before its filtering. Optional analytical context only.'),
 'AA': ('Xu et al. Modeling All-Atom Glycan Structures via Hierarchical Message Passing and Multi-Scale Pre-training (ICML 2025)', 'https://arxiv.org/abs/2506.01376', 'Representation learning, not evidence of whole-glycan functional generation.'),
 'ML': ('Xu et al. GlycanML: A Multi-Task and Multi-Structure Benchmark for Glycan Machine Learning (ICLR 2025)', 'https://arxiv.org/abs/2405.16206', 'Prediction benchmark; task code license does not establish every upstream data license.'),
 'CONTACT': ('Thomès et al. GlyContact analyzes glycan 3D structures at scale. Nature Communications (2025)', 'https://doi.org/10.1038/s41467-025-67590-y', 'Structural analysis and interaction modeling; illustrates continuing glyco-AI research.'),
 'CANDY': ('Urban et al. Predicting glycan structure from tandem mass spectrometry via deep learning. Nature Methods (2024)', 'https://doi.org/10.1038/s41592-024-02314-6', 'Analytical identification, not de novo ligand design.'),
 'GLYLES': ('Joeres et al. GlyLES. Journal of Cheminformatics (2023)', 'https://doi.org/10.1186/s13321-023-00704-0', 'Translator, not semantic/biosynthetic validator; published timing approximately 19 ms on its own corpus/hardware.'),
 'WORK': ('glycowork maintained repository', 'https://github.com/BojarLab/glycowork', 'MIT code; parsing, graphs, motif operations and models. Check source-specific data terms.'),
 'RDKIT': ('RDKit getting started and sanitization', 'https://www.rdkit.org/docs/GettingStartedInPython.html', 'BSD-3-Clause toolkit; sanitization does not prove synthesizability or function.'),
 'BENCH': ('Workspace validity benchmark', '../../tasks/validity_benchmark.json', 'Local CPU measurement, 22 October 2026; not a Colab benchmark. Mean 379.5 ms over 200 GlyLES→RDKit attempts.'),
 'SNA': ('Systematic synthesis of bisected N-glycans and unique recognitions by glycan-binding proteins. Chemical Science (2022)', 'https://doi.org/10.1039/D1SC05435J', 'Primary experimental context for SNA versus MAL-I and 6′/3′ sialyllactosamine recognition.'),
 'PLATFORM': ('Cross-platform comparison of glycan microarray formats (2014)', 'https://pubmed.ncbi.nlm.nih.gov/24658466/', 'Primary cross-platform study; presentation and assay context matter.'),
 'SIGLEC': ('An atlas of human siglecs integrates expression, affinity, and cis/trans sialoglycan recognition profiles. Nature Communications (2026)', 'https://doi.org/10.1038/s41467-026-71086-8', 'Functional recognition evidence; useful later biological extension, not the proposed cheap training baseline.'),
 'GALECTIN': ('Galectin-1, -2, and -3 exhibit differential recognition of sialylated glycans and blood group antigens (2008)', 'https://pubmed.ncbi.nlm.nih.gov/18216021/', 'Galectins recognize β-galactoside contexts; do not conflate them with sialic-acid-binding Siglecs.'),
 'BOJAR': ('Daniel Bojar Group, University of Gothenburg', 'https://www.gu.se/index.php/en/research/daniel-bojar', 'Institutional evidence of active glycan-focused machine learning research.'),
 'MATSUI': ('Nagoya University: GlycanGT announcement (2026)', 'https://www.nagoya-u.ac.jp/researchinfo/result/2026/04/ai-108.html', 'Institutional source verifies authors, structure-completion focus and publication.'),
 'ERC': ('University of Gothenburg: ERC grant for glycan research (2025)', 'https://www.gu.se/en/news/erc-grant-for-bojars-research-on-glycans', 'External funding and biological research demand; not proof of demand for any arbitrary generated structure.'),
}

SLIDES=[]
def add(title, subtitle, items=(), visual=None, refs=(), notes='', kind='standard'):
 SLIDES.append(dict(title=title,subtitle=subtitle,items=list(items),visual=visual,refs=list(refs),notes=notes,kind=kind))

add('Designing glycans\nfor a chosen lectin', 'A small-compute generative modeling proposal',
 [('WHOLE TREES','Generate new monosaccharide connectivity and linkage labels.'),('FUNCTIONAL CONDITION','Aim for a specified assay response; audit every claim.')], 'cover', ['DESC','GUIDE'],
 'This presentation follows the target-conditioned generation problem in the supplied glycan folder, rather than redefining the project as single-token completion. It is a proposal and evidence audit. No generator has been trained for this deck and no improved biological activity is claimed. The course guide requires measured feasibility before final topic acceptance. The full vision uses a target protein representation; the bounded pilot uses a small set of experimentally represented lectin IDs. This distinction is fundamental to keeping the scope honest.', 'cover')

add('The project in one sentence', 'Generate multiple valid glycan structures under a specified biological condition.',
 [('INPUT','Lectin identity + desired response class + optional motif.'),('OUTPUT','A complete, labelled glycan tree; branching is generated.'),('DELIVERABLE','A ranked, audited candidate set and a reproducible benchmark.')], 'task', ['DESC','BRIEF'],
 'The intended output is a carbohydrate chemical structure, not a protein binder, a property label or a completed fixed skeleton. A condition can be a target lectin identity with high/low normalized array-response bins. A structural motif can also be requested. New targets are not automatically supported: the small target-ID pilot only addresses lectins represented in the selected data. In a computer-only project, candidates remain hypotheses. Their value is a reproducible generation-and-audit method that could prioritize subsequent experiments.')

add('Glycans are recognition surfaces', 'Their biological meaning depends on both chemistry and presentation.',
 [('GLYCOCALYX','Glycoproteins and glycolipids display diverse glycan epitopes.'),('LECTINS','Carbohydrate-binding proteins recognize particular glycan contexts.'),('CONTEXT','Density, scaffold, accessibility and conformation influence recognition.')], 'cell', ['LO','CONTACT'],
 'The cell-surface illustration is schematic. Glycans can be linear or branched; this project restricts its output to connected tree-like structures supported by the chosen grammar. Recognition occurs at a three-dimensional interface even when the model uses a two-dimensional labelled graph. Display on a protein or membrane can make a major contribution. We therefore avoid assuming that a free glycan, an array-immobilized glycan and a densely displayed glycan have interchangeable activities.')

add('The structure is more than a sugar list', 'Node identity, bond chemistry and branching all carry information.',
 [('NODES','Gal, GlcNAc, Man, Fuc, Neu5Ac and other supported sugars.'),('EDGES','Anomeric configuration plus donor/acceptor carbon positions.'),('TOPOLOGY','The reducing-end root and nonreducing branches define the tree.')], 'symbols', ['GLYLES','DESC'],
 'Conventional SNFG-style icons are used throughout the deck: galactose is a yellow circle; mannose a green circle; GlcNAc a blue square; fucose a red triangle; Neu5Ac a purple diamond. A monosaccharide count cannot distinguish linkage isomers. Anomeric information is most naturally an edge/donor attribute; terminal reducing residues may have an unspecified anomeric state. The representation must preserve stereo- and linkage labels during canonicalization and comparison.')

add('One linkage can change recognition', 'A useful pilot contrasts related epitopes rather than arbitrary molecules.',
 [('MOTIF A','Neu5Ac(α2–6)Gal(β1–4)GlcNAc'),('MOTIF B','Neu5Ac(α2–3)Gal(β1–4)GlcNAc'),('PILOT TARGETS','SNA and a specified MAL-I preparation, subject to data coverage.')], 'linkages', ['SNA','PLATFORM'],
 'These are illustrative sialyllactosamine motifs, not generated results. Primary experimental studies show different recognition by SNA and MAL-I. Their preferences are context-dependent; the motif is not a sufficient universal binding rule. Maackia preparations and names vary, so match the precise reagent and metadata instead of merging every MAA/MAL label. The proposed target pair must be confirmed to have adequate overlapping glycans, usable assay metadata and suitable measurement-data reuse terms.')

add('Why design new glycan candidates?', 'Potential users need selectivity, interpretable probes and useful presentation.',
 [('RECOGNITION PROBES','Help experimentalists discriminate related lectin preferences.'),('DECOY CANDIDATES','Explore ligands that might compete with pathogen attachment.'),('IMMUNE GLYCOBIOLOGY','Investigate interactions involving Siglecs or galectins in later studies.')], 'applications', ['SIGLEC','GALECTIN','ERC'],
 'These applications motivate the field, but the proposed student study is not a therapeutic development program. Siglecs bind sialylated glycans; galectins recognize beta-galactoside contexts and should not be described as equivalent sialic-acid receptors. Binding may activate, cluster, inhibit or have no useful functional consequence depending on context. Antibody Fc engineering is also a meaningful glycan application, but it is a different design problem and is excluded from this pilot. The immediate output is an assay-aware candidate shortlist.')

add('Three tasks that must stay separate', 'Only the final column is this proposal’s central generative task.',
 [('COMPLETION','Recover missing sugar or linkage labels on a supplied structure.'),('IDENTIFICATION','Infer a glycan from spectra or an experimental binding fingerprint.'),('INVERSE DESIGN','Generate a whole structure for a requested target/property.')], None, ['GT','BART','BOLTZ'],
 'Masked prediction can be a generative training objective, but recovering one class label is not the same research question as designing whole new glycan topologies. Spectral generation is a genuine conditional-generation task whose condition is analytical evidence. A Boltzmann sampler that reconstructs structures from a binding fingerprint is relevant inverse-inference prior art. Neither should be presented as proof that protein-sequence-conditioned ligand design is already solved. This proposal trains a probability distribution over entire structure-building trajectories.')

add('A bounded, testable research question', 'Can constrained conditioning improve valid, novel yield at equal compute?',
 [('MAIN QUESTION','Does grammar-masked conditional generation outperform filtering?'),('BIOLOGICAL PILOT','One or two named lectins; assay-aware high/low response conditions.'),('SCOPE LIMIT','Small sugar vocabulary; bounded tree size; no new-target claim.')], 'tree', ['DESC','BRIEF'],
 'The proposed bound is 3–15 sugar residues for an initial pilot; these are design choices rather than dataset statistics. Start with common supported monosaccharides and explicitly listed linkages. The study compares a small conditional autoregressive generator, an unconditional generator followed by selection, and simple statistical/mutation baselines. If functional labels cannot be licensed, downloaded and validated, a motif-only task may remain possible but must be renamed and must not be represented as solved binding design.')

add('Formal problem: a distribution over trees', 'Learn a generator; use property scores as fallible evidence.',
 [('STRUCTURE','G = (V, E, sugar labels, linkage labels), rooted at the reducing end.'),('CONDITION','c = (lectin ID, response bin, optional motif).'),('GENERATOR','pθ(G | c) = ∏t pθ(action t | earlier actions, c).')], 'formula', ['DESC'],
 'A deterministic traversal gives each labelled tree a reproducible construction sequence. The decoder chooses sugar identity, parent attachment site, anomer and linkage, then branch/stop actions. Hard masks restrict the support of the distribution. The initial loss is conditional negative log-likelihood on eligible structures and measured-response bins. A guidance score can later combine predicted response, size and novelty penalties. A score threshold does not ensure experimental affinity, and ensemble variance is not a validity proof. No binding predictor needs to be differentiated through for the basic comparison.')

add('What does one training example mean?', 'Structure records and functional measurements are different data units.',
 [('STRUCTURE CORPUS','One canonical glycan tree; useful for learning chemical syntax.'),('FUNCTION TABLE','Glycan + lectin + response + assay/context metadata.'),('CRITICAL DISTINCTION','Many interaction rows can share the same small glycan library.')], 'array', ['LO','PLATFORM'],
 'Keep glycan identifiers, reagent/preparation, concentration, platform, linker, replicate and normalization information where available. The paper’s interaction count is not the number of independent molecules or independent wet-lab discoveries. An array records fluorescence or a normalized assay response; it is not automatically a dissociation constant. Treat high/low classes as within-context labels and retain continuous values. Every table needs explicit units, censoring and missing-value policies. Repeats must not leak across train and test.')

add('Structural data are small enough to inspect', 'A practical starting corpus is publicly available; usable counts require filtering.',
 [('GLYCANGT','83,739 pretraining glycans in the paper; 83,740 in the repository.'),('GLYCOSMOS','Public structures; source data CC BY 4.0.'),('DOWNLOAD SIZE','GlycanGT source archive ≈7.7 MB, including more than just training data.')], 'data', ['GT','GTCODE','GTARCH','COSLICENSE'],
 'The count discrepancy is one record and should be reported rather than hidden. These are source-release counts, not the count after our restricted grammar, size bounds, canonical deduplication and structural-family splitting. The October audit listed a GlyCosmos bulk CSV around 79.71 MB, but release sizes change. Registry resources overlap, so do not add counts from GlyTouCan and GlyCosmos. Download public training files rather than relying on gated model weights. Record exact bytes, release, checksum, schema and license at execution time.')

add('Binding data are the real bottleneck', 'Public files exist; reuse rights and target-specific coverage still decide feasibility.',
 [('LECTINORACLE','Paper reports 564,647 unique protein–glycan interactions.'),('GLYGEN ARRAY','An explicitly licensed portal is an alternative; bulk assembly remains to verify.'),('STOP CONDITION','No functional training until measurement-data rights and splits are settled.')], 'bottleneck', ['LO','LOCODE','ARRAY'],
 'The legacy LectinOracle repository is archived and points users to glycowork. MIT applies to code; it is not sufficient evidence that every original CFG/Imperial measurement has the same license. The previous workspace audit recorded around 12.76 MB for the main CSV, but that is not a newly downloaded verified file in this presentation. GlyGen portal counts refer to dataset collections, not individual measurements, and the full bulk export was not executed. These unresolved checks prevent an all-pass screening claim.')

add('Split by structure before any training', 'A random interaction-row split can make generalization look easier than it is.',
 [('CANONICALIZE','Unify branch order, sugar names, anomers and linkage labels.'),('GROUP','Put isomorphic glycans and close structural families in one group.'),('FREEZE','Use the same train/validation/test boundaries for predictors and generators.')], 'split', ['BRIEF','GUIDE'],
 'Hashing can efficiently bucket candidates, but exact labelled isomorphism resolves potential collisions. A four-iteration Weisfeiler–Lehman hash is not a family-distance metric. Family grouping needs a declared similarity such as common labelled subtree or motif similarity, with threshold sensitivity reported. No structure from an evaluation family should occur in unsupervised pretraining if the claim is generalization to unseen glycan families. For transfer to new lectins, add a separate protein-family holdout; this pilot does not make that claim.')

add('Why 100× compute cannot buy the labels', 'More sampled structures do not create new experimental interaction evidence.',
 [('CHEAP','Generate millions of plausible sequences or pseudo-labels.'),('EXPENSIVE','Measure binding under controlled presentation and assay conditions.'),('ARGUMENT','Compute can improve inference, but cannot establish unmeasured ground truth.')], 'scarcity', ['GUIDE','LO','PLATFORM'],
 'The course’s compute-invariance argument should be framed around functional measurements, not around the existence of glycan strings. A large structural corpus and synthetic examples can improve representation learning, so it would be wrong to claim that compute cannot help at all. The invariant is epistemic: predictions and simulations are not additional measured binding labels. If the final project becomes only a motif-label task where labels are computable, this particular scarcity argument weakens and topic qualification must be reconsidered.')

add('Prior work solves neighboring tasks', 'No “first glycan generator” claim is needed.',
 [('SweetTalk · 2021','Language modeling and property-guided local editing.'),('Boltzmann model · 2024','Candidate structures from measured lectin fingerprints.'),('GlycoBART · 2025','Glycan strings generated from MS/MS spectra.')], None, ['SWEETTALK','BOLTZ','BART'],
 'These are direct reasons to avoid saying the generative side is empty. The distinction is the condition, the output space and the evaluation protocol. SweetTalk is important historical prior art even though it predates the main 2022–2026 window. The Boltzmann approach uses experimental fingerprints to infer identities. GlycoBART performs analytical sequencing. None of these distinctions guarantees novelty of our entire proposed combination. A narrow reproducible gap must survive a full paper/config/code audit before being claimed.')

add('Predictors and completion models are tools', 'They support the pipeline but are not interchangeable with a whole-tree generator.',
 [('LectinOracle / SweetNet','Predict binding or learn glycan representations.'),('GlycanGT / GlycanAA','Masked recovery and representation/property learning.'),('GlycanML / GlyContact','Prediction benchmarks and structural analysis resources.')], None, ['LO','SWEETNET','GT','AA','ML','CONTACT'],
 'Predictive models can supply frozen scorers, encoders or diagnostic tests. Their performance does not certify a generator, and their training budgets are not automatically feasible student baselines. Do not fully retrain large models merely to claim a precedent. The selected generator is deliberately compact and new as an implementation; the course allows a new baseline if the pipeline is measured. A full literature log must identify data, code, compute, metrics and limitations for each relevant study, distinguishing paper verification from repository-only inference.')

add('The contribution is controlled generation', 'Two methodological levers, plus an audit that can falsify apparent gains.',
 [('LEVER 1','Mask chemically impossible actions during tree construction.'),('LEVER 2','Condition generation on target-specific response or motif requests.'),('AUDIT','Check whether gains survive independent scoring and near-neighbor analysis.')], 'levers', ['DESC','GUIDE'],
 'The empirical claim is modest: an improvement in valid, condition-compliant and non-memorized candidates at an equal compute and sampling budget. It does not require a state-of-the-art biological discovery claim. Independent scorers should differ in model family and ideally assay source; changing only random seeds yields correlated errors. The experiment can also be informative if scores fail to generalize: demonstrating failure under a stronger split is a valid critique when methods and evidence are documented.')

add('A small autoregressive tree generator', 'Train the generator; keep large protein encoders out of the critical path.',
 [('CONDITION ENCODER','A learned lectin-ID embedding plus response/motif flags.'),('DECODER','Proposed 2-layer GRU, hidden size 128; small action vocabulary.'),('STATE','Track open branches and occupied attachment positions.')], 'architecture', ['DESC','BRIEF'],
 'This is a proposed architecture, not a published timing result. A deterministic depth-first linearization still represents a non-grid chemical graph; the grammar operates on tree state rather than plain text syntax. A graph generator could be substituted later, but a compact GRU makes a low-compute baseline easier to implement. Parameter count depends on the final vocabulary and condition dimensions and must be measured. Protein-sequence conditioning is a later extension with cached embeddings; ESM-2 dimensions depend on the chosen variant and are not universally 1,280.')

add('Generation is a sequence of chemical decisions', 'The topology is built, not supplied as a fixed skeleton.',
 [('START','Choose a reducing-end residue and initialize the tree state.'),('GROW','Select parent/site, sugar, anomer and a compatible linkage.'),('BRANCH / STOP','Open or close a branch; stop within the size bound.')], 'actions', ['DESC'],
 'Every training glycan is serialized into an action sequence after canonicalization. Teacher forcing trains the decoder to assign probability to valid construction steps. During sampling, available actions depend on the state. A typical mask prevents a second attachment to an already occupied acceptor position, forbids a Neu5Ac donor linkage from carbon 1 and prevents syntactic branch mismatches. The initial grammar handles a restricted chemistry. Excluded modifications are a stated scope choice rather than evidence that the molecules are invalid in biology.')

add('Training does not require reinforcement learning', 'Establish conditional likelihood first; add guidance only if the scorer is credible.',
 [('PHASE A','Learn the structure distribution on the canonical corpus.'),('PHASE B','Fine-tune on eligible target/response-labelled examples.'),('PHASE C','Sample under constraints; compare simple reranking with conditioning.')], 'training', ['BRIEF'],
 'A neural binding predictor is not a prerequisite for structural pretraining or motif conditioning. Functional guidance, however, requires a predictor that first passes its own held-out test. Use measured labels for fine-tuning rather than pretending millions of pseudo-labelled glycans are new ground truth. For a fair baseline, include the same decoder trained without conditions, followed by the same selection budget. Reinforcement learning is optional and outside the minimum scope; it could add instability and consume the entire budget before basic comparisons are established.')

add('Validate the binding evaluator before guiding', 'A strong self-score is insufficient evidence of a useful generated structure.',
 [('FIT','Train a small motif/fingerprint or graph predictor on training families.'),('CHECK','Evaluate held-out ranking, calibration and simple motif baselines.'),('FREEZE','Use a separate locked evaluator to audit generator-selected candidates.')], 'scorer', ['LO','PLATFORM','GUIDE'],
 'The scorer predicts normalized assay response, not necessarily affinity. Establish whether the task is regression, within-array ranking or high/low classification before selecting metrics. Score all generator variants with the same evaluators. A model used to choose candidates is not an independent test of those candidates. Avoid tuning the generator on the test evaluator. A released LectinOracle checkpoint may include our evaluation glycans and therefore cannot be called independent without a training-provenance audit. If evaluator validity fails, stop functional claims.')

add('Uncertainty filters are useful, not proofs', 'Low disagreement can coexist with shared bias.',
 [('USEFUL SIGNAL','Flag candidates far from measured chemistry or with scorer disagreement.'),('FAILURE MODE','Several models may confidently share the same extrapolation error.'),('REPORT','Separate in-domain, uncertain and unsupported candidates.')], 'uncertainty', ['DESC','BRIEF'],
 'The supplied description said an ensemble variance threshold eliminates adversarial out-of-distribution artifacts. That guarantee is not justified. Ensembles may share data, architecture, featurization and errors. Use uncertainty to prioritize or abstain, inspect the effect of thresholds and report accepted yield as well as scores. A deliberately different evaluator and similarity-stratified analysis can expose some failures but do not substitute for measurements. It is also invalid to claim that high predicted binding ensures efficacy, therapeutic safety or biological selectivity.')

add('Validity has four distinct layers', 'Every accepted structure must pass the declared scope checks.',
 [('TREE + GRAMMAR','Connected, acyclic, supported sugar/linkage labels; no occupied-site conflict.'),('ATOM-LEVEL CHECK','Faithful GlyLES conversion followed by RDKit sanitization.'),('BIOLOGY + FUNCTION','Biosynthesis, synthesis and binding require additional evidence.')], 'validity', ['GLYLES','WORK','RDKIT'],
 'Layer one is the project-specific structural checker. Layer two includes conversion coverage, warnings and atom-level checks. GlyLES explicitly does not perform semantic glycan validation, so a successful translation is not a complete biochemical certificate. Treat ignored modifications as unsupported rather than silently deleting them. A grammar can enforce a restricted structural language, but it cannot guarantee that a glycosyltransferase pathway or synthetic route exists. Layer four is functional confirmation; a binding surrogate only supplies a proxy. Report each layer separately, not one ambiguous validity percentage.')

add('Novelty must survive structural comparison', 'A new string can encode an old glycan—or a one-step copy.',
 [('EXACT COPIES','Canonical labelled-tree identity; hash buckets plus isomorphism.'),('NEAR COPIES','Nearest labelled subtree/motif similarity and edit-distance diagnostics.'),('DISCLOSURE','Publish the nearest training neighbors for selected candidates.')], 'neighbors', ['GUIDE','BRIEF'],
 'Use graph attributes for sugar identity, anomer, donor/acceptor sites and modifications. Branch reordering must not count as novelty. Hash inequality or equality alone is not a universal chemical proof: verify the canonicalization implementation and handle collisions. For near-duplicate analysis, state the chosen distance, normalization and threshold. A small subset can use exact tree-edit distances; a scalable motif/subtree index can screen the full corpus. Visual nearest-neighbor tables make copying easy to inspect. Separately check overlap with predictor training data.')

add('Evaluate joint success, not a single score', 'A useful candidate must clear several tests simultaneously.',
 [('STRUCTURE','Grammar pass, conversion coverage, uniqueness and size distribution.'),('CONTROL','Requested motif rate and held-out response-ranking performance.'),('GENERALIZATION','Exact-copy rate, nearest-neighbor distance and evaluator agreement.')], 'metrics', ['GUIDE','BRIEF'],
 'Define audited yield as the number of generated samples that are structurally valid, condition-compliant, unique and outside a predeclared near-copy threshold, divided by the number sampled. Functional criteria remain proxy criteria unless measured. For prediction use metrics appropriate to the label, such as Spearman ranking or AUPRC for imbalanced classes; estimate uncertainty with family-level resampling. Count invalid and rejected outputs rather than dropping them from every denominator. Match number of samples and oracle calls between methods. Report distributions, not only best examples.')

add('A small experiment matrix isolates the levers', 'Use the same decoder, split, sampling budget and evaluation procedure.',
 [('B0 · SIMPLE','Markov/tree sampler and seed-mutation search.'),('B1 · NEURAL','Unconditional GRU + post-filtering / reranking.'),('B2–B4 · ABLATIONS','Conditional; grammar-masked; conditional + grammar-masked.')], 'matrix', ['GUIDE','SWEETTALK','BOLTZ'],
 'B0 is a conceptual baseline inspired by historical statistical/editing methods, not a claim of exact paper reproduction without source code. The 2×2 neural design crosses conditioning on/off with grammar masking on/off. The unconditional row still has access to the same reranker when the comparison is filter versus condition. This separates conditioning benefit from the benefit of rejection. Use paired seeds where budget permits. If the four-hour envelope cannot cover the required comparisons, reduce corpus size, epochs and sample count uniformly before expanding to additional methods.')

add('What would count as a good result?', 'Pre-register the decision rules; do not invent success percentages.',
 [('MODEL RESULT','Higher audited yield than equal-budget baselines, with uncertainty.'),('SCIENTIFIC RESULT','Explain whether improvements survive stronger splits and independent scoring.'),('NEGATIVE RESULT','Document when high self-scores disappear under the audit.')], 'results', ['GUIDE'],
 'No result bars appear here because experiments have not been run. The presentation is a Phase 1 proposal. Pre-register any minimum practical improvement and near-copy threshold after inspecting validation data, before opening the test set. A negative outcome can be useful: for example, the generator increases its own binding predictor’s score but loses that gain on a separate evaluator. Biological claims remain limited to the evidence available. The goal is a defensible empirical paper, not a promise of a new drug or a universal glycan designer.')

add('The smoke test is the admission ticket', 'The course requires measurements on the intended student platform.',
 [('SETUP','Fresh Colab/Kaggle session; install + fetch + load in under 5 minutes.'),('TRAIN','50 steps / one epoch; record hardware, VRAM and step time.'),('CHECK','100+ structures; time parser, semantic checks, conversion and scorer.')], 'smoke', ['GUIDE'],
 'A small dataset and model are not enough to assert feasibility. The guide requires a fresh-session setup measurement, a 12–16 GB memory micro-batch test and a training-time projection. Exclude notebook warmup and include data loading transparently. Time at least 100 samples for checkers and report mean, median, p95 and failure counts, because unsupported candidates can dominate cost. No Colab smoke test has been run in preparing this deck. Admission remains pending until these measurements and data-rights checks are complete.')

add('A four-GPU-hour envelope—not a benchmark', 'Proposed allocation; update it using measured throughput.',
 [('TRAIN + COMPARE','2.0 h generator comparisons + 0.5 h predictor fitting.'),('EVALUATE','0.5 h sampling/evaluation + 1.0 h contingency.'),('CPU WORK','Parsing and conversion also consume session wall time.')], 'budget', ['GUIDE','BENCH'],
 'These are proposed allocations summing to four GPU-hours, not measured or paper-reported runtimes. CPU-only work may use no GPU time while still keeping a Colab session busy. The saved local checker benchmark measured 200 GlyLES-to-RDKit attempts, mean about 380 ms and 182 parseable conversions, on an Intel i3 laptop. Some failures were compatibility/coverage issues and some warnings indicated ignored modifications; conversion success is not full semantic validity. This evidence does not establish training time, setup time or fresh Colab speed. Use a small corpus and low sampling count if projections exceed the envelope.')

add('Four weeks, with a decision at each boundary', 'Every week produces a reviewable artifact.',
 [('WEEK 1','Freeze data, licenses, grammar and split; pass the smoke test.'),('WEEKS 2–3','Train baselines; integrate conditions, masks and audit tables.'),('WEEK 4','Run bounded ablations; publish reproducible results and limitations.')], 'timeline', ['GUIDE'],
 'Map the implementation to course Weeks 16–19: Week 16 produces the setup and W&B artifacts; Week 17 trains the baseline and records convergence/system logs; Week 18 integrates checkers and memorization tables; Week 19 adds the extension, completes ablations and publishes the interactive report. Stop expanding scope if Week 1 cannot establish the functional data pipeline. A motif-only fallback is technically possible but changes the scientific claim and may weaken the measurement-scarcity argument. Do not quietly relabel it as binding design.')

add('W&B records evidence, not just loss curves', 'The guide requires artifacts, system logs and a public interactive report.',
 [('ARTIFACTS','Raw snapshot, preprocessing manifest, split IDs and checkpoints.'),('RUN LOGS','Seed/config, loss, wall time, VRAM and validity metrics.'),('SAMPLE TABLE','Generated tree, condition, scores, rejection reason and nearest neighbor.')], 'tracking', ['GUIDE'],
 'The sample table must make a generated candidate traceable to its model version, training split and evaluation procedure. Keep failures and rejected candidates. Logs should distinguish training scorer, independent evaluator and structural checker. Version dataset licenses and any filtering policy alongside data artifacts. The course expects an interactive W&B Report and a live ten-minute code/dashboard defense. Access to W&B is experiment tracking infrastructure, not a hidden prerequisite for downloading the scientific dataset. Never upload tokens or original restricted data to public reports.')

add('Relevance in 2026: active, specialized research', 'The application is credible; publication growth needs a separate count audit.',
 [('GOTHENBURG','Bojar Lab: glycan ML, interactions and structural analysis.'),('NAGOYA / iGCORE','Matsui Lab: graph representations and completion.'),('RECENT TRAJECTORY','CandyCrunch 2024 → GlyContact 2025 → GlycanGT 2026.')], 'research', ['BOJAR','MATSUI','CANDY','CONTACT','GT','ERC'],
 'These are examples of continuing methodological development, not counts showing annual growth in a single narrowly defined literature. R1 is supported by official institutional pages, and R2 by the cited venues. R4 is supported by biological questions and funded glycoscience programs. R3 remains partially established because a screened, deduplicated publication corpus for 2023–2026 has not been assembled. H2 is also uncertain: academic concentration does not prove low crowding or eliminate commercial interest. Large generative chemistry models are not the intended competitive benchmark for this four-week study.')

add('Headroom: constraint control and evaluation', 'The strongest gap is a bounded empirical question, not an absence claim.',
 [('H1 · HEADROOM','Quantify validity/control trade-offs rather than assuming unsaturated SOTA.'),('H2 · CROWDING','Specialized academic work is visible; low scooping risk is unproven.'),('H3 · AUDIT','Test proxy exploitation and near-copy dependence explicitly.')], 'headroom', ['GUIDE','BRIEF'],
 'There is no verified universal claim that no whole-tree protein-conditioned generator exists. The narrow proposal may still be useful if it measures a poorly characterized trade-off at student compute scale. Treat hypotheses about predictor exploitation as things to test, not accusations against papers that were not fully audited. Good critique is operational: define the condition, build leakage-resistant splits, use independently trained evaluators, publish nearest neighbors, and reveal how much apparently strong performance comes from memorization or familiar motifs.')

add('All eight course gates: a candid status', 'The topic is not fully qualified until the pending evidence is measured.',
 [('SUPPORTED','Structured output; natural conditional generation; two methodological levers.'),('CONDITIONAL','Scarcity argument; validity implementation; licensed functional data; copy audit.'),('PENDING','Fresh-platform setup, end-to-end timing and memory test.')], 'gates', ['GUIDE','BRIEF'],
 'Gate 1 passes in formulation because the output is a labelled tree. Gate 2 is supported only if functional measurement scarcity remains central. Gate 3 passes as a conditional generative formulation. Gate 4 requires implementing and benchmarking a composite checker rather than merely naming libraries. Gate 5 has at least conditioning and grammar constraints. Gate 6 passes for a structural corpus but the functional-label license/export is unresolved. Gate 7 is not measured. Gate 8 has an algorithmic plan but no executed audit. Since the guide requires all eight, do not describe the project as fully accepted yet.')

add('The five risks that can change the project', 'Each has an explicit action rather than a hidden assumption.',
 [('DATA / PREDICTOR','Unclear rights or weak held-out predictor → stop functional guidance.'),('COMPUTE / COVERAGE','Over budget or unsupported chemistry → shrink scope and remeasure.'),('MEMORIZATION','Near-copy dependence → stronger splits, simple baselines and revised claims.')], 'risks', ['BRIEF','GUIDE'],
 'Additional biological risks include array-to-solution transfer, effects of multivalency, unknown synthesis feasibility and target-context mismatch. Removing unsupported sugars changes the domain and should be quantified. An unreliable predictor cannot be rescued merely by a more powerful generator. A training model that fits in memory may still be too slow end-to-end. The fallback motif task is a distinct claim and should be requalified against the course’s measurement-bound focus. These are limitations of the proposed evidence, not reasons to imply that glycan research lacks real-world importance.')

add('The full vision is larger than the pilot', 'Keep target-sequence conditioning as a separately tested extension.',
 [('PILOT','Target ID + response class; generate whole trees in a narrow domain.'),('EXTENSION','Cache protein embeddings; condition across sufficiently sampled targets.'),('NEW CLAIM','Unseen-lectin transfer requires protein-family holdout and enough labels.')], 'scope', ['DESC','LO'],
 'The original description assumes a 200-amino-acid lectin domain and 1,280-dimensional ESM-2 embedding. Neither is universal: lectin architectures vary and embeddings depend on the encoder variant. In the pilot there is no expensive end-to-end protein-model training. If cached embeddings are added, count their extraction/setup costs and confirm rights and split boundaries. Conditioning on a sequence does not demonstrate generalization to a new target. This extension is excluded unless the core model, data and budget tests are already complete.')

add('The decision to defend', 'Proceed with functional generation only after the first-week evidence gates pass.',
 [('WHAT WE BUILD','A small, conditional whole-tree generator with chemical action masks.'),('WHAT WE TEST','Valid, controlled, novel yield under stronger splits and independent scoring.'),('WHAT WE CLAIM','Computational candidate-design evidence; biological function remains unverified.')], 'closing', ['DESC','GUIDE'],
 'The project is worth pursuing if a suitable measured functional table can be licensed and assembled, a simple evaluator generalizes beyond trivial motif recognition, and the smoke test fits the compute envelope. Otherwise, redesign the scientific task explicitly rather than forcing a falsely qualified result. The contribution is a reproducible constrained generative-modeling study. The final research package should include source audits, honest negative results, all baselines and a readable candidate table. No generated structure is a validated ligand merely because it passes grammar checks.')

add('Appendix A · Guide-to-deck mapping', 'This presentation explains the plan; it does not replace the required report.',
 [('PHASE 1 · 60%','8–10 page two-column proposal; formalism, qualification and peer response.'),('PHASE 2 · 40%','Code, trained baselines, checker/memorization audit, W&B report and defense.'),('STILL REQUIRED','15+ audited papers; empirical smoke test; appendices A–D and AI audit log.')], None, ['GUIDE'],
 'Course sections map to this deck as follows: domain mechanics and introduction are slides 3–6; formalism slides 8–10 and 18–20; related work slides 15–16; qualification/scarcity slides 14 and 34; evaluation slides 21–27; smoke test and execution slides 28–31; risks and limitations slides 33–36. Slide positions may be read from the generated notes. The supplied guide also specifies peer review with at least three citation/link spot checks, an author response, a 15+ paper log and a separate AI usage/verification appendix. None of those is marked complete merely because the presentation exists.')

add('Appendix B · Corrections to the source draft', 'Preserve the idea; remove guarantees the evidence does not support.',
 [('NO UNIVERSAL FIRST','Replace “no glycan generators” with a narrow audited gap.'),('NO FUNCTION GUARANTEE','Array score ≠ affinity; ensemble agreement ≠ binding proof.'),('NO HASH GUARANTEE','WL hashing helps deduplication; it does not certify family novelty.')], None, ['DESC','BRIEF','GLYLES','LO'],
 'Other corrections: not all glycans are branched; tree-only topology is a chosen scope. Do not present the average of 7.1 residues or 91 heavy atoms as universal facts without its original dataset. Galectin-3 is not a Siglec-like sialic-acid receptor. Omit the unsupported percentage of therapeutic monoclonal antibodies. A 7.7 MB repository archive is not a pure training-data file. Code licenses do not automatically cover source measurements. The published GlyLES timing is not the workspace’s measured timing. Hardware performance targets and method improvements are proposals, not results.')

add('Appendix C · Data and checker ledger', 'Provenance matters more than a large headline row count.',
 [('CONFIRMED SOURCE CLAIMS','83,739 glycans in GlycanGT; 564,647 interactions in LectinOracle.'),('HISTORICAL LOCAL MEASUREMENT','200 conversion attempts: mean ≈380 ms on an Intel i3 CPU.'),('NOT YET MEASURED','Eligible target rows; clean split sizes; setup; T4 training and evaluator speed.')], None, ['GT','LO','BENCH','BRIEF'],
 'The local benchmark succeeded in producing parseable molecules for 182 of 200 attempts. The remaining cases cannot be equated with invalid biology because notation/version compatibility contributes. Some conversions issued ignored-modification warnings, so success does not imply faithful full chemistry. The original GlyLES benchmark reported about 19 ms per supported glycan on different hardware. The raw file-size figures in the workspace brief are snapshots; the plan requires fresh exact bytes and checksums. Record source data rights, source URL, retrieval date, filtering code and a reproducible count at every stage.')

add('Appendix D · Glossary and claim boundaries', 'Definitions used consistently throughout the proposal.',
 [('GLYCAN / LECTIN','A carbohydrate structure / a carbohydrate-binding protein.'),('RFU / AFFINITY','Assay fluorescence / a thermodynamic binding quantity; not interchangeable.'),('NOVEL / FUNCTIONAL','Structurally distinct / experimentally active; separate claims.')], None, ['LO','GLYLES','PLATFORM'],
 'Other useful definitions: anomer describes configuration at the anomeric center; linkage specifies donor and acceptor positions; motif is a labelled substructure; glycoform is a particular glycosylated molecular form; canonicalization maps equivalent representations to a consistent representation; conditional generation samples structures given a requested context; a surrogate is a model predicting a measured quantity; a held-out family is a predeclared structural group excluded from fitting; abstention means refusing to trust a proxy outside its supported domain. These definitions prevent the scientific claim from expanding beyond available evidence.')

# References stay readable; all slide citations also hyperlink to the source register.
for idx, keys in enumerate([
 ['GT','LO','SWEETTALK','SWEETNET','BOLTZ'],
 ['BART','AA','ML','CONTACT','CANDY'],
 ['GLYLES','SNA','PLATFORM','SIGLEC','GALECTIN'],
 ['COSMOS','COSLICENSE','GTCODE','GTARCH','ARRAY'],
 ['WORK','RDKIT','BOJAR','MATSUI','ERC'],
]):
 add(f'Primary sources · {idx+1}/5', 'Clickable citations; full URLs and qualifications are in sources.md.',
     [(k,SOURCES[k][0]) for k in keys],None,keys,
     'These references are a reading and citation register, not a claim that the course’s full Appendix B audit has been completed. Older papers are retained when they establish essential prior art or measurement context. In each formal paper-log row, still record model/data versions, licenses, training compute, evaluation and limitations at the primary source. The bibliography includes resources as well as papers; resources must not be counted as trained-generative-model precedents.',kind='references')

COL={'bg':'101C2D','panel':'1A2A40','panel2':'213650','ink':'F4F7FA','muted':'B7C6D6','teal':'4DE0C1','blue':'75B6FF','orange':'FFB970','red':'FF7F84','line':'516780','white':'FFFFFF'}
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
FONT='DejaVu Sans'; DISPLAY='DejaVu Sans'
def rgb(c): return RGBColor.from_string(COL.get(c,c))
def shape(sl,x,y,w,h,fill='panel',typ=MSO_SHAPE.ROUNDED_RECTANGLE,line=None):
 s=sl.shapes.add_shape(typ, Inches(x), Inches(y), Inches(w), Inches(h));s.fill.solid();s.fill.fore_color.rgb=rgb(fill)
 s.line.fill.background() if line is None else None
 if line:s.line.color.rgb=rgb(line)
 if typ==MSO_SHAPE.ROUNDED_RECTANGLE:
  try:s.adjustments[0]=0.12
  except Exception:pass
 return s
def tx(sl,text,x,y,w,h,size=22,color='ink',bold=False,align=None):
 s=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=s.text_frame;tf.clear();tf.word_wrap=True
 tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
 for i,line in enumerate(text.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.font.name=FONT;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=rgb(color)
  p.space_after=Pt(6)
  if align is not None:p.alignment=align
 return s
def line(sl,x1,y1,x2,y2,color='line',width=2):
 s=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2));s.line.color.rgb=rgb(color);s.line.width=Pt(width);return s
def pill(sl,text,x,y,w,color='teal'):
 shape(sl,x,y,w,.34,fill='panel2');tx(sl,text,x+.09,y+.045,w-.18,.24,10,color,True)
def arrow(sl,x,y,w=.48,h=.28):shape(sl,x,y,w,h,'teal',MSO_SHAPE.RIGHT_ARROW)
SUG={'Gal':('FFD447',MSO_SHAPE.OVAL),'Man':('59BD63',MSO_SHAPE.OVAL),'Glc':('238CE6',MSO_SHAPE.OVAL),'GlcNAc':('238CE6',MSO_SHAPE.RECTANGLE),'GalNAc':('FFD447',MSO_SHAPE.RECTANGLE),'Fuc':('F05A62',MSO_SHAPE.ISOSCELES_TRIANGLE),'Neu5Ac':('B891EE',MSO_SHAPE.DIAMOND)}
def sugar(sl,name,x,y,r=.18,label=False):
 fill,typ=SUG[name];shape(sl,x-r,y-r,2*r,2*r,fill,typ,line='white')
 if label:tx(sl,name,x-.46,y+r+.08,.92,.34,12,align=PP_ALIGN.CENTER)
def glycan(sl,x,y,w=4.7,h=2.8,cap=True,labels=False):
 p=[(.94,.5,'GlcNAc'),(.77,.5,'GlcNAc'),(.60,.5,'Man'),(.44,.22,'Man'),(.44,.78,'Man'),(.28,.22,'GlcNAc'),(.28,.78,'GlcNAc'),(.12,.22,'Gal'),(.12,.78,'Gal')]
 edges=[(0,1),(1,2),(2,3),(2,4),(3,5),(4,6),(5,7),(6,8)]
 for a,b in edges:line(sl,x+p[a][0]*w,y+p[a][1]*h,x+p[b][0]*w,y+p[b][1]*h,'muted',2)
 for u,v,n in p:sugar(sl,n,x+u*w,y+v*h,.145)
 if cap:
  line(sl,x+.12*w,y+.22*h,x-.03*w,y+.22*h,'muted',2);sugar(sl,'Neu5Ac',x-.03*w,y+.22*h,.17)
 if labels:tx(sl,'reducing end',x+.68*w,y+.57*h,1.4,.3,11,'muted')
def boxlabel(sl,title,body,x,y,w,h=1.05,color='teal'):
 shape(sl,x,y,w,h);tx(sl,title,x+.16,y+.12,w-.32,.29,13,color,True);tx(sl,body,x+.16,y+.47,w-.32,h-.5,17)
def smallflow(sl,labels,x,y,w=5.1):
 n=len(labels);bw=w/n-.12
 for i,l in enumerate(labels):
  shape(sl,x+i*w/n,y,bw,.88,'panel2');tx(sl,l,x+i*w/n+.07,y+.22,bw-.14,.58,14,align=PP_ALIGN.CENTER)
  if i<n-1:arrow(sl,x+(i+1)*w/n-.1,y+.32,.18,.18)
def diagram(sl,kind,x=7.05,y=2.0,w=5.55,h=4.5):
 if kind in ('cover','tree','task','closing','scope'):
  glycan(sl,x+.35,y+.55,w-1,2.9,labels=True)
  pill(sl,'ILLUSTRATIVE GLYCAN TREE',x+.4,y+.05,3.0)
  if kind=='task':smallflow(sl,['condition','generator','candidates'],x+.15,y+3.5,w-.2)
  elif kind=='scope':smallflow(sl,['target ID','whole tree','sequence later'],x+.1,y+3.5,w-.1)
  else:tx(sl,'Sugar identities + linkages + branches',x+.1,y+3.7,w-.1,.6,16,'muted')
 elif kind=='cell':
  shape(sl,x,y+3.2,w,.55,'panel2',MSO_SHAPE.RECTANGLE)
  for i in range(3):
   xx=x+.85+i*1.7
   shape(sl,xx-.12,y+2.8,.24,.9,'blue')
   line(sl,xx,y+2.8,xx,y+1.9,'muted',2)
   sugar(sl,'GlcNAc',xx,y+2.48,.14);sugar(sl,'Gal',xx,y+2.0,.14)
   line(sl,xx,y+2.0,xx-.38,y+1.5,'muted',2);sugar(sl,'Neu5Ac',xx-.38,y+1.5,.16)
  shape(sl,x+1.1,y+.35,1.2,.7,'orange',MSO_SHAPE.CLOUD)
  tx(sl,'lectin',x+2.55,y+.55,1.5,.35,17,'orange');line(sl,x+2.3,y+.75,x+2.5,y+.75,'orange')
  tx(sl,'membrane / protein or lipid scaffold',x+.2,y+3.95,w-.4,.45,15,'muted')
 elif kind=='symbols':
  for i,n in enumerate(['Gal','GlcNAc','Man','Fuc','Neu5Ac','GalNAc']):
   xx=x+.85+(i%3)*1.7;yy=y+.7+(i//3)*1.55;sugar(sl,n,xx,yy,.28,True)
  tx(sl,'Conventional SNFG-style symbols',x+.3,y+3.9,w-.6,.5,16,'muted')
 elif kind=='linkages':
  for row,linkname in enumerate(['α2–6','α2–3']):
   yy=y+1+row*1.65
   line(sl,x+.8,yy,x+2.5,yy,'muted');line(sl,x+2.5,yy,x+4.25,yy,'muted')
   for n,xx in [('Neu5Ac',x+.8),('Gal',x+2.5),('GlcNAc',x+4.25)]:sugar(sl,n,xx,yy,.25)
   tx(sl,linkname,x+1.25,yy-.55,1.2,.35,19,'orange',True);tx(sl,'β1–4',x+3.0,yy-.55,1.15,.35,18)
  tx(sl,'Same residues. Different recognition context.',x+.1,y+3.9,w-.1,.55,15,'muted')
 elif kind=='applications':
  for i,(a,b) in enumerate([('01','Analytical recognition'),('02','Candidate decoys'),('03','Mechanistic probes')]):
   shape(sl,x+.1,y+.2+i*1.25,.7,.7,'panel2',MSO_SHAPE.OVAL);tx(sl,a,x+.22,y+.36+i*1.25,.5,.3,17,'teal',True)
   tx(sl,b,x+1.05,y+.38+i*1.25,w-1.1,.65,21)
  tx(sl,'Applications require experimental confirmation.',x+.1,y+4.1,w-.1,.45,14,'muted')
 elif kind=='formula':
  shape(sl,x+.05,y+.5,w-.1,1.45,'panel2');tx(sl,'pθ(G | c)',x+.3,y+.72,w-.6,.6,42,'teal',True,PP_ALIGN.CENTER)
  tx(sl,'whole tree  |  requested condition',x+.25,y+1.43,w-.5,.4,16,'muted',align=PP_ALIGN.CENTER)
  smallflow(sl,['valid actions','sample','grow tree'],x+.1,y+2.65,w-.2)
  tx(sl,'PROPOSED FORMULATION',x+.4,y+3.9,w-.8,.4,12,'orange',True)
 elif kind in ('array','data','bottleneck'):
  if kind=='array':
   for row in range(4):
    for col in range(6):
     colors=['panel2','panel2','teal','blue','orange'];color=colors[(row*3+col*2)%5]
     shape(sl,x+.45+col*.78,y+.5+row*.68,.27,.27,color,MSO_SHAPE.OVAL)
   tx(sl,'Each spot is an assay context, not a Kd.',x+.1,y+3.7,w-.1,.6,17,'muted')
  else:
   a='STRUCTURES' if kind=='data' else 'INTERACTION ROWS';b='83,739' if kind=='data' else '564,647'
   tx(sl,b,x+.2,y+.7,w-.4,1,53,'teal',True,PP_ALIGN.CENTER);tx(sl,a,x+.2,y+1.85,w-.4,.5,15,'muted',True,PP_ALIGN.CENTER)
   tx(sl,'paper-reported count; not the final pilot dataset',x+.2,y+2.65,w-.4,.9,17,'muted',align=PP_ALIGN.CENTER)
 elif kind=='split':
  for i,(n,col) in enumerate([('TRAIN','teal'),('VALIDATION','blue'),('TEST','orange')]):
   shape(sl,x+.1+i*1.82,y+.8,1.55,2.4,'panel2');tx(sl,n,x+.2+i*1.82,y+1.02,1.35,.4,12,col,True,PP_ALIGN.CENTER)
   for k in range(3):sugar(sl,'Man' if i!=2 else 'Gal',x+.55+i*1.82+(k%2)*.55,y+1.85+(k//2)*.65,.16)
  tx(sl,'Families stay together across all models.',x+.1,y+3.7,w-.1,.65,17,'muted')
 elif kind=='scarcity':
  tx(sl,'100×',x+.2,y+.65,w-.4,1.2,68,'teal',True,PP_ALIGN.CENTER)
  tx(sl,'more compute',x+.2,y+1.85,w-.4,.5,23,align=PP_ALIGN.CENTER)
  tx(sl,'≠',x+.2,y+2.45,w-.4,.8,40,'orange',True,PP_ALIGN.CENTER)
  tx(sl,'new measured binding labels',x+.1,y+3.45,w-.2,.7,21,align=PP_ALIGN.CENTER)
 elif kind in ('levers','architecture','training','scorer','tracking','smoke'):
  maps={
   'levers':[('01','Condition'),('02','Constrain'),('03','Audit')],
   'architecture':[('c','ID + response + motif'),('GRU','2 layers · hidden 128'),('STATE','Attachment sites + branches')],
   'training':[('A','Structure pretraining'),('B','Conditional fine-tuning'),('C','Constrained sampling')],
   'scorer':[('FIT','Training structures'),('FREEZE','Validated evaluator'),('AUDIT','Held-out / independent scores')],
   'tracking':[('DATA','Versioned artifacts'),('RUN','Training + system metrics'),('REPORT','Samples + nearest neighbors')],
   'smoke':[('<5 min','Fresh setup'),('50 steps','Memory + throughput'),('100+','Checker timing samples')]}
  for i,(a,b) in enumerate(maps[kind]):
   shape(sl,x+.15,y+.15+i*1.35,w-.3,1.0,'panel2');tx(sl,a,x+.33,y+.34+i*1.35,1.1,.5,17,'teal',True);tx(sl,b,x+1.55,y+.34+i*1.35,w-1.9,.65,17)
 elif kind=='actions':
  for i,a in enumerate(['ROOT','ATTACH','BRANCH','STOP']):
   boxlabel(sl,a,['initialize','choose sugar + site','grow another arm','finish structure'][i],x+(i%2)*2.8,y+.3+(i//2)*1.85,2.5,1.45)
 elif kind=='uncertainty':
  for i,a in enumerate(['scorer A','scorer B','scorer C']):
   boxlabel(sl,a,'high score',x+.1,y+.1+i*1.15,2.1,.94)
  tx(sl,'Shared bias?',x+2.65,y+1.12,2.4,.6,26,'orange',True)
  tx(sl,'agreement ≠ evidence of binding',x+.1,y+3.9,w-.1,.6,18,'muted')
 elif kind=='validity':
  labels=[('01','Tree / grammar','teal'),('02','Faithful atom mapping','blue'),('03','Synthesis / biosynthesis','orange'),('04','Biological function','red')]
  for i,(a,b,c) in enumerate(labels):
   shape(sl,x+.15+i*.16,y+.15+i*1.05,w-.3-i*.32,.84,'panel2');tx(sl,a+'  '+b,x+.32+i*.16,y+.38+i*1.05,w-.65-i*.32,.45,17,c,True)
 elif kind=='neighbors':
  glycan(sl,x+.4,y+.0,w-1,1.8,cap=True)
  glycan(sl,x+.4,y+2.15,w-1,1.8,cap=False)
  tx(sl,'candidate vs nearest training neighbor',x+.2,y+4.1,w-.4,.4,15,'muted')
 elif kind=='metrics':
  for i,(a,c) in enumerate([('VALID','teal'),('CONTROLLED','blue'),('UNIQUE','orange'),('NOT A NEAR COPY','teal')]):
   shape(sl,x+.1,y+.12+i*1.05,w-.2,.78,'panel2');tx(sl,a,x+.35,y+.33+i*1.05,w-.7,.4,18,c,True)
 elif kind=='matrix':
  tx(sl,'NO MASK',x+1.4,y+.08,1.7,.4,13,'muted',True);tx(sl,'MASK',x+3.5,y+.08,1.7,.4,13,'muted',True)
  for row in range(2):
   tx(sl,['UNCOND.','COND.'][row],x+.05,y+1+row*1.55,1.1,.55,12,'muted',True)
   for col in range(2):
    shape(sl,x+1.3+col*2.1,y+.65+row*1.55,1.88,1.25,'panel2');tx(sl,f'B{1+row+2*col}',x+1.55+col*2.1,y+.98+row*1.55,1.4,.5,28,'teal',True,PP_ALIGN.CENTER)
  tx(sl,'+ simple statistical / mutation baselines',x+.1,y+4.1,w-.1,.4,15,'muted')
 elif kind=='results':
  tx(sl,'No results\ninvented.',x+.3,y+.9,w-.6,1.9,45,'teal',True)
  tx(sl,'The contribution must survive the audit.',x+.3,y+3.4,w-.6,.9,23,'muted')
 elif kind=='budget':
  vals=[(2.,'Generators','teal'),(.5,'Predictor','blue'),(.5,'Evaluation','orange'),(1.,'Contingency','line')];xx=x+.1
  for value,label,c in vals:
   ww=(w-.2)*value/4;shape(sl,xx,y+1,ww,1.05,c,MSO_SHAPE.RECTANGLE);xx+=ww
  tx(sl,'4 GPU-hours',x+.1,y+2.45,w-.2,.8,40,'teal',True,PP_ALIGN.CENTER)
  tx(sl,'PROPOSED ALLOCATION · NOT MEASURED',x+.1,y+3.7,w-.2,.6,12,'orange',True,PP_ALIGN.CENTER)
 elif kind=='timeline':
  line(sl,x+.2,y+1.2,x+w-.2,y+1.2,'line',4)
  for i,(a,b) in enumerate([('W16','Data'),('W17','Baseline'),('W18','Audit'),('W19','Ablate')]):
   xx=x+.45+i*1.55;shape(sl,xx-.19,y+1.0,.38,.38,'teal',MSO_SHAPE.OVAL);tx(sl,a,xx-.35,y+.3,1,.4,16,'teal',True);tx(sl,b,xx-.35,y+1.7,1.3,.6,15)
  tx(sl,'Week 1 is a go / no-go gate.',x+.1,y+3.5,w-.1,.7,23,'orange')
 elif kind=='research':
  for i,(a,b) in enumerate([('2024','CandyCrunch'),('2025','GlyContact'),('2026','GlycanGT')]):
   tx(sl,a,x+.2,y+.3+i*1.3,1.5,.55,26,'teal',True);tx(sl,b,x+1.9,y+.35+i*1.3,3.3,.65,22)
 elif kind=='headroom':
  for i,(a,b) in enumerate([('H1','Measure the gap'),('H2','Avoid certainty'),('H3','Audit the proxy')]):boxlabel(sl,a,b,x+.1,y+.15+i*1.35,w-.2,1.1)
 elif kind=='gates':
  labels=['Graph','Scarcity','Generation','Checker','Levers','Data','Compute','Copies'];colors=['teal','orange','teal','orange','teal','orange','red','orange']
  for i,(a,c) in enumerate(zip(labels,colors)):
   xx=x+.1+(i%2)*2.8;yy=y+.1+(i//2)*1.05;shape(sl,xx,yy,2.55,.78,'panel2');tx(sl,f'{i+1}  {a}',xx+.16,yy+.22,2.25,.4,16,c,True)
 elif kind=='risks':
  for i,(a,b) in enumerate([('DATA','rights + context'),('PROXY','generalization'),('BUDGET','timing + coverage')]):
   boxlabel(sl,a,b,x+.1,y+.2+i*1.35,w-.2,1.1,'orange')

def footer(sl,idx,refs):
 line(sl,.55,6.98,12.78,6.98,'line',.6)
 x=.58
 for k in refs[:7]:
  w=max(.40,min(1.1,len(k)*.065+.18));s=tx(sl,k,x,7.10,w,.2,8.5,'muted')
  r=s.text_frame.paragraphs[0].runs[0];url=SOURCES[k][1]
  if url.startswith('http'):r.hyperlink.address=url
  x+=w+.12
 tx(sl,'PROPOSAL  /  04 NOV 2026',8.1,7.10,3.8,.2,8.5,'muted',align=PP_ALIGN.RIGHT)
 tx(sl,f'{idx:02d}',12.1,7.08,.6,.25,10,'teal',True,PP_ALIGN.RIGHT)

for i,d in enumerate(SLIDES,1):
 sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=rgb('bg')
 shape(sl,.0,.0,.12,7.5,'teal',MSO_SHAPE.RECTANGLE)
 if d['kind']=='cover':
  pill(sl,'RESEARCH PROPOSAL',.65,.65,2.4)
  tx(sl,d['title'],.65,1.5,7.0,2.25,43,'ink',True)
  tx(sl,d['subtitle'],.68,4.0,6.2,.8,23,'muted')
  tx(sl,'Structured generation • experimental labels • honest evaluation',.68,5.25,5.9,.9,19,'teal')
  diagram(sl,'cover',7.4,2.,5.1,4.1)
 else:
  tx(sl,d['title'],.62,.55,12.0,.72,30,'ink',True)
  tx(sl,d['subtitle'],.65,1.34,12.0,.65,17,'muted')
  if d['kind']=='references':
   for j,(key,name) in enumerate(d['items']):
    yy=2.13+j*.87;tx(sl,key,.7,yy,.95,.4,11,'teal',True)
    s=tx(sl,name,1.8,yy,10.7,.67,15)
    r=s.text_frame.paragraphs[0].runs[0];r.hyperlink.address=SOURCES[key][1]
  elif d['visual']:
   for j,(a,b) in enumerate(d['items']):
    yy=2.2+j*1.46;tx(sl,a,.7,yy,5.6,.4,12,'teal',True);tx(sl,b,.7,yy+.46,5.55,.87,20)
   diagram(sl,d['visual'])
  else:
   for j,(a,b) in enumerate(d['items']):
    yy=2.15+j*1.48;shape(sl,.68,yy,11.95,1.23,'panel');tx(sl,a,.9,yy+.17,3.05,.82,16,'teal',True);tx(sl,b,4.15,yy+.19,8.1,.86,20)
 footer(sl,i,d['refs'])
 urls='\n'.join(f'[{k}] {SOURCES[k][0]}\n{SOURCES[k][1]}\nQualification: {SOURCES[k][2]}' for k in d['refs'])
 sl.notes_slide.notes_text_frame.text=f"{d['title'].replace(chr(10),' ')}\n\n{d['notes']}\n\nSources:\n{urls}\n\nVisuals: original editable schematic; no plotted model-performance data."

prs.core_properties.title='Target-conditioned glycan generation'
prs.core_properties.subject='A bounded generative-modeling proposal aligned to the Final Project Guide'
prs.core_properties.author='Konstantine'
prs.core_properties.keywords='glycans, generative models, lectins, proposal, validity, memorization'
deck_path=OUT/'glycan_project_presentation.pptx'
prs.save(deck_path)
# Keep hyperlinks legible on the dark background in PowerPoint and LibreOffice.
with zipfile.ZipFile(deck_path) as z:
 entries=[(info,z.read(info.filename)) for info in z.infolist()]
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(deck_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for info,data in entries:
  if info.filename.startswith('ppt/theme/') and info.filename.endswith('.xml'):
   root=ET.fromstring(data)
   for tag,color in [('hlink',COL['teal']),('folHlink',COL['blue'])]:
    el=root.find(f'.//a:clrScheme/a:{tag}',ns)
    if el is not None:
     for child in list(el):el.remove(child)
     ET.SubElement(el,'{'+ns['a']+'}srgbClr',{'val':color})
   data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
  z.writestr(info,data)

notes=['# Glycan project presentation — expanded speaker notes','', 'Prepared 4 November 2026. Source proposal preserved; corrections and unverified requirements are explicit.','']
for i,d in enumerate(SLIDES,1):
 notes += [f"## {i:02d}. {d['title'].replace(chr(10),' ')}",'',d['subtitle'],'']
 notes += [f'- **{a}:** {b}' for a,b in d['items']]
 notes += ['',d['notes'],'','Sources: '+', '.join(f'[{k}]({SOURCES[k][1]})' for k in d['refs']), '']
(OUT/'speaker_notes.md').write_text('\n'.join(notes))
source_text=['# Primary-source register and evidence qualifications','', 'Checked/reconciled 4 November 2026. Historical workspace snapshot figures are identified below; no new model training or fresh Colab smoke test was performed.','', 'The course guide requires 15+ complete primary-paper audit rows. This register contains papers and supporting resources, and does not claim that requirement is completed.','']
for k,(a,u,q) in SOURCES.items():source_text += [f'## {k} — {a}','',f'[Open source]({u})','',q,'']
(OUT/'sources.md').write_text('\n'.join(source_text))
(OUT/'slide_manifest.json').write_text(json.dumps(SLIDES,indent=2,ensure_ascii=False))
print(f'Built {len(SLIDES)} slides: {OUT / "glycan_project_presentation.pptx"}')
