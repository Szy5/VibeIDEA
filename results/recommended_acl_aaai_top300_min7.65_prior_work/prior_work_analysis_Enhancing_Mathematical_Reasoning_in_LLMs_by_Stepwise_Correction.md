# Prior Work Analysis Report

## Target Paper

**Title:** Enhancing Mathematical Reasoning in LLMs by Stepwise Correction

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Best-of-N decoding methods instruct large language models (LLMs) to generate multiple solutions, score each using a scoring function, and select the highest scored as the final answer to mathematical reasoning problems.However, this repeated independent process often leads to the same mistakes, making the selected solution still incorrect.We propose a novel prompting method named Stepwise Correction (STEPCO) that helps LLMs identify and revise incorrect steps in their generated reasoning paths.It iterates verification and revision phases that employ a process-supervised verifier.The verifythen-revise process not only improves answer correctness but also reduces token consumption with fewer paths needed to generate.With STEPCO, a series of LLMs demonstrate exceptional performance.Notably, using GPT-4o as the backend LLM, STEPCO achieves an average accuracy of 94.1 across eight datasets, significantly outperforming the state-of-the-art Best-of-N method by +2.4, while reducing token consumption by 77.8%.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Let’s Verify Step by Step** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2305.20050)]
- *Authors:* Hunter Lightman et al.
- *Direct Connection:* It established process supervision and step-level verifiers as superior to outcome-only scoring, a core mechanism adopted here to estimate per-step likelihood of correctness and localize the first erroneous step.

### 🏷️ Inspiration

**Making Language Models Better Reasoners with Step-Aware Verifier (DiVeRSe)** (2023)
- *Authors:* Yifei Li et al.
- *Direct Connection:* DiVeRSe’s step-aware verification of intermediate reasoning informed the idea of using per-step confidence signals, which are here transformed from mere selection signals into actionable feedback to prompt targeted step revisions.

**Improve Mathematical Reasoning in Language Models by Automated Process Supervision (OmegaPRM)** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2406.06592)]
- *Authors:* Liangchen Luo et al.
- *Direct Connection:* OmegaPRM’s automated process supervision for estimating step quality inspired the current paper’s automatic process annotation approach and the use of learned step-quality scores to guide iterative correction.

### 🏷️ Gap Identification

**CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing** (2024)
- *Authors:* Zhibin Gou et al.
- *Direct Connection:* CRITIC demonstrated an effective extrinsic verify-and-revise loop but only at the final-answer level, a limitation directly addressed here by localizing and revising the first wrong step using a process-supervised verifier.

**Large Language Models Cannot Self-Correct Reasoning Yet** (2024)
- *Authors:* Jie Huang et al.
- *Direct Connection:* By showing that intrinsic self-correction often fails without external feedback and leads to repeated mistakes, this paper motivates the use of an external verifier and structured stepwise feedback to break error repetition.

### 🏷️ Baseline

**Training verifiers to solve math word problems** (2021) [[arXiv](https://arxiv.org/abs/arXiv:2110.14168)]
- *Authors:* Karl Cobbe et al.
- *Direct Connection:* This work introduced the Best-of-N sampling-and-verification paradigm for math reasoning that the current paper directly targets as its primary baseline, addressing its failure mode when the correct path is absent by adding step-level feedback rather than outcome-only selection.

### 🏷️ Extension

**Math-Shepherd: Verify and Reinforce LLMs Step-by-Step without Human Annotations** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2312.08935)]
- *Authors:* Peiyi Wang et al.
- *Direct Connection:* Math-Shepherd’s automated process supervision for training step-level verifiers is extended here by introducing a new D+/D− sampling tree to annotate step quality and by converting verifier outputs into targeted step revisions.

---

## Synthesis: How Prior Work Led to This Paper

Best-of-N sampling with outcome-level verification demonstrated that generating multiple solutions and selecting the highest-scored one can improve math reasoning, but it also highlighted a brittle failure mode when the correct path is not sampled and repeated errors persist. Process supervision shifted verification from outcomes to steps, showing that human-like assessment of intermediate steps provides stronger signals for correctness and that an error at any step greatly increases the chance of a wrong final answer. Step-aware verification operationalized this idea by assigning confidence to individual steps during reasoning, enabling finer-grained assessments than outcome scoring. Extrinsic self-correction introduced a verify-and-revise loop by bringing in external tools or models to critique model outputs, though such methods typically verified only final answers. Empirically, intrinsic self-correction was shown to be unreliable without external feedback, often repeating the same mistakes. Concurrently, automated process supervision methods demonstrated how to build step-level supervision without human labels, using rollouts or Monte Carlo strategies to estimate step quality and train verifiers.
Together, these works exposed a clear opportunity: combine automated step-level supervision with an extrinsic correction loop that acts precisely where reasoning goes astray. The current paper synthesizes this by training a process-supervised verifier via an automatic D+/D− annotation tree to score each step’s likelihood of leading to the correct answer, then running a verify-then-revise loop that freezes verified steps and rewrites from the first low-probability step onward. This coupling transforms step verification from a selection tool into actionable guidance, directly addressing Best-of-N’s coverage and repetition issues while overcoming prior correction methods’ lack of step localization, yielding higher accuracy with fewer samples.

---

*Analysis generated on: 2026-04-05T12:01:32.126021*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
