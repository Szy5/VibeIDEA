# Prior Work Analysis Report

## Target Paper

**Title:** Synergistic Multi-Agent Framework with Trajectory Learning for Knowledge-Intensive Tasks

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent advancements in Large Language Models (LLMs) have led to significant breakthroughs in various natural language processing tasks. However, generating factually consistent responses in knowledge-intensive scenarios remains a challenge due to issues such as hallucination, difficulty in acquiring long-tailed knowledge, and limited memory expansion. This paper introduces SMART, a novel multi-agent framework that leverages external knowledge to enhance the interpretability and factual consistency of LLM-generated responses. SMART comprises four specialized agents, each performing a specific sub-trajectory action to navigate complex knowledge-intensive tasks. We propose a multi-agent co-training paradigm, Long-Short Trajectory Learning, which ensures synergistic collaboration among agents while maintaining fine-grained execution by each agent. Extensive experiments on five knowledge-intensive tasks demonstrate SMART's superior performance compared to widely adopted knowledge internalization and knowledge enhancement methods. Our framework can extend beyond knowledge-intensive tasks to more complex scenarios.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Inspiration

**Enabling Large Language Models to Generate Text with Citations** (2023)
- *Authors:* Tianyu Gao et al.
- *Direct Connection:* This work’s explicit citation-conditioned generation and evaluation directly informed SMART’s Response Generator design to emit grounded answers with document-level citations as a first-class output.

### 🏷️ Gap Identification

**Ra-DIT: Retrieval-Augmented Dual Instruction Tuning** (2023) [[arXiv](https://arxiv.org/abs/2310.01352)]
- *Authors:* Xilun V. Lin et al.
- *Direct Connection:* Ra-DIT showed that end-to-end instruction tuning with retrieval improves grounding but lacks explicit step-wise supervision, motivating SMART’s two-stage Long-Short Trajectory Learning to retain per-agent precision while enforcing global synergy.

**Recomp: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation** (2023) [[arXiv](https://arxiv.org/abs/2310.04408)]
- *Authors:* Fengbin Xu et al.
- *Direct Connection:* By highlighting the need to filter and compress contexts at document/sentence granularity yet relying on separate modules, this work motivated SMART’s integrated Fact Locator that learns document- and span-level relevance within the trajectory to reduce distraction and error accumulation.

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2210.03629)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* ReAct’s prompting-based interleaving of reasoning and actions without training exposed the lack of learned coordination in multi-step pipelines, motivating SMART’s learned inter-agent transitions via trajectory tokens to reduce cascading errors.

### 🏷️ Baseline

**Small LLMs are Weak Tool Learners: A Multi-LLM Agent** (2024) [[arXiv](https://arxiv.org/abs/2401.07324)]
- *Authors:* Wenqi Shen et al.
- *Direct Connection:* As a modular multi-agent baseline that combines independently tuned agents without joint training, this work provided the primary comparison point that SMART aims to surpass by co-training agents with Long-Short Trajectory Learning for synergistic execution.

### 🏷️ Extension

**Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection** (2023) [[arXiv](https://arxiv.org/abs/2310.11511)]
- *Authors:* Akari Asai et al.
- *Direct Connection:* Self-RAG’s use of specialized feedback tokens and an internal critic to supervise retrieval and generation directly inspired SMART’s trajectory head/end tokens and its long-trajectory supervision that coordinates agent transitions via self-critique signals.

**Query Rewriting in Retrieval-Augmented Large Language Models** (2023)
- *Authors:* Xinyao Ma et al.
- *Direct Connection:* Their demonstration that rewriting clarifies complex user intents for better retrieval underpins SMART’s Intent Reconstructor, which generalizes query rewriting to unify formats, decompose multi-hop intents, and standardize downstream retrieval.

---

## Synthesis: How Prior Work Led to This Paper

Self-RAG showed that large language models can supervise their own retrieval and generation using specialized feedback tokens and a self-critic, demonstrating the power of tokenized control signals and reflective supervision to improve factuality. Ra-DIT established that end-to-end instruction tuning with retrieval boosts grounding, but it offered no explicit mechanisms to preserve phase-specific precision, leaving step-level control under-optimized. Work on citation-anchored generation made citations a first-class output objective, proving that making provenance explicit improves fidelity and enables downstream evaluation. Query rewriting for retrieval-augmented models revealed that clarifying user intent—by reformulating ambiguous or multi-format inputs—reliably improves retrieval, highlighting the need for a dedicated intent clarification stage. Studies on compression and selective augmentation showed the value of document- and sentence-level filtering, but their reliance on separate modules made them vulnerable to error propagation. Prompt-based pipelines like ReAct, and modular multi-LLM agents, demonstrated effective multi-step behavior without learning inter-step coordination, exposing a gap in trainable, synergistic control across phases.
Collectively, these works suggested a path forward: unify intent clarification, retrieval, relevance filtering, and grounded generation under trainable, token-mediated control. SMART synthesizes these insights by instantiating specialized agents for intent, retrieval, fact location, and citation-grounded response, then introducing trajectory head/end tokens to supervise both fine-grained per-agent behaviors and learned inter-agent transitions. The resulting Long-Short Trajectory Learning preserves step-specific competencies while aligning global execution, a natural evolution from feedback-token supervision, end-to-end retrieval tuning, and modular evidence selection toward a cohesive, co-trained multi-agent system.

---

*Analysis generated on: 2026-04-05T11:37:57.390657*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
