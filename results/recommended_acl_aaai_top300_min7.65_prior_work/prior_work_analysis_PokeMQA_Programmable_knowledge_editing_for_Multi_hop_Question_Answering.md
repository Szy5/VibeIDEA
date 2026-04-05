# Prior Work Analysis Report

## Target Paper

**Title:** PokeMQA: Programmable knowledge editing for Multi-hop Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> PokeMQA: Programmable knowledge editing for Multi-hop Question Answering

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Measuring and Narrowing the Compositionality Gap in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2210.03350)]
- *Authors:* Ofir Press et al.
- *Direct Connection:* By popularizing structured question decomposition prompting for compositional reasoning, this work provides the prompting paradigm PokeMQA adopts to sequentially decompose multi-hop questions and to assess stepwise reasoning.

### 🏷️ Inspiration

**Decomposed Prompting: A Modular Approach for Solving Complex Tasks** (2022) [[arXiv](https://arxiv.org/abs/2210.02406)]
- *Authors:* Tushar Khot et al.
- *Direct Connection:* By showing that modular (decomposed) prompting outperforms mixed-task prompting, this paper directly motivated PokeMQA’s decision to decouple question decomposition from conflict detection instead of using a single multipurpose prompt.

### 🏷️ Baseline

**MQuAKE: Assessing knowledge editing in language models via multi-hop questions** (2023) [[arXiv](https://arxiv.org/abs/2305.14795)]
- *Authors:* Zexuan Zhong et al.
- *Direct Connection:* MQuAKE introduced the MeLLo memory-based editor that stores edits as natural-language statements and couples question decomposition with in-prompt conflict checking—an approach PokeMQA directly builds on for memory representation while explicitly decoupling and replacing the in-prompt conflict check with a programmable scope detector.

### 🏷️ Extension

**Memory-based Model Editing at Scale** (2022)
- *Authors:* Eric Mitchell et al.
- *Direct Connection:* This work established memory-based editing and formalized the notion of an edit’s scope, which PokeMQA extends by redefining scope at the atomic-question level and training a two-stage scope detector g(t, q) to retrieve applicable edits during multi-hop reasoning.

**Efficient One-Pass End-to-End Entity Linking for Questions** (2020) [[arXiv](https://arxiv.org/abs/2010.02413)]
- *Authors:* Belinda Z. Li et al.
- *Direct Connection:* ELQ provides the end-to-end entity linking mechanism that PokeMQA operationalizes to identify key entities and fetch Wikidata facts to construct knowledge prompts that steer the first subquestion decomposition.

### 🏷️ Related Problem

**Can we edit factual knowledge by in-context learning?** (2023) [[arXiv](https://arxiv.org/abs/2305.12740)]
- *Authors:* Ce Zheng et al.
- *Direct Connection:* This paper showed that conditioning on edited facts in prompts can steer model behavior without weight updates, supporting PokeMQA’s memory-based, prompt-calibrated editing and motivating explicit retrieval of relevant edits during inference.

---

## Synthesis: How Prior Work Led to This Paper

Work on multi-hop knowledge editing began to take shape with MQuAKE, which framed multi-hop editing as storing edits in natural language and using MeLLo’s multipurpose prompt to interleave question decomposition and edit conflict checks. Memory-based Model Editing at Scale introduced the memory-editing paradigm and the core idea of an edit’s scope, establishing that edits could be applied at inference time by consulting external stores rather than modifying parameters. Decomposed Prompting showed that complex tasks benefit from modularization rather than mixing instructions, highlighting that conflating heterogeneous subtasks in a single prompt can degrade performance. Efficient One-Pass End-to-End Entity Linking (ELQ) provided a fast mechanism to identify entities in questions and link them to knowledge bases, enabling the retrieval of salient facts that can be injected as auxiliary context. In-context editing demonstrated that conditioning on edited facts can steer model outputs without weight changes, reinforcing the feasibility of external-memory-based updates. Measuring and Narrowing the Compositionality Gap emphasized structured question decomposition as a practical prompting strategy for compositional reasoning.
Together, these works revealed a key opportunity: memory-based editing is practical, but coupling multi-hop decomposition with conflict checking strains few-shot prompting and obscures edit applicability. Building on edit scope, modular prompting, and in-context conditioning, the natural next step is to decouple tasks—using a trainable scope detector to decide when an edit applies (redefining scope over atomic questions) and an entity-linked knowledge prompt to stabilize the crucial first subquestion—yielding a more reliable, controllable pipeline for multi-hop QA under continual knowledge updates.

---

*Analysis generated on: 2026-04-05T12:04:22.163229*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
