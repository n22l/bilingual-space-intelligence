# Proposed architecture

**Status: Local lexical-retrieval milestone implemented; broader architecture remains proposed.**

`src/space_search.py` loads a JSON manifest and UTF-8 text, splits paragraphs, builds in-memory TF-IDF vectors, and returns original passages plus source metadata. Demo mode reads only synthetic fixtures. Private mode validates an external non-Git directory and writes result JSON only there. There are no network calls, saved indexes, caches, generated answers, or translation models. See the [local guide](local-retrieval.md).

Components below describe the broader planned system and are expected to evolve.

## Scope and flow

The proposed system starts with curated public documents and ends with inspectable evidence records. Retrieval should be useful independently of answer generation.

1. **Source intake:** maintain a source manifest, rights notes, retrieval dates, and document identifiers. Preserve versions or content hashes when permitted.
2. **Ingestion and parsing:** extract text and document structure from selected formats. Retain headings, page numbers, paragraph identifiers, and original-language text. Flag extraction failures; do not silently treat broken text as complete.
3. **Metadata and normalization:** validate required fields, preserve unknown dates, distinguish publication dates from event dates, and record original entity names alongside proposed normalized identifiers.
4. **Indexing:** split text into passages with stable document/version references and source locations. Compare a simple lexical baseline with semantic retrieval before choosing a more complex approach.
5. **Question and retrieval:** accept a research question, language, and optional metadata filters. Return ranked passages with provenance. Future bilingual query expansion should preserve the original query and record transformations.
6. **Structured claims:** derive bounded assertions from retrieved passages, assign evidence status with a rationale, and attach supporting and conflicting evidence. Abstain where evidence is insufficient.
7. **Citation and provenance checks:** verify that each cited location resolves and that the cited passage supports the claim. A valid URL alone does not establish support.
8. **Evaluation:** assess retrieval separately from generation and retain reproducible experiment settings and error analyses.

## Proposed data contracts

| Record | Planned fields |
| --- | --- |
| Document | ID, title, URL, publisher, publication date, language, country/system, source type, retrieval date, rights notes, version/hash where practical |
| Passage | ID, document/version ID, original text, location, language, parsing warnings |
| Claim | Assertion, country/system, event date or period, as-of date, evidence status and rationale, supporting/conflicting passage IDs, uncertainty |
| Translation | Original passage ID, translated text, source/target languages, method and review status |
| Research result | Question, retrieved passages, claims, citations, unresolved gaps, relevant system configuration |

These are conceptual contracts, not implemented schemas. Unknown values must remain explicit. Preserve date precision and avoid inventing exact dates from month-only or year-only sources.

The status vocabulary is defined in the [root README](../README.md#evidence-status-framework). Labels apply to scoped assertions: a demonstrated landing does not establish operational reuse. Source reliability, claim support, and milestone status are separate judgments.

## Bilingual handling

Keep Chinese and English source text intact. Translations should be labeled derivatives linked to originals. Preserve names, units, qualifiers, negation, and distinctions such as target versus achievement. Entity aliases and transliterations should remain reviewable; uncertain matches must not be silently merged.

## Boundaries and unresolved choices

Phase 1 should be a local, minimal retrieval workflow over a deliberately small corpus. No service architecture, cloud deployment, model provider, vector database, or orchestration framework is selected.

Before implementation, decide the initial formats, corpus size and date range, citation locator convention, language balance, storage format, and retrieval baseline. Handle document content as untrusted input: embedded instructions must not override system behavior. Secrets and restricted source files must stay out of Git.

For launch economics, label source-reported values, measured events, and analyst assumptions separately. Any future calculations should expose inputs, units, time windows, and missing variables.
