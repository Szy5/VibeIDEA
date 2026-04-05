# Prior Work Analysis Report

## Target Paper

**Title:** Boosting Language Models Reasoning with Chain-of-Knowledge Prompting

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Boosting Language Models Reasoning with Chain-of-Knowledge Prompting

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This paper introduced the step-by-step rationale prompting paradigm that CoK explicitly restructures into evidence triples plus explanation hints, serving as the baseline prompting format that CoK modifies to reduce hallucinations.

**Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?** (2020)
- *Authors:* Alon Jacovi et al.
- *Direct Connection:* This paper’s formalization of faithfulness underpins CoK’s faithfulness verification criterion, guiding the design of a similarity-based check between explanations, evidence, and answers.

### 🏷️ Inspiration

**Rethinking with Retrieval: Faithful Large Language Model Inference** (2022)
- *Authors:* Hangfeng He et al.
- *Direct Connection:* This work’s generate–retrieve–verify loop inspired CoK’s rethinking process, which iteratively verifies and injects corrected knowledge, but at a finer granularity using explicit evidence triples.

### 🏷️ Extension

**Large Language Models are Zero-Shot Reasoners** (2022) [[arXiv](https://arxiv.org/abs/2205.11916)]
- *Authors:* Takeshi Kojima et al.
- *Direct Connection:* The authors’ zero-shot CoT with “Let’s think step by step” is directly used to automatically generate the explanation hints (CoK-EH) for in-context exemplars before adding structured evidence.

**Knowledge-in-Context: Towards Knowledgeable Semi-Parametric Language Models** (2022) [[arXiv](https://arxiv.org/abs/2210.16433)]
- *Authors:* Xiaoman Pan et al.
- *Direct Connection:* CoK relies on Pan et al.’s KB construction and retrieval tool to obtain candidate triples, which are then curated into the evidence triple component (CoK-ET) of the prompts.

**Learning Entity and Relation Embeddings for Knowledge Graph Completion (TransR)** (2015)
- *Authors:* Yankai Lin et al.
- *Direct Connection:* TransR’s scoring function is directly adopted in CoK’s factuality verification to assign plausibility scores to generated triples that are not found via exact KB match.

### 🏷️ Related Problem

**Making Language Models Better Reasoners with Step-Aware Verifier** (2023)
- *Authors:* Yifei Li et al.
- *Direct Connection:* Li et al.’s step-level verification of CoT motivated CoK’s F2-Verification to assess and filter unreliable reasoning by checking each explicit evidence piece for factuality and overall faithfulness.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-Thought (CoT) prompting showed that eliciting step-by-step rationales improves multi-step reasoning, establishing a format that organizes generation into intermediate steps. Zero-shot CoT demonstrated that simple prompts like “Let’s think step by step” can automatically produce such rationales without labeled demonstrations, offering a scalable way to generate explanations. In parallel, Knowledge-in-Context proposed retrieving structured knowledge from external knowledge bases to augment prompts and delivered tools to construct and query large, multi-domain KBs. Efforts to improve faithfulness at inference time introduced iterative generate–retrieve–verify loops with retrieval to reduce wrongness, while step-aware verification examined chain-of-thought at the granularity of individual steps to detect faulty reasoning. Foundationally, work on definitional clarity for faithfulness formalized what it means for an explanation to accurately reflect a model’s reasoning, and knowledge graph embedding methods such as TransR provided a way to score the plausibility of triples that are not directly present in a KB.
Collectively, these threads exposed a gap: free-form CoT makes faithfulness and factuality hard to verify because explanations lack explicit, checkable evidence. The natural next step was to restructure rationales into verifiable units by marrying CoT-style explanations with KB-grounded triples retrieved and curated via knowledge-in-context. Building on zero-shot CoT for scalable explanation hints, leveraging KB retrieval to supply candidate evidence, and using exact-match or TransR-based plausibility for factuality alongside a faithfulness criterion informed by prior definitions, the new approach adds a rethinking loop that injects corrected triples when reliability is low. This synthesis transforms ambiguous rationales into checkable chains of knowledge, addressing the specific weaknesses identified by earlier CoT and verification work.

---

*Analysis generated on: 2026-04-05T11:53:19.005958*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
