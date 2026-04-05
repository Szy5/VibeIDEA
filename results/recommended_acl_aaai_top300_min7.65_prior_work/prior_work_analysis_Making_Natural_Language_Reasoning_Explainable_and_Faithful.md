# Prior Work Analysis Report

## Target Paper

**Title:** Making Natural Language Reasoning Explainable and Faithful

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Neural models, including large language models (LLMs), achieve superior performance on logical reasoning tasks such as question answering. To elicit reasoning capabilities from LLMs, recent works propose using the chain-of-thought (CoT) mechanism to generate both the reasoning chain and the answer, which enhances the model’s capabilities in conducting reasoning. However, due to LLM’s uninterpretable nature and the extreme flexibility of free-form explanations, several challenges remain: such as struggling with inaccurate reasoning, hallucinations, and not aligning with human preferences. In this talk, we will focus on (1) our design of leveraging structured information (that is grounded to the context), for the explainable complex question answering and reasoning; (2) our multi-module interpretable framework for inductive reasoning, which conducts step-wise faithful reasoning with iterative feedback.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering** (2018) [[arXiv](https://arxiv.org/abs/1809.09600)]
- *Authors:* Zhilin Yang et al.
- *Direct Connection:* HotpotQA defined multi-hop QA with supporting facts, directly framing the task setting where the current work builds entity–relation graphs from context to produce faithful, grounded reasoning and answers.

**Language Models as Inductive Reasoners** (2022) [[arXiv](https://arxiv.org/abs/2212.10923)]
- *Authors:* Z. Yang et al.
- *Direct Connection:* This work showed LLMs can transform natural language facts into candidate rules but that the process is opaque and prone to hallucinations, directly motivating the current paper’s modular decomposition with interpretable checking and iterative refinement for faithful induction.

### 🏷️ Inspiration

**Cognitive Graph for Multi-Hop Reading Comprehension** (2019) [[arXiv](https://arxiv.org/abs/1905.05412)]
- *Authors:* Yuwei Ding et al.
- *Direct Connection:* This paper demonstrated that constructing entity-centric graphs from text and performing graph-based reasoning improves multi-hop interpretability, a key idea the current work adapts by extracting semantic graphs and using them to strictly guide LLM reasoning and explanations.

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2210.03629)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* ReAct’s integration of step-wise thoughts with environment-grounded actions and feedback informs the current work’s step-wise, feedback-driven reasoning design, particularly the iterative verification and correction loop for faithful rule induction.

### 🏷️ Gap Identification

**Self-Consistency Improves Chain of Thought Reasoning in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* By showing CoT’s variability and reliance on sampling for accuracy rather than faithfulness, this paper motivates the need for structured, grounded guidance that the current work provides via semantic graphs and verification.

### 🏷️ Baseline

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This work established free-form chain-of-thought generation as the dominant way to elicit LLM reasoning, which the current paper directly constrains by replacing unconstrained CoT with structured, context-grounded semantic graphs to improve faithfulness.

### 🏷️ Extension

**Self-Refine: Iterative Refinement with Self-Feedback** (2023) [[arXiv](https://arxiv.org/abs/2303.17651)]
- *Authors:* Aman Madaan et al.
- *Direct Connection:* Building on the idea of model-generated critiques to iteratively improve outputs, the current work extends this paradigm by instantiating dedicated clarity, reality, and novelty checkers that supply explicit feedback to refine induced rules.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-thought prompting revealed that large language models can improve on reasoning tasks by producing step-by-step explanations, but it did so through unconstrained, free-form rationales. Subsequent work on self-consistency highlighted that such chains vary widely and require sampling to stabilize answers, sharpening concerns about faithfulness rather than merely accuracy. Multi-hop QA was framed by HotpotQA, which mandated reasoning across multiple pieces of evidence and provided supporting facts, situating the need for explanations grounded in the input. Graph-based multi-hop reading comprehension research showed that extracting entity–relation graphs from text and reasoning over them makes the process more interpretable, indicating the value of structured, context-grounded representations. In parallel, “Language Models as Inductive Reasoners” demonstrated that LLMs can induce rules from facts but often hallucinate and lack interpretability. Agent-style methods such as ReAct introduced step-wise reasoning intertwined with environment-grounded actions and feedback, while Self-Refine showed that explicit critiques can iteratively improve model outputs.
Together, these works expose a gap: free-form CoT enhances capability but is unfaithful, while graph-based methods provide structure yet were not leveraged to steer LLM reasoning or rule induction; and LLM-induced rules lack verification. The current work synthesizes these insights by extracting semantic graphs from context to strictly guide reasoning for multi-hop QA, yielding grounded, faithful explanations, and by decomposing inductive rule generation into interpretable modules that provide clarity, reality, and novelty checks with iterative feedback, naturally extending self-improvement loops with structured verification.

---

*Analysis generated on: 2026-04-05T11:38:21.934929*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
