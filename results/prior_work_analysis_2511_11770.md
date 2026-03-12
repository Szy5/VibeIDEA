# Prior Work Analysis Report

## Target Paper

**Title:** Learning to Refine: An Agentic RL Approach for Iterative SPARQL Query Construction

**arXiv ID:** [2511.11770](https://arxiv.org/abs/2511.11770)

**Abstract:** 
> Generating complex, logically-sound SPARQL queries for multi-hop questions remains a critical bottleneck for Knowledge Graph Question Answering, as the brittle nature of one-shot generation by Large Language Models (LLMs) hinders reliable interaction with structured data. Current methods lack the adaptive policies needed to dynamically debug queries based on real-time execution feedback. This paper introduces a novel agentic framework where an LLM learns a resilient policy for the sequential process of iterative SPARQL construction. We show that a compact 3B-parameter model, trained exclusively via outcome-driven Reinforcement Learning (GRPO) without supervised fine-tuning, can learn effective policies for this task, discovering how to systematically recover from execution errors and refine its queries toward a correct answer. On a curated, executable single-answer subset of LC-QuAD 2.0, our agent achieves 49.7\% accuracy post-entity-linking, a significant 17.5 percentage point improvement over the strongest iterative zero-shot baseline. Further analysis reveals that while the agent's capability is driven by RL, its performance is enhanced by an explicit deliberative reasoning step that acts as a cognitive scaffold to improve policy precision. This work presents a generalizable blueprint for teaching agents to master formal, symbolic tools through interaction, bridging the gap between probabilistic LLMs and the structured world of Knowledge Graphs.

**Innovation pattern:** Gap-Driven Reframing (confidence: high)

Secondary patterns: Representation Shift & Primitive Recasting

*Reasoning:* Reframes static NL→SPARQL parsing gap into an agentic, iterative RL refinement loop (gap-driven reframing); also recasts query construction into an action/representation learning problem (representation shift).

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models** (2024) [[arXiv](https://arxiv.org/abs/2402.03300)]
- *Authors:* Zhihao Shao et al.
- *Direct Connection:* Developed and demonstrated Group Relative Policy Optimization (GRPO) for sparse, outcome-driven training of LLM policies, which this work reuses as the core RL algorithm to learn SPARQL refinement from terminal rewards.

**Semantic Parsing on Freebase from Question-Answer Pairs** (2013)
- *Authors:* Jacob Berant et al.
- *Direct Connection:* Formalized the core mapping of natural-language questions to executable formal queries over knowledge bases, establishing the problem formulation (NL→formal query) that this work reframes as a sequential decision process over SPARQL actions.

### 🏷️ Inspiration

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2210.03629)]
- *Authors:* Shunjie Yao et al.
- *Direct Connection:* Introduced the think→act→observe agentic loop that directly motivated framing SPARQL construction as interleaved internal reasoning and external (KG) actions, providing the agentic control-flow the paper adapts for iterative query refinement.

**Tree of Thoughts: Deliberate Problem Solving with Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.10601)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* Introduced explicit deliberative planning that structures internal reasoning to improve downstream decisions, which directly inspired the paper's use of an explicit <think> deliberation block as a cognitive scaffold during RL policy learning.

### 🏷️ Gap Identification

**LEGO: Latent Execution-Guided Reasoning for Multi-Hop Question Answering on Knowledge Graphs** (2021)
- *Authors:* Hao Ren et al.
- *Direct Connection:* Demonstrated the benefit of using (latent) execution signals to guide multi-hop KGQA reasoning, exposing the limitation of non-adaptive pipelines and motivating a learned, interaction-driven policy that explicitly interprets execution feedback.

### 🏷️ Extension

**Agentic Reasoning and Tool Integration for LLMs via Reinforcement Learning** (2025)
- *Authors:* Jaspreet Singh et al.
- *Direct Connection:* Showed practical RL-based fine-tuning of agentic LLMs and recommended training practices (e.g., loss masking to avoid predicting environment tokens), techniques this paper directly adopts when tuning an LLM policy for executable SPARQL actions.

### 🏷️ Related Problem

**StructGPT: A General Framework for Large Language Model to Reason over Structured Data** (2023) [[arXiv](https://arxiv.org/abs/2305.09645)]
- *Authors:* Jiejiang Jiang et al.
- *Direct Connection:* Provided concrete methods for prompting LLMs to reason over structured sources and emit structured queries, which the paper moves beyond by replacing fixed prompting heuristics with an RL-learned iterative SPARQL construction policy.

---

## Synthesis: How Prior Work Led to This Paper

Prior work established three complementary threads of relevant knowledge. Agentic frameworks like ReAct defined the concrete think→act→observe control loop for LLMs interacting with external tools, while StructGPT and related systems demonstrated practical prompting and structured-output techniques for reasoning over KGs and emitting formal queries. Semantic parsing work (Berant et al.) provided the formal NL→query problem formulation that grounds the task in executable SPARQL, and LEGO showed the concrete value of using execution-derived feedback to steer multi-hop KGQA—exposing the limitations of static, non-adaptive pipelines. On the optimization side, DeepSeekMath operationalized Group Relative Policy Optimization (GRPO) for sparse, outcome-based training of LLM policies, and contemporaneous agentic-RL work (ARTIST) codified engineering practices such as loss masking and RL fine-tuning for tool-using agents. Finally, Tree of Thoughts highlighted how an explicit deliberative planning stage can scaffold and regularize difficult decision-making. Together these works reveal a clear opportunity: combine an agentic think–act loop, execution-feedback supervision, and GRPO-style outcome-driven policy optimization while using explicit deliberation to regularize learning; the natural next step is to fuse those elements into an RL-trained LLM policy that iteratively constructs and debugs executable SPARQL queries against a KG.

---

*Analysis generated on: 2026-03-09T00:38:29.142504*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=13921, output=1180*
