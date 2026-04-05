# Prior Work Analysis Report

## Target Paper

**Title:** CogMG: Collaborative Augmentation Between Large Language Model and Knowledge Graph

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models have become integral to question-answering applications despite their propensity for generating hallucinations and factually inaccurate content.Querying knowledge graphs to reduce hallucinations in LLM meets the challenge of incomplete knowledge coverage in knowledge graphs.On the other hand, updating knowledge graphs by information extraction and knowledge graph completion faces the knowledge update misalignment issue.In this work, we introduce a collaborative augmentation framework, CogMG, leveraging knowledge graphs to address the limitations of LLMs in QA scenarios, explicitly targeting the problems of incomplete knowledge coverage and knowledge update misalignment.The LLMs identify and decompose required knowledge triples that are not present in the KG, enriching them and aligning updates with real-world demands.We demonstrate the efficacy of this approach through a supervised fine-tuned LLM within an agent framework, showing significant improvements in reducing hallucinations and enhancing factual accuracy in QA responses.Our code 1 and video 2 are publicly available.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**ReAct: Synergizing Reasoning and Acting in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2210.03629)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* CogMG directly adopts ReAct’s thought–action–observation agent paradigm to orchestrate question decomposition, formal KG querying, triple completion, and RAG-based verification as modular tools.

**KQA Pro: A Dataset with Explicit Compositional Programs for Complex Question Answering over Knowledge Base** (2022)
- *Authors:* Shulin Cao et al.
- *Direct Connection:* CogMG uses KoPL from KQA-Pro as the formal program language and trains parsing/decomposition on its question–program pairs to derive the explicit required triples for KG queries.

### 🏷️ Inspiration

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model with Knowledge Graph** (2023) [[arXiv](https://arxiv.org/abs/2307.07697)]
- *Authors:* Jiashuo Sun et al.
- *Direct Connection:* It demonstrates how KGs can ground LLM reasoning to reduce hallucinations, which CogMG adopts as the starting point for querying KGs before adding its explicit triple-decomposition and update loop to handle KG misses.

### 🏷️ Gap Identification

**InstructUIE: Multi-task Instruction Tuning for Unified Information Extraction** (2023) [[arXiv](https://arxiv.org/abs/2304.08085)]
- *Authors:* Xiao Wang et al.
- *Direct Connection:* As an IE-based KG updating approach that broadly extracts triples from text, it exemplifies the 'aimless' updates CogMG seeks to fix by harvesting only triples demanded by unanswered queries.

**CP-KGC: Constrained-Prompt Knowledge Graph Completion with Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2310.08279)]
- *Authors:* Rui Yang et al.
- *Direct Connection:* By inferring links from existing graph structure without user-driven prioritization, it highlights the update misalignment that CogMG addresses via user-demand-aligned triple acquisition and verification.

### 🏷️ Extension

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020) [[arXiv](https://arxiv.org/abs/2005.11401)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* CogMG extends RAG by using retrieved documents not just to ground answers but to automatically verify and correct LLM-completed triples before adding them to the KG.

---

## Synthesis: How Prior Work Led to This Paper

Work on combining knowledge graphs with large language models has shown that structured knowledge can ground and constrain LLM reasoning: Think-on-Graph uses KG structure to reduce hallucinations by guiding inference over entities and relations. The ReAct paradigm operationalizes LLMs as agents that interleave reasoning with tool use through a thought–action–observation loop, enabling modular pipelines where the model plans, calls tools, and integrates feedback. KQA-Pro contributes explicit compositional programs (KoPL) for KBQA, providing parallel question–program pairs and a formal language that makes the intermediate logical steps and target triples explicit. Retrieval-Augmented Generation demonstrates that retrieved documents can reliably ground LLM outputs, suggesting a mechanism to validate or correct model-produced facts using external corpora. Meanwhile, instruction-tuned information extraction such as InstructUIE scales triple harvesting from text but pursues broad, schema-wide updates, and LLM-driven KGC like CP-KGC infers new links from existing graphs—both illustrating update strategies that are powerful yet misaligned with immediate user information needs.
Synthesizing these threads reveals a gap: methods either reason over what the KG already contains or update KGs broadly without aligning to real queries. The natural next step is to fuse ReAct-style agentic planning with KoPL-based decomposition to explicitly enumerate required triples, then use RAG to verify and correct parametric completions, turning missed KG queries into targeted, auditable updates. CogMG embodies this closed loop, leveraging KG grounding to curb hallucinations while converting KG gaps surfaced by user questions into prioritized, verified graph evolution.

---

*Analysis generated on: 2026-04-05T11:38:35.452308*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
