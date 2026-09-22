# Architecture

## Implemented

`src/research_search.py` contains the domain-independent local workflow. Keeping ingestion, retrieval, metadata validation, and evaluation in one small standard-library module avoids unnecessary abstractions. `src/space_search.py` delegates to its CLI for compatibility.

1. Explicitly select bundled synthetic demo data or an external private directory.
2. Validate `documents.json` and its relative file references; read prepared UTF-8 text.
3. Split at blank lines into original-language paragraphs with `id:pN` references.
4. Build in-memory TF-IDF vectors and rank positive cosine matches for the query; break ties by passage ID.
5. Return up to five passages, scores, source metadata, and paragraph numbers.
6. For evaluation, repeat retrieval for each question and compute expected-passage hit rate at 5 on labeled answerable cases.

Demo JSON is printed. Private JSON is saved only in the validated external directory; fixed terminal messages avoid exposing text, queries, and paths. No network requests, persistent indexes, caches, generated answers, translation models, or evidence-status classification exist. Original paragraph content is retained, with surrounding whitespace stripped during segmentation; references locate extracted text, not original PDF pages.

## Core/domain separation

The core requires no jurisdiction, aerospace entity, or status vocabulary. Optional `domain` metadata is preserved without inference or filtering. Language-tag syntax is accepted independently from the current ASCII/Chinese tokenizer, which has only English/Chinese retrieval fixtures.

[src/domains/aerospace/](../src/domains/aerospace/README.md) documents the first application and its proposed annotation taxonomy. These files are not runtime plugins. The [domain model](domain-model.md) defines the current metadata contract and planned extension points. There is no universal evidence-status enum.

## Retrieval and verification

```text
SOURCE
  ↓ ingestion and retrieval (implemented)
RETRIEVED PASSAGE
  ↓ researcher assesses relevance
POTENTIAL EVIDENCE
  ↓ human checks original source, scope, date, and qualifiers
HUMAN-VERIFIED EVIDENCE
  ↓ reasoned link to a bounded assertion
SUPPORTED CLAIM
```

Only the first transition is automated. Evaluation compares retrieved IDs to human-authored labels; it does not verify the source or conclusion. A matching URL or high score is not proof of factual support. Original source text remains the authoritative evidence input. Future translations must be labeled derivatives linked to originals.

## Planned architecture

Prepared or parsed documents → validated metadata and versions → retrieval → structured evidence records → citation-grounded generation → independently evaluated claims.

Future parsing should retain page/section locations and extraction warnings. Document hashes and corpus versions should stabilize evidence labels. Entity normalization must preserve original names and uncertain matches. A later evidence-record layer may select a domain vocabulary with explicit review rationales; planned translation records would preserve source/target language, method, and review status.

Generation, contradiction handling, claim support checks, multilingual query expansion, and metadata filtering are not implemented. No database, deployment framework, or model provider has been selected. Introduce modules only when working functionality warrants them, and a second domain only after the first workflow is validated. Treat source instructions as untrusted document content, never as instructions to the engine.
