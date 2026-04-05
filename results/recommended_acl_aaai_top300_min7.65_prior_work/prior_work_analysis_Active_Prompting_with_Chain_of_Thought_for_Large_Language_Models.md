# Prior Work Analysis Report

## Target Paper

**Title:** Active Prompting with Chain-of-Thought for Large Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> The increasing scale of large language models (LLMs) brings emergent abilities to various complex tasks requiring reasoning, such as arithmetic and commonsense reasoning.It is known that the effective design of taskspecific prompts is critical for LLMs' ability to produce high-quality answers.In particular, an effective approach for complex questionand-answering tasks is example-based prompting with chain-of-thought (CoT) reasoning, which significantly improves the performance of LLMs.However, current CoT methods rely on a fixed set of human-annotated exemplars, which are not necessarily the most effective examples for different tasks.This paper proposes a new method, Active-Prompt, to adapt LLMs to different tasks with task-specific example prompts (annotated with human-designed CoT reasoning).For this purpose, we propose a solution to the key problem of determining which questions are the most important and helpful to annotate from a pool of task-specific queries.By borrowing ideas from the related problem of uncertainty-based active learning, we introduce several metrics to characterize the uncertainty so as to select the most uncertain questions for annotation.Experimental results demonstrate the superiority of our proposed method, achieving superior performance on eight complex reasoning tasks.Further analyses of different uncertainty metrics, pool sizes, zero-shot learning, and accuracy-uncertainty relationships demonstrate the effectiveness of our method. 1(1) Uncertainty Estimation

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-thought prompting elicits reasoning in large language models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This work established few-shot chain-of-thought exemplars as the mechanism for eliciting reasoning in LLMs and highlighted the practical reliance on a small, fixed set of human-crafted examples—precisely the limitation addressed here by selecting task-specific questions for annotation.

**Toward optimal active learning through sampling estimation of error reduction** (2001)
- *Authors:* Nicholas Roy et al.
- *Direct Connection:* This classic active learning work introduced entropy-based selection principles that we adapt to in-context prompting by ranking questions via answer-distribution entropy to prioritize annotation.

### 🏷️ Inspiration

**Fast rates in pool-based batch active learning** (2022)
- *Authors:* Claudio Gentile et al.
- *Direct Connection:* This work’s theoretical and empirical evidence that reducing model uncertainty accelerates learning motivates our strategy of selecting the most uncertain questions for CoT annotation.

### 🏷️ Baseline

**Automatic chain of thought prompting in large language models** (2022) [[arXiv](https://arxiv.org/abs/2210.03493)]
- *Authors:* Zhuosheng Zhang et al.
- *Direct Connection:* Auto-CoT’s automatic prompt construction via clustering and zero-shot CoT is the primary competing approach that our uncertainty-driven exemplar selection improves upon by selecting from a training pool rather than traversing the test set.

### 🏷️ Extension

**Self-consistency improves chain of thought reasoning in language models** (2022) [[arXiv](https://arxiv.org/abs/2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* Their multi-sample CoT generation and majority-vote scheme directly informs our method’s computation of uncertainty via disagreement/entropy over k sampled rationales and is also used for inference.

**Reducing labeling effort for structured prediction tasks** (2005)
- *Authors:* Aron Culotta et al.
- *Direct Connection:* Their least-confidence/uncertainty sampling ideas are operationalized here as simple disagreement-based uncertainty over multiple LLM answers to drive which questions to annotate.

### 🏷️ Related Problem

**Large language models are zero-shot reasoners** (2022) [[arXiv](https://arxiv.org/abs/2205.11916)]
- *Authors:* Takeshi Kojima et al.
- *Direct Connection:* Zero-shot CoT’s 'Let’s think step by step' enables generating reasoning without seed exemplars, which we adopt as an alternative way to obtain k sampled rationales for uncertainty estimation when few-shot seeds are unavailable.

---

## Synthesis: How Prior Work Led to This Paper

Few-shot chain-of-thought prompting showed that adding worked reasoning steps to exemplars elicits strong reasoning in LLMs, but it depended on a small, fixed set of human-curated examples, leaving open which examples best serve a given task. Self-consistency then demonstrated that sampling multiple chains and aggregating answers improves reliability, revealing a rich distribution over reasoning paths that can be exploited beyond voting. Auto-CoT proposed automatic prompt construction by clustering questions and using zero-shot chains, offering a way to automate exemplar discovery but relying on traversing test data rather than principled selection from task pools. Zero-shot CoT further established that simply priming models with “Let’s think step by step” can elicit chains without any seeds, enabling sampling-based strategies even when labeled exemplars are absent. In parallel, classic active learning work introduced entropy- and confidence-based selection criteria to prioritize uncertain instances for annotation, and subsequent theory showed that reducing uncertainty via active selection yields fast performance gains. These ideas collectively suggested that selectively annotating the most informative items can dramatically boost performance under tight budgets.
Synthesizing these strands, the current work reframes exemplar choice as an active selection problem: it samples multiple chains per question (in the spirit of self-consistency), quantifies uncertainty via disagreement/entropy (from active learning), and then annotates only the most uncertain questions with chain-of-thought rationales. This replaces static, hand-picked exemplars with task-tailored ones and can even be seeded by zero-shot chains, yielding a practical, data-efficient pathway to stronger reasoning prompts across diverse tasks.

---

*Analysis generated on: 2026-04-05T12:07:06.701093*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
