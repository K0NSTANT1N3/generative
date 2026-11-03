# Research request: choosing a project for my generative modeling final research project

## About me
I am in the last semester of my bachelor's degree. I have advanced machine learning experience: I have trained models in PyTorch and implemented research papers from scratch. I like a balance of experiments and math (probability, linear algebra, optimization). I have no strong background in any specific science or engineering field, so a domain with a short learning curve is a plus.

I want this project to help me get into a strong master's program and get research assistant positions at university labs. My final outputs will be a conference-style paper (aiming for a workshop paper or an arXiv preprint), a clean public GitHub repo, and a blog post.

## Course context
This is my university's final research project, called "Measurement-Bound Generative Modeling for Structured Domains." It is now Week 6 (October 2026), the domain scanning stage.
- Phase 1 (Weeks 6–15): problem selection, literature audit, formal problem formulation, a feasibility smoke test, and an 8–10 page two-column proposal paper.
- Phase 2 (Weeks 16–19): only 4 weeks to build the code, train a baseline, run validity and memorization checks, and test one methodological improvement, all tracked in Weights & Biases.

## Compute limits
Free Google Colab or Kaggle GPU only (T4 or P100 class, 12–16 GB VRAM, limited session time). The baseline must train and evaluate in roughly under 4 GPU-hours total, and environment setup must take under 5 minutes. Small datasets are fine and even preferred.

## Topic preference
I prefer practical topics where a practitioner could actually use the generated output and test it (simulate it, build it, or fabricate it). Investigate these domains first:
1. Electronic circuits (e.g., analog circuit topologies or netlists, checked with a SPICE simulator such as ngspice)
2. Power grid topologies (e.g., synthetic grid generation, checked with pandapower, PyPSA, or MATPOWER)
3. CAD and mechanical design (e.g., constrained parametric sketches, 3D construction sequences)
4. Floor plans and building layouts
5. Practical chemistry (e.g., molecules or materials for industrial use, checked with RDKit)

You may add other practical engineering domains if they fit better. I prefer to avoid biology and physics, but if a biology or physics problem is clearly stronger than every alternative, include up to two of them and explain why.

## Hard requirements: every candidate must pass all 8 gates
1. Abstract structure: outputs are graphs, sets, rule-bound symbolic sequences, or geometries. Grid data (images, audio, weather fields) and plain text tokens do not count.
2. 100x compute invariance: real ground-truth data is scarce for real-world reasons (physical measurement or lab testing, legal confidentiality or security restrictions, rare expert annotation), so 100x more compute could not create more of it. Practical domains fail this gate most often, so test it hardest and explain the reasoning concretely.
3. Natural generation formulation: inverse design, conditional generation, or generating many different valid outputs.
4. Checkable validity: a free, fast, automatic validity checker, solver, or surrogate model exists. Give its name, link, and approximate runtime per sample.
5. Open research levers: at least two unsolved directions (e.g., representation, constraint-guided sampling, loss design, evaluation metrics).
6. Instant open-access data: a public dataset with an open license, or a free open-source simulator, that downloads immediately. Anything requiring application forms, credentialing, waitlists, or data use agreements is disqualified. Check this carefully, because some well-known datasets require a request form.
7. Compute feasibility within the limits above.
8. Checkable memorization: a clear algorithm to detect exact or near duplicates of training samples (e.g., canonical forms, graph hashing, nearest-neighbor distance in a canonical representation).

## Scoring for candidates that pass
Score each from 0 to 2 on:
- R1: Active labs at recognized universities publish on it (name the labs and one recent paper each).
- R2: Papers appear at top ML venues (NeurIPS, ICML, ICLR, AISTATS) or top domain venues (e.g., IEEE Transactions journals, DAC, ICCAD).
- R3: Publication count is growing from 2023 to 2026.
- R4: Real-world demand is documented by a credible organization or a clear industry need.
- H1: Current baselines leave clear room for improvement.
- H2: The area is not dominated by large industry labs with huge compute.
- H3: Existing papers have weak or gamed metrics, unverified memorization, or other flaws I could critique.

## What I need back
1. Short answer: your top recommendation in 3–4 sentences.
2. Screening table: 6–8 concrete candidate problems (specific problem statements, not just domains), with pass/fail on each of the 8 gates and a one-line reason for every fail.
3. Score table: R1–R4 and H1–H3 for every candidate that passes, with totals.
4. Deep dive on the top 3, covering:
   - Problem statement in 2–3 sentences, plus a rough formal setup (input space, output space, conditions, constraints)
   - The 100x compute argument
   - Dataset: URL, license, number of samples, disk size, file format
   - Validity checker: name, link, what it checks, rough speed per sample
   - Baseline generative models with code links, including the model family (diffusion, flow matching, VAE, GAN, autoregressive)
   - Two or more open levers I could realistically work on in 4 weeks
   - Memorization check protocol
   - GPU-hour estimate on a free T4
   - Why a practitioner would care, and how they could test the output
   - Main risks and a fallback plan
5. Starter reading list for the top recommendation: 15–20 papers in a table with title, venue and year, DOI or arXiv link, code or data link, license, and one known flaw or limitation.
6. Claims to verify: a list of the facts in your answer that I should double-check at the primary source first.

## Honesty rules
- Only cite papers, datasets, and repos you actually found. Never invent titles, authors, links, or numbers.
- For every dataset size, license, and runtime figure, say whether you confirmed it at the source or are estimating it.
- If no candidate passes all 8 gates, say so plainly and show the closest options and which gates they fail.
- Prefer primary sources (paper PDFs, official repos, dataset pages) over blogs or summaries.
