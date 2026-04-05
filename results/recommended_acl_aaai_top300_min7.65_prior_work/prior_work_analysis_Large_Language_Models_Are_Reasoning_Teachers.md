# Prior Work Analysis Report

## Target Paper

**Title:** Large Language Models Are Reasoning Teachers

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent works have shown that chain-of-thought (CoT) prompting can elicit language models to solve complex reasoning tasks, step-by-step. However, prompt-based CoT methods are dependent on very large models such as GPT-3 175B which are prohibitive to deploy at scale. In this paper, we use these large models as reasoning teachers to enable complex reasoning in smaller models and reduce model size requirements by several orders of magnitude. We propose Fine-tune-CoT, a method that generates reasoning samples from very large teacher models to fine-tune smaller models. We evaluate our method on a wide range of public models and complex tasks. We find that Fine-tune-CoT enables substantial reasoning capability in small models, far outperforming prompt-based baselines and even the teacher model in many tasks. Additionally, we extend our method by leveraging the teacher model's ability to generate multiple distinct rationales for each original sample. Enriching the fine-tuning data with such diverse reasoning results in a substantial performance boost across datasets, even for very small models. We conduct ablations and sample studies to understand the emergence of reasoning capabilities of student models. Our code implementation and data are available at https://github.com/itsnamgyu/reasoning-teacher.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Large Language Models Are Zero-Shot Reasoners** (2022) [[arXiv](https://arxiv.org/abs/2205.11916)]
- *Authors:* Takeshi Kojima et al.
- *Direct Connection:* The paper’s zero-shot CoT instruction (“Let’s think step by step”) is the exact prompting strategy used to generate teacher rationales for constructing fine-tuning data in a task-agnostic, low-context way.

**Show Your Work: Scratchpads for Intermediate Computation** (2021)
- *Authors:* Maxwell Nye et al.
- *Direct Connection:* This paper established that fine-tuning with intermediate “scratchpad” steps enhances reasoning, providing the foundational insight that supervising on multi-step rationales (rather than only answers) is beneficial, though it relied on costly annotated steps.

### 🏷️ Inspiration

**Explanations from Large Language Models Make Small Reasoners Better** (2022) [[arXiv](https://arxiv.org/abs/2210.06726)]
- *Authors:* Shiyang Li et al.
- *Direct Connection:* By showing that LLM-produced explanations can improve smaller models on specific tasks, it inspired the general idea of leveraging teacher-generated rationales to teach small students across a wider range of reasoning problems.

**Self-Consistency Improves Chain of Thought Reasoning in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2203.07347)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* By showing that sampling multiple diverse CoT paths and aggregating improves answers, it provided the key insight behind generating multiple distinct rationales per sample (“diverse reasoning”) to strengthen the supervision signal for students.

### 🏷️ Gap Identification

**Large Language Models Can Self-Improve** (2022) [[arXiv](https://arxiv.org/abs/2210.11610)]
- *Authors:* Jiaxin Huang et al.
- *Direct Connection:* This work explored self-generated CoT for iterative improvement mainly in very large proprietary models and limited settings, motivating a more accessible teacher–student approach that systematically targets small, open models and broad tasks.

### 🏷️ Baseline

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This work introduced few-shot chain-of-thought prompting and highlighted its heavy reliance on very large models, forming both the main prompting baseline and the specific scalability limitation that the new method addresses by transferring CoT to smaller models.

### 🏷️ Extension

**STaR: Bootstrapping Reasoning With Reasoning** (2022) [[arXiv](https://arxiv.org/abs/2203.14465)]
- *Authors:* Ethan Zelikman et al.
- *Direct Connection:* STaR demonstrated training on model-generated rationales filtered by answer correctness; the new method extends this idea by adopting correctness-based filtering but using a separate large teacher to distill reasoning into smaller students and at scale.

---

## Synthesis: How Prior Work Led to This Paper

Few-shot chain-of-thought prompting established that step-by-step rationales can unlock strong reasoning but typically only in very large models, with chain-of-thought serving as both an effective technique and a scalability pain point. Zero-shot CoT then showed that a simple “Let’s think step by step” instruction can elicit rationales without task-specific exemplars, making it a cost-effective way to produce explanations. STaR demonstrated that models can be trained on their own generated rationales, using answer-correctness filtering to curate supervision, and thereby validated the notion that rationales themselves are a powerful training signal. Complementing this, scratchpad training revealed that injecting explicit intermediate computations into fine-tuning improves reasoning, albeit at the cost of human-crafted steps. Concurrently, LLM self-improvement and LLM-generated explanations for small models suggested that teacher-produced rationales could be used to elevate smaller students, though prior demonstrations were typically narrow in task coverage or centered on very large, proprietary systems. Finally, self-consistency showed that multiple valid reasoning paths exist and that sampling diverse chains can boost performance.
Bringing these strands together revealed a natural opportunity: use zero-shot CoT to let a strong teacher cheaply generate step-by-step solutions across tasks, curate them by answer correctness as in STaR, and fine-tune smaller students on these rationales as suggested by scratchpad and explanation-based training. The recognition from self-consistency that many distinct chains can solve a problem directly motivated augmenting each example with multiple diverse rationales to amplify supervision, thus addressing the key limitation of CoT’s reliance on huge models by distilling their reasoning into compact, deployable students.

---

*Analysis generated on: 2026-04-05T11:57:26.254589*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
