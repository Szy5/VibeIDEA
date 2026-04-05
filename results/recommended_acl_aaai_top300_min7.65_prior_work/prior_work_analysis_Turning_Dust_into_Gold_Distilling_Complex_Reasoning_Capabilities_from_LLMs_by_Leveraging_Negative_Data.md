# Prior Work Analysis Report

## Target Paper

**Title:** Turning Dust into Gold: Distilling Complex Reasoning Capabilities from LLMs by Leveraging Negative Data

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLMs) have performed well on various reasoning tasks, but their inaccessibility and numerous parameters hinder wide application in practice. One promising way is distilling the reasoning ability from LLMs to small models by the generated chain-of-thought reasoning paths. In some cases, however, LLMs may produce incorrect reasoning chains, especially when facing complex mathematical problems. Previous studies only transfer knowledge from positive samples and drop the synthesized data with wrong answers. In this work, we illustrate the merit of negative data and propose a model specialization framework to distill LLMs with negative samples besides positive ones. The framework consists of three progressive steps, covering from training to inference stages, to absorb knowledge from negative data. We conduct extensive experiments across arithmetic reasoning tasks to demonstrate the role of negative data in distillation from LLM.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This work established the use of explicit chain-of-thought rationales for reasoning, providing the rationale-centric supervision that the current paper distills—and crucially extends—to incorporate negative (incorrect) chains rather than discarding them.

**PaD: Program-aided Distillation Specializes Large Models in Reasoning** (2023) [[arXiv](https://arxiv.org/abs/2305.13888)]
- *Authors:* Xiaoqing Zhu et al.
- *Direct Connection:* PaD crystalized the model specialization pipeline (CoT distillation, self-enhancement, and self-consistency), which the present paper systematically modifies across all stages to leverage negative data for training and inference.

### 🏷️ Gap Identification

**Negative Training for Neural Dialogue Response Generation** (2020)
- *Authors:* Tianxing He et al.
- *Direct Connection:* This work showed how to penalize undesired outputs using negative samples, and its limitation of only using negatives to suppress behaviors explicitly motivates the current paper’s dual-view design to both extract positive knowledge from negatives and avoid their pitfalls.

### 🏷️ Baseline

**Specializing Smaller Language Models towards Multi-Step Reasoning** (2023) [[arXiv](https://arxiv.org/abs/2301.12726)]
- *Authors:* Yao Fu et al.
- *Direct Connection:* This study distilled LLM-generated CoT into small models as a primary specialization baseline that the current work improves upon by exploiting negative samples rather than filtering them out.

### 🏷️ Extension

**Self-Consistency Improves Chain of Thought Reasoning in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2203.07374)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* By introducing voting across diverse CoT samples, this paper provided the inference-time aggregation scheme that the current work directly extends with adaptive weighting via a learned ranker to counteract equal-weighted votes for poor rationales.

**Diversifying Neural Dialogue Generation via Negative Distillation** (2022)
- *Authors:* Yiwei Li et al.
- *Direct Connection:* By framing a ‘negative teacher’ whose predictions the student should diverge from, this paper directly inspires the current work’s KL-based calibration that uses a negative-trained assistant to weight self-distillation toward crucial rationales.

### 🏷️ Related Problem

**Training Verifiers to Solve Math Word Problems** (2021) [[arXiv](https://arxiv.org/abs/2110.14168)]
- *Authors:* Karl Cobbe et al.
- *Direct Connection:* This paper’s verifier paradigm for scoring solution candidates informs the current work’s learned ranking model used to reweight candidate CoT answers during adaptive self-consistency.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-thought prompting showed that explicit reasoning traces markedly improve language model solvability by providing stepwise rationales, which became the supervision backbone for reasoning-oriented distillation. Self-consistency then revealed that sampling multiple diverse rationales and voting can raise accuracy, exposing an inference-time aggregation mechanism centered on CoT samples. Building on this, specialization efforts distilled LLM-generated chains into smaller models to attain multi-step reasoning capability, and PaD codified a three-stage pipeline—distillation, self-enhancement, and self-consistency—that has guided subsequent model specialization designs. In parallel, negative training and unlikelihood-style approaches demonstrated that negative examples can steer models away from undesirable outputs, while negative distillation introduced the idea of a negative teacher whose predictions the student should diverge from. Finally, verifier-based methods for math tasks established that learned scoring of candidate solutions can guide selection beyond naive probability or majority rules.
Taken together, these works revealed both the power and the limitations of existing pipelines: CoT distillation and self-consistency were effective but routinely discarded negative samples; negative training leveraged negatives only to suppress behavior, missing their positive informational content; and inference aggregation often equally weighted fallible chains. The natural next step was to systematically incorporate negative data across the entire specialization pipeline: extract reusable knowledge from incorrect chains during training via a dual-view mechanism, calibrate self-distillation by contrasting a negative-trained assistant and a positive model, and replace uniform voting with a learned ranker that scores candidate rationales, thereby converting traditionally discarded or underused negative evidence into guidance for both training and inference.

---

*Analysis generated on: 2026-04-05T12:07:33.169143*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
