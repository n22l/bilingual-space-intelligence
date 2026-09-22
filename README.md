# Technical Research Engine

> Evidence-grounded AI research for U.S.–China aerospace analysis.

**Status: Early development — local retrieval demo implemented**

Bilingual Space Intelligence is an independent applied-AI engineering project exploring how multilingual retrieval, NLP, generative AI, structured evidence extraction, and evaluation can support rigorous aerospace research. **US–China Space Watch / 中美航天观察**, an independent publication, provides a real-world application environment.

This repository includes a working offline lexical-retrieval demo for English and Chinese text, source metadata, and a top-five evidence evaluation command. It uses explicitly synthetic fixtures; no real research corpus, held-out benchmark, generated answers, or deployed service is included.

## Run the demo

Requires Python 3.10+ and Git; no third-party Python packages or hosted API. From the repository root:

```powershell
python -B src/space_search.py --mode demo search --question "refurbishment replacement parts"
python -B src/space_search.py --mode demo search --question "翻修 工时 零件"
python -B src/space_search.py --mode demo evaluate
python -B -m unittest discover -s tests -v
```

See [local setup, privacy boundary, and private corpus instructions](docs/local-retrieval.md). Private material must live in an external sibling `space-watch-private/` directory, outside every Git working tree. `.gitignore` is only a secondary safeguard. Demo mode never reads private configuration. Private mode requires `SPACE_DATA_DIR` and saves results there without printing passages.

Retrieval uses English words and Chinese character sequences. It does not implement automatic translation or general cross-language semantic matching. Search scores do not establish answerability.

## The problem

Reliable comparative U.S.–China aerospace research spans English and Chinese sources, different terminology and transliterations, fragmented primary-source information, changing program timelines, official announcements, demonstrated hardware milestones, and incomplete public information.

A generic LLM response is insufficient when source provenance and evidence status matter. The central research problem is distinguishing what has actually happened from what has been announced or planned, and from what remains proposed or uncertain.

## Project objective

The planned **Bilingual Space Intelligence Engine** will retrieve, analyze, compare, translate, classify, and cite public-source information about U.S. and Chinese space programs. Evidence retrieval and evaluation will take priority over fluent answer generation.

The intended flow below is a proposal, not an implemented architecture:

```text
Public-source documents
        ↓
Ingestion / parsing
        ↓
Metadata + normalization
        ↓
Indexing / retrieval
        ↓
Research question
        ↓
Evidence retrieval
        ↓
Structured claim generation
        ↓
Citation / provenance
        ↓
Evaluation
```

Research questions will query the document index; document and passage provenance should be retained throughout the process. See [proposed architecture](docs/architecture.md).

## Planned structured output

The following is a field template, not a research answer or an implemented API:

```text
Claim:                    <one bounded assertion>
Evidence:                 <original passage and location>
Source:                   <document ID, title, publisher, URL>
Publication date:         <source date or unknown>
Country/system:           <relevant country and named program/system>
Original language:        <language of the evidence passage>
Translation:              <translation when appropriate, separately labeled>
Evidence status:          <one category below, with rationale>
Confidence / uncertainty: <evidence limits, conflicts, and missing information>
```

Future records should also preserve event dates, the temporal scope of a claim, retrieval dates, and links to all supporting or conflicting passages. Uncertainty should be explained; model-generated confidence numbers will not be treated as calibrated probabilities.

## Evidence-status framework

These proposed labels describe the status of a specific claim or milestone as of a stated date, not the credibility of an entire organization.

| Status | Intended meaning |
| --- | --- |
| DEMONSTRATED | Evidence supports that the specified event or capability was demonstrated under stated conditions. |
| OPERATIONAL | Evidence supports routine or in-service use within the specified scope. |
| TESTING | The specified capability is undergoing tests; the intended outcome is not established. |
| PLANNED | A responsible organization has announced an intended activity or program. |
| TARGETED | A date, cadence, performance level, or other goal is stated as an aim rather than an achieved result. |
| PROPOSED | A concept or option has been put forward without evidence of a committed implementation plan. |
| DELAYED | Evidence explicitly supports a postponement relative to an identified earlier schedule. |
| CANCELLED | Evidence explicitly supports termination of the specified effort. |
| UNKNOWN | Available evidence is insufficient, ambiguous, or unresolved. |

Separating these states prevents a future target from being reported as an achievement or a test from being treated as routine service. An official announcement is evidence of what was announced; it is not automatically independent verification of the underlying capability.

