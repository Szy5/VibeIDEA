# Prior Work Analysis Report

## Target Paper

**Title:** Inductive Learning of Logical Theories with LLMs: A Expressivity-graded Analysis

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> This work presents a novel systematic methodology to analyse the capabilities and limitations of Large Language Models (LLMs) with feedback from a formal inference engine, on logic theory induction. The analysis is complexity-graded w.r.t. rule dependency structure, allowing quantification of specific inference challenges on LLM performance. Integrating LLMs with formal methods is a promising frontier in the Natural Language Processing field, as an important avenue for improving model inference control and explainability. In particular, inductive learning over complex sets of facts and rules, poses unique challenges for current autoregressive models, as they lack explicit symbolic grounding. While they can be complemented by formal systems, the properties delivered by LLMs regarding inductive learning, are not well understood and quantified. Empirical results indicate that the largest LLMs can achieve competitive results against a SOTA Inductive Logic Programming (ILP) system baseline, but also that tracking long predicate relationship chains is a more difficult obstacle than theory complexity for LLMs.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Inductive logic programming** (1991)
- *Authors:* Stephen Muggleton et al.
- *Direct Connection:* This work defined the ILP problem of inducing a hypothesis H such that H ∪ BK entails positives and excludes negatives, which is the exact formal objective used for the LLM theory generation and Prolog-based evaluation in this paper.

**Synthetic Datasets and Evaluation Tools for Inductive Neural Reasoning** (2021)
- *Authors:* Claudio Cornelio et al.
- *Direct Connection:* It introduced the RuDaS generator and the expressivity taxonomy (CHAIN, RDG, DRDG, and variants) that this paper directly adopts to synthesize datasets and grade theory induction difficulty by rule-dependency structure.

### 🏷️ Inspiration

**Verification and Refinement of Natural Language Explanations through LLM-Symbolic Theorem Proving** (2024) [[arXiv](https://arxiv.org/abs/2405.01379)]
- *Authors:* Xue Quan et al.
- *Direct Connection:* This work’s LLM-in-the-loop verification and iterative symbolic refinement with external provers directly inspires the paper’s design of a formal inference module that critiques and steers LLM-generated theories.

**Large Language Models can Learn Rules (Hypotheses-to-Theories)** (2024) [[arXiv](https://arxiv.org/abs/2310.07064)]
- *Authors:* Zhengyang Zhu et al.
- *Direct Connection:* Its generate–verify pipeline showing LLMs can induce explicit rules motivates the paper’s approach of prompting LLMs to produce Prolog theories that are verified and refined via a formal interpreter.

### 🏷️ Gap Identification

**Faith and Fate: Limits of Transformers on Compositionality** (2023) [[arXiv](https://arxiv.org/abs/2305.18654)]
- *Authors:* Nouha Dziri et al.
- *Direct Connection:* By documenting transformers’ struggles with compositional reasoning and long dependency chains, it motivates the paper’s expressivity-graded analysis and the focus on chain-depth and dependency complexity.

### 🏷️ Baseline

**Learning programs by learning from failures** (2021)
- *Authors:* Andrew Cropper et al.
- *Direct Connection:* Popper serves as the primary SOTA ILP system baseline against which the LLM+Prolog approach is compared across expressivity levels, framing the competitive target for theory induction quality.

### 🏷️ Extension

**Self-Refine: Iterative Refinement with Self-Feedback** (2023) [[arXiv](https://arxiv.org/abs/2303.17651)]
- *Authors:* Aman Madaan et al.
- *Direct Connection:* The paper’s iterative refinement loop extends Self-Refine’s self-critique template by replacing self-generated feedback with formal feedback from a Prolog inference engine to guide successive theory updates.

---

## Synthesis: How Prior Work Led to This Paper

Inductive Logic Programming established the learning objective of finding a hypothesis H that, together with background knowledge, entails all positives while excluding negatives, providing the formal backbone for logic theory induction. Building on this, a practical route to stress-test inductive reasoning was offered by a synthetic generator and taxonomy that stratify rule structures into CHAIN, RDG, DRDG and recursive/mixed variants, enabling controlled variation of rule-dependency expressivity. On the algorithmic side, Popper introduced a state-of-the-art ILP system based on learning-from-failures, setting a rigorous baseline for the quality and efficiency of learned logic programs. Parallel advances in LLM-guided reasoning proposed iterative refinement procedures where a model critiques and improves its own outputs, while complementary LLM-symbolic work showed that integrating external theorem provers can verify and refine generated content. Demonstrating the feasibility of rule learning with LLMs, a generate–verify pipeline showed that explicit rule libraries can be induced and validated, bridging free-form text models and formal rule induction. In contrast, analyses of transformer compositionality highlighted persistent failures on long relational chains and compositional generalization. Together, these threads reveal both a methodological opportunity and a diagnostic need: combine ILP’s formal objective with expressivity-graded synthetic tasks, and couple LLMs to a formal inference engine in an iterative loop. The resulting synthesis—LLM-driven theory generation refined by Prolog feedback and evaluated across graded rule-dependency classes—naturally follows from these foundations, allowing direct comparison to Popper while quantifying where LLMs falter (e.g., chain depth) versus where they remain robust under noise and complexity.

---

*Analysis generated on: 2026-04-05T11:59:53.896333*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
