# Prior Work Analysis Report

## Target Paper

**Title:** Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph

**arXiv ID:** [2307.07697](https://arxiv.org/abs/2307.07697)

**Abstract:** 
> Although large language models (LLMs) have achieved significant success in various tasks, they often struggle with hallucination problems, especially in scenarios requiring deep and responsible reasoning. These issues could be partially addressed by introducing external knowledge graphs (KG) in LLM reasoning. In this paper, we propose a new LLM-KG integrating paradigm ``$\hbox{LLM}\otimes\hbox{KG}$'' which treats the LLM as an agent to interactively explore related entities and relations on KGs and perform reasoning based on the retrieved knowledge. We further implement this paradigm by introducing a new approach called Think-on-Graph (ToG), in which the LLM agent iteratively executes beam search on KG, discovers the most promising reasoning paths, and returns the most likely reasoning results. We use a number of well-designed experiments to examine and illustrate the following advantages of ToG: 1) compared with LLMs, ToG has better deep reasoning power; 2) ToG has the ability of knowledge traceability and knowledge correctability by leveraging LLMs reasoning and expert feedback; 3) ToG provides a flexible plug-and-play framework for different LLMs, KGs and prompting strategies without any additional training cost; 4) the performance of ToG with small LLM models could exceed large LLM such as GPT-4 in certain scenarios and this reduces the cost of LLM deployment and application. As a training-free method with lower computational cost and better generality, ToG achieves overall SOTA in 6 out of 9 datasets where most previous SOTAs rely on additional training.

**Innovation pattern:** Cross-Domain Synthesis (confidence: high)

Secondary patterns: Modular Pipeline Composition, Representation Shift & Primitive Recasting

*Reasoning:* Combines symbolic KG graph‑walking/path‑ranking methods with LLM chain‑of‑thought—a clear cross‑domain synthesis; also composes modular controller+retrieval pipeline and treats paths as structured primitives.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Chain‑of‑Thought Prompting Elicits Reasoning in Large Language Models** (2022)
- *Authors:* Wei et al.
- *Direct Connection:* Established that prompting LLMs to produce intermediate, stepwise chains of reasoning improves complex inference, which ToG leverages to have the LLM produce and evaluate candidate graph traversal steps (enabling beam search scoring and traceable rationales).

**Path Ranking Algorithm (PRA) for Relation Extraction and Link Prediction** (2011)
- *Authors:* Lao et al.
- *Direct Connection:* Introduced path‑based features and search over graph paths to support reasoning and link prediction, providing the technical precedent for exploring and ranking candidate reasoning paths on a KG that ToG operationalizes with LLM‑guided beam search.

### 🏷️ Inspiration

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023)
- *Authors:* Yao et al.
- *Direct Connection:* Proposed treating LLMs as agents that interleave reasoning (thoughts) and external actions, a concrete agentic interaction pattern that directly inspired ToG's design of an LLM agent executing iterative KG actions and using intermediate textual reasoning to guide graph search.

### 🏷️ Gap Identification

**Toolformer: Language Models Can Teach Themselves to Use Tools** (2023)
- *Authors:* Schick et al.
- *Direct Connection:* Showed effective LLM integration with external tools by training to call APIs, highlighting both the power and training cost of tool use and motivating ToG's objective of a plug‑and‑play, training‑free LLM↔KG interaction mechanism that still attains reliable external knowledge use.

### 🏷️ Baseline

**MINERVA: Learning to Reason over Paths in Knowledge Bases with Reinforcement Learning** (2018)
- *Authors:* Das et al.
- *Direct Connection:* Demonstrated a successful agent‑based approach that navigates KGs to answer queries by discovering paths, providing the primary baseline formulation of graph traversal for multi‑hop reasoning that ToG directly improves by using LLMs for action selection and traceable path outputs.

### 🏷️ Extension

**DeepPath: A Reinforcement Learning Method for Knowledge Graph Reasoning** (2017)
- *Authors:* Xiong et al.
- *Direct Connection:* Introduced the idea of framing multi‑hop question answering as an agent that walks a knowledge graph to find reasoning paths via learned policies, a paradigm that ToG inherits but replaces learned RL policies with an LLM-guided, training‑free beam search over the KG.

---

## Synthesis: How Prior Work Led to This Paper

Several prior lines of work supply the concrete techniques and gaps that underpin the present approach. Early KG reasoning systems such as DeepPath and MINERVA formulated multi‑hop question answering as an agent that traverses a knowledge graph to discover explanatory paths, establishing the agentic graph‑walking formulation and the importance of producing explicit multi‑step paths; these works define the baseline graph‑search objective that the new method seeks to retain while changing the controller. The Path Ranking Algorithm contributed the idea of treating graph paths as first‑class structured features and ranking candidate paths as part of reasoning, which motivates ToG’s focus on exploring and scoring multiple path candidates. In parallel, Chain‑of‑Thought prompting showed that LLMs can produce intermediate, human‑readable reasoning traces that improve complex inference, and ReAct demonstrated how LLMs can be cast as agents that interleave reasoning and environment actions; together these two ideas suggest using an LLM to both propose and justify graph traversal actions. Finally, Toolformer highlighted the benefits and costs of integrating LLMs with external tools, pointing to the value of a training‑free, plug‑and‑play integration. Combined, these threads expose an opportunity to replace learned RL controllers with an LLM agent that conducts beam search over KG paths, producing traceable, correctable, and high‑quality multi‑hop reasoning without additional task‑specific training—precisely the synthesis realized by the new Think‑on‑Graph paradigm.

---

*Analysis generated on: 2026-03-08T23:56:07.769752*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=2079, output=1088*
