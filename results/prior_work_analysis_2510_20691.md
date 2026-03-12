# Prior Work Analysis Report

## Target Paper

**Title:** Plan Then Retrieve: Reinforcement Learning-Guided Complex Reasoning over Knowledge Graphs

**arXiv ID:** [2510.20691](https://arxiv.org/abs/2510.20691)

**Abstract:** 
> Knowledge Graph Question Answering aims to answer natural language questions by reasoning over structured knowledge graphs. While large language models have advanced KGQA through their strong reasoning capabilities, existing methods continue to struggle to fully exploit both the rich knowledge encoded in KGs and the reasoning capabilities of LLMs, particularly in complex scenarios. They often assume complete KG coverage and lack mechanisms to judge when external information is needed, and their reasoning remains locally myopic, failing to maintain coherent multi-step planning, leading to reasoning failures even when relevant knowledge exists. We propose Graph-RFT, a novel two-stage reinforcement fine-tuning KGQA framework with a 'plan-KGsearch-and-Websearch-during-think' paradigm, that enables LLMs to perform autonomous planning and adaptive retrieval scheduling across KG and web sources under incomplete knowledge conditions. Graph-RFT introduces a chain-of-thought fine-tuning method with a customized plan-retrieval dataset activates structured reasoning and resolves the GRPO cold-start problem. It then introduces a novel plan-retrieval guided reinforcement learning process integrates explicit planning and retrieval actions with a multi-reward design, enabling coverage-aware retrieval scheduling. It employs a Cartesian-inspired planning module to decompose complex questions into ordered subquestions, and logical expression to guide tool invocation for globally consistent multi-step reasoning. This reasoning retrieval process is optimized with a multi-reward combining outcome and retrieval specific signals, enabling the model to learn when and how to combine KG and web retrieval effectively.

**Innovation pattern:** Modular Pipeline Composition (confidence: high)

Secondary patterns: Cross-Domain Synthesis, Principled Probabilistic Modeling & Uncertainty

*Reasoning:* The work decomposes reasoning into planning and retrieval modules with a two-stage SFT→RL pipeline (modular pipeline composition), while integrating CoT, retrieval, KGs (cross-domain synthesis) and KL‑constrained RL principles (probabilistic/RL modeling).

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2402.03300)]
- *Authors:* Zhihong Shao et al.
- *Direct Connection:* Provided the GRPO-style KL-constrained reinforcement fine-tuning formulation and practical lessons about the cold-start instability that Graph-RFT builds on and explicitly mentions resolving via CoT SFT.

### 🏷️ Inspiration

**Chain of Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* Introduced chain-of-thought supervision for stepwise reasoning that this paper directly adopts as a supervised fine-tuning paradigm to activate explicit planning and decomposition and to provide a stable initialization for subsequent RL.

**Search and Refine During Think: Autonomous Retrieval-Augmented Reasoning of LLMs** (2025) [[arXiv](https://arxiv.org/abs/arXiv:2505.11277)]
- *Authors:* Yaorui Shi et al.
- *Direct Connection:* Proposed the idea of interleaving retrieval and refinement during reasoning (AutoRefine), which directly inspired Graph-RFT's retrieval-specific reward signals and the refine-during-think retrieval scheduling design.

### 🏷️ Gap Identification

**Generate-on-Graph: Treat LLM as both agent and KG in Incomplete Knowledge Graph Question Answering** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2404.14741)]
- *Authors:* Yao Xu et al.
- *Direct Connection:* Framed the LLM–KG interaction as an agentic process but exhibited locally myopic decision-making and reliance on LLM internal knowledge when KGs are incomplete; Graph-RFT targets these exact limitations with global planning and adaptive retrieval.

### 🏷️ Baseline

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2307.07697)]
- *Authors:* Jiashuo Sun et al.
- *Direct Connection:* Established the think‑search‑generate paradigm for KG-centred LLM reasoning that Graph-RFT directly compares to and extends by adding explicit global planning and RL-driven adaptive KG/web retrieval scheduling.

**Paths-over-Graph: Knowledge Graph Empowered Large Language Model Reasoning** (2025)
- *Authors:* Xingyu Tan et al.
- *Direct Connection:* Used retrieval of reasoning paths/subgraphs as augmented inputs for LLMs (a retrieval‑augmented KGQA approach) that Graph-RFT extends by learning when to invoke KG vs web retrieval and how to sequence multi-step tool calls.

### 🏷️ Extension

**KG-Agent: An Efficient Autonomous Agent Framework for Complex Reasoning over Knowledge Graph** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2402.11163)]
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* Designed an iterative agent with a multifunctional toolbox and KG executor for smaller LLMs, providing the multi-tool agent architecture that Graph-RFT extends with explicit plan tokens, Cartesian-inspired decomposition, and a multi‑reward RL to learn retrieval scheduling.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-thought prompting introduced the concrete technique of stepwise, tokenized reasoning traces that make explicit decomposition and planning learnable; Graph-RFT leverages that supervised CoT finetuning to bootstrap structured plans. Work on KL‑constrained RL fine‑tuning (the GRPO-style formulations) supplied the policy‑optimization backbone and highlighted cold‑start instability, which motivates Graph-RFT’s CoT SFT-to‑RL two‑stage strategy. Recent retrieval‑during‑thinking methods (AutoRefine) contributed the insight that retrieval-specific supervision and iterative refinement improve evidence coverage, directly motivating Graph-RFT’s retrieval‑specific rewards and coverage signals. Concurrent KG‑centric LLM systems (ToG/Think‑on‑Graph and PoG/Paths‑over‑Graph) established the think/search/generate and path‑augmentation paradigms — practical baselines whose assumptions (static retrieval, local decisions) Graph‑RFT targets. Generate‑on‑Graph exposed the failure modes of local decision‑making and overreliance on parametric knowledge under incomplete KGs, explicitly identifying the gap Graph‑RFT fills with global planning and adaptive tool use. Finally, agentic multi‑tool architectures such as KG‑Agent provided the iterative tool‑calling design that Graph‑RFT extends by adding explicit plan tokens, logical functions for dependency tracking, and a multi‑reward RL objective that jointly optimizes answer correctness and retrieval coverage, enabling the natural next step of learning when and how to coordinate KG and web retrieval in complex, incomplete‑KG settings.

---

*Analysis generated on: 2026-03-09T00:31:19.994368*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=16715, output=1290*
