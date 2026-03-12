# Prior Work Analysis Report

## Target Paper

**Title:** KnowCoder-A1: Incentivizing Agentic Reasoning Capability with Outcome Supervision for KBQA

**arXiv ID:** [2510.25101](https://arxiv.org/abs/2510.25101)

**Abstract:** 
> Knowledge Base Question Answering (KBQA) aims to answer natural-language questions over a structured Knowledge Base (KB). Recent work improves KBQA by adopting an agentic reasoning paradigm, in which Large Language Models (LLMs) iteratively decompose a question, generate its corresponding logical queries, and interact with the KB to derive the answer. However, these methods typically fine-tune LLMs on reasoning trajectories synthesized via process supervision, which offers weak incentives for exploration and thus fails to strengthen the agentic reasoning ability. In this paper, we propose KnowCoder-A1, an LLM that can autonomously perform agentic reasoning on KBs to obtain answers. To incentivize autonomous exploration, KnowCoder-A1 trains the LLM under outcome-only supervision via a multi-stage curriculum reinforcement learning with an easy-to-hard curriculum. To establish foundational agentic capabilities, KnowCoder-A1 first fine-tunes the LLM on a small set of high-quality trajectories obtained through outcome-based rejection sampling. Then, to alleviate the reward sparsity inherent in outcome-only supervision, it applies multi-stage curriculum RL with reward schedules that progress from easy to hard. Trained with outcome-only supervision, KnowCoder-A1 exhibits powerful reasoning behaviors and consistently outperforms prior approaches across three mainstream datasets. Notably, on the zero-shot subset of GrailQA, KnowCoder-A1 achieves up to an 11.1% relative improvement while using only one-twelfth of the training data, demonstrating strong agentic reasoning capabilities.

**Innovation pattern:** Gap-Driven Reframing (confidence: high)

Secondary patterns: Representation Shift & Primitive Recasting

*Reasoning:* Identifies a concrete limitation of prompt-only agentic reasoning and reframes the problem toward outcome-supervised trajectories; also shifts representation by making internal 'thought' tokens and tool-call trajectories explicit.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2305.16291 (commonly cited as ReAct 2023))]
- *Authors:* Yao et al.
- *Direct Connection:* Introduced the ReAct agent paradigm of interleaving explicit natural-language reasoning (thoughts) with tool calls (actions), which this paper adopts as the core agentic interaction format and trajectory structure.

### 🏷️ Inspiration

**Interactive-KBQA** (2024)
- *Authors:* Xiong et al.
- *Direct Connection:* Provided the concrete KB toolset (e.g., SEARCHTYPES, SEARCHGRAPHPATTERNS, EXECUTESPARQL), prompting strategies, and empirical evidence of limitations for prompt-only agents that directly motivated the paper's tool design and critique of prompting-based agentic methods.

**Training powerful LLM agents with end-to-end reinforcement learning** (2025) [[arXiv](https://arxiv.org/abs/github.com/0russwest0/Agent-R1 (technical report/code))]
- *Authors:* Ouyang et al.
- *Direct Connection:* Demonstrated end-to-end RL for LLM agents and practical considerations for agentic policy training, motivating KnowCoder-A1's choice to use RL (rather than only SFT) to cultivate autonomous exploratory behaviors.

### 🏷️ Gap Identification

**KG-Agent: An efficient autonomous agent framework for complex reasoning over knowledge graph** (2024)
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* Represented the finetuning/process‑supervision approaches that synthesize stepwise trajectories from gold logical forms, whose lack of exploration and over-reliance on process supervision this paper explicitly targets and seeks to overcome.

### 🏷️ Baseline

**KBQA-o1: Agentic knowledge base question answering with Monte Carlo Tree Search** (2025)
- *Authors:* Haoran Luo et al.
- *Direct Connection:* Serves as the primary agentic KBQA strong baseline using MCTS to expand trajectories at inference, which KnowCoder-A1 directly compares to and aims to outperform with a data- and compute-efficient outcome-supervised RL pipeline.

### 🏷️ Extension

**Group Relative Policy Optimization (GRPO) / related Group-normalized policy methods** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2402.03300 (DeepSeekMath paper that introduces GRPO variant))]
- *Authors:* Shao et al.
- *Direct Connection:* Introduced the group-wise relative advantage normalization and optimization formulation that KnowCoder-A1 adopts (an on‑policy GRPO variant) to stabilize outcome-only RL across multiple rollouts per question.

---

## Synthesis: How Prior Work Led to This Paper

Prior work established both the agentic interaction format and its practical tooling and optimization primitives. ReAct concretely formalized interleaving explicit natural-language 'thought' steps with tool calls, supplying the trajectory format and rationale for keeping reasoning tokens explicit during training. Interactive‑KBQA operationalized that paradigm for KBQA, furnishing specific tools (SEARCHTYPES, SEARCHGRAPHPATTERNS, EXECUTESPARQL) and showing the limits of prompt-only strategies, which directly informed KnowCoder‑A1’s tool design and its critique of prompting. Several finetuning/process‑supervision papers (e.g., KG‑Agent and related SFT trajectory methods) demonstrated the common pipeline of decomposing gold logical forms into idealized trajectories, thereby exposing the exploration and robustness gaps that this work addresses. On the optimization side, GRPO introduced group-wise relative advantage normalization and a practical policy objective that stabilizes learning from multiple rollouts per query and was adopted (with an on‑policy variant) here. Finally, recent demonstrations of end‑to‑end RL for LLM agents highlighted how RL can instill autonomous corrective behaviors rather than mere imitation. Together these threads pointed to a natural next step: replace brittle process supervision and inference‑time MCTS with a small, outcome‑filtered cold start plus curriculumized outcome‑only RL (using group‑normalized policy updates) so the agent is incentivized to explore, recover from noisy tool feedback, and converge from easy-to-hard reward criteria—precisely the empirical trajectory KnowCoder‑A1 pursues.

---

*Analysis generated on: 2026-03-09T00:32:25.145782*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=15841, output=1112*
