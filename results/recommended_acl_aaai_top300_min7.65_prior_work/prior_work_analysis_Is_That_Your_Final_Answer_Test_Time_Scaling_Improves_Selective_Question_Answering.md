# Prior Work Analysis Report

## Target Paper

**Title:** Is That Your Final Answer? Test-Time Scaling Improves Selective Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Scaling the test-time compute of large language models has demonstrated impressive performance on reasoning benchmarks.However, existing evaluations of test-time scaling make the strong assumption that a reasoning system should always give an answer to any question provided.This overlooks concerns about whether a model is confident in its answer, and whether it is appropriate to always provide a response.To address these concerns, we extract confidence scores during reasoning for thresholding model responses.We find that increasing compute budget at inference time not only helps models answer more questions correctly, but also increases confidence in correct responses.We then extend the current paradigm of zero-risk responses during evaluation by considering settings with non-zero levels of response risk, and suggest a recipe for reporting evaluations under these settings. 1

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Selective classification for deep neural networks** (2017)
- *Authors:* Yonatan Geifman and Ran El-Yaniv
- *Direct Connection:* Provides the selection-function framework (confidence-thresholding to trade coverage for accuracy) that this work directly instantiates by accepting answers only when the model’s estimated confidence exceeds a threshold.

**Selective question answering under domain shift** (2020)
- *Authors:* Amita Kamath et al.
- *Direct Connection:* Introduces selective QA as a formal problem where a system may abstain, motivating the paper’s formulation of QA with refusals and its evaluation focus on accuracy–coverage tradeoffs.

### 🏷️ Inspiration

**Building Watson: An overview of the DeepQA project** (2010)
- *Authors:* David Ferrucci et al.
- *Direct Connection:* Establishes Jeopardy-style, penalty-based QA evaluation that directly inspires the paper’s ‘Jeopardy Odds’ utility with negative rewards for incorrect answers and rewards for correct ones.

### 🏷️ Gap Identification

**DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning** (2025) [[arXiv](https://arxiv.org/abs/2501.12948)]
- *Authors:* DeepSeek-AI et al.
- *Direct Connection:* Showcases high performance from long chain-of-thought test-time scaling while evaluating in a zero-risk, always-answer regime, highlighting the gap this work addresses by introducing abstention and risk-aware evaluation.

### 🏷️ Baseline

**s1: Simple test-time scaling** (2025) [[arXiv](https://arxiv.org/abs/2501.19393)]
- *Authors:* Niklas Muennighoff et al.
- *Direct Connection:* Provides both a primary baseline system and the budget-forcing procedure (strict token-limit enforcement for chains of thought) that the paper adopts to control test-time compute.

### 🏷️ Related Problem

**Quizbowl: The Case for Incremental Question Answering** (2021) [[arXiv](https://arxiv.org/abs/1904.04792)]
- *Authors:* Pedro Rodriguez et al.
- *Direct Connection:* Demonstrates game-like QA settings that penalize incorrect buzzing to encourage calibrated abstention, directly informing the paper’s risk-sensitive evaluation ethos.

---

## Synthesis: How Prior Work Led to This Paper

Selective prediction research established a concrete mechanism for abstention: by thresholding a model’s confidence, a system can trade off coverage for accuracy (Geifman and El‑Yaniv). In question answering, this idea was formalized as selective QA, where the model may refuse to answer when uncertain, grounding evaluation on accuracy–coverage considerations under distribution shift (Kamath et al.). Game‑show settings such as Jeopardy embedded explicit penalties for wrong answers alongside rewards for correct ones, demonstrating how utility functions can incentivize calibrated answering behavior (Ferrucci et al.). In parallel, test‑time compute scaling with long chains of thought showed strong gains on hard reasoning tasks but was reported in a zero‑risk, always‑answer paradigm; s1 introduced a simple approach and a practical budget‑forcing mechanism for strictly controlling the number of generated reasoning tokens, while DeepSeek‑R1 demonstrated reinforced long‑form reasoning under the same always‑answer assumption. Quizbowl‑style incremental QA further highlighted that penalizing incorrect responses can elicit beneficial abstentions when confidence is low (Rodriguez et al.).

Together, these strands revealed a clear opportunity: modern test‑time scaling methods improve accuracy but ignore the decision of whether to answer at all under real costs. By combining budget‑controlled reasoning (from s1) with selective prediction principles (confidence‑thresholded acceptance) and utility functions mirroring Jeopardy‑like penalties, the present work evaluates how increasing inference budgets affects both correctness and confidence, maps performance over accuracy‑coverage‑risk trade spaces, and proposes risk‑aware reporting (‘Jeopardy Odds’) as a natural next step for benchmarking compute‑scaling systems that must decide not only how long to think but also when to answer.

---

*Analysis generated on: 2026-04-05T12:03:32.223916*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
