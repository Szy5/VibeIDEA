# Prior Work Analysis Report

## Target Paper

**Title:** Exclusion of Thought: Mitigating Cognitive Load in Large Language Models for Enhanced Reasoning in Multiple-Choice Tasks

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Exclusion of Thought: Mitigating Cognitive Load in Large Language Models for Enhanced Reasoning in Multiple-Choice Tasks

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Gap Identification

**POE: Process of Elimination for Multiple Choice Reasoning** (2023)
- *Authors:* Chenkai Ma and Xinya Du
- *Direct Connection:* POE’s two-step self-scoring for MCQs inspired elimination-style reasoning, but its continued exposure to all options left models vulnerable to distractors—an explicit limitation EoT addresses by actually removing low-confidence options from the prompt.

**It’s Not Easy Being Wrong: Large Language Models Struggle with Process of Elimination Reasoning** (2024)
- *Authors:* Nishant Balepur et al.
- *Direct Connection:* This work showed LLMs often fail PoE-style tasks, highlighting that simply reasoning about eliminations is insufficient and motivating EoT’s design to reduce cognitive load by minimizing distractor exposure through prompt recomposition.

**Multiple-Choice Questions are Efficient and Robust LLM Evaluators** (2024) [[arXiv](https://arxiv.org/abs/2405.11966)]
- *Authors:* Ziyin Zhang et al.
- *Direct Connection:* This study empirically demonstrated that removing a distractor option in GSM8K-MC dramatically boosts accuracy, directly motivating EoT’s subtractive strategy to eliminate distractors and relieve cognitive load.

### 🏷️ Baseline

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* CoT is the primary additive reasoning baseline whose multi-step chains EoT plugs into and improves upon by replacing attention-consuming option exposure with subtractive, elimination-based prompting.

### 🏷️ Extension

**Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback** (2023)
- *Authors:* Katherine Tian et al.
- *Direct Connection:* EoT extends this calibrated confidence elicitation by using model-calibrated probabilities to compute exclusion confidence (Pexclude) and drive the confidence-gap thresholding that governs iterative elimination.

**Self-Consistency Improves Chain-of-Thought Reasoning in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* EoT adopts the self-consistency idea of sampling multiple reasoning chains and aggregates them as local scores, resampling when the confidence gap is small to robustify elimination decisions.

### 🏷️ Related Problem

**Eliminating Reasoning via Inferring with Planning: A New Framework to Guide LLMs’ Non-Linear Thinking** (2023) [[arXiv](https://arxiv.org/abs/2310.12342)]
- *Authors:* Yongqi Tong et al.
- *Direct Connection:* This planning-based prompting guides elimination within a single prompt but keeps distractors visible; EoT contrasts by iteratively reconstructing the input to prevent re-attending to eliminated options.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-Thought established that prompting models to generate intermediate steps enhances reasoning, but it does so by adding more content to the prompt while keeping all options visible. Process-of-Elimination (POE) introduced a two-step self-scoring scheme specifically for multiple-choice questions, encouraging elimination-style thinking yet still presenting all options together, which leaves room for distractor-driven errors. Empirical evidence deepened this concern: large language models often struggle with PoE-style reasoning, indicating that simply instructing models to eliminate choices does not overcome distractor interference. Planning-style prompting sought to guide non-linear elimination within a single prompt, but retained visibility of ruled-out options, risking renewed attention to distractors. In parallel, calibrated confidence elicitation provided practical techniques for extracting more reliable probability estimates from instruction-tuned models, while self-consistency showed that sampling and aggregating multiple reasoning chains can improve robustness. Finally, studies on MCQ evaluation demonstrated that the mere presence or removal of distractors can cause large swings in accuracy, underscoring distractor sensitivity as a central bottleneck. Together, these insights revealed a gap: existing methods either add more reasoning content or discuss eliminations without actually reducing option exposure. The natural next step was a subtractive prompting framework that physically removes low-confidence distractors from the prompt, uses calibrated probabilities to govern exclusions, and leverages multi-chain aggregation to stabilize decisions. EoT synthesizes these strands by iteratively eliminating options, recalibrating confidence, and reconstructing the input so models no longer re-attend to eliminated distractors, thereby reducing cognitive load and improving MCQ reasoning.

---

*Analysis generated on: 2026-04-05T12:01:10.375674*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
