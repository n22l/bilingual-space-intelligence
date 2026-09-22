# Technical Research Engine

> Evidence-grounded AI research infrastructure for complex technical subjects.

An independent applied-AI engineering project developing an evidence-grounded research workflow for complex technical subjects, starting with English- and Chinese-language aerospace sources.

**Status: Early development.** An initial local text-ingestion, passage-retrieval, and retrieval-evaluation workflow is implemented. Broader research capabilities remain under development. The public demonstration uses synthetic documents; application to other technical subjects is planned and has not been evaluated.

## Current implementation

- Ingest prepared UTF-8 text documents with a JSON source manifest.
- Segment text at blank lines and retrieve original-language passages with lexical TF-IDF cosine similarity.
- Preserve source metadata and return paragraph references such as `document-id:p2`.
- Evaluate whether labeled supporting evidence appears among the first five retrieved passages.

No generated answers, automatic translation, automated fact verification, contradiction resolution, hallucination detection, or unsupported-question detection are implemented. Retrieval scores are not confidence estimates.

## Run the demo

Requires Python 3.10+ and Git on PATH. No third-party Python packages, credentials, model downloads, or network services are required. From the repository root:

```powershell
python -B src/research_search.py --mode demo search --question "refurbishment replacement parts"
python -B src/research_search.py --mode demo search --question "翻修 工时 零件"
python -B src/research_search.py --mode demo evaluate
python -B -m unittest discover -s tests -v
```

The old `src/space_search.py` command remains a compatibility entry point. Private mode prefers `TECH_RESEARCH_DATA_DIR`, falling back to `SPACE_DATA_DIR` only when the new variable is absent. It writes results to the configured external non-Git directory without printing passages. Demo mode ignores both settings. See the [local guide](docs/local-retrieval.md).

## Why this exists

Complex technical research involves fragmented sources, changing terminology, multilingual material, and incomplete or conflicting information. Useful research requires source provenance, primary-source verification, explicit uncertainty, and reproducible evaluation. Retrieved text must remain distinguishable from interpretation and verified conclusions.

## Implemented architecture

```text
Prepared UTF-8 documents + source manifest
        ↓
Validated local ingestion → blank-line passage segmentation
        ↓
In-memory TF-IDF retrieval ← research query
        ↓
Ranked original passages + source metadata + paragraph references
        ↓
Retrieval evaluation against manually labeled passage IDs (k = 5)
```

Search and evaluation are separate commands; evaluation runs search for each labeled question. The index is rebuilt per command. No saved index, database, service, or model provider is required. See [architecture](docs/architecture.md) for implemented and planned components.

## Current evaluation

The current evaluation checks whether **at least one** labeled supporting passage appears among the first five results for each labeled answerable question. Hit rate at 5 is the number of such hits divided by the number of answerable questions. Two manually labeled unanswerable demo questions are inspection-only and excluded from this denominator.

The bundled smoke set contains eight invented documents, ten passages, and six answerable questions. It is not a held-out benchmark. Its results do not establish answer accuracy, full evidence coverage, citation entailment, translation quality, cross-language retrieval quality, or automatic detection of unsupported questions. The [evaluation plan](docs/evaluation-plan.md) separates current scoring from future assessment.

## Domain architecture

```text
Core research engine (implemented local retrieval/evaluation)
    ├── Aerospace Intelligence — first application; synthetic demo implemented
    └── Additional technical domain — planned, not implemented or evaluated
```

The core does not require an aerospace taxonomy, jurisdiction, or fixed pair of languages. An optional `domain` metadata field preserves an explicit source label; it does not activate specialized processing or filtering. Aerospace concepts and the proposed status vocabulary live under [src/domains/aerospace/](src/domains/aerospace/README.md). A future domain configuration layer will be driven by real requirements rather than empty integrations. See the [domain model](docs/domain-model.md).

The intended multilingual research infrastructure is initially tested with English- and Chinese-language synthetic aerospace material. Tokenization still uses ASCII alphanumeric tokens and Chinese characters/bigrams. Accepting other language tags does not establish retrieval support or quality in those languages. Entity normalization, terminology alignment, translation-aware and cross-language retrieval remain planned.

## First application: Aerospace Intelligence

Reusable-rocket economics and launch-cadence research for **US–China Space Watch / 中美航天观察** provides the first real-world research application. It includes launch vehicles, missions, recovery, reuse, providers, and the distinction between demonstrated capability and announced plans. Launch counts alone cannot establish profitability.

This is a reusable software project. Editorial material, production source collections, and research conclusions remain private and subject to human review. No real research corpus or private evaluation results are distributed here.

## Roadmap

| Phase | Status and scope |
| --- | --- |
| 0 — Foundation | Implemented: local text ingestion, passage retrieval, metadata preservation, retrieval evaluation. |
| 1 — Robust ingestion | Planned: broader parsing, metadata validation, normalization, deduplication. |
| 2 — Multilingual evidence retrieval | Planned: entity normalization, terminology alignment, improved cross-language retrieval. |
| 3 — Structured evidence | Planned: evidence records, domain-specific statuses, provenance, claim/evidence relationships. |
| 4 — Citation-grounded generation | Planned: evidence-based answers, citations, unsupported-claim controls. |
| 5 — Evaluation expansion | Planned: ranking metrics, citation correctness, claim consistency, unsupported-claim rate, multilingual evaluation. |
| 6 — Additional domain | Planned only after aerospace validation: one new domain to test reusable abstractions. |

Evaluation accompanies each phase. See the [roadmap](docs/roadmap.md) for scope and validation gates.

## Public/private boundary

Reusable code, documentation, tests, the evaluation framework, and synthetic demonstration data belong in public Git. Production documents, copyrighted/local source extracts, editorial notes, unpublished research, research outputs, and private evaluation sets remain outside **every Git working tree**. Ignore rules are secondary safeguards. See [public/private separation](docs/public-private-boundary.md) and [source policy](docs/data-sources.md).

## Repository guide

- [Local retrieval guide](docs/local-retrieval.md): commands, metadata, private setup, and compatibility.
- [Architecture](docs/architecture.md), [domain model](docs/domain-model.md), and [roadmap](docs/roadmap.md).
- [Evaluation plan](docs/evaluation-plan.md), [data sources](docs/data-sources.md), and [public/private boundary](docs/public-private-boundary.md).
- [Source](src/README.md), [tests](tests/README.md), [data](data/README.md), [examples](examples/README.md), and [notebooks](notebooks/README.md).

## Academic independence and license

This is an independent personal project, not an official University of Colorado Boulder project. It does not publish course assignments or imply university sponsorship or endorsement.

Original code, documentation, and synthetic fixtures use the [MIT License](LICENSE). Third-party materials retain their respective rights; source inclusion does not grant redistribution permission.
