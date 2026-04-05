# Prior Work Analysis Report

## Target Paper

**Title:** HOLMES: Hyper-Relational Knowledge Graphs for Multi-hop Question Answering using LLMs

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> HOLMES: Hyper-Relational Knowledge Graphs for Multi-hop Question Answering using LLMs

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering** (2018)
- *Authors:* Zhilin Yang et al.
- *Direct Connection:* HotpotQA established the multi-hop, multi-document distractor setting and evaluation protocol that directly frames the task and constraints HOLMES targets.

**MuSiQue: Multi-hop Questions via Single-hop Question Composition** (2022)
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* MuSiQue supplies a controlled-hop benchmark used to evaluate and tune HOLMES’s k-hop traversal and pruning strategies for multi-step reasoning.

### 🏷️ Inspiration

**Learning to Retrieve Reasoning Paths over Wikipedia Graph for Question Answering** (2020)
- *Authors:* Akari Asai et al.
- *Direct Connection:* The idea of navigating an entity-document graph to gather multi-hop evidence inspired HOLMES’s breadth-first traversal over a bipartite entity–document graph seeded by query entities.

### 🏷️ Gap Identification

**Hierarchy-aware Multi-hop Question Answering over Knowledge Graphs** (2023)
- *Authors:* Junnan Dong et al.
- *Direct Connection:* By highlighting that triple-only KGs omit qualifiers and contextual constraints crucial for inference, this work motivated HOLMES to add document-level qualifiers via a hyper-relational representation.

### 🏷️ Baseline

**Leveraging structured information for explainable multi-hop question answering and reasoning** (2023)
- *Authors:* Ruosen Li and Xinya Du
- *Direct Connection:* HOLMES builds on StructQA’s LLM-based triple extraction from supporting documents but addresses its query-agnostic, context-free triples and redundant raw-text prompts by constructing and using only a query-focused, context-qualified graph.

### 🏷️ Extension

**Iterative Zero-shot LLM Prompting for Knowledge Graph Construction** (2023)
- *Authors:* Salvatore Carta et al.
- *Direct Connection:* HOLMES extends the idea of building KGs from unstructured text via zero-shot prompting by augmenting extracted triples into hyper-relational quadruples and then schema-pruning them for QA.

### 🏷️ Related Problem

**Revisiting Relation Extraction in the Era of Large Language Models** (2023)
- *Authors:* Somin Wadhwa et al.
- *Direct Connection:* This work’s finding that LLMs reliably perform relation extraction with prompting directly informed HOLMES’s triple extraction step during graph construction.

---

## Synthesis: How Prior Work Led to This Paper

StructQA showed that prompting LLMs to extract document-level triples and pairing them with raw passages can enable explainable multi-hop QA, but its extraction is query-agnostic and the outputs lack contextual qualifiers, creating ambiguity and long prompts. HotpotQA formalized the distractor-rich, multi-document setting that makes such ambiguity and verbosity especially harmful, and MuSiQue introduced controlled hop complexity that pressures systems to manage evidence traversal and pruning effectively. Earlier, Asai and colleagues demonstrated that multi-hop reasoning benefits from traversing an entity-centric graph over Wikipedia to collect chains of evidence, providing a concrete mechanism for graph navigation seeded by the query. Work on knowledge-graph-based multi-hop QA, such as hierarchy-aware approaches, emphasized that triple-only representations overlook qualifiers and context needed for correct inference. In parallel, iterative zero-shot prompting showed that KGs can be constructed directly from unstructured text, and investigations into LLM-based relation extraction established that prompted LLMs can faithfully extract entities and relations without task-specific training.
Together, these works surfaced a clear opportunity: combine query-driven graph navigation with context-preserving representations and prompt-efficient inputs. The natural next step was to construct an entity–document graph from supporting evidence, extract triples via LLM prompting, and upgrade them into hyper-relational structures that retain document-level context. By pruning this graph with a query-aligned schema—guided by in-domain relational patterns—and feeding only the distilled, verbalized facts to the reader LLM, the approach synthesizes traversal, extraction, and context preservation into a compact, query-centered pipeline for multi-hop QA.

---

*Analysis generated on: 2026-04-05T12:00:11.162191*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
