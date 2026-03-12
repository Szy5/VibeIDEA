# Prior Work Analysis Report

## Target Paper

**Title:** RTQA : Recursive Thinking for Complex Temporal Knowledge Graph Question Answering with Large Language Models

**arXiv ID:** [2509.03995v1](https://arxiv.org/abs/2509.03995v1)

**Abstract:** 
> Current temporal knowledge graph question answering (TKGQA) methods primarily focus on implicit temporal constraints, lacking the capability of handling more complex temporal queries, and struggle with limited reasoning abilities and error propagation in decomposition frameworks. We propose RTQA, a novel framework to address these challenges by enhancing reasoning over TKGs without requiring training. Following recursive thinking, RTQA recursively decomposes questions into sub-problems, solves them bottom-up using LLMs and TKG knowledge, and employs multi-path answer aggregation to improve fault tolerance. RTQA consists of three core components: the Temporal Question Decomposer, the Recursive Solver, and the Answer Aggregator. Experiments on MultiTQ and TimelineKGQA benchmarks demonstrate significant Hits@1 improvements in "Multiple" and "Complex" categories, outperforming state-of-the-art methods. Our code and data are available at https://github.com/zjukg/RTQA.

**Innovation pattern:** Modular Pipeline Composition (confidence: high)

Secondary patterns: Cross-Domain Synthesis, Inference-Time Control & Guided Sampling

*Reasoning:* Focuses on decomposed, modular prompting/pipeline for temporal KGQA (tree-of-thought style), combining retrieval+LLM techniques (cross-domain synthesis) and inference-time guided reasoning.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Multi-granularity temporal question answering over knowledge graphs** (2023)
- *Authors:* Ziyang Chen et al.
- *Direct Connection:* Introduced the MultiTQ formulation/dataset and multi-granular temporal QA categories (year/month/day) that RTQA uses for evaluation and adopts as the problem formulation backbone for multi-granular temporal reasoning.

**TEQUILA: temporal question answering over knowledge bases** (2018)
- *Authors:* Zhen Jia et al.
- *Direct Connection:* Pioneered semantic-parsing approaches that map temporal natural language questions into executable logical forms, establishing the semantic-parsing lineage and motivating RTQA’s choice to avoid brittle logical-form generation through robust LLM-based recursive decomposition and retrieval.

### 🏷️ Inspiration

**Decomposed prompting: A modular approach for solving complex tasks** (2023)
- *Authors:* Tushar Khot et al.
- *Direct Connection:* Introduced the explicit decomposed-prompting paradigm for breaking complex tasks into modular subproblems, directly inspiring RTQA’s design of LLM-driven temporal question decomposition and the use of systematic prompts to generate sub-questions.

### 🏷️ Gap Identification

**CronKGQA: Question answering over temporal knowledge graphs** (2021)
- *Authors:* Apoorv Saxena et al.
- *Direct Connection:* Presented embedding-based temporal KGQA techniques and exposed their limitations on complex, multi-constraint temporal queries, a shortcoming RTQA explicitly targets by combining decomposition, retrieval, and LLM reasoning.

### 🏷️ Baseline

**TimeR4: Time-aware retrieval-augmented large language models for temporal knowledge graph question answering** (2024)
- *Authors:* Xinying Qian et al.
- *Direct Connection:* Established a state-of-the-art LLM + retrieval approach for TKGQA that RTQA directly compares with and improves upon, motivating RTQA’s stronger handling of compound temporal constraints and multi-hop temporal queries.

### 🏷️ Extension

**Probabilistic tree-of-thought reasoning for answering knowledge-intensive complex questions** (2023)
- *Authors:* Shulin Cao et al.
- *Direct Connection:* Provided tree-of-thought / structured multi-step decomposition guidelines and prompt engineering that RTQA adapts and extends to temporal scenarios (explicitly cited as the basis for RTQA’s decomposition prompt design and hierarchical solving strategy).

---

## Synthesis: How Prior Work Led to This Paper

Recent advances established two complementary lines of work relevant to temporal KGQA: modular decomposition of complex tasks and retrieval-augmented LLM reasoning over knowledge. Decomposed prompting (Khot et al., 2023) introduced the modular, few-shot prompting paradigm for splitting hard problems into subproblems, while Cao et al. (2023) supplied concrete tree-of-thought style decomposition guidelines and prompt templates that make hierarchical, multi-step solving reliable; RTQA explicitly adapts these decomposition and prompting ideas for temporal constraints. On the TKGQA side, TimeR4 (Qian et al., 2024) demonstrated the power of time-aware retrieval + LLMs and served as the immediate SOTA baseline whose failure modes (compound temporal constraints, error cascading) motivated improvements. Foundational resources such as MultiTQ (Chen et al., 2023) defined the multi-granular temporal QA formulation and evaluation splits RTQA adopts, while earlier TKGQA approaches—CronKGQA (Saxena et al., 2021) and semantic-parsing systems like TEQUILA (Jia et al., 2018)—highlighted key gaps: embedding or rigid logical-form methods fail on multi-constraint, multi-hop temporal reasoning and brittle decomposition. Taken together, these threads revealed an opportunity to synthesize structured decomposition (tree-of-thought style prompts), retrieval-grounded LLM reasoning, and robustness mechanisms; RTQA follows this natural next step by implementing recursive bottom-up solving over LLM-generated temporal sub-questions and adding multi-path answer aggregation to mitigate error propagation and address the specific weaknesses observed in prior TKGQA methods.

---

*Analysis generated on: 2026-03-09T09:27:34.201132*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=18526, output=1083*
