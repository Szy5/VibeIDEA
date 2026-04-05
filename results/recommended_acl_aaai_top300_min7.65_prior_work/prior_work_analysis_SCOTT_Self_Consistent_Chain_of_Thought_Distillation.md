# Prior Work Analysis Report

## Target Paper

**Title:** SCOTT: Self-Consistent Chain-of-Thought Distillation

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LMs) beyond a certain scale, demonstrate the emergent capability of generating free-text rationales for their predictions via chain-of-thought (CoT) prompting.While CoT can yield dramatically improved performance, such gains are only observed for sufficiently large LMs. Even more concerning, there is little guarantee that the generated rationales are consistent with LM's predictions or faithfully justify the decisions. In this work, we propose SCOTT, a faithful knowledge distillation method to learn a small, self-consistent CoT model from a teacher model that is orders of magnitude larger. To form better supervision, we elicit rationales supporting the gold answers from a large LM (teacher) by contrastive decoding, which encourages the teacher to generate tokens that become more plausible only when the answer is considered. To ensure faithful distillation, we use the teacher-generated rationales to learn a student LM with a counterfactual reasoning objective, which prevents the student from ignoring the rationales to make inconsistent predictions. Experiments show that while yielding comparable performance, our method leads to a more faithful model than baselines. Further analysis shows that such a model respects the rationales more when making decisions; thus, we can improve its performance more by refining its rationales.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* Established the self-rationalization (rationale-then-answer) paradigm and showed that CoT improves reasoning only in large LMs, defining the target behavior and scale gap that the distillation framework aims to bridge.

### 🏷️ Inspiration

**PINTO: Faithful Language Reasoning Using Prompt-Generated Rationales** (2022) [[arXiv](https://arxiv.org/abs/2211.01562)]
- *Authors:* Peifeng Wang et al.
- *Direct Connection:* Argued for and explored faithfulness in language reasoning using prompt-generated rationales, inspiring SCOTT’s emphasis on self-consistency and faithful supervision when learning to reason with CoT.

### 🏷️ Gap Identification

**Explanations from Large Language Models Make Small Reasoners Better** (2022) [[arXiv](https://arxiv.org/abs/2210.06726)]
- *Authors:* Shiyang Li et al.
- *Direct Connection:* Showed that distilling LLM-generated explanations improves small models but treated rationales as auxiliary regularizers not tied to decisions, motivating SCOTT’s counterfactual objective to ensure predictions depend on the provided rationale.

**The Unreliability of Explanations in Few-Shot In-Context Learning** (2022) [[arXiv](https://arxiv.org/abs/2205.03401)]
- *Authors:* Xi Ye et al.
- *Direct Connection:* Demonstrated that LMs’ generated explanations can contradict predictions and lack faithfulness, directly motivating SCOTT’s focus on aligning rationales with answers and enforcing consistency during distillation.

### 🏷️ Baseline

**KNIFE: Knowledge Distillation with Free-Text Rationales** (2022) [[arXiv](https://arxiv.org/abs/2212.09721)]
- *Authors:* Aaron Chan et al.
- *Direct Connection:* Introduced a KD pipeline that transfers free-text rationales from a teacher to a student, serving as the primary framework SCOTT strengthens by enforcing answer-grounded supervision and student self-consistency.

### 🏷️ Extension

**Contrastive Decoding: Open-ended Text Generation as Optimization** (2022) [[arXiv](https://arxiv.org/abs/2210.15097)]
- *Authors:* Xiang Lisa Li et al.
- *Direct Connection:* Provides the core decoding idea SCOTT adapts—prefer tokens whose plausibility increases when conditioned on specific context—which is extended to elicit answer-grounded rationales by contrasting gold versus perturbed answers.

### 🏷️ Related Problem

**Distilling Multi-Step Reasoning Capabilities of Large Language Models into Smaller Models via Semantic Decompositions** (2022) [[arXiv](https://arxiv.org/abs/2212.00193)]
- *Authors:* Kumar Shridhar et al.
- *Direct Connection:* Showed that multi-step reasoning behaviors can be distilled into small models via structured decompositions, informing SCOTT’s pursuit of reasoning distillation but highlighting the need to handle open-ended CoT with faithfulness constraints.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-thought prompting established that prompting large language models to articulate step-by-step rationales before answering improves reasoning quality, defining the self-rationalization setup and highlighting that such gains emerge only at large scales. Contrastive decoding introduced an optimization view of generation that suppresses generic, overly plausible tokens by favoring those whose likelihood increases under specific conditioning; this offers a principled mechanism to discourage hallucinations during open-ended generation. Distillation works that transfer LLM-generated explanations to smaller models demonstrated practical performance benefits but typically treated rationales as auxiliary signals that do not shape predictions at inference, leaving the connection between rationale and answer tenuous. KNIFE further instantiated knowledge distillation with free-text rationales as the primary supervision channel. Simultaneously, empirical analyses showed few-shot in-context explanations to be unreliable and sometimes contradictory, underscoring a lack of faithfulness in generated rationales. Finally, research on distilling multi-step reasoning via structured decompositions verified that complex reasoning behaviors can be transferred to compact models, though largely in constrained, math-oriented settings, while investigations into faithful language reasoning with prompt-generated rationales argued for aligning explanations with underlying decisions.
Together, these strands revealed a gap: small models benefit from distilled rationales but lack mechanisms to ensure those rationales truly ground and govern predictions. The natural next step is to elicit rationales explicitly conditioned on correct answers using a contrastive mechanism to curb hallucination, and to train students so that different rationales yield different answers via counterfactual supervision. By combining answer-grounded rationale extraction with an objective that ties prediction causally to the provided rationale, this synthesis yields a self-consistent, faithful chain-of-thought distillation pipeline that preserves performance while making the model’s reasoning accountable.

---

*Analysis generated on: 2026-04-05T11:55:22.764778*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
