# Primary-source register and evidence qualifications

Checked/reconciled 4 November 2026. Historical workspace snapshot figures are identified below; no new model training or fresh Colab smoke test was performed.

The course guide requires 15+ complete primary-paper audit rows. This register contains papers and supporting resources, and does not claim that requirement is completed.

## GUIDE — Course final-project guide

[Open source](../../Final Project Guide.pdf)

Local supplied PDF; pp. 3–12 and appendices. Requirements, not empirical results.

## DESC — Project problem description

[Open source](../glycan-problem-description.md)

User-supplied proposal. Claims are qualified or corrected in the deck.

## BRIEF — Glycan project brief

[Open source](../glycan_project.md)

Workspace literature/data audit, 26 October 2026; historical file sizes are snapshot-specific.

## GT — Kitani et al. GlycanGT. Bioinformatics (2026)

[Open source](https://doi.org/10.1093/bioinformatics/btag147)

Masked graph representation/completion; paper reports 83,739 pretraining glycans.

## GTCODE — GlycanGT source and public processed data

[Open source](https://github.com/matsui-lab/GlycanGT)

Repository count 83,740; Apache-2.0 code. Data rights inherit their sources.

## GTARCH — GlycanGT versioned source archive

[Open source](https://zenodo.org/records/18636040)

About 7.7 MB source ZIP, not a standalone training-data-size claim. Archived metadata previously audited as CC BY 4.0.

## COSMOS — GlyCosmos downloads

[Open source](https://glycosmos.org/download)

Structure corpus; includes ambiguous records. October audit listing approximately 79.71 MB CSV; freeze exact release before training.

## COSLICENSE — GlyCosmos official data license

[Open source](https://glycosmos.org/license)

CC BY 4.0 for copyrightable dataset content; checked at the primary page.

## TOUCAN — GlyTouCan terms

[Open source](https://doc.glytoucan.org/en/Terms-and-Conditions)

CC0 registry; includes incompletely specified structures and overlaps GlyCosmos.

## LO — Lundstrøm et al. LectinOracle. Advanced Science (2022)

[Open source](https://doi.org/10.1002/advs.202103807)

Binding prediction, not generation. Reports 564,647 protein–glycan interactions; not 564,647 unique glycans.

## LOCODE — LectinOracle legacy repository

[Open source](https://github.com/BojarLab/LectinOracle)

Archived; points to maintained glycowork. MIT code does not settle all original measurement-data rights.

## ARRAY — GlyGen Glycan Array Data Repository

[Open source](https://glygen.ccrc.uga.edu/ggarray/)

October workspace audit: 989 study/dataset collections, 533 glycans, CC BY 4.0. Full bulk export not verified; not used as a confirmed downloaded training table.

## SWEETTALK — Bojar et al. Deep-Learning Resources for Studying Glycan-Mediated Host-Microbe Interactions. Cell Host & Microbe (2021)

[Open source](https://doi.org/10.1016/j.chom.2020.10.004)

Historical language modeling and property-guided local editing; no broad first-generator claim is warranted.

## SWEETNET — Burkholz et al. Using graph convolutional neural networks to learn a representation for glycans. Cell Reports (2021)

[Open source](https://doi.org/10.1016/j.celrep.2021.109251)

Graph predictor and representation baseline, not a whole-tree generator.

## BOLTZ — Yom et al. A Boltzmann model predicts glycan structures from lectin binding. Analytical Chemistry (2024)

[Open source](https://doi.org/10.1021/acs.analchem.3c04992)

Inverse identification from an experimental binding fingerprint; distinguish from designing new ligands for target sequences.

## BART — Abtheen et al. Transformer-based Deep Learning for Glycan Structure Inference from Tandem Mass Spectrometry (2025 preprint)

[Open source](https://doi.org/10.1101/2025.07.02.662857)

Spectra-conditioned sequence generation; not a training baseline within the proposed budget.

## BARTDATA — GlycoBART data release

[Open source](https://zenodo.org/records/15741423)

CC BY 4.0 release; paper describes 510,160 spectra and 3,590 identities before its filtering. Optional analytical context only.

## AA — Xu et al. Modeling All-Atom Glycan Structures via Hierarchical Message Passing and Multi-Scale Pre-training (ICML 2025)

[Open source](https://arxiv.org/abs/2506.01376)

Representation learning, not evidence of whole-glycan functional generation.

## ML — Xu et al. GlycanML: A Multi-Task and Multi-Structure Benchmark for Glycan Machine Learning (ICLR 2025)

[Open source](https://arxiv.org/abs/2405.16206)

Prediction benchmark; task code license does not establish every upstream data license.

## CONTACT — Thomès et al. GlyContact analyzes glycan 3D structures at scale. Nature Communications (2025)

[Open source](https://doi.org/10.1038/s41467-025-67590-y)

Structural analysis and interaction modeling; illustrates continuing glyco-AI research.

## CANDY — Urban et al. Predicting glycan structure from tandem mass spectrometry via deep learning. Nature Methods (2024)

[Open source](https://doi.org/10.1038/s41592-024-02314-6)

Analytical identification, not de novo ligand design.

## GLYLES — Joeres et al. GlyLES. Journal of Cheminformatics (2023)

[Open source](https://doi.org/10.1186/s13321-023-00704-0)

Translator, not semantic/biosynthetic validator; published timing approximately 19 ms on its own corpus/hardware.

## WORK — glycowork maintained repository

[Open source](https://github.com/BojarLab/glycowork)

MIT code; parsing, graphs, motif operations and models. Check source-specific data terms.

## RDKIT — RDKit getting started and sanitization

[Open source](https://www.rdkit.org/docs/GettingStartedInPython.html)

BSD-3-Clause toolkit; sanitization does not prove synthesizability or function.

## BENCH — Workspace validity benchmark

[Open source](../../tasks/validity_benchmark.json)

Local CPU measurement, 22 October 2026; not a Colab benchmark. Mean 379.5 ms over 200 GlyLES→RDKit attempts.

## SNA — Systematic synthesis of bisected N-glycans and unique recognitions by glycan-binding proteins. Chemical Science (2022)

[Open source](https://doi.org/10.1039/D1SC05435J)

Primary experimental context for SNA versus MAL-I and 6′/3′ sialyllactosamine recognition.

## PLATFORM — Cross-platform comparison of glycan microarray formats (2014)

[Open source](https://pubmed.ncbi.nlm.nih.gov/24658466/)

Primary cross-platform study; presentation and assay context matter.

## SIGLEC — An atlas of human siglecs integrates expression, affinity, and cis/trans sialoglycan recognition profiles. Nature Communications (2026)

[Open source](https://doi.org/10.1038/s41467-026-71086-8)

Functional recognition evidence; useful later biological extension, not the proposed cheap training baseline.

## GALECTIN — Galectin-1, -2, and -3 exhibit differential recognition of sialylated glycans and blood group antigens (2008)

[Open source](https://pubmed.ncbi.nlm.nih.gov/18216021/)

Galectins recognize β-galactoside contexts; do not conflate them with sialic-acid-binding Siglecs.

## BOJAR — Daniel Bojar Group, University of Gothenburg

[Open source](https://www.gu.se/index.php/en/research/daniel-bojar)

Institutional evidence of active glycan-focused machine learning research.

## MATSUI — Nagoya University: GlycanGT announcement (2026)

[Open source](https://www.nagoya-u.ac.jp/researchinfo/result/2026/04/ai-108.html)

Institutional source verifies authors, structure-completion focus and publication.

## ERC — University of Gothenburg: ERC grant for glycan research (2025)

[Open source](https://www.gu.se/en/news/erc-grant-for-bojars-research-on-glycans)

External funding and biological research demand; not proof of demand for any arbitrary generated structure.
