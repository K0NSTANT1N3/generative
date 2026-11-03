# Research request: finding a generative modeling problem where nearly all data that exists is already public and will stay scarce

## About me
I am in the last semester of my bachelor's degree. I have advanced machine learning experience: I have trained models in PyTorch and implemented research papers from scratch. I like a balance of experiments and math (probability, linear algebra, optimization). I have no strong background in any specific science or engineering field, so a domain with a short learning curve is a plus.

My goal is a conference-style paper (workshop paper or arXiv preprint), a clean public GitHub repo, and a blog post, to help me get into a strong master's program and research assistant positions.

## Course context
University final research project: "Measurement-Bound Generative Modeling for Structured Domains." It is Week 6 (October 2026), the domain scanning stage.
- Phase 1 (Weeks 6–15): problem selection, literature audit, formal problem formulation, feasibility smoke test, 8–10 page two-column proposal paper.
- Phase 2 (Weeks 16–19): only 4 weeks to build the code, train a baseline, run validity and memorization checks, and test one methodological improvement, tracked in Weights & Biases.

## Compute limits
Free Google Colab or Kaggle GPU only (T4 or P100, 12–16 GB VRAM). Baseline must train and evaluate in under ~4 GPU-hours total; environment setup under 5 minutes. Small datasets are fine and preferred.

## What makes this search different (the most important part)
I have already screened ideas like analog circuit topologies (AnalogGenie dataset) and molecules with measured solubility (AqSolDB). I rejected them because much larger PRIVATE datasets exist (chip companies' proprietary designs, pharma companies' internal measurements), so anyone with private data could train a better model.

I want problems where:
- **A. Public completeness:** all, or at least ~90%, of the data that exists anywhere in the world is already public. No company, government, or institution holds a substantially larger private collection. Explain concretely why (e.g., the data is public by law, like regulatory approvals; nature made a finite set, like mineral species; each instance is a public object, like metro networks).
- **B. Permanent scarcity:** the amount of data cannot grow significantly in the near future (next 5–10 years), because each new sample is extremely expensive, slow, legally gated, or naturally limited. Give the current total count and the approximate growth rate per year, with sources.
- **C. Active research:** at least one university lab or research group is working on generative modeling (or closely related ML) for this problem now or in the recent past (2022–2026). Name the lab, the people, and one paper each, with links.

Example directions I thought of (unverified; verify, reject, or improve on them, and find better ones): approved drug molecules (FDA/EMA approvals are public, ~50 new per year), registered pesticide/agrochemical active ingredients, recognized mineral species and their crystal structures (IMA list), zeolite framework types (IZA database), metro/subway network graphs (OpenStreetMap). Do not limit yourself to these. Also think about: other regulatory lists, finite natural inventories, historical or one-of-a-kind engineered artifacts, and expert-curated catalogs.

Prefer practical engineering or chemistry domains where a practitioner could use and test the output. Avoid biology and physics unless a candidate is clearly stronger than all alternatives (max two, explain why).

## Hard requirements from my course: every candidate must also pass all 8 gates
1. **Abstract structure:** outputs are graphs, sets, rule-bound symbolic sequences, or geometries. Grid data (images, audio, weather fields) and plain text do not count.
2. **100x compute invariance:** 100x more compute cannot create more ground-truth data (physical measurement, regulatory approval, legal restriction, or rare expert annotation).
3. **Natural generation formulation:** inverse design, conditional generation, or generating many different valid outputs.
4. **Checkable validity:** a free, fast, automatic validity checker, solver, or surrogate exists. Give name, link, what it checks, runtime per sample.
5. **Open research levers:** at least two unsolved directions (representation, constraint-guided sampling, loss design, evaluation metrics, etc.).
6. **Instant open-access data:** public dataset with an open license, downloadable immediately. No application forms, credentialing, waitlists, or data use agreements. Check the license carefully.
7. **Compute feasibility** within the limits above.
8. **Checkable memorization:** a clear algorithm to detect exact or near duplicates of training samples (canonical forms, graph hashing, nearest-neighbor distance).

Note: with very small datasets (hundreds of samples), say honestly whether training a generative model is still meaningful, and whether pretraining on a larger related public corpus is a reasonable workaround without breaking criteria A and B.

## Scoring for candidates that pass (0–2 each)
- R1: active labs at recognized universities publish on it (name labs + one recent paper each)
- R2: papers at top ML venues (NeurIPS, ICML, ICLR, AISTATS) or top domain venues
- R3: publication count growing 2023–2026
- R4: real-world demand documented by a credible organization or clear industry need
- H1: current baselines leave clear room for improvement
- H2: not dominated by large industry labs with huge compute
- H3: existing papers have weak or gamed metrics, unverified memorization, or other flaws I could critique

## What I need back
1. **Short answer:** top recommendation in 3–4 sentences.
2. **Screening table:** 6–10 concrete candidate problems (specific problem statements, not just domains), pass/fail on criteria A, B, C and all 8 gates, with a one-line reason for every fail. Include the rejected candidates too, so I see why they failed.
3. **Score table:** R1–R4 and H1–H3 for every candidate that passes, with totals.
4. **Deep dive on the top 3:**
   - Problem statement (2–3 sentences) and rough formal setup (input space, output space, conditions, constraints)
   - Public-completeness argument (criterion A) and permanent-scarcity argument with counts and growth rate (criterion B)
   - Dataset: URL, license, number of samples, disk size, file format
   - Validity checker: name, link, what it checks, speed per sample
   - Baseline generative models with code links and model family (diffusion, flow matching, VAE, GAN, autoregressive)
   - Two or more open levers realistic in 4 weeks
   - Memorization check protocol
   - GPU-hour estimate on a free T4
   - Why a practitioner would care and how they could test the output
   - Main risks and a fallback plan
5. **Starter reading list for the top recommendation:** 15–20 papers in a table with title, venue and year, DOI or arXiv link, code/data link, license, and one known flaw or limitation.
6. **Claims to verify:** list the facts in your answer I should double-check at the primary source first.

## Honesty rules
- Only cite papers, datasets, labs, and repos you actually found. Never invent titles, authors, links, or numbers.
- For every dataset size, license, count, growth rate, and runtime, say whether you confirmed it at the source or are estimating it.
- If no candidate passes everything, say so plainly and show the closest options and which criteria they fail.
- Prefer primary sources (paper PDFs, official repos, dataset pages, regulator websites) over blogs or summaries.
