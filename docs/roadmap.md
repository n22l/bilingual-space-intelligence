# Roadmap

**Current stage: Phase 0 — Foundation.** Local text ingestion, original-language passage retrieval, source metadata, paragraph references, and synthetic retrieval evaluation work today. Broader capabilities are planned. Phase numbers describe scope, not release dates; evaluation begins now and accompanies every addition.

| Phase | Scope | Validation gate |
| --- | --- | --- |
| 0 — Foundation (implemented) | Prepared UTF-8 text ingestion, in-memory lexical retrieval, metadata preservation, expected-passage hit@5, external private mode. | Preserve synthetic regression and privacy tests; establish a reviewed private retrieval baseline. |
| 1 — Robust ingestion (planned) | Broader document parsing, improved metadata validation, document normalization, deduplication, traceable versions and locations. | Inspect extraction fidelity and evidence references against original documents; do not silently accept missing content. |
| 2 — Multilingual evidence retrieval (planned) | Entity normalization, terminology alignment, improved cross-language retrieval. | Compare English/Chinese retrieval to the lexical baseline; inspect false entity merges and terminology failures. |
| 3 — Structured evidence (planned) | Evidence records, domain-selected statuses, provenance, claim/evidence relationships. | Review original passages, status rationales, dates, units, and scope independently. |
| 4 — Citation-grounded generation (planned) | Evidence-based answers, citations, explicit uncertainty, unsupported-claim controls. | Measure citation support and unsupported assertions; fluent output is insufficient. |
| 5 — Evaluation expansion (planned) | Additional retrieval/ranking metrics, citation correctness, claim/evidence consistency, unsupported-claim rate, multilingual assessment. | Define denominators, annotation protocol, held-out cases, and limitations before reporting scores. |
| 6 — Additional domain (planned) | Add one technical domain only after aerospace validation; refactor from actual second-domain requirements. | Demonstrate reuse with reviewed data rather than empty schemas or integrations. |

## Recommended next engineering task

Create a versioned, manually reviewed private aerospace retrieval benchmark and failure report using the existing evaluator. Freeze document/passage versions, label supporting passages and unsupported questions, separate development and held-out cases, and record hit@5 with error analysis. Inspect any existing private collections locally before curating additions; this repository makes no assertion about their completeness or validation. Keep production text and private results outside Git. Do not add answer generation yet.
