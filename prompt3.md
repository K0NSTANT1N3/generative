# Research request: audit existing generative-model work on glycans and microbial natural products

## What I need
I am choosing a final research project in generative modeling and have narrowed it to two candidate domains. I need you to find the **existing generative-model papers and projects** in each, and for every one report exactly what they were trying to do, what data they used, whether I can get that data for free right now, and how long training took.

The two domains:

1. **Glycans (carbohydrate structures).** Generative or inverse-design models over glycan structures (branched trees of monosaccharides). Related: glycan–lectin binding prediction (LectinOracle), glycan representation learning (SweetNet, GlycanGT, GlycanAA, GlycoBART), the glycowork package, GlyTouCan, glycan microarray binding data.
2. **Microbial natural products.** Generative models producing natural-product-like molecules, especially for antibiotic discovery. Related: NPGPT, COCONUT database, NP Atlas, the Cell 2025 de novo antibiotic design paper, the JACS Au 2025 Gram-negative pipeline.

Do not restrict yourself to the names above; they are starting points, and I want anything else you find from 2022–2026.

## For EVERY paper or project you find, give me these fields
Report them in a table, one row per paper, plus a short paragraph under each where the table is too cramped.

1. **Title, authors, lab/university, venue, year, link (DOI or arXiv).**
2. **Goal / objective — in one plain sentence.** What problem were they actually solving? Specifically: what did the model GENERATE, and what did it generate it FOR? Distinguish clearly between:
   - unconditional generation (just making structures that look like the training data), versus
   - conditional / inverse design (generating structures that achieve a stated function or property).
   If it is conditional, say exactly what the conditioning signal was.
3. **Model family and size.** Diffusion, flow matching, VAE, GAN, autoregressive/language model, graph transformer, etc. Parameter count if stated.
4. **Training data:** dataset name, number of samples, what each sample is, and the exact URL.
5. **Can I get that data for free, right now, with no application form?** State the license explicitly (CC0, CC BY 4.0, MIT, "no license stated", gated, registration required, etc.) and the download size and file format. Flag anything requiring registration, login, a request form, or a data use agreement — those are disqualifying for me.
6. **Training compute: how many GPU-hours, what hardware, how many epochs, what batch size.** This is the field I care about most and the one papers most often omit. If the paper does not report it, say so explicitly, then check: the GitHub repo's training config/README, the appendix, the supplementary material, and any reported wall-clock times. If it is still unavailable, say "not reported" and give your own estimate with the reasoning (dataset size x model size), clearly labelled as an estimate.
7. **Is code released?** Link it, and give the license.
8. **Evaluation metrics used,** and especially: did they check for **memorization or near-duplicates of training data**? If they only report "novelty" as "not an exact copy", say so.
9. **Stated limitations or flaws** — from the authors themselves, and any you can see.

## Then answer these questions directly
- **Which specific sub-problems in these two domains have already been solved, and which are still open?** I want to find a gap, not redo existing work.
- **For glycans specifically: has anyone published a generative / inverse-design glycan model, or does only binding prediction exist?** If the generative side is empty, say so plainly, because that is the gap I would target.
- **Which of the two domains is more crowded with large, well-funded labs?** I want to avoid competing with industrial-scale compute.
- **Rank every project you found by how reproducible it is on a free Google Colab T4 (16 GB VRAM, under 4 GPU-hours total, environment setup under 5 minutes).**

## My constraints (so you can filter)
- Free Google Colab or Kaggle GPU only: T4 or P100 class, 12–16 GB VRAM.
- Baseline training plus evaluation must fit in roughly **under 4 GPU-hours total**, and environment setup must take under 5 minutes.
- Data must be **downloadable immediately** under an open license. No application forms, credentialing, waitlists, or data use agreements.
- I have 4 weeks of implementation time, alone, after a planning phase.
- I need a free, fast, automatic validity checker for generated structures. For each domain, name the tool, link it, say what it checks, and give its runtime per sample.

## Honesty rules
- Only cite papers, datasets, labs, and repos you actually found. Never invent titles, authors, links, or numbers.
- For every dataset size, license, and training-time figure, state whether you **confirmed it at the primary source** or are **estimating**. Label every estimate as an estimate.
- If a paper does not report training compute, say "not reported" rather than guessing silently.
- If you cannot find a generative model in one of these domains, say so plainly. An honest empty result is more useful to me than a padded list.
- Prefer primary sources: the paper PDF, the official GitHub repo, the dataset's own page.
