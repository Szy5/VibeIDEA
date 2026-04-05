# Prior Work Analysis Report

## Target Paper

**Title:** Interactive-KBQA: Multi-Turn Interactions for Knowledge Base Question Answering with Large Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Interactive-KBQA: Multi-Turn Interactions for Knowledge Base Question Answering with Large Language Models

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**KQA Pro: A dataset with explicit compositional programs for complex question answering over knowledge base** (2022)
- *Authors:* Shulin Cao et al.
- *Direct Connection:* KQA Pro’s explicit compositional program types and Wikidata qualifier structures directly shaped Interactive-KBQA’s exemplar taxonomy and specialized SPARQL patterns for qualifiers and counts used in multi-turn reasoning.

### 🏷️ Inspiration

**Few-shot in-context learning on knowledge base question answering (KB-BINDER)** (2023)
- *Authors:* Tianle Li et al.
- *Direct Connection:* KB-BINDER’s idea of drafting logical forms with few-shot exemplars and then refining them against the KB directly inspired Interactive-KBQA’s move to interleave KB calls within the generation process, enabling stepwise SPARQL construction guided by intermediate observations.

### 🏷️ Gap Identification

**Think-on-Graph: Deep and responsible reasoning of large language model on knowledge graph** (2024)
- *Authors:* Jiashuo Sun et al.
- *Direct Connection:* Think-on-Graph demonstrated iterative LLM reasoning on KGs but assumed golden entities, a limitation explicitly addressed by Interactive-KBQA through its SearchNodes and SearchGraphPatterns tools that integrate entity linking and predicate discovery into the reasoning loop.

**RNG-KBQA: Generation augmented iterative ranking for knowledge base question answering** (2022)
- *Authors:* Xi Ye et al.
- *Direct Connection:* RNG-KBQA’s retrieve-then-generate T5 pipeline for logical forms requires large annotated data and offers limited transparency, shortcomings that Interactive-KBQA overcomes by replacing heavy training with exemplar-guided, on-KB interactive SPARQL assembly.

### 🏷️ Baseline

**DecAF: Joint decoding of answers and logical forms for question answering over knowledge bases** (2023)
- *Authors:* Donghan Yu et al.
- *Direct Connection:* DecAF is a primary SP-based competitor that jointly decodes logical forms and answers with substantial supervision, against which Interactive-KBQA positions its few-shot, interpretable multi-turn approach and reports competitive gains especially on complex query types.

### 🏷️ Extension

**StructGPT: A general framework for large language model to reason over structured data** (2023)
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* StructGPT introduced the agent–environment paradigm with dedicated interfaces for querying structured sources, which Interactive-KBQA generalizes by designing three database-agnostic SPARQL tools (SearchNodes, SearchGraphPatterns, ExecuteSPARQL) to support multi-turn reasoning across Freebase, Wikidata, and Movie KBs.

### 🏷️ Related Problem

**KG-Agent: An efficient autonomous agent framework for complex reasoning over knowledge graph** (2024)
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* KG-Agent showed the viability of autonomous LLM agents for KG reasoning and constructed instruction-style datasets, informing Interactive-KBQA’s agentic design and its human-machine annotated, step-wise instruction data for fine-tuning.

---

## Synthesis: How Prior Work Led to This Paper

StructGPT established an agent–environment view for LLMs reasoning over structured data by exposing dedicated interfaces that let the model query and interpret structured sources in multiple steps. KB-BINDER demonstrated that few-shot in-context exemplars can guide LLMs to draft logical forms and then refine them into executable queries by consulting the knowledge base, suggesting a tight coupling between generation and KB feedback. Think-on-Graph showed that iterative reasoning on knowledge graphs via LLMs improves multi-hop performance but typically relies on golden entities, revealing a bottleneck in practical settings. DecAF and RNG-KBQA advanced semantic parsing for KBQA by jointly decoding logical forms and answers or by retrieve-then-generate pipelines, yet both depend on heavy supervision and yield limited process transparency. KQA Pro introduced explicit compositional programs and qualifier-rich structures on Wikidata, providing concrete categories (e.g., count, qualifier constraints) that clarify where systems must handle complex operators and schema idiosyncrasies. Meanwhile, KG-Agent validated agent-based frameworks for KG reasoning and emphasized instruction-style data for agent training.
Together, these works defined both the promise and limitations of LLM-driven KBQA: multi-step interaction is powerful, but pipelines often assume gold entities, require extensive training, and obscure reasoning. The natural next step was to fuse agentic interfaces with few-shot exemplars into a unified, multi-turn, SPARQL-centered toolset that lets LLMs search entities, discover graph patterns, and execute queries in situ. By aligning exemplar types with compositional operators (as in KQA Pro) and integrating entity and predicate search to remove gold assumptions (addressing ToG’s gap), the resulting interactive framework produces transparent, stepwise reasoning and competitive accuracy without large-scale supervision.

---

*Analysis generated on: 2026-04-05T11:39:33.758476*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
