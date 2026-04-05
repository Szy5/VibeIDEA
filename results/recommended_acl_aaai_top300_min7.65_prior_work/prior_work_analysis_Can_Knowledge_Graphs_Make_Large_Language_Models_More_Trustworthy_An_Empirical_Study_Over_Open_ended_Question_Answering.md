# Prior Work Analysis Report

## Target Paper

**Title:** Can Knowledge Graphs Make Large Language Models More Trustworthy? An Empirical Study Over Open-ended Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent works integrating Knowledge Graphs (KGs) have shown promising improvements in enhancing the reasoning capabilities of Large Language Models (LLMs).However, existing benchmarks primarily focus on closedended tasks, leaving a gap in evaluating performance on more complex, real-world scenarios.This limitation also hinders a thorough assessment of KGs' potential to reduce hallucinations in LLMs.To address this, we introduce OKGQA 1 , a new benchmark specifically designed to evaluate LLMs augmented with KGs in open-ended, real-world question answering settings.OKGQA reflects practical complexities through diverse question types and incorporates metrics to quantify both hallucination rates and reasoning improvements in LLM+KG models.To consider the scenarios in which KGs may contain varying levels of errors, we propose a benchmark variant, OKGQA-P, to assess model performance when the semantics and structure of KGs are deliberately perturbed and contaminated.In this paper, we aims to (1) explore whether KGs can make LLMs more trustworthy in an open-ended setting, and (2) conduct a comparative analysis to shed light on method design.We believe this study can facilitate a more complete performance comparison and encourages continuous improvement in integrating KGs with LLMs to mitigate hallucination, and make LLMs more trustworthy.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**The Value of Semantic Parse Labeling for Knowledge Base Question Answering** (2016)
- *Authors:* Wen-tau Yih et al.
- *Direct Connection:* This work established the closed-ended KGQA setting and popularized extracting 2-hop KG neighborhoods (e.g., WebQSP), a subgraph-sampling practice directly adopted for OKGQA’s DBpedia subgraph construction while motivating the shift to open-ended answers.

**FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation** (2023)
- *Authors:* Sewon Min et al.
- *Direct Connection:* FActScore’s atomic-fact decomposition and verification procedure is directly used to quantify hallucination in OKGQA’s open-ended answers.

**Long-form Factuality in Large Language Models** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2403.18802)]
- *Authors:* Jerry Wei et al.
- *Direct Connection:* The SAFE agentic verification framework from this work is adopted to assess factual support in long-form outputs, enabling OKGQA’s hallucination measurement.

### 🏷️ Gap Identification

**The Web as a Knowledge-Base for Answering Complex Questions** (2018)
- *Authors:* Alon Talmor et al.
- *Direct Connection:* By framing complex question answering with fixed outputs or logical forms, this benchmark exemplified the closed-ended evaluation gap that OKGQA explicitly addresses to expose hallucinations in open-ended long-form responses.

### 🏷️ Baseline

**Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2212.10509)]
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* IRCoT serves as the primary non-KG RAG baseline (retrieving Wikipedia text) against which the KG-based triplet/path/subgraph methods are compared to demonstrate improved factuality and hallucination control.

### 🏷️ Extension

**Learning to Deceive Knowledge Graph Augmented Models via Targeted Perturbation** (2020) [[arXiv](https://arxiv.org/abs/arXiv:2010.12872)]
- *Authors:* Mrigank Raman et al.
- *Direct Connection:* OKGQA-P extends this paper’s perturbation operators (relation swapping/replacement, edge rewiring/deletion) and semantic/structural similarity metrics (ATS, SC2D, SD2) to evaluate robustness under contaminated KGs.

**G-Retriever: Retrieval-Augmented Generation for Textual Graph Understanding and Question Answering** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2402.07630)]
- *Authors:* Xiaoxin He et al.
- *Direct Connection:* OKGQA’s subgraph-retrieval variant builds directly on G-Retriever’s Prize-Collecting Steiner Tree (PCST) approach to assemble compact, high-relevance graph contexts for generation.

---

## Synthesis: How Prior Work Led to This Paper

Closed-ended KGQA benchmarks such as Yih et al. introduced semantic parse-based evaluation and popularized extracting 2-hop neighborhoods to form manageable subgraphs, establishing a practical yet constrained setting. Talmor and Berant broadened question complexity but still evaluated through fixed outputs or logical forms, leaving limited visibility into how models might fabricate content when answers must be composed freely. To evaluate factuality in genuinely long-form outputs, Min et al. provided FActScore, which decomposes responses into atomic claims and verifies each against an external source. Wei et al. further operationalized long-form factuality with the SAFE agentic verifier, using iterative web search to check support for claims, offering a complementary lens on hallucination. On the retrieval side for graph contexts, He et al. proposed PCST-based subgraph assembly to maximize relevance while keeping context compact, offering a principled way to supply graph evidence to LLMs. Finally, Raman et al. demonstrated how to perturb KGs with relation swaps/replacements and edge rewiring/deletions, and introduced semantic/structural similarity metrics (ATS, SC2D, SD2) to quantify KG degradation.
Together, these works revealed both the gap—closed-ended KGQA hides hallucination—and the tools to fill it: atomic long-form factuality metrics (FActScore, SAFE), principled subgraph retrieval (PCST), and controlled KG perturbations with measurable drift. Building on this foundation, the current study formulates an open-ended KGQA benchmark that measures hallucination directly, compares KG-based retrieval variants against a strong IRCoT baseline, and introduces a perturbed-KG setting using Raman et al.’s operators and metrics to assess robustness, making the trustworthiness question empirically testable.

---

*Analysis generated on: 2026-04-05T11:38:14.185902*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
