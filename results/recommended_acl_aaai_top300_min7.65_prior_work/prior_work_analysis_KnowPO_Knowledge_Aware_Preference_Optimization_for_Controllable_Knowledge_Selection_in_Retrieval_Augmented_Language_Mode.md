# Prior Work Analysis Report

## Target Paper

**Title:** KnowPO: Knowledge-Aware Preference Optimization for Controllable Knowledge Selection in Retrieval-Augmented Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> By integrating external knowledge, Retrieval-Augmented Generation (RAG) has become an effective strategy for mitigating the hallucination problems that large language models (LLMs) encounter when dealing with knowledge-intensive tasks. However, in the process of integrating external non-parametric supporting evidence with internal parametric knowledge, inevitable knowledge conflicts may arise, leading to confusion in the model's responses. To enhance the knowledge selection of LLMs in various contexts, some research has focused on refining their behavior patterns through instruction-tuning. Nonetheless, due to the absence of explicit negative signals and comparative objectives, models fine-tuned in this manner may still exhibit undesirable behaviors such as contextual ignorance and contextual overinclusion. To this end, we propose a Knowledge-aware Preference Optimization strategy, dubbed KnowPO, aimed at achieving adaptive knowledge selection based on contextual relevance in real retrieval scenarios. Concretely, we proposed a general paradigm for constructing knowledge conflict datasets, which comprehensively cover various error types and learn how to avoid these negative signals through preference optimization methods. Simultaneously, we proposed a rewriting strategy and data ratio optimization strategy to address preference imbalances. Experimental results show that KnowPO outperforms previous methods for handling knowledge conflicts by over 37%, while also exhibiting robust generalization across various out-of-distribution datasets.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Entity-Based Knowledge Conflicts in Question Answering** (2022) [[arXiv](https://arxiv.org/abs/2109.05052)]
- *Authors:* Longpre et al.
- *Direct Connection:* This work formalized knowledge-conflict scenarios and showed LMs’ tendency to favor parametric over contextual knowledge, establishing the precise problem setting that KnowPO targets with adherence-focused supervision.

**Know What You Don’t Know: Unanswerable Questions for SQuAD** (2018) [[arXiv](https://arxiv.org/abs/1806.03822)]
- *Authors:* Rajpurkar et al.
- *Direct Connection:* SQuAD2.0’s answerable/unanswerable annotations enabled KnowPO’s controlled construction of conflicting versus irrelevant contexts and the formulation of preference pairs for adherence and robustness.

### 🏷️ Gap Identification

**Large Language Models Can Be Easily Distracted by Irrelevant Context** (2023) [[arXiv](https://arxiv.org/abs/2302.00093)]
- *Authors:* F. Shi et al.
- *Direct Connection:* By demonstrating that LLMs overuse irrelevant context, this paper motivated KnowPO’s explicit noise-robustness objective and guided the construction of irrelevant-context preference pairs.

**ClashEval: Quantifying the tug-of-war between an LLM’s internal prior and external evidence** (2024) [[arXiv](https://arxiv.org/abs/2404.10198)]
- *Authors:* Wu et al.
- *Direct Connection:* ClashEval showed that high prior token probabilities make external evidence hard to override, directly motivating KnowPO’s preference training to mitigate internal-prior dominance and its analysis of prior-probability effects.

**Disentangling Length from Quality in Direct Preference Optimization** (2024) [[arXiv](https://arxiv.org/abs/2403.19159)]
- *Authors:* Park et al.
- *Direct Connection:* By revealing DPO’s susceptibility to length bias, this work prompted KnowPO’s rewriting strategy to align positive/negative response lengths and prevent length-driven reward hacking during preference optimization.

### 🏷️ Baseline

**Trusting Your Evidence: Hallucinate Less with Context-aware Decoding** (2023) [[arXiv](https://arxiv.org/abs/2305.14739)]
- *Authors:* W. Shi et al.
- *Direct Connection:* As a leading decoding-time approach conditioning on context, CAD served as a primary baseline whose coherence trade-offs motivated KnowPO’s training-time solution to improve adherence without harming fluency.

### 🏷️ Extension

**Direct Preference Optimization: Your Language Model is Secretly a Reward Model** (2024) [[arXiv](https://arxiv.org/abs/2305.18290)]
- *Authors:* Rafailov et al.
- *Direct Connection:* KnowPO directly extends DPO by defining knowledge-aware preference pairs that penalize contextual ignorance and contextual overinclusion, while adding response-length alignment and pair-ratio balancing to tailor DPO for RAG knowledge-conflict training.

---

## Synthesis: How Prior Work Led to This Paper

Direct Preference Optimization introduced an efficient way to align language models with pairwise human preferences, but its vanilla objective is agnostic to domain-specific pitfalls and can be biased by response length. Work on DPO’s length confounds showed that longer responses can be spuriously preferred, indicating the need for length-controlled data when using preference learning. In parallel, entity-centric studies of knowledge conflicts established that large language models habitually privilege internal parametric knowledge over contextual evidence, precisely defining when adherence to retrieved content should be enforced. Research demonstrating that LLMs are easily distracted by irrelevant passages highlighted the complementary requirement of noise robustness, while analyses quantifying the tug-of-war between internal priors and external evidence revealed that high-probability internal answers are especially resistant to contextual override. At the method level, context-aware decoding provided a contrastive baseline that conditions on evidence at inference time, yet it can degrade semantic coherence, suggesting a need for training-time solutions.
Bringing these strands together naturally suggested a preference-learning approach purpose-built for retrieval settings: construct controlled conflicting and irrelevant contexts (facilitated by answerability annotations) and encode two explicit negative behaviors—contextual ignorance and overinclusion—into preference pairs. Extending DPO with length-aligned outputs and a balanced ratio of adherence-versus-robustness pairs directly addresses known DPO biases and the internal-prior dominance, enabling a trained model to selectively trust retrieved evidence while resisting distractors.

---

*Analysis generated on: 2026-04-05T12:06:19.427671*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