Claims should be split when labels would otherwise overlap: a test demonstration and a future operational target are separate assertions. Missing updates alone do not establish delay or cancellation. Annotation rules will be refined before evaluation.

## Initial use case

The first planned development use case supports research for:

**Reusable Rockets: The Hidden Economics Behind U.S. and Chinese Launch Cadence**

A guiding question is:

> How does launch cadence affect the economics and operational value of reusable launch systems in the United States and China?

The first real research corpus will deliberately be small and curated. It will prioritize public primary sources wherever practical, rather than attempt to index the entire aerospace internet. Candidate source categories include NASA, FAA, other U.S. government sources, CNSA, CMSA, Chinese government sources, aerospace organizations and companies, and technical publications. No real-source collection is included; the runnable demo uses invented documents only.

The research should separate observed launches and reuse events from announced cadence targets and economic assumptions. Launch counts alone cannot establish profitability; missing cost, refurbishment, utilization, and demand evidence should remain explicit.

## Planned technical areas

- Python and document ingestion/parsing
- Embeddings, semantic retrieval, and metadata filtering
- Retrieval-augmented generation (RAG) and generative AI
- Bilingual English/Chinese NLP
- Entity extraction and normalization
- Chinese–English terminology alignment
- Structured generation and claim verification
- Data engineering, automated evaluation, and citation verification

Frameworks, storage systems, embedding models, and model providers have not been selected.

## Evaluation philosophy

The project will be evaluated on evidence quality, not only on how convincing generated answers sound. Planned evaluation will examine retrieval relevance, citation correctness, claim–source consistency, evidence-status classification, unsupported-claim rate, bilingual terminology handling, entity resolution, and answer completeness.

A manually verified evaluation set should include answerable, unanswerable, ambiguous, and conflicting-source questions. The implemented evaluation checks expected-passage hits in the top five on authored synthetic fixtures; unsupported questions are inspection-only. Broader metrics and real-corpus results require reviewed data and actual experiments. The [evaluation plan](docs/evaluation-plan.md) describes the proposed protocol.

## Roadmap

| Phase | Planned scope |
| --- | --- |
| Phase 0 — Specification | Initial repository, architecture, evidence schema, source policy, and evaluation design documented. |
| Phase 1 — Minimal retrieval system | Local text ingestion, metadata, passage retrieval, and source references implemented for synthetic demo data; real-corpus validation remains. |
| Phase 2 — Grounded answer generation | Structured claims, evidence-status classification, and bilingual support. |
| Phase 3 — Evaluation | Manually verified question set, retrieval and citation evaluation, and unsupported-claim testing. |
| Phase 4 — Expansion | Larger corpus, entity normalization, terminology alignment, and more sophisticated research workflows. |

Evaluation design begins in Phase 0; reference questions should be prepared before system tuning. Possible later work includes knowledge graphs, multimodal document/image retrieval, media provenance, and automated aerospace visualization pipelines. These are exploratory directions, not commitments.

See the [expanded roadmap](docs/roadmap.md).

## Relationship to US–China Space Watch

US–China Space Watch / 中美航天观察 provides real research questions and publication production use cases. The AI system is intended to improve research traceability, source discovery, fact checking, evidence organization, and bilingual research.

This repository is an AI engineering project. Editorial decisions and conclusions remain subject to human review; the system should expose missing or conflicting evidence rather than automatically generate unsupported conclusions.

## Academic independence

This is an independent personal project, not an official University of Colorado Boulder project. It does not contain or publish course assignments. Concepts learned through graduate study may inform independently developed work. No university sponsorship or endorsement is implied.

## Repository guide

- [Local retrieval guide](docs/local-retrieval.md): runnable commands, private mode, and evaluation schemas
- [Architecture](docs/architecture.md): proposed components and evidence flow
- [Roadmap](docs/roadmap.md): phased scope and completion criteria
- [Evaluation plan](docs/evaluation-plan.md): proposed annotation and assessment protocol
- [Data sources](docs/data-sources.md): source priorities, metadata, and rights policy
- [src/](src/README.md), [tests/](tests/README.md), [data/](data/README.md), [examples/](examples/README.md), [notebooks/](notebooks/README.md): intended future uses

## License

Original project code and documentation are provided under the [MIT License](LICENSE), chosen for straightforward reuse with attribution. Third-party documents, excerpts, images, and datasets retain their respective rights; repository licensing does not grant permission to redistribute them.
