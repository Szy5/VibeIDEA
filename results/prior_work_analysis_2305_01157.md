# Prior Work Analysis Report

## Target Paper

**Title:** Complex Logical Reasoning over Knowledge Graphs using Large Language Models

**arXiv ID:** [2305.01157](https://arxiv.org/abs/2305.01157)

**Abstract:** 
> Reasoning over knowledge graphs (KGs) is a challenging task that requires a deep understanding of the complex relationships between entities and the underlying logic of their relations. Current approaches rely on learning geometries to embed entities in vector space for logical query operations, but they suffer from subpar performance on complex queries and dataset-specific representations. In this paper, we propose a novel decoupled approach, Language-guided Abstract Reasoning over Knowledge graphs (LARK), that formulates complex KG reasoning as a combination of contextual KG search and logical query reasoning, to leverage the strengths of graph extraction algorithms and large language models (LLM), respectively. Our experiments demonstrate that the proposed approach outperforms state-of-the-art KG reasoning methods on standard benchmark datasets across several logical query constructs, with significant performance gain for queries of higher complexity. Furthermore, we show that the performance of our approach improves proportionally to the increase in size of the underlying LLM, enabling the integration of the latest advancements in LLMs for logical reasoning over KGs. Our work presents a new direction for addressing the challenges of complex KG reasoning and paves the way for future research in this area.

**Innovation pattern:** Gap-Driven Reframing (confidence: high)

Secondary patterns: Modular Pipeline Composition, Representation Shift & Primitive Recasting

*Reasoning:* Identifies limitations of geometry-based KG query methods and reframes the task toward LLM-based reasoning (gap-driven). Reuses decompositional/compositional querying (modular pipeline) and contrasts prior box/geometric representations (representation shift).

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Embedding Logical Queries on Knowledge Graphs** (2018)
- *Authors:* Will Hamilton et al.
- *Direct Connection:* Formulated the problem of answering first-order logical (FOL) queries over KGs via learned embeddings and established the query types and benchmark tasks (projection, intersection, union) that LARK adopts as its formal problem statement and evaluation targets.

### 🏷️ Inspiration

**Complex Query Answering with Neural Link Predictors (CQD)** (2021)
- *Authors:* Erik Arakelyan et al.
- *Direct Connection:* Demonstrated that decomposing complex KG queries into simpler sub-queries and composing intermediate answers improves performance, directly inspiring LARK's strategy of decomposing FOL queries into elementary operations and composing results—but replacing learned composition with LLM reasoning over retrieved subgraphs.

**Decomposed Prompting: A Modular Approach for Solving Complex Tasks** (2023)
- *Authors:* Tushar Khot et al.
- *Direct Connection:* Proposed a modular decomposition of complex tasks into sub-prompts and sequential solving; LARK adopts this concrete decomposed-prompting idea to deterministically split logical queries into single-operation LLM prompts and to schedule dependent prompts using cached intermediate answers.

**Least-to-most Prompting Enables Complex Reasoning in Large Language Models** (2023)
- *Authors:* Denny Zhou et al.
- *Direct Connection:* Provided empirical evidence that LLMs solve complex problems better when guided through an ordered sequence of simpler subtasks, motivating LARK's logically-ordered chain decomposition and sequential LLM answering to improve multi-step KG reasoning.

**Decoupling Knowledge from Memorization: Retrieval-Augmented Prompt Learning** (2022)
- *Authors:* Xiang Chen et al.
- *Direct Connection:* Presented retrieval-augmented prompting that augments LLM context with retrieved external information; LARK adapts this retrieval concept to KGs by deterministically extracting k-hop subgraph neighborhoods as context prompts rather than using semantic web retrieval.

### 🏷️ Gap Identification

**Beta Embeddings for Multi-hop Logical Reasoning in Knowledge Graphs** (2020)
- *Authors:* Hongyu Ren & Jure Leskovec
- *Direct Connection:* Provided a geometry-based method that uniquely handled negation in KG queries but exposed limitations in handling complex/negation queries and motivated LARK's move to an LLM-based inference that can answer negation and complex chains without learned geometric coverage.

### 🏷️ Baseline

**Query2Box: Reasoning over Knowledge Graphs in Vector Space using Box Embeddings** (2020)
- *Authors:* Hongyu Ren et al.
- *Direct Connection:* Introduced the box-geometry formulation and the comprehensive set of multi-operation query types and decomposition patterns that LARK uses for comparison and whose limitations (dataset-specific learned geometries) LARK explicitly seeks to overcome.

---

## Synthesis: How Prior Work Led to This Paper

Early work framed logical query answering over KGs as a geometric embedding problem and established the formal FOL query types and benchmarks: GQE defined the foundational task and evaluation constructs, while Query2Box operationalized multi-hop and set-operator queries using box geometries and provided the decomposition taxonomy used widely in the field. BetaE extended these geometry-based approaches to model uncertainty and notably added support for negation, revealing where geometry-based methods struggle on complex logical constructs. Parallel research on compositional methods (CQD) showed that decomposing complex KG queries into simpler sub-queries and composing intermediate answers yields measurable gains, a concrete strategy LARK reuses. Around the same time, work in prompting for LLMs demonstrated that complex reasoning benefits from explicit decomposition and ordered solving: least-to-most prompting and decomposed prompting proved that LLMs perform better when complex tasks are split into ordered subtasks and prior answers are used to inform later steps. Retrieval-augmented prompt learning introduced the practical pattern of supplying retrieved context to LLMs, which LARK adapts by deterministically extracting k-hop KG neighborhoods as context. Together, these threads—formal KG query formulations and benchmarks, geometric embedding baselines (and their limits on negation/complexity), decomposition-and-compose strategies, LLM decomposition prompting, and retrieval-augmented context—naturally pointed to a decoupled design: retrieve a compact, deterministic KG neighborhood and drive logically-decomposed LLM prompts that sequentially consume cached intermediate answers, enabling LARK’s core innovation of LLM-guided chain reasoning over KG subgraphs.

---

*Analysis generated on: 2026-03-09T00:26:12.310959*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=16658, output=1207*
