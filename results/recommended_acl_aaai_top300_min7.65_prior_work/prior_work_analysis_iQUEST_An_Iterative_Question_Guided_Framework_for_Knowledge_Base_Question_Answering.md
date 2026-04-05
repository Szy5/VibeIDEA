# Prior Work Analysis Report

## Target Paper

**Title:** iQUEST: An Iterative Question-Guided Framework for Knowledge Base Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> While Large Language Models (LLMs) excel at many natural language processing tasks, they often suffer from factual inaccuracies in knowledge-intensive scenarios.Integrating external knowledge resources, particularly knowledge graphs (KGs), provides a transparent and updatable foundation for more reliable reasoning.Knowledge Base Question Answering (KBQA), which queries and reasons over KGs, is central to this effort, especially for complex, multi-hop queries.However, multi-hop reasoning poses two key challenges: (1) maintaining coherent reasoning paths, and (2) avoiding prematurely discarding critical multi-hop connections.To address these issues, we introduce iQUEST, a question-guided KBQA framework that iteratively decomposes complex queries into simpler sub-questions, ensuring a structured and focused reasoning trajectory.Additionally, we integrate a Graph Neural Network (GNN) to look ahead and incorporate 2hop neighbor information at each reasoning step.This dual approach strengthens the reasoning process, enabling the model to explore viable paths more effectively.Detailed experiments demonstrate the consistent improvement delivered by iQUEST across four benchmark datasets and four LLMs.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**The Web as a Knowledge-Base for Answering Complex Questions (ComplexWebQuestions)** (2018) [[arXiv](https://arxiv.org/abs/1803.06643)]
- *Authors:* Alon Talmor and Jonathan Berant
- *Direct Connection:* ComplexWebQuestions established the multi-hop, compositional KBQA setting that necessitates decomposition and explicit reasoning, directly framing the problem iQUEST targets.

### 🏷️ Inspiration

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* iQUEST adopts CoT’s explicit, step-wise prompting paradigm to structure intermediate reasoning, iteratively updating prompts with sub-questions and partial answers at each hop.

### 🏷️ Gap Identification

**Chain-of-Question: A Progressive Question Decomposition Approach for Complex Knowledge Base Question Answering** (2024)
- *Authors:* Peng Yixing et al.
- *Direct Connection:* By performing a mostly one-off progressive decomposition before reasoning, Chain-of-Question exposes the need for adaptive, state-dependent sub-question generation that iQUEST implements at each step.

**Question Decomposition Tree for Answering Complex Questions over Knowledge Bases** (2023)
- *Authors:* Xiang Huang et al.
- *Direct Connection:* QDT preserves entity semantics with delimiter-based splits but lacks adaptive, iterative guidance during traversal, a limitation directly addressed by iQUEST’s step-by-step sub-questioning guided by evolving context.

### 🏷️ Baseline

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph** (2024)
- *Authors:* Jiashuo Sun et al.
- *Direct Connection:* As a primary LLM-agent baseline that explores KGs from a topic node using largely local signals, ToG motivates iQUEST’s improvements in maintaining coherent paths and avoiding 1-hop myopia via iterative guidance and 2-hop lookahead.

**Interactive-KBQA: Multi-turn Interactions for Knowledge Base Question Answering with Large Language Models** (2024)
- *Authors:* Guanming Xiong et al.
- *Direct Connection:* Interactive-KBQA’s iterative SPARQL refinement over primarily 1-hop neighbors serves as a comparator whose limitations in long-horizon coherence and deeper path exploration iQUEST directly addresses.

### 🏷️ Extension

**Inductive Representation Learning on Large Graphs (GraphSAGE)** (2017) [[arXiv](https://arxiv.org/abs/1706.02216)]
- *Authors:* Will Hamilton et al.
- *Direct Connection:* iQUEST extends GraphSAGE-style neighborhood aggregation by using it to fuse 2-hop signals into 1-hop neighbor representations for relevance scoring conditioned on each sub-question.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-Thought prompting introduced the idea that large language models become more reliable reasoners when guided through explicit, stepwise intermediate steps, providing a general recipe for decomposing complex queries into tractable subproblems. In knowledge-graph QA, Think-on-Graph operationalized LLMs as agents that traverse from a topic entity, but largely relied on local cues, making exploration vulnerable to path drift and premature pruning. Interactive-KBQA similarly used multi-turn LLM interactions to iteratively refine SPARQL queries, yet its reliance on 1-hop neighborhoods limited deeper lookahead. Question Decomposition Tree showed how delimiter-based splitting can preserve entity semantics, but it performs a one-time segmentation rather than adapting to intermediate evidence. Chain-of-Question further advanced progressive decomposition, pairing an LLM with a smaller model, but still did not generate sub-questions dynamically at each hop. Meanwhile, GraphSAGE provided a practical neighborhood aggregation mechanism to inject multi-hop structure into node representations by melding k-hop neighbors’ signals into richer local embeddings. ComplexWebQuestions established the need for these capabilities by curating compositional, multi-hop queries that require both decomposition and robust multi-hop traversal.
Collectively, these works revealed a gap: one-off decomposition and 1-hop–centric exploration struggle to maintain coherent multi-hop paths and often discard promising connections too early. The natural next step was to combine CoT-style, adaptive sub-questioning at every hop—continually informed by the evolving context—with a learned lookahead that carries 2-hop neighborhood signals into each selection decision. By fusing dynamic, question-guided prompting with GraphSAGE-like aggregation for path-aware relevance scoring, the new framework preserves focus across hops while reducing brittle pruning, making multi-hop KB reasoning more reliable on complex benchmarks.

---

*Analysis generated on: 2026-04-04T22:33:00.922009*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
