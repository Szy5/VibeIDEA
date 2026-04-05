# Prior Work Analysis Report

## Target Paper

**Title:** ThinkSum: Probabilistic reasoning over sets using large language models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) have a substantial capacity for high-level analogical reasoning: reproducing patterns in linear text that occur in their training data (zero-shot evaluation) or in the provided context (few-shot in-context learning). However, recent studies show that even the more advanced LLMs fail in scenarios that require reasoning over multiple objects or facts and making sequences of logical deductions. We propose a two-stage probabilistic inference paradigm, ThinkSum, which reasons over sets of objects or facts in a structured manner. In the first stage (Think - retrieval of associations), a LLM is queried in parallel over a set of phrases extracted from the prompt or an auxiliary model call. In the second stage (Sum - probabilistic inference or reasoning), the results of these queries are aggregated to make the final prediction. We demonstrate the possibilities and advantages of ThinkSum on the BIG-bench suite of LLM evaluation tasks, achieving improvements over the state of the art using GPT-family models on thirteen difficult tasks, often with far smaller model variants. We also compare and contrast ThinkSum with other proposed modifications to direct prompting of LLMs, such as variants of chain-of-thought prompting. Our results suggest that because the probabilistic inference in ThinkSum is performed outside of calls to the LLM, ThinkSum is less sensitive to prompt design, yields more interpretable predictions, and can be flexibly combined with latent variable models to extract structured knowledge from LLMs. Overall, our proposed paradigm represents a promising approach for enhancing the reasoning capabilities of LLMs.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**An Explanation of In-Context Learning as Implicit Bayesian Inference** (2021) [[arXiv](https://arxiv.org/abs/2111.02080)]
- *Authors:* Sang Michael Xie et al.
- *Direct Connection:* Its Bayesian perspective on in-context learning motivated ThinkSum’s explicit external Bayesian-style aggregation (mixtures and products of LM scores) rather than relying on implicit inference within self-attention.

### 🏷️ Inspiration

**Self-Consistency Improves Chain of Thought Reasoning in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* Its central idea of aggregating multiple reasoning paths inspired ThinkSum’s Sum stage, which averages/products LM likelihoods across many structured substitutions instead of voting over sampled rationales.

**Language Model Cascades** (2022) [[arXiv](https://arxiv.org/abs/2207.10342)]
- *Authors:* David Dohan et al.
- *Direct Connection:* By framing prompt variants and multi-step LM use in a probabilistic, controller-driven pipeline, this work informed ThinkSum’s parallel LM ‘Think’ calls and explicit probabilistic ‘Sum’ inference outside the model.

### 🏷️ Gap Identification

**Coherence Boosting: When Your Pretrained Language Model Is Not Paying Enough Attention** (2022)
- *Authors:* Nikolay Malkin et al.
- *Direct Connection:* By documenting recency bias and surface-form competition when appending context, this work identified a failure mode that ThinkSum avoids by moving reasoning outside the prompt and aggregating across structured alternatives.

### 🏷️ Baseline

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* Used as the primary baseline, this work’s within-model rationale generation directly motivates ThinkSum’s choice to externalize the reasoning step and combine LM-evaluated hypotheses via probabilistic aggregation to reduce prompt sensitivity.

### 🏷️ Extension

**Calibrate Before Use: Improving Few-Shot Performance of Language Models** (2021) [[arXiv](https://arxiv.org/abs/2102.09690)]
- *Authors:* Zihao Zhao et al.
- *Direct Connection:* ThinkSum extends the calibration-by-premise-erasure idea by explicitly using ratios of conditional to unconditional likelihoods when scoring substituted prompts in its mixture, directly borrowing this debiasing step.

### 🏷️ Related Problem

**Decomposed Prompting: A Modular Approach for Solving Complex Tasks** (2022) [[arXiv](https://arxiv.org/abs/2210.02406)]
- *Authors:* Tushar Khot et al.
- *Direct Connection:* Showing that external control-flow and modular subproblem prompting improves complex reasoning, this work informed ThinkSum’s controller-like separation of ‘Think’ and ‘Sum’ while replacing the final step with formal probabilistic inference over sets.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-thought prompting showed that inserting intermediate rationales enables large language models to solve multi-step problems, but it performs all reasoning inside the LM’s linear workspace and is highly sensitive to prompt phrasing and examples. Self-consistency improved such reasoning by sampling multiple rationale paths and aggregating them, highlighting that combining many weak signals can yield stronger conclusions. Language Model Cascades framed prompting as a probabilistic, controller-driven composition of LM calls, encouraging structured multi-step use of LMs and making explicit the role of probabilistic combination across prompt variants. A Bayesian account of in-context learning clarified how priors and likelihoods are implicitly combined within models, suggesting that explicit, external Bayesian aggregation—via mixtures and products—could be beneficial. Decomposed prompting further demonstrated that modular pipelines with external control-flow can tackle complex tasks more reliably than monolithic prompting. Calibration-by-premise-erasure provided a concrete, likelihood-ratio technique to correct unconditional biases in LM scoring. Finally, analyses of recency bias and surface-form competition showed how appending auxiliary text can mislead models, underscoring the brittleness of within-prompt reasoning.
Taken together, these works point to a gap: while decomposition and aggregation help, doing both entirely inside the LM leaves systems fragile. The natural next step is to separate fast associative retrieval from slow reasoning, using parallel LM calls to retrieve structured sets and explicit probabilistic inference to aggregate their likelihoods. Building on self-consistent aggregation, controller-driven cascades, and Bayesian calibration, ThinkSum formalizes this separation with a ‘Think’ stage for set construction and a ‘Sum’ stage for mixture/product-based inference, yielding robustness and interpretability beyond prompt-engineered chains.

---

*Analysis generated on: 2026-04-05T11:37:37.820761*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
