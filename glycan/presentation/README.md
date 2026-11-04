# Glycan project presentation

Editable PowerPoint and PDF presentation based on `../glycan-problem-description.md`, the other glycan-folder notes, and the local `Final Project Guide.pdf`.

The deck describes **target-conditioned whole-glycan generation**, with a bounded pilot and explicit feasibility gates. It is a research proposal, not a claim of completed training or experimentally validated binding. The full protein-sequence-conditioned architecture is distinguished from the smaller target-ID-conditioned pilot.

## Files

- `glycan_project_presentation.pptx`: editable slides, vector diagrams, speaker notes and clickable references.
- `glycan_project_presentation.pdf`: shareable slide export.
- `speaker_notes.md`: expanded explanations and slide-level sources.
- `sources.md`: source register and qualification of numerical claims.
- `preview.png`: contact sheet of selected slides.
- `build_presentation.py`: reproducible slide-generation source.

Run `python build_presentation.py` after installing `requirements.txt`. PDF export uses LibreOffice. Rendering and contact-sheet review use PyMuPDF and Pillow, which are optional review dependencies.

All diagrams are original schematic illustrations constructed from editable PowerPoint shapes. Sugar symbols use conventional SNFG-style shapes and colors; drawings do not claim experimentally observed geometry. No model-performance results are fabricated.

## Important qualifications

- Structural-data count: GlycanGT paper reports 83,739 glycans; the repository reports 83,740. A source archive's compressed size is not the size of a pure training-data file.
- Functional labels: array fluorescence is assay-dependent and is not automatically a solution dissociation constant. Original measurement-data reuse terms must be checked independently of code licenses.
- Compute: the four-GPU-hour plan is a proposed allocation, not a benchmark. Setup and training smoke tests remain required.
- Source document corrections are explained in the appendix; original notes are preserved.
- The guide's complete 15+ paper audit and empirical smoke-test requirements remain unfinished. The deck explicitly identifies those outstanding deliverables.
