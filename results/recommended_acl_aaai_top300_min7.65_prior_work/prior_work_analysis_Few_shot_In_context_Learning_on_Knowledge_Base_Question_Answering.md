# Prior Work Analysis Report

## Target Paper

**Title:** Few-shot In-context Learning on Knowledge Base Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Question answering over knowledge bases is considered a difficult problem due to the challenge of generalizing to a wide variety of possible natural language questions. Additionally, the heterogeneity of knowledge base schema items between different knowledge bases often necessitates specialized training for different knowledge base question-answering (KBQA) datasets. To handle questions over diverse KBQA datasets with a unified training-free framework, we propose KB-BINDER, which for the first time enables few-shot in-context learning over KBQA tasks. Firstly, KB-BINDER leverages large language models like Codex to generate logical forms as the draft for a specific question by imitating a few demonstrations. Secondly, KB-BINDER grounds on the knowledge base to bind the generated draft to an executable one with BM25 score matching. The experimental results on four public heterogeneous KBQA datasets show that KB-BINDER can achieve a strong performance with only a few in-context demonstrations. Especially on GraphQA and 3-hop MetaQA, KB-BINDER can even outperform the state-of-the-art trained models. On GrailQA and WebQSP, our model is also on par with other fully-trained models. We believe KB-BINDER can serve as an important baseline for future research. We plan to release all the code and data. Our code is available at https://github.com/ltl3A87/KB-BINDER.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Evaluating Large Language Models Trained on Code** (2021) [[arXiv](https://arxiv.org/abs/2107.03374)]
- *Authors:* Mark Chen et al.
- *Direct Connection:* By demonstrating that Codex can translate natural language into structured, executable code from few in-context exemplars, this paper enabled KB-BINDER’s draft logical form generation via LLM imitation of <question, logical form> pairs.

### 🏷️ Inspiration

**What Makes Good In-Context Examples for GPT-3?** (2021) [[arXiv](https://arxiv.org/abs/2101.06804)]
- *Authors:* Jiachang Liu et al.
- *Direct Connection:* This study showed that retrieving semantically similar examples improves in-context learning, directly motivating KB-BINDER-R’s BM25-based exemplar retrieval to select demonstrations covering relevant schema items.

### 🏷️ Gap Identification

**Few-shot Complex Knowledge Base Question Answering via Meta Reinforcement Learning** (2020) [[arXiv](https://arxiv.org/abs/2010.15877)]
- *Authors:* Yuncheng Hua et al.
- *Direct Connection:* This prior ‘few-shot’ approach required ~2,000 labeled questions to train a meta-learner, highlighting the lack of true training-free few-shot KBQA that KB-BINDER explicitly addresses with in-context generation and binding.

### 🏷️ Baseline

**ArcaneQA: Dynamic Program Induction and Contextualized Encoding for Knowledge Base Question Answering** (2022)
- *Authors:* Yu Gu et al.
- *Direct Connection:* As a strong supervised KBQA system that relies on candidate-generation heuristics and fine-tuning, ArcaneQA serves as KB-BINDER’s primary baseline that it seeks to match or surpass without training or KB-specific heuristics.

### 🏷️ Extension

**Binding Language Models in Symbolic Languages** (2022) [[arXiv](https://arxiv.org/abs/2210.02875)]
- *Authors:* Zhoujun Cheng et al.
- *Direct Connection:* This work’s generate-then-bind paradigm for text-to-SQL—prompting an LLM to propose a program and then schema-linking it to an executable query—directly inspired KB-BINDER’s extension to KB logical forms with explicit entity and relation binding under graph constraints.

**Self-Consistency Improves Chain-of-Thought Reasoning in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* The self-consistency idea—sampling multiple reasoning outputs and majority voting—was adapted in KB-BINDER by sampling multiple logical-form drafts and voting on executed answers to improve robustness.

### 🏷️ Related Problem

**Semantic Parsing via Staged Query Graph Generation: Question Answering with Knowledge Base** (2015)
- *Authors:* Scott Wen-tau Yih et al.
- *Direct Connection:* Its staged query graph generation with entity linking and relation constraints (e.g., 2-hop neighborhoods and domain–range compatibility) informed KB-BINDER’s relation binder that restricts candidate relations to 2-hop vicinities and type-consistent links.

---

## Synthesis: How Prior Work Led to This Paper

A few pivotal strands set the stage for training-free few-shot KBQA. Binder showed that an LLM can propose a formal program and then be tethered to a real schema, using a post hoc linking stage to turn free-form outputs into executable SQL. Codex established that code-generation LLMs can translate natural language into structured, executable artifacts with only a handful of demonstrations, validating the feasibility of prompting for logical forms. Independent analyses of in-context learning revealed that carefully chosen demonstrations matter: retrieving semantically similar examples improves prompt effectiveness and sample efficiency. In parallel, self-consistency demonstrated that sampling multiple candidate solutions and majority voting significantly boosts reliability. Earlier KBQA semantic parsing research introduced staged query graph generation with entity linking and relation constraints—such as pruning to 2-hop neighborhoods and enforcing domain–range compatibility—codifying practical ways to reduce the search space in large KBs. Meanwhile, strong supervised systems like ArcaneQA and meta-learning attempts like few-shot meta-RL for KBQA highlighted two limitations: reliance on KB-specific heuristics with large labeled datasets, or a ‘few-shot’ setup that still needs thousands of labels to pretrain a meta-learner.
Together, these works suggested a path where LLMs generate approximate, semantically structured drafts that need not be schema-valid, then a KB-aware binding step resolves them into executable queries. By pairing Codex-powered draft generation with a Binder-style schema grounding extended to KB graphs—augmented by retrieved exemplars and self-consistency voting, and guided by classic relation and neighborhood constraints—the field had a natural next step: a truly training-free, few-shot KBQA pipeline that generalizes across heterogeneous schemas without bespoke heuristics.

---

*Analysis generated on: 2026-04-05T12:01:32.120869*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
