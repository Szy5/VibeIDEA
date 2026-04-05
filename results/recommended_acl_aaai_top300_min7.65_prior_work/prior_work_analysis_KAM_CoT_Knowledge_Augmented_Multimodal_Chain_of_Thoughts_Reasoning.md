# Prior Work Analysis Report

## Target Paper

**Title:** KAM-CoT: Knowledge Augmented Multimodal Chain-of-Thoughts Reasoning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLMs) have demonstrated impressive performance in natural language processing tasks by leveraging chain of thought (CoT) that enables step-by-step thinking. Extending LLMs with multimodal capabilities is the recent interest, but incurs computational cost and requires substantial hardware resources. To address these challenges, we propose KAM-CoT a framework that integrates CoT reasoning, Knowledge Graphs (KGs), and multiple modalities for a comprehensive understanding of multimodal tasks. KAM-CoT adopts a two-stage training process with KG grounding to generate effective rationales and answers. By incorporating external knowledge from KGs during reasoning, the model gains a deeper contextual understanding reducing hallucinations and enhancing the quality of answers. This knowledge-augmented CoT reasoning empowers the model to handle questions requiring external context, providing more informed answers. Experimental findings show KAM-CoT outperforms the state-of-the-art methods. On the ScienceQA dataset, we achieve an average accuracy of 93.87%, surpassing GPT-3.5 (75.17%) by 18% and GPT-4 (83.99%) by 10%. Remarkably, KAM-CoT achieves these results with only 280M trainable parameters at a time, demonstrating its cost-efficiency and effectiveness.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**ScienceQA: A Multi-Modal Dataset for Multi-Type Problem Solving in Science** (2022)
- *Authors:* Lu et al.
- *Direct Connection:* ScienceQA provides the multimodal science questions with human explanations and the explain-then-answer training setup that KAM-CoT leverages in its two-stage rationale-and-answer training pipeline.

### 🏷️ Inspiration

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* KAM-CoT adopts and extends the step-by-step rationale generation paradigm introduced by Chain-of-Thought prompting, but grounds those intermediate steps in external knowledge to improve faithfulness.

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2210.03629)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* KAM-CoT adopts ReAct’s core insight of interleaving reasoning with external information acquisition by grounding chain-of-thought steps in a knowledge graph during inference and training.

**Retrieval-Augmented Generation for Knowledge-Intensive NLP** (2020) [[arXiv](https://arxiv.org/abs/2005.11401)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* KAM-CoT adapts the retrieval-augmented generation principle to structured sources by replacing text passage retrieval with KG grounding during rationale construction.

### 🏷️ Gap Identification

**OK-VQA: A Visual Question Answering Benchmark Requiring External Knowledge** (2019)
- *Authors:* Kenneth Marino et al.
- *Direct Connection:* By demonstrating that many visual questions require external knowledge beyond the image, OK-VQA motivates KAM-CoT’s use of knowledge graphs to support multimodal reasoning.

### 🏷️ Extension

**Multimodal Chain-of-Thought Reasoning in Language Models** (2023)
- *Authors:* Zhang et al.
- *Direct Connection:* KAM-CoT directly builds on the multimodal CoT formulation that fuses visual and textual evidence into explicit reasoning traces, extending it by injecting knowledge-graph grounding into the chain to reduce hallucination and handle knowledge-intensive queries.

### 🏷️ Related Problem

**QA-GNN: Reasoning with Language Models and Knowledge Graphs for Commonsense Question Answering** (2021)
- *Authors:* Michihiro Yasunaga et al.
- *Direct Connection:* KAM-CoT borrows the idea of entity linking and KG grounding from QA-GNN to inject structured commonsense knowledge into the reasoning process for question answering.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-Thought prompting showed that eliciting explicit intermediate reasoning steps enables large language models to solve complex problems more reliably by supervising or prompting stepwise rationales. Multimodal Chain-of-Thought extended this idea to vision-language settings, demonstrating that textual and visual evidence can be fused within an explicit reasoning trace to tackle multimodal questions, particularly on benchmarks with explanation supervision. ScienceQA established a multimodal science question answering task with human explanations and common training/evaluation protocols for explanation-first, answer-second pipelines, seeding techniques that learn to generate rationales before predicting answers. ReAct revealed that combining reasoning traces with targeted external information acquisition reduces hallucinations by interleaving thought and tool use. QA-GNN provided a template for grounding questions in knowledge graphs via entity linking and graph reasoning to inject structured commonsense into QA models. OK-VQA highlighted the insufficiency of visual and textual context alone for many questions, underscoring the need for external knowledge to answer knowledge-intensive queries. Retrieval-Augmented Generation furnished a general mechanism to supply external knowledge at generation time for knowledge-intensive tasks.
Together, these works exposed a gap: multimodal CoT improves interpretability and accuracy, but it lacks faithful external grounding, while knowledge-augmented QA injects facts without explicit stepwise reasoning or multimodal fusion. KAM-CoT naturally synthesizes these threads by adopting ScienceQA’s explain-then-answer setup and MM-CoT’s multimodal rationales, while operationalizing ReAct/RAG’s external augmentation through explicit KG grounding (inspired by QA-GNN and OK-VQA) within the chain-of-thought, yielding more informed, less hallucinated reasoning at low computational cost.

---

*Analysis generated on: 2026-04-04T22:28:53.559388*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
