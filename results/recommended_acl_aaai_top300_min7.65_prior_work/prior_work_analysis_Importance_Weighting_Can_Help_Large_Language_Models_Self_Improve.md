# Prior Work Analysis Report

## Target Paper

**Title:** Importance Weighting Can Help Large Language Models Self-Improve

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) have shown remarkable capability in numerous tasks and applications. However, fine-tuning LLMs using high-quality datasets under external supervision remains prohibitively expensive. In response, LLM self-improvement approaches have been vibrantly developed recently. The typical paradigm of LLM self-improvement involves training LLM on self-generated data, part of which may be detrimental and should be filtered out due to the unstable data quality. While current works primarily employs filtering strategies based on answer correctness, in this paper, we demonstrate that filtering out correct but with high distribution shift extent (DSE) samples could also benefit the results of self-improvement. Given that the actual sample distribution is usually inaccessible, we propose a new metric called DS weight to approximate DSE, inspired by the Importance Weighting methods. Consequently, we integrate DS weight with self-consistency to comprehensively filter the self-generated samples and fine-tune the language model. Experiments show that with only a tiny valid set (up to 5% size of the training set) to compute DS weight, our approach can notably promote the reasoning ability of current LLM self-improvement methods. The resulting performance is on par with methods that rely on external supervision from pre-trained reward models.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Self-Consistency Improves Chain of Thought Reasoning in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2203.11171)]
- *Authors:* Wang et al.
- *Direct Connection:* Its majority-vote self-consistency mechanism is used to assess answer correctness, which the current paper combines with DS weight to jointly filter self-generated samples.

**Machine Learning in Non-Stationary Environments: Introduction to Covariate Shift Adaptation** (2012)
- *Authors:* Sugiyama and Kawanabe
- *Direct Connection:* This monograph provides the importance weighting framework for covariate shift, which motivates the current paper’s formulation of per-sample weights to approximate distribution mismatch between valid and self-generated data.

### 🏷️ Gap Identification

**The Curse of Recursion: Training on Generated Data Makes Models Forget** (2023) [[arXiv](https://arxiv.org/abs/2305.17493)]
- *Authors:* Shumailov et al.
- *Direct Connection:* It explicitly shows that training on model-generated data induces harmful distribution shift, directly motivating the current paper to identify and filter high-distribution-shift (high-DSE) samples.

### 🏷️ Baseline

**Large Language Models Can Self-Improve** (2023)
- *Authors:* Huang et al.
- *Direct Connection:* This work established the majority-vote self-consistency pipeline for training on self-generated data, which the current paper directly augments by adding a distribution-shift-based filter (DS weight) on top of the LMSI correctness filter.

### 🏷️ Extension

**Rethinking Importance Weighting for Deep Learning under Distribution Shift** (2020) [[arXiv](https://arxiv.org/abs/2006.04647)]
- *Authors:* Fang et al.
- *Direct Connection:* The paper’s validation-based surrogate objective for importance weighting directly informs Eq. (2) in the current work, which is adapted to compute a per-sample DS weight from valid-set and training losses.

### 🏷️ Related Problem

**MoT: Memory-of-Thought Enables ChatGPT to Self-Improve** (2023)
- *Authors:* Li and Qiu
- *Direct Connection:* By filtering with entropy-based uncertainty, this work highlights a correctness/uncertainty axis in self-improvement that the current paper complements with a distribution-shift axis, showing DSE is largely orthogonal to uncertainty.

**Self-Alignment with Instruction Backtranslation** (2024)
- *Authors:* Li et al.
- *Direct Connection:* This work demonstrates LLM self-filtering for correctness without external rewards, underscoring a focus on correctness that the current paper expands by introducing a DSE-based criterion for filtering.

---

## Synthesis: How Prior Work Led to This Paper

Prior work on LLM self-improvement established that filtering self-generated data is crucial and practical. Large Language Models Can Self-Improve (LMSI) operationalized a pipeline that generates multiple candidates per question and retains the most consistent answer, showing self-consistency correlates with correctness. Self-Consistency Improves Chain of Thought provided the majority-vote mechanism underpinning that correctness filter. In parallel, MoT introduced entropy-based uncertainty filtering to discard high-uncertainty generations, highlighting the uncertainty dimension in data selection, while Self-Alignment showed LLMs can self-filter for correctness without external reward models. Outside LLMs, the importance weighting literature formalized how to correct for covariate shift by reweighting training samples; the monograph by Sugiyama and Kawanabe articulated this framework, and Fang et al.’s DIW provided a validation-based surrogate objective for estimating importance weights in deep settings. Critically, The Curse of Recursion demonstrated that training on model-generated data can induce harmful distribution shifts, identifying a failure mode not addressed by correctness- or uncertainty-only filters. Together, these works revealed that existing self-improvement largely emphasizes correctness and uncertainty while neglecting distribution mismatch, and that importance weighting offers a principled tool to account for such shift. The current paper synthesizes these insights by adapting DIW’s valid-set surrogate to compute a simple per-sample distribution shift weight from model losses, symmetrizing it to measure distribution shift extent, and integrating this DSE signal alongside self-consistency. This yields a natural next step: filter correct yet high-shift samples to mitigate recursion-induced drift, improving self-improvement without relying on external reward models.

---

*Analysis generated on: 2026-04-05T12:07:31.563991*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
