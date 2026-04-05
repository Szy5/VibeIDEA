# Prior Work Analysis Report

## Target Paper

**Title:** Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph

**arXiv ID:** [2307.07697v6](https://arxiv.org/abs/2307.07697v6)

**Abstract:** 
> Although large language models (LLMs) have achieved significant success in various tasks, they often struggle with hallucination problems, especially in scenarios requiring deep and responsible reasoning. These issues could be partially addressed by introducing external knowledge graphs (KG) in LLM reasoning. In this paper, we propose a new LLM-KG integrating paradigm ``$\hbox{LLM}\otimes\hbox{KG}$'' which treats the LLM as an agent to interactively explore related entities and relations on KGs and perform reasoning based on the retrieved knowledge. We further implement this paradigm by introducing a new approach called Think-on-Graph (ToG), in which the LLM agent iteratively executes beam search on KG, discovers the most promising reasoning paths, and returns the most likely reasoning results. We use a number of well-designed experiments to examine and illustrate the following advantages of ToG: 1) compared with LLMs, ToG has better deep reasoning power; 2) ToG has the ability of knowledge traceability and knowledge correctability by leveraging LLMs reasoning and expert feedback; 3) ToG provides a flexible plug-and-play framework for different LLMs, KGs and prompting strategies without any additional training cost; 4) the performance of ToG with small LLM models could exceed large LLM such as GPT-4 in certain scenarios and this reduces the cost of LLM deployment and application. As a training-free method with lower computational cost and better generality, ToG achieves overall SOTA in 6 out of 9 datasets where most previous SOTAs rely on additional training.

**Innovation pattern:** Modular Pipeline Composition (confidence: high)

Secondary patterns: Cross-Domain Synthesis

*Reasoning:* ToG explicitly composes specialized modules (KG beam search, LLM-driven pruning/scoring, path evaluation) into a disciplined pipeline (modular decomposition) while synthesizing graph search algorithms with LLM reasoning, i.e., cross-domain integration.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022)
- *Authors:* Xuezhi Wei et al.
- *Direct Connection:* Established step-by-step prompting to elicit internal reasoning from LLMs, which ToG leverages when asking the model to evaluate, rank, and explain candidate KG paths during its iterative 'think' and pruning steps.

### 🏷️ Inspiration

**ReAct: Synergizing Reasoning and Acting in Language Models** (2022)
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* Introduced the paradigm of treating an LLM as an agent that interleaves reasoning and actions against external resources, directly inspiring ToG’s design to let an LLM actively query and act on a knowledge graph during multi-step reasoning.

**BeamQA: Multi-hop Knowledge Graph Question Answering with Sequence-to-Sequence Prediction and Beam Search** (2023)
- *Authors:* Farah Atif et al.
- *Direct Connection:* Applied beam-search over knowledge graph paths for multi-hop QA, providing the concrete beam-search-on-KG algorithmic template that ToG adopts and augments by using an LLM to score/prune candidate paths.

**SKILL: Structured Knowledge Infusion for Large Language Models** (2022)
- *Authors:* Fedor Moiseev et al.
- *Direct Connection:* Showed how LLMs can be used to inject and align structured knowledge with models and knowledge sources, informing ToG’s capability for traceability and human/LLM-assisted correction of KG triples discovered during reasoning.

### 🏷️ Gap Identification

**Chain of knowledge: A framework for grounding large language models with structured knowledge bases** (2023)
- *Authors:* Tianle Li et al.
- *Direct Connection:* Represented the prevalent LLM ⊕ KG paradigm that retrieves KG facts to augment prompts but treats LLM as a translator; ToG was motivated to address the limitations of this loose coupling by tightly integrating the LLM into the graph search loop.

### 🏷️ Extension

**StructGPT: A General Framework for Large Language Model to Reason over Structured Data** (2023)
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* Demonstrated prompting LLMs to inspect and operate on structured knowledge (KG) — ToG extends this idea into a formal, iterative beam-search framework (entity/relation search + LLM-based prune/evaluate) with richer path management and stopping criteria.

---

## Synthesis: How Prior Work Led to This Paper

ReAct introduced the concrete agent paradigm where an LLM alternates between internal reasoning and external actions, giving the conceptual foundation for treating the model as an active explorer rather than a passive translator; this idea is the behavioral core ToG borrows when the LLM issues KG queries and uses answers to guide subsequent steps. BeamQA provided the algorithmic precedent for applying beam search on a knowledge graph to enumerate multi-hop candidate paths, supplying the search/width/depth mechanics that ToG adapts and couples with LLM-based scoring. StructGPT demonstrated prompting LLMs to operate over structured data and thus served as an immediate predecessor that ToG extends into a disciplined pipeline of relation/entity search, LLM-driven pruning, and path-based evaluation. Chain-of-Thought gave the prompting methodology to elicit stepwise judgments and explanations from LLMs, which ToG leverages for path scoring, decision thresholds, and answer generation. Work like "Chain of knowledge" typifies the loose LLM ⊕ KG approaches and highlighted their reliance on KG completeness, motivating a tighter LLM⊗KG coupling; meanwhile SKILL showed feasibility and value in using LLMs to inject and correct structured knowledge, directly informing ToG’s traceability and corrective feedback design. Together these threads — agentic LLM behavior (ReAct), beam search over KG (BeamQA), LLM-structured-data interfacing (StructGPT), stepwise prompting (CoT), the identified limits of LLM⊕KG pipelines, and techniques for knowledge infusion/correction (SKILL) — naturally converge to the ToG idea: an LLM-driven, beam-search-on-graph framework that iteratively explores, ranks, explains, and if needed corrects KG-backed reasoning paths.

---

*Analysis generated on: 2026-03-08T15:53:03.791224*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=17175, output=1128*
