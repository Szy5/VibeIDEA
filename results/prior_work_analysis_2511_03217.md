# Prior Work Analysis Report

## Target Paper

**Title:** Hybrid Fact-Checking that Integrates Knowledge Graphs, Large Language Models, and Search-Based Retrieval Agents Improves Interpretable Claim Verification

**arXiv ID:** [2511.03217](https://arxiv.org/abs/2511.03217)

**Abstract:** 
> Large language models (LLMs) excel in generating fluent utterances but can lack reliable grounding in verified information. At the same time, knowledge-graph-based fact-checkers deliver precise and interpretable evidence, yet suffer from limited coverage or latency. By integrating LLMs with knowledge graphs and real-time search agents, we introduce a hybrid fact-checking approach that leverages the individual strengths of each component. Our system comprises three autonomous steps: 1) a Knowledge Graph (KG) Retrieval for rapid one-hop lookups in DBpedia, 2) an LM-based classification guided by a task-specific labeling prompt, producing outputs with internal rule-based logic, and 3) a Web Search Agent invoked only when KG coverage is insufficient. Our pipeline achieves an F1 score of 0.93 on the FEVER benchmark on the Supported/Refuted split without task-specific fine-tuning. To address Not enough information cases, we conduct a targeted reannotation study showing that our approach frequently uncovers valid evidence for claims originally labeled as Not Enough Information (NEI), as confirmed by both expert annotators and LLM reviewers. With this paper, we present a modular, opensource fact-checking pipeline with fallback strategies and generalization across datasets.

**Innovation pattern:** Cross-Domain Synthesis (confidence: high)

Secondary patterns: Gap-Driven Reframing, Modular Pipeline Composition

*Reasoning:* The work explicitly combines distinct paradigms (knowledge graphs + LLM agents/RAG) into a hybrid verification method — a cross‑domain synthesis — driven by KG coverage gaps and realized as a modular retrieval/agent pipeline.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Fever: a large-scale dataset for fact extraction and verification** (2018)
- *Authors:* James Thorne et al.
- *Direct Connection:* Provided the Supported/Refuted/Not‑Enough‑Information problem formulation and benchmark labels that the paper uses as its primary evaluation target and motivates KG-first + fallback handling of NEI.

**Retrieval-Augmented Generation for Knowledge-Intensive NLP** (2020)
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* Introduced the retrieval-augmented generation paradigm that directly informs the paper's web‑fallback design—conditioning a verifier on retrieved external evidence rather than relying solely on model internal knowledge.

### 🏷️ Inspiration

**KG‑GPT: A general framework for reasoning on knowledge graphs using large language models** (2023)
- *Authors:* Jiho Kim et al.
- *Direct Connection:* Showed how LLMs can be integrated with KG data for reasoning, directly inspiring the paper's choice to combine LLM classification with structured KG evidence rather than treating KGs and LLMs as isolated modules.

**Generate‑on‑Graph: Treat LLM as both agent and KG for incomplete knowledge graph question answering** (2024)
- *Authors:* Yao Xu et al.
- *Direct Connection:* Presented an agent–KG hybrid perspective (LLMs filling missing KG information) that motivated the paper's agent‑based, real‑time pipeline design and the decision to invoke web agents when KG evidence is insufficient.

### 🏷️ Gap Identification

**Zero‑shot fact‑checking with semantic triples and knowledge graphs** (2024)
- *Authors:* Moy Yuan and Andreas Vlachos
- *Direct Connection:* Demonstrated zero‑shot KG retrieval and triple‑based verification but also exposed limitations (coverage/NEI handling) that the present paper explicitly addresses by adding KG‑first orchestration and a targeted web fallback for NEI cases.

### 🏷️ Baseline

**Evidence‑based interpretable open‑domain fact‑checking with large language models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2312.05834)]
- *Authors:* Xin Tan et al.
- *Direct Connection:* Operated as a directly comparable web‑retrieval + LLM fact‑checking approach (and is cited/compared in results), providing the open‑domain LLM baseline that the hybrid KG‑first + fallback pipeline aims to outperform in interpretability and coverage.

### 🏷️ Extension

**FactKG: Fact verification via reasoning on knowledge graphs** (2023)
- *Authors:* Jiho Kim et al.
- *Direct Connection:* Demonstrated KG-based fact verification techniques and highlighted KG coverage/connectivity limits that this paper extends by adding a web‑retrieval fallback and KG-first orchestration to improve coverage and interpretability.

---

## Synthesis: How Prior Work Led to This Paper

The FEVER benchmark established the exact Supported/Refuted/Not‑Enough‑Information task formulation and evaluation framework that this work targets, making NEI handling a central concern; Lewis et al.'s Retrieval‑Augmented Generation introduced the concrete pattern of conditioning a verifier on retrieved external evidence, which the paper adopts for its web‑fallback stage. FactKG and KG‑GPT explored how structured triples and LLMs can be used for fact verification and reasoning over KGs, revealing both the strengths (interpretability, precise triples) and the coverage/connectivity shortcomings that motivate hybrid designs. Generate‑on‑Graph articulated an agent–KG hybrid approach—treating LLMs as agents that fill KG gaps—directly inspiring the pipeline's agentic decision to invoke web search only when KG evidence is insufficient. Prior open‑domain LLM fact‑checking work (Tan et al.) supplied a directly comparable web‑retrieval + LLM baseline and concrete evidence‑processing prompts, while Yuan & Vlachos' zero‑shot triple extraction and KG retrieval highlighted the specific gap around NEI and zero‑shot generalization. Together these works carve out a clear opportunity: preserve KG precision and interpretability by performing a KG‑first verification pass, and cover KG blind spots by conditioning a retrieval‑augmented LLM agent only when necessary—yielding a modular, zero‑shot pipeline that merges the concrete KG reasoning techniques, RAG‑style conditioning, and agentic fallback strategies developed in the cited literature.

---

*Analysis generated on: 2026-03-09T00:29:35.466358*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=12242, output=1186*
