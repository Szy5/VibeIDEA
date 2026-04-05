# Prior Work Analysis Report

## Target Paper

**Title:** T-SciQ: Teaching Multimodal Chain-of-Thought Reasoning via Large Language Model Signals for Science Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLMs) have recently demonstrated exceptional performance in various Natural Language Processing (NLP) tasks. They have also shown the ability to perform chain-of-thought (CoT) reasoning to solve complex problems. Recent studies have explored CoT reasoning in complex multimodal scenarios, such as the science question answering task, by fine-tuning multimodal models with high-quality human-annotated CoT rationales. However, collecting high-quality COT rationales is usually time-consuming and costly. Besides, the annotated rationales are hardly accurate due to the external essential information missed. To address these issues, we propose a novel method termed T-SciQ that aims at teaching science question answering with LLM signals. The T-SciQ approach generates high-quality CoT rationales as teaching signals and is advanced to train much smaller models to perform CoT reasoning in complex modalities. Additionally, we introduce a novel data mixing strategy to produce more effective teaching data samples for simple and complex science question answer problems. Extensive experimental results show that our T-SciQ method achieves a new state-of-the-art performance on the ScienceQA benchmark, with an accuracy of 96.18%. Moreover, our approach outperforms the most powerful fine-tuned baseline by 4.5%. The code is publicly available at https://github.com/T-SciQ/T-SciQ.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Learn to Explain: Multimodal Reasoning via Thought Chains for Science Question Answering** (2022)
- *Authors:* Lu et al.
- *Direct Connection:* This work introduced the ScienceQA benchmark with human lectures/solutions and the multimodal CoT formulation that T-SciQ targets, providing the problem setup, evaluation protocol, and evidence that human explanations can be insufficient for complex science QA.

### 🏷️ Inspiration

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Wei et al.
- *Direct Connection:* The core idea that prompting LLMs to produce step-by-step rationales improves reasoning directly motivates T-SciQ’s generation of QA-CoT signals used as teaching data.

**Large Language Models are Zero-Shot Reasoners** (2022) [[arXiv](https://arxiv.org/abs/2205.11916)]
- *Authors:* Kojima et al.
- *Direct Connection:* Demonstrating zero-shot CoT via simple prompts underpins T-SciQ’s zero-shot prompting scheme to obtain rationales without task-specific fine-tuning.

**Large Language Models Are Reasoning Teachers** (2022) [[arXiv](https://arxiv.org/abs/2212.10071)]
- *Authors:* Ho et al.
- *Direct Connection:* By showing that LLM-generated rationales can teach smaller models via fine-tuning, this work provides the teacher–student distillation paradigm that T-SciQ extends to multimodal ScienceQA with mixed CoT/PCoT signals.

### 🏷️ Baseline

**Multimodal Chain-of-Thought Reasoning in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2302.00923)]
- *Authors:* Zhang et al.
- *Direct Connection:* T-SciQ adopts the Multimodal-CoT two-stage framework (rationale generation then answer inference) as its student architecture, replacing human-annotated rationales with LLM-generated CoT/PCoT and adding a data-mixing strategy to overcome its reliance on costly annotations.

### 🏷️ Extension

**Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.04091)]
- *Authors:* Wang et al.
- *Direct Connection:* T-SciQ directly follows Plan-and-Solve to generate plan-based CoT (PCoT) that decomposes complex questions into subproblems, forming one of its two teaching signals.

---

## Synthesis: How Prior Work Led to This Paper

A two-stage multimodal chain-of-thought framework established that training a rationale generator and an answer predictor yields strong ScienceQA performance when guided by human explanations, but it required costly annotations and struggled when external knowledge was missing. The ScienceQA benchmark defined the multimodal multiple-choice setting with lectures and solutions as supervision, making explicit the need to combine images, textual context, and background knowledge for scientific reasoning. Chain-of-thought prompting showed that eliciting step-by-step rationales from large language models improves reasoning quality, while zero-shot prompting revealed that such rationales can be produced without task-specific fine-tuning using simple instructions. Plan-and-solve prompting advanced this by generating an explicit plan that decomposes complex problems into simpler substeps before solving, effectively structuring reasoning for harder cases. Complementing these, the reasoning-teacher paradigm demonstrated that LLM-generated rationales can be distilled into smaller student models through supervised fine-tuning.
Bringing these strands together revealed a clear opportunity: use LLMs to generate high-quality teaching signals for multimodal ScienceQA, leveraging both direct CoT rationales for simpler items and plan-based decompositions for harder ones, and train within a proven two-stage multimodal architecture. The natural next step was to mix these two types of signals per skill—selected via validation—to exploit their complementary strengths, thereby avoiding annotation bottlenecks while improving robustness on complex, knowledge-intensive questions. This synthesis enables smaller multimodal students to internalize planning and reasoning patterns originally elicited in large language models.

---

*Analysis generated on: 2026-04-05T11:55:54.727965*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
