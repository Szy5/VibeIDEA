# Prior Work Analysis Report

## Target Paper

**Title:** Improving Complex Reasoning over Knowledge Graph with Logic-Aware Curriculum Tuning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Answering complex queries over incomplete knowledge graphs (KGs) is a challenging job. Most previous works have focused on learning entity/relation embeddings and simulating first-order logic operators with various neural networks. However, they are bottlenecked by the inability to share world knowledge to improve logical reasoning, thus resulting in suboptimal performance. In this paper, we propose a complex reasoning schema over KG upon large language models (LLMs), containing a curriculum-based logical-aware instruction tuning framework, named LACT. Specifically, we augment the arbitrary first-order logical queries via binary tree decomposition, to stimulate the reasoning capability of LLMs. To address the difficulty gap among different types of complex queries, we design a simple and flexible logic-aware curriculum learning framework. Experiments across widely used datasets demonstrate that LACT has substantial improvements~(brings an average +5.5% MRR score) over advanced methods, achieving the new state-of-the-art.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Embedding Logical Queries on Knowledge Graphs** (2018)
- *Authors:* Hamilton et al.
- *Direct Connection:* This work formalized answering EFO1 logical queries via computation graphs (DAGs) over KGs, providing the query structures and graph view that LACT textualizes and converts into logic-equivalent trees for LLM supervision.

**Beta Embeddings for Multi-Hop Logical Reasoning in Knowledge Graphs** (2020)
- *Authors:* Ren and Leskovec
- *Direct Connection:* By introducing EFO1 reasoning with negation and highlighting divergence mitigated by DNF reformulation, this paper set the problem formulation and limitations that LACT sidesteps by avoiding neural operator learning and instead transforming queries into logic-equivalent trees.

**Curriculum Learning** (2009)
- *Authors:* Bengio et al.
- *Direct Connection:* This seminal work introduced training from easy to hard, which LACT operationalizes via a logic-aware curriculum that measures difficulty by the number of decomposed sub-queries and mixes easy/medium/hard stages.

### 🏷️ Inspiration

**Complex Query Answering with Neural Link Predictors** (2020)
- *Authors:* Arakelyan et al.
- *Direct Connection:* It showed that decomposing complex logical queries into simpler one-hop subproblems reduces difficulty, directly inspiring LACT’s binary-tree-based decomposition used to create stepwise reasoning chains for instruction tuning.

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2201.11903)]
- *Authors:* Wei et al.
- *Direct Connection:* It established that step-by-step rationales boost LLM reasoning, motivating LACT to embed explicit decomposition chains in the supervision signal rather than relying solely on in-context prompting.

### 🏷️ Gap Identification

**Complex Logical Reasoning over Knowledge Graphs using Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2305.01157)]
- *Authors:* Choudhary and Reddy
- *Direct Connection:* This initial LLM-based approach relied on prompting with manual query handling and incurred high inference cost and hallucination, directly motivating LACT’s fine-tuned, KG-informed, curriculum-based framework on open models.

### 🏷️ Extension

**Answering complex logical queries on knowledge graphs via query computation tree optimization** (2023)
- *Authors:* Bai et al.
- *Direct Connection:* By introducing query computation tree optimization, this work provided the tree-based view of logical queries that LACT extends by systematically converting DAGs to binary computation trees and using reverse-level traversal to derive training step sequences.

---

## Synthesis: How Prior Work Led to This Paper

Early work formalized complex logical reasoning on knowledge graphs by casting EFO1 queries as computation graphs, defining standard query structures and DAG-based execution (Hamilton et al., 2018). Subsequent advances modeled negation and multi-hop reasoning via Beta distributions, while emphasizing DNF reformulations to avoid embedding divergence, setting both the expressive target and practical constraints of operator-learning approaches (Ren and Leskovec, 2020). In parallel, neural systems showed that reducing query difficulty by decomposing complex queries into simpler one-hop subproblems improves performance, grounding a decomposition paradigm for logic queries (Arakelyan et al., 2020). That perspective was refined with query computation tree optimization, which explicitly reified logical queries as trees to streamline reasoning over KGs (Bai et al., 2023). Independently, chain-of-thought prompting demonstrated that making intermediate steps explicit improves LLM reasoning, encouraging stepwise supervision as a mechanism for enhancing complex inference (Wei et al., 2022). The learning dynamics behind such steps naturally align with curriculum learning’s principle of progressing from easy to hard examples to stabilize training and improve generalization (Bengio et al., 2009). Meanwhile, an early attempt to apply LLMs to complex KG queries via prompting exposed practical limitations—hallucination, manual query-type handling, and cost-heavy multi-step prompting—highlighting the need for fine-tuned, logic-aware solutions (Choudhary and Reddy, 2023). Together, these works revealed a path: represent logical queries as trees, decompose them into explicit reasoning steps, and train LLMs with a curriculum. The natural next step is to synthesize KG-aware instruction tuning with binary-tree-based step supervision and a difficulty-aware schedule, thereby leveraging world knowledge and stabilizing learning for complex logical reasoning.

---

*Analysis generated on: 2026-04-05T11:37:53.879153*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
