# Prior Work Analysis Report

## Target Paper

**Title:** Basic Reading Distillation

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) have demonstrated remarkable abilities in various natural language processing areas, but they demand high computation resources which limits their deployment in real-world.Distillation is one technique to solve this problem through either knowledge distillation or task distillation.Both distillation approaches train small models to imitate specific features of LLMs, but they all neglect basic reading education for small models on generic texts that are unrelated to downstream tasks.In this paper, we propose basic reading distillation (BRD) which educates a small model to imitate LLMs basic reading behaviors, such as named entity recognition, question raising and answering, on each sentence.After such basic education, we apply the small model on various tasks including language inference benchmarks and BIG-bench tasks.It shows that the small model can outperform or perform comparable to over 20x bigger LLMs.Analysis reveals that BRD effectively influences the probability distribution of the small model, and has orthogonality to either knowledge distillation or task distillation.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Distilling the Knowledge in a Neural Network** (2015) [[arXiv](https://arxiv.org/abs/1503.02531)]
- *Authors:* Geoffrey Hinton et al.
- *Direct Connection:* This work established the teacher–student distillation paradigm based on matching teacher logits, which BRD reinterprets by replacing latent logit imitation with explicit, sentence-level reading behaviors for the student to imitate.

### 🏷️ Inspiration

**Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes** (2023)
- *Authors:* Cheng-Yu Hsieh et al.
- *Direct Connection:* By showing that teacher-generated rationales enable more effective student training than labels alone, this paper directly inspired BRD’s use of explicit teacher signals via question-raising-and-answering as the supervised behaviors to imitate.

**Orca: Progressive Learning from Complex Explanation Traces of GPT-4** (2023) [[arXiv](https://arxiv.org/abs/2306.02707)]
- *Authors:* Subhabrata Mukherjee et al.
- *Direct Connection:* This work showed that small models benefit from learning from teacher explanation traces, motivating BRD to elicit and distill explanation-like signals—teacher questions and answers about each sentence—outside of any specific task.

### 🏷️ Gap Identification

**The False Promise of Imitating Proprietary LLMs** (2023) [[arXiv](https://arxiv.org/abs/2305.15717)]
- *Authors:* Arnav Gudibande et al.
- *Direct Connection:* This critique identified limited data scale and diversity in model imitation as a core weakness, motivating BRD to construct per-sentence reading-behavior supervision from web corpora to achieve effectively unlimited, diverse training signals.

### 🏷️ Baseline

**Want to Reduce Labeling Cost? GPT-3 Can Help** (2021)
- *Authors:* Shuohang Wang et al.
- *Direct Connection:* This task-distillation approach uses teacher-generated task labels as supervision, serving as a primary baseline that BRD departs from by distilling on generic sentences rather than downstream task datasets.

**Knowledge Distillation of Large Language Models (MiniLLM)** (2023) [[arXiv](https://arxiv.org/abs/2306.08543)]
- *Authors:* Yuxian Gu et al.
- *Direct Connection:* MiniLLM provides a strong LLM knowledge distillation method (reverse KL) that BRD directly compares against and later combines with, underscoring BRD’s orthogonality to logit-matching KD by adding explicit basic reading education.

### 🏷️ Related Problem

**Pre-training to Learn in Context** (2023)
- *Authors:* Yuxian Gu et al.
- *Direct Connection:* PICL demonstrated synthesizing intrinsic tasks from general corpora for in-context learning, informing BRD’s idea of deriving supervision from plain text while motivating its deviation from PICL’s retriever trained on downstream tasks by generating always-labeled NER/Q&A signals.

---

## Synthesis: How Prior Work Led to This Paper

Teacher–student distillation was formalized by Hinton et al., who supervised students with teacher logits, shaping a line of work that compresses large models by imitating internal distributions. Task-oriented imitation advanced in parallel, typified by Wang et al., who reduced labeling cost by supervising students with GPT-3’s task predictions. A key refinement emerged in distilling explicit reasoning signals: Hsieh et al. showed that incorporating teacher chain-of-thought rationales is more data-efficient than labels alone, suggesting that explicit, interpretable behaviors can transfer higher-order competencies. At the same time, critiques by Gudibande et al. highlighted that imitation pipelines suffer from constrained scale and diversity, and Orca demonstrated that learning from rich explanation traces helps smaller models acquire more general capability. In a related direction, PICL showed that intrinsic tasks can be synthesized from pretraining corpora to train in-context learning, albeit relying on retrievers trained on downstream tasks and sometimes lacking explicit labels. MiniLLM provided a strong, practical KD approach for LLMs, emphasizing reverse-KL logit matching as an effective baseline. Collectively, these works suggested two opportunities: first, that explicit, interpretable signals (rationales and explanation-like behaviors) can be powerful teaching targets; second, that scaling imitation beyond task-specific datasets is essential to overcome data diversity limitations. The natural next step was to synthesize abundant, label-ready supervision directly from generic text by eliciting basic reading behaviors—such as per-sentence named entity extraction and question-raising/answering—to educate a student model. By training on these ubiquitous, explicit signals and mixing them with original text, the approach remains orthogonal to logit-based KD and task distillation, scales to massive corpora, and transfers broadly across downstream tasks while remaining interpretable.

---

*Analysis generated on: 2026-04-05T11:59:47.419856*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
