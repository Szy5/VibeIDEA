# Prior Work Analysis Report

## Target Paper

**Title:** Encoder of Thoughts: Enhancing Planning Ability in Language Agents Through Structural Embedding

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLMs), when combined with agent mechanisms, show great promise in applications requiring robust planning ability, such as financial analysis and medical diagnostics. However, the increasingly complex reasoning structures designed to enhance the planning ability of language agents often exceed the processing and comprehension capabilities of LLMs, thereby limiting their effectiveness. To address these challenges, we introduce the Encoder of Thoughts (EoT), a novel reasoning structure modeling method based on graph neural networks. EoT processes the reasoning structures of planning methods through a plug-and-play structural encoder and aligns these structural information with the input space of LLMs, enabling seamless integration with existing language agents. Experiments on multi-step reasoning and plan generation demonstrate that EoT significantly improves the performance of language agents. Moreover, EoT demonstrated stable results when combined with different LLMs and planning algorithms, further underscoring its potential for broader application.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Graph of Thoughts: Solving Elaborate Problems with Large Language Models** (2024) [[arXiv](https://arxiv.org/abs/2308.09687)]
- *Authors:* Maciej Besta et al.
- *Direct Connection:* Formalizes reasoning processes as general graphs rather than trees, directly motivating EoT’s decision to model action/thought structures as graphs that need efficient, non-textual representation.

### 🏷️ Inspiration

**GraphGPT: Graph Instruction Tuning for Large Language Models** (2024)
- *Authors:* Jiaqi Tang et al.
- *Direct Connection:* Shows that aligning graph encodings with LLM inputs improves graph-centric tasks, inspiring EoT’s plug-and-play projection of GNN-derived graph features into the LLM’s input space for planning.

### 🏷️ Gap Identification

**GPT4Graph: Can Large Language Models Understand Graph Structured Data? An Empirical Evaluation and Benchmarking** (2023) [[arXiv](https://arxiv.org/abs/2305.15066)]
- *Authors:* Jiaqi Guo et al.
- *Direct Connection:* Finds that LLMs struggle with graph-structured inputs via natural language prompts and are highly sensitive to input format, motivating EoT’s replacement of verbose textual graph descriptions with compact structural embeddings.

**When is Tree Search Useful for LLM Planning? It Depends on the Discriminator** (2024) [[arXiv](https://arxiv.org/abs/2402.10890)]
- *Authors:* Zhuohan Chen et al.
- *Direct Connection:* Shows that the gains from tree search hinge on reliable state evaluation/discrimination, highlighting LLMs’ weak structural understanding and motivating EoT’s graph-derived embeddings to stabilize planning.

### 🏷️ Baseline

**Tree of Thoughts: Deliberate Problem Solving with Large Language Models** (2024) [[arXiv](https://arxiv.org/abs/2305.10601)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* Introduces search over intermediate 'thoughts' with BFS-style expansion and scoring, which EoT plugs into for both training data construction and evaluation and serves as the primary planning baseline EoT augments.

**Reasoning with Language Model is Planning with World Model** (2023) [[arXiv](https://arxiv.org/abs/2305.14992)]
- *Authors:* Shibo Hao et al.
- *Direct Connection:* Provides the MCTS-based planning loop and reward settings adopted in experiments, forming the main MCTS competitor whose reliance on text-only state representations EoT directly addresses by injecting structural embeddings.

### 🏷️ Extension

**GraphLLM: Boosting Graph Reasoning Ability of Large Language Model** (2023) [[arXiv](https://arxiv.org/abs/2310.05845)]
- *Authors:* Zhiqiang Chai et al.
- *Direct Connection:* Demonstrates integrating a GNN encoder with an LLM to inject graph structural signals, which EoT extends by encoding planning/action graphs into token-aligned embeddings to guide action generation and evaluation.

---

## Synthesis: How Prior Work Led to This Paper

Tree of Thoughts established deliberate problem solving by expanding and scoring intermediate thoughts via breadth-first search, making the planning process an explicit search over structured intermediate states. Reasoning via Planning then embedded language models within Monte Carlo Tree Search, showing how selection, simulation, and backpropagation can guide long-horizon decisions, while relying on text-form planning states and rewards. Graph of Thoughts generalized this perspective by casting reasoning as arbitrary graphs, enabling richer dependencies than trees but further inflating prompt complexity as structures grew. Parallel research on graph–LLM integration showed how to represent graph structure for language models: GraphLLM injected GNN-derived structural features into LLMs to improve node and graph reasoning, and GraphGPT aligned graph encodings and instructions with LLM inputs to enhance graph-centric tasks. Empirical findings from GPT4Graph demonstrated that LLMs’ graph understanding is brittle and prompt-format dependent, and analyses of tree search utility revealed that unreliable state evaluation can blunt planning benefits, underscoring LLMs’ limited structural comprehension.
Collectively, these works revealed both the promise of search-based thought graphs and the bottleneck of conveying structure through natural language. A natural next step was to preserve the successful BFS/MCTS planning loops of ToT and RAP while replacing unwieldy textual graph descriptions with compact, learned structural signals. By extending GNN-to-LLM integration ideas to encode action/thought graphs into token-aligned embeddings, the current work fuses structural understanding with the standard agent workflow, improving state estimation and action selection without altering the underlying search algorithms.

---

*Analysis generated on: 2026-04-05T11:54:15.630293*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
