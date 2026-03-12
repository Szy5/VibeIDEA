# Prior Work Analysis Report

## Target Paper

**Title:** GraphDancer: Training LLMs to Explore and Reason over Graphs via Curriculum Reinforcement Learning

**arXiv ID:** [2602.02518](https://arxiv.org/abs/2602.02518)

**Abstract:** 
> Large language models (LLMs) increasingly rely on external knowledge to improve factuality, yet many real-world knowledge sources are organized as heterogeneous graphs rather than plain text. Reasoning over such graph-structured knowledge poses two key challenges: (1) navigating structured, schema-defined relations requires precise function calls rather than similarity-based retrieval, and (2) answering complex questions often demands multi-hop evidence aggregation through iterative information seeking. We propose GraphDancer, a reinforcement learning (RL) framework that teaches LLMs to navigate graphs by interleaving reasoning and function execution. To make RL effective for moderate-sized LLMs, we introduce a graph-aware curriculum that schedules training by the structural complexity of information-seeking trajectories using an easy-to-hard biased sampler. We evaluate GraphDancer on a multi-domain benchmark by training on one domain only and testing on unseen domains and out-of-distribution question types. Despite using only a 3B backbone, GraphDancer outperforms baselines equipped with either a 14B backbone or GPT-4o-mini, demonstrating robust cross-domain generalization of graph exploration and reasoning skills. Our code and models can be found at https://yuyangbai.com/graphdancer/ .

**Innovation pattern:** Gap-Driven Reframing (confidence: high)

Secondary patterns: Data-Centric Optimization & Active Sampling, Representation Shift & Primitive Recasting

*Reasoning:* Starts from a concrete empirical gap (linearized/RAG retrieval fails on heterogeneous graphs) and reframes the task with schema-aware executable graph APIs plus a curriculum sampling strategy—combining data-centric/active sampling and a representation shift to typed graph primitives.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Graph chain-of-thought: Augmenting large language models by reasoning on graphs** (2024)
- *Authors:* Bowen Jin et al.
- *Direct Connection:* Introduced the iterative, function-call-driven graph interaction protocol and released GRBench (the multi-domain graph QA benchmark and environment design including typed graph functions) that this work adopts as the problem formulation, evaluation suite, and the exact graph function API to be optimized via RL.

### 🏷️ Inspiration

**Search-R1: Training LLMs to reason and leverage search engines with reinforcement learning** (2025)
- *Authors:* Bowen Jin et al.
- *Direct Connection:* Formulated information-seeking over external resources as an MDP and used RL to train LLMs to interleave reasoning with external actions, inspiring the formal MDP viewpoint where graph function calls are actions and observations are environment responses optimized by policy learning.

**DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning** (2025)
- *Authors:* Daya Guo et al.
- *Direct Connection:* Showed that reinforcement learning with verifiable, rule-based rewards can substantially improve multi-step reasoning and information‑seeking behavior in LLMs, motivating the use of rule-based accuracy/format rewards and KL-regularized policy optimization for internalizing multi-round graph exploration.

### 🏷️ Gap Identification

**Language is all a graph needs** (2024)
- *Authors:* Ruosong Ye et al.
- *Direct Connection:* Demonstrated linearized retrieval/augmentation of graphs for single-pass LLM answering and exposed shortcomings of similarity-based text retrieval on heterogeneous graph queries, motivating precise, schema-aware function calls and multi‑round exploration instead of flat RAG-style retrieval.

**Toolformer: Language models can teach themselves to use tools** (2023)
- *Authors:* Timo Schick et al.
- *Direct Connection:* Demonstrated SFT/self-supervised approaches for exposing tool use to LLMs but also highlighted limits of supervised/tool‑annotation-centric training to generalize across unseen tool schemas, motivating an RL-based training regime to internalize robust, generalizable function‑call behaviors on graphs.

### 🏷️ Extension

**Curriculum reinforcement learning from easy to hard tasks improves llm reasoning** (2025)
- *Authors:* Shubham Parashar et al.
- *Direct Connection:* Proposed Gaussian/easy-to-hard curriculum schedules for RL training of LLMs and sampling-based curriculum machinery that this work directly extends into a graph-aware curriculum by defining structural difficulty levels (S-/E‑rounds) and introducing a biased mixture scheduler to stabilize exposure to hard multi-hop graph traces.

---

## Synthesis: How Prior Work Led to This Paper

Graph chain-of-thought (Jin et al., 2024) established the concrete problem setup used here: an LLM alternates between natural-language reasoning and typed graph function calls, and it released GRBench plus the exact deterministic graph-function API (RetrieveNode, NeighborCheck, NodeFeature, NodeDegree) that this line of work uses as the environment. Ye et al. (2024) empirically showed that linearized retrieval over graphs and RAG-style augmentation fail to handle heterogeneous, schema-driven relations and multi-hop aggregation, calling for schema-aware, executable access. Parashar et al. (2025) developed Gaussian easy-to-hard curriculum sampling for RL on LLM reasoning tasks, providing the sampling primitives and scheduling intuition that were adapted and extended into a graph-aware structural difficulty decomposition and a biased-mixture scheduler. Concurrent RL-for-retrieval work (Jin et al., 2025; Guo et al., 2025) framed information seeking as an MDP and demonstrated that verifiable, rule-based rewards plus RL can elicit robust multi-step search/reasoning behavior, directly informing the choice to optimize a policy with rule-based accuracy/format rewards and KL regularization. Finally, Toolformer (Schick et al., 2023) exposed the limitations of purely supervised/self-supervised tool-use training, motivating a shift to RL to better generalize to unseen schemas. Together these strands revealed a clear opportunity: the graph-interaction API and benchmark existed, prompting baselines relied on prompting or SFT and curricula for generic reasoning existed, and RL had proven effective for multi-step information seeking—so the natural next step was to synthesize a graph-structured MDP, rule-based RL objective, and a curriculum that is aware of graph structural difficulty to train LLMs to internalize precise, multi-round graph exploration and reasoning behaviors.

---

*Analysis generated on: 2026-03-09T09:28:53.670576*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=17086, output=1199*
