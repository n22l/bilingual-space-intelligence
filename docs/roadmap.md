# Roadmap

**Current stage: Phase 0 — Specification.** This roadmap describes intended work, not completed functionality. It carries no delivery-date commitments.

## Phase 0 — Specification

Define the architecture, conceptual evidence schema, status taxonomy, source policy, and evaluation design. This repository supplies an initial draft of each.

Before Phase 1, settle the corpus boundaries, source rights review, metadata conventions, and annotation rules. No corpus or evaluation dataset exists yet.

## Phase 1 — Minimal retrieval system

Proposed v0.1 scope:

- Curate a small English/Chinese primary-source collection for reusable-launch and launch-cadence research.
- Record source metadata and parsing limitations.
- Parse the selected formats into traceable passages.
- Establish a simple retrieval baseline and return passages with inspectable citations.
- Prepare manually checked reference questions before tuning retrieval.

Completion should mean a researcher can trace retrieved passages back to the exact source location and inspect failures. Fluent answer generation is not a Phase 1 requirement.

## Phase 2 — Grounded answer generation

Add structured claims linked to passages, evidence-status classification, and explicit uncertainty or abstention. Add bilingual question handling and labeled translations with original text retained.

Completion should require claim-level citations and manual review of status distinctions, translation fidelity, and unsupported assertions. Quantitative acceptance thresholds remain to be defined after baseline experiments.

## Phase 3 — Evaluation

Formalize and version the manually verified question set. Run retrieval, citation, evidence-status, and unsupported-claim evaluations; include unanswerable questions and conflicting or outdated evidence.

Publish actual methods, denominators, limitations, and error analyses alongside measured results. Protect held-out questions from prompt and model tuning. Evaluation preparation begins earlier; this phase consolidates systematic measurement.

## Phase 4 — Expansion

Expand only after errors in the small corpus are understood. Candidate improvements include additional documents, entity normalization, Chinese–English terminology alignment, temporal comparisons, and richer research workflows.

Assess each expansion against the existing baseline and extend coverage without concealing earlier failure cases.

## Possible later work

Knowledge graphs, multimodal document/image retrieval, media provenance, and automated aerospace visualization pipelines may be explored if evidence needs justify them. They are not guaranteed deliverables.

## Recommended next task

Define and manually review a v0.1 corpus manifest and a small set of research questions for the reusable-launch use case. Specify inclusion dates, languages, document formats, rights constraints, expected evidence locations, and unanswerable cases before implementing ingestion.
