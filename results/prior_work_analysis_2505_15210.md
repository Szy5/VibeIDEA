# Prior Work Analysis Report

## Target Paper

**Title:** Deliberation on Priors: Trustworthy Reasoning of Large Language Models on Knowledge Graphs

**arXiv ID:** [2505.15210](https://arxiv.org/abs/2505.15210)

**Abstract:** 
> Knowledge graph-based retrieval-augmented generation seeks to mitigate hallucinations in Large Language Models (LLMs) caused by insufficient or outdated knowledge. However, existing methods often fail to fully exploit the prior knowledge embedded in knowledge graphs (KGs), particularly their structural information and explicit or implicit constraints. The former can enhance the faithfulness of LLMs' reasoning, while the latter can improve the reliability of response generation. Motivated by these, we propose a trustworthy reasoning framework, termed Deliberation over Priors (DP), which sufficiently utilizes the priors contained in KGs. Specifically, DP adopts a progressive knowledge distillation strategy that integrates structural priors into LLMs through a combination of supervised fine-tuning and Kahneman-Tversky optimization, thereby improving the faithfulness of relation path generation. Furthermore, our framework employs a reasoning-introspection strategy, which guides LLMs to perform refined reasoning verification based on extracted constraint priors, ensuring the reliability of response generation. Extensive experiments on three benchmark datasets demonstrate that DP achieves new state-of-the-art performance, especially a Hit@1 improvement of 13% on the ComplexWebQuestions dataset, and generates highly trustworthy responses. We also conduct various analyses to verify its flexibility and practicality. The code is available at https://github.com/reml-group/Deliberation-on-Priors.

**Innovation pattern:** Inference-Time Control & Guided Sampling (confidence: high)

Secondary patterns: Modular Pipeline Composition, Gap-Driven Reframing

*Reasoning:* Centers on inference-time deliberation/verification to improve trustworthy KG reasoning (guidance at sampling/time of use), while composing modular planning/retrieval/instantiation steps and addressing a gap in faithful path-based grounding.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Constraint-based Question Answering with Knowledge Graph** (2016)
- *Authors:* J. Bao et al.
- *Direct Connection:* DP uses the constraint taxonomy (type, multi-entity, explicit/implicit time, ordinal) introduced by this work as the predefined constraint prior set for introspective verification and backtracking of instantiated KG reasoning paths.

### 🏷️ Inspiration

**Debate on Graph: A Flexible and Reliable Reasoning Framework for Large Language Models** (2025)
- *Authors:* J. Ma et al.
- *Direct Connection:* DoG’s use of deliberative mechanisms (multi-agent debate and iterative verification) to increase answer reliability directly motivated DP’s emphasis on deliberate verification and backtracking, but DP replaces multi-agent debate with constraint-guided introspection and path-level distillation.

### 🏷️ Baseline

**Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning** (2024)
- *Authors:* L. Luo et al.
- *Direct Connection:* This work established the paradigm of prompting/fine-tuning LLMs to generate relation-paths over KGs and grounding answers from those paths, which DP directly improves by moving from RoG’s one-to-one path mapping toward a one-to-many shortest-path weak supervision collection and by distilling structural priors to produce more faithful path generation.

### 🏷️ Extension

**KTO: Model Alignment as Prospect Theoretic Optimization** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2402.01306)]
- *Authors:* K. Ethayarajh et al.
- *Direct Connection:* DP directly adopts and adapts the Kahneman–Tversky optimization (KTO) objective from this paper to perform preference-aware fine-tuning on imbalanced synthetic positive/negative relation-path data, extending KTO’s use to relation-path preference modeling during knowledge distillation.

### 🏷️ Related Problem

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph** (2024)
- *Authors:* J. Sun et al.
- *Direct Connection:* Think-on-Graph formalized stepwise LLM reasoning over KGs (topic-entity identification, iterative retrieval, and path refinement), which informed DP’s planning/instantiation design while DP departs by shifting costly online stepwise retrieval into offline distillation of structural priors and by adding constraint-driven introspection.

**StructGPT: A General Framework for Large Language Model to Reason over Structured Data** (2023)
- *Authors:* J. Jiang et al.
- *Direct Connection:* StructGPT provided a general methodology for steering LLMs to operate on structured inputs (tables/graphs), and DP builds on that direction by focusing specifically on exploiting KG structural priors (relation-path extraction and distillation) and introducing constraint-based verification to reduce hallucination.

---

## Synthesis: How Prior Work Led to This Paper

Prior work established both the technical pieces DP assembles and the gaps it fills. Luo et al. (RoG) demonstrated generating relation-paths with LLMs and grounding answers from those paths, setting the direct baseline for faithful, path-based KG reasoning but typically using one-to-one mappings between question and a single path. Think-on-Graph and StructGPT developed stepwise and structured-data reasoning paradigms for LLMs, formalizing topic-entity identification, iterative retrieval, and plan generation over graphs and structured inputs—providing the planning/instantiation and structured prompting blueprints DP leverages. DoG introduced deliberative reliability techniques (debate/iterative verification) to reduce unfaithful outputs, motivating DP’s focus on deliberation; however, DP opts for introspection with explicit constraint priors rather than multi-agent debate. Bao et al. provided the practical constraint taxonomy (type, multi-entity, explicit/implicit time, ordinal) that DP directly uses for verification and backtracking. Finally, Ethayarajh et al.’s KTO supplied a prospect-theoretic preference optimization objective that DP adopts and adapts to handle severe class imbalance when training on synthetically perturbed positive/negative relation-paths. Together these works reveal an opportunity: existing methods either generate paths without fully exploiting multiple shortest-path priors, or they rely on runtime stepwise retrieval and debate without explicit constraint-guided verification, and conventional preference training struggles with imbalanced perturbed path data. DP naturally follows by collecting one-to-many shortest-path weak supervision, distilling those structural priors into LLMs via SFT plus KTO-based preference optimization, and adding constraint-driven introspection and backtracking to produce more faithful and reliable KG-grounded generation.

---

*Analysis generated on: 2026-03-08T23:57:01.132751*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=16269, output=1190*
