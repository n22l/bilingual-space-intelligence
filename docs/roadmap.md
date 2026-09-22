# Roadmap

**Current stage: Phase 1 — Minimal local retrieval milestone.** Text ingestion, metadata, paragraph retrieval, synthetic demo evaluation, and external private-mode boundaries are implemented. Real primary-source corpus curation and validation remain outstanding. Later phases remain planned, with no delivery-date commitments.

## Phase 0 — Specification

Define the architecture, conceptual evidence schema, status taxonomy, source policy, and evaluation design. This repository supplies an initial draft of each.

Before real-corpus use, settle the corpus boundaries, source rights review, metadata conventions, and annotation rules. Only synthetic fixtures and smoke questions exist; no real research corpus or reviewed research benchmark is included.

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

Privately curate ten primary-source documents and ten manually verified questions (including two unsupported cases) for the reusable-launch use case. Specify inclusion dates, languages, document formats, rights constraints, expected evidence locations, and unanswerable cases before using real research inputs.
