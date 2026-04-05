# Prior Work Analysis Report

## Target Paper

**Title:** DistilQwen2.5: Industrial Practices of Training Distilled Open Lightweight Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Enhancing computational efficiency and reducing deployment costs for large language models (LLMs) have become critical challenges in various resource-constrained scenarios.In this work, we present DistilQwen2.5, a family of distilled, lightweight LLMs derived from the public Qwen2.5 models.These distilled models exhibit enhanced instruction-following capabilities compared to the original models based on a series of distillation techniques that incorporate knowledge from much larger LLMs.In our industrial practice, we first leverage powerful proprietary LLMs with varying capacities as multi-agent teachers to select, rewrite, and refine instruction-response pairs that are more suitable for student LLMs to learn.After standard fine-tuning, we further leverage a computationally efficient model fusion approach that enables student models to progressively integrate fine-grained hidden knowledge from their teachers.Experimental evaluations demonstrate that the distilled models possess significantly stronger capabilities than their original checkpoints.Additionally, we present use cases to illustrate the applications of our framework in real-world scenarios.To facilitate practical use, we have released all the DistilQwen2.5 models to the open-source community. 1* C. Wang and J. Yan contributed equally to this work.Correspondence to: C. Wang.1 Our trained lightweight models and our processed large instruction-following dataset are released in Hugging-Face.Please refer to the four models DistilQwen2.5-0.5B-Instruct,DistilQwen2.5-1.5B-Instruct,DistilQwen2.5-3B-Instruct,DistilQwen2

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This paper introduced CoT prompting, the specific reasoning format the authors explicitly elicit in rewritten instruction-response pairs to transfer structured reasoning to smaller students.

### 🏷️ Inspiration

**Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes** (2023)
- *Authors:* Cheng-Yu Hsieh et al.
- *Direct Connection:* This work showed that injecting Chain-of-Thought (CoT) rationales into distillation data markedly boosts small models’ reasoning, directly motivating the paper’s rewriting agent to generate CoT-style responses for complex tasks during black-box KD.

### 🏷️ Gap Identification

**MiniLLM: Knowledge Distillation of Large Language Models** (2024)
- *Authors:* Yuxian Gu et al.
- *Direct Connection:* By relying on reverse KL white-box distillation that requires online teacher inference, this work’s high memory/compute cost highlighted a practical barrier the authors address via offline top-K logits storage and divergence over only top tokens.

**Rethinking Kullback–Leibler Divergence in Knowledge Distillation for Large Language Models** (2025)
- *Authors:* Taiqiang Wu et al.
- *Direct Connection:* Its adaptive forward+reverse KL objectives improved white-box KD but retained substantial runtime and memory burdens, directly motivating the paper’s efficient top-K divergence design and distributed offline logits generation.

### 🏷️ Extension

**Distilling Instruction-Following Abilities of Large Language Models with Task-Aware Curriculum Planning** (2024)
- *Authors:* Yuanhao Yue et al.
- *Direct Connection:* The task-aware curriculum planning approach informed the selection agent’s task-balance criterion, which the authors explicitly follow to choose higher-value instruction-response pairs.

**Building a Family of Data Augmentation Models for Low-Cost LLM Fine-Tuning on the Cloud** (2024) [[arXiv](https://arxiv.org/abs/2412.04871)]
- *Authors:* Yuanhao Yue et al.
- *Direct Connection:* The authors adopt this work’s cloud-friendly preprocessing and augmentation pipeline as the starting point for constructing and cleaning the instruction-tuning corpus used in black-box KD.

**Knowledge Fusion of Large Language Models (FuseLLM)** (2024)
- *Authors:* Fanqi Wan et al.
- *Direct Connection:* The token alignment technique from this work is directly used to match teacher–student vocabularies, enabling the proposed top-K logits fusion in white-box distillation.

---

## Synthesis: How Prior Work Led to This Paper

Hsieh et al. demonstrated that distilling step-by-step rationales significantly strengthens small models’ reasoning, making Chain-of-Thought (CoT) supervision a high-yield signal for distillation. Wei et al. established CoT prompting as a concrete mechanism for eliciting decomposed reasoning, providing the exact format to inject into training targets. Yue et al. (task-aware curriculum planning) showed that selecting and balancing instruction data by task type improves instruction-following transfer, specifying a practical criterion for data curation. Complementing this, Yue et al. (cloud data augmentation) detailed a robust, scalable preprocessing and augmentation pipeline for low-cost fine-tuning, offering an immediately usable backbone for instruction corpus construction. On the white-box front, Wan et al. (FuseLLM) introduced token alignment for cross-vocabulary fusion, a necessary operation when merging knowledge across heterogeneous LLMs. Meanwhile, MiniLLM (Gu et al.) and Wu et al. revealed that reverse-KL or adaptive KL objectives can enhance distillation but impose heavy online teacher inference and memory demands at LLM scale.
Together these works surfaced a clear opportunity: combine high-quality, CoT-rich instruction data with principled task-balanced selection while avoiding the prohibitive costs of conventional white-box KD. The paper synthesizes these insights by deploying multi-agent black-box augmentation (expansion, CoT rewriting, selection by task balance, and verification) to encode teacher knowledge into data, then follows with an efficient white-box phase that leverages token alignment and offline top-K teacher logits to approximate KL-based objectives with minimal compute and I/O. This progression was a natural next step to industrialize LLM distillation across sizes while preserving reasoning and instruction fidelity.

---

*Analysis generated on: 2026-04-05T11:58:32.647650*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
