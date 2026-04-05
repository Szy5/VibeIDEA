# Prior Work Analysis Report

## Target Paper

**Title:** REANO: Optimising Retrieval-Augmented Reader Models through Knowledge Graph Generation

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Open domain question answering (ODQA) aims to answer questions with knowledge from an external corpus.Fusion-in-Decoder (FiD) is an effective retrieval-augmented reader model to address this task.Given that FiD independently encodes passages, which overlooks the semantic relationships between passages, some studies use knowledge graphs (KGs) to establish dependencies among passages.However, they only leverage knowledge triples from existing KGs, which suffer from incompleteness and may lack certain information critical for answering given questions.To this end, in order to capture the dependencies between passages while tacking the issue of incompleteness in existing KGs, we propose to enhance the retrievalaugmented reader model with a knowledge graph generation module (REANO).Specifically, REANO consists of a KG generator and an answer predictor.The KG generator aims to generate KGs from the passages; the answer predictor then generates answers based on the passages and the generated KGs.Experimental results on five ODQA datasets indicate that compared with baselines, REANO 1 can improve the exact match score by up to 2.7% on the EntityQuestion dataset, with an average improvement of 1.8% across all the datasets.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**REBEL: Relation Extraction By End-to-End Language Generation** (2021)
- *Authors:* Pere-Lluís Huguet Cabot et al.
- *Direct Connection:* REANO trains its intra-context relation extractor under distant supervision using the REBEL dataset’s aligned Wikipedia text–Wikidata triples, enabling it to generate high-quality triples from passages.

### 🏷️ Inspiration

**Improving Multi-hop Knowledge Base Question Answering by Learning Intermediate Supervision Signals** (2021)
- *Authors:* Gaole He et al.
- *Direct Connection:* REANO’s relation-aware GNN that weights neighboring triples by question–relation similarity is inspired by He et al.’s question-conditioned message passing for multi-hop KBQA.

### 🏷️ Gap Identification

**KG-FiD** (2022)
- *Authors:* Wenhao Yu et al.
- *Direct Connection:* KG-FiD showed that adding KG signals to FiD can help multi-hop reasoning but relied on existing KGs like Wikidata, whose incompleteness motivated REANO to generate KGs directly from the retrieved passages.

**GRAPE: Knowledge Graph Enhanced Passage Reader for Open-Domain Question Answering** (2022)
- *Authors:* Mingxuan Ju et al.
- *Direct Connection:* GRAPE fused external KG and contextual representations to aid reading, yet its dependence on pre-existing KG triples highlighted missing-fact failures that REANO addresses by inducing graphs from passages.

### 🏷️ Baseline

**Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering** (2021) [[arXiv](https://arxiv.org/abs/2007.01282)]
- *Authors:* Gautier Izacard et al.
- *Direct Connection:* REANO adopts FiD as its reader backbone and directly augments it by appending a GNN-selected, triple-derived passage to address FiD’s limitation of independently encoding passages without modeling their relations.

### 🏷️ Extension

**DocuNet: Document-level Relation Extraction as Image Segmentation** (2021)
- *Authors:* Zhang et al.
- *Direct Connection:* REANO instantiates its intra-context relation extraction component with DocuNet to efficiently predict relations between all entity pairs within a passage in a single forward pass, enabling scalable KG generation from text.

### 🏷️ Related Problem

**Empowering Language Models with Knowledge Graph Reasoning for Open-Domain Question Answering** (2022)
- *Authors:* Ziniu Hu et al.
- *Direct Connection:* OREOLM demonstrated gains from explicit KG reasoning for ODQA, informing REANO’s reasoning over a graph while underscoring the fragility of depending on incomplete external KGs.

---

## Synthesis: How Prior Work Led to This Paper

Fusion-in-Decoder established a powerful generative reader that encodes each retrieved passage separately and fuses them in the decoder, but by design it leaves inter-passage relationships implicit. Subsequent KG-enhanced readers sought to inject structured relational signals: GRAPE fused external knowledge graph representations into passage encodings, while KG-FiD attached KG-derived structure to improve multi-hop reasoning in FiD; OREOLM further showed that explicit KG reasoning benefits open-domain QA. However, all three largely depended on triples sourced from existing KGs such as Wikidata, where missing facts and coverage gaps can omit critical information that is present in the retrieved passages. On the information extraction side, DocuNet provided an efficient document-level relation extraction mechanism that can predict relations for all entity pairs within a passage in one forward pass, and the REBEL dataset offered distantly supervised text–triple alignments at scale to train such relation extractors. For reasoning over graphs, relation-aware GNNs for KBQA, exemplified by He et al., introduced question-conditioned message passing that prioritizes edges likely to be useful for answering a given query.

Together, these works revealed a clear opportunity: preserve FiD’s strong generative reading while explicitly modeling inter- and intra-passage relations without relying on incomplete external KGs. The natural next step is to induce a knowledge graph directly from the retrieved passages (leveraging DocuNet trained on REBEL) and perform question-aware graph reasoning to surface only the most relevant triples. By selecting top-K question-relevant triples via a relation-aware GNN and appending them as an additional “structured” passage, the approach integrates structured multi-hop cues into FiD’s decoding, addressing the coverage limitations of prior KG-enhanced readers while retaining generative strengths.

---

*Analysis generated on: 2026-04-05T12:09:20.571338*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
