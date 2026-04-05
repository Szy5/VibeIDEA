# Prior Work Analysis Report

## Target Paper

**Title:** Large Language and Reasoning Models are Shallow Disjunctive Reasoners

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLMs) and Systematic Reasoning Large Language Models (LLMs) have been found to struggle with systematic reasoning. Even on tasks where they appear to perform well, their performance often depends on shortcuts rather than genuine reasoning abilities, leading them to collapse on out-of-distribution (OOD) examples. Post-training strategies based on reinforcement learning and chain-of-thought prompting have recently been hailed as a step change. However, little is known about the potential of the resulting “Large Reasoning Models” (LRMs) beyond maths and programming-based problem solving, where genuine OOD problems can be sparse. In this paper, we focus on tasks that require systematic relational composition for qualitative spatial and temporal reasoning. The setting allows fine control over problem difficulty to precisely measure OOD generalization. We find that zero-shot LRMs generally outperform their LLM counterparts in single-path reasoning tasks but struggle in the multi-path setting. While showing comparatively better results, fine-tuned LLMs are also not capable of multi-path generalization. We also provide evidence for the behavioral interpretation of this—namely, that LRMs are shallow disjunctive reasoners.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Systematic relational reasoning with epistemic graph neural networks** (2025)
- *Authors:* Irtaza Khalid and Steven Schockaert
- *Direct Connection:* This work introduces the STaR benchmark and its k- (path length) and b- (path count) controlled construction for RCC-8/IA, which the current paper directly adopts to generate OOD disjunctive reasoning instances and to supply composition tables in the prompt.

**Maintaining knowledge about temporal intervals** (1983)
- *Authors:* James F. Allen
- *Direct Connection:* The Interval Algebra provides the 13 JEPD temporal relations and their composition table that define the temporal half of the tasks, serving as the exact ground-truth calculus the models are asked to apply.

**A Spatial Logic based on Regions and Connection** (1992)
- *Authors:* David A. Randell et al.
- *Direct Connection:* RCC-8 supplies the eight JEPD spatial relations and their composition rules, forming the precise relational labels and compositions that the paper’s spatial tasks require models to compute.

**The Algebraic Closure of Qualitative Constraint Networks** (2005)
- *Authors:* Jochen Renz and Gérard Ligozat
- *Direct Connection:* This work formalizes the algebraic closure algorithm for qualitative spatial/temporal reasoning, which the paper uses as the reference procedure and interprets LRMs as shallow, error-prone simulators of—especially failing at unions/intersections across multiple paths.

### 🏷️ Inspiration

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* The paper probes the limits of chain-of-thought’s stepwise, single-path derivational bias introduced by Wei et al., contrasting its effectiveness on Horn-like chains with its struggle to combine multiple disjunctive paths via composition tables.

### 🏷️ Baseline

**DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning** (2025) [[arXiv](https://arxiv.org/abs/2501.12948)]
- *Authors:* Daya Guo et al.
- *Direct Connection:* R1-style RL post-training underlies the distilled Qwen reasoning models evaluated as primary LRMs, whose failures on multi-path STaR cases are central to the paper’s ‘shallow disjunctive reasoner’ diagnosis.

**Competitive programming with large reasoning models** (2025) [[arXiv](https://arxiv.org/abs/2502.06807)]
- *Authors:* OpenAI et al.
- *Direct Connection:* The o3 family provides the flagship LRM (o3-mini) tested zero-shot, whose strong single-path (b=1) but collapsing multi-path performance empirically anchors the paper’s core claim about shallow disjunctive reasoning.

---

## Synthesis: How Prior Work Led to This Paper

The STaR benchmark established a synthetic, controllable setting for qualitative spatial and temporal reasoning, parameterizing difficulty through the length of paths (k) and the number of distinct paths (b), and grounding each instance in composition tables for RCC-8 and the Interval Algebra. RCC-8 formalized eight jointly exhaustive and pairwise disjoint spatial relations and their compositions, while the Interval Algebra introduced thirteen such temporal relations; together they provide the exact label spaces and composition rules that define correct inferences in these tasks. The algebraic closure algorithm of Renz and Ligozat articulated how qualitative constraint networks should be solved via iterative composition, union, and intersection over sets of possible relations, capturing the need to combine information across multiple paths. Chain-of-thought prompting demonstrated how LLMs can generate stepwise derivations that are effective on single-path or Horn-like reasoning chains. Subsequent reinforcement-learning–trained large reasoning models, exemplified by DeepSeek-R1 and OpenAI’s o3 series, operationalized this CoT-centric approach into models optimized to produce and evaluate extended reasoning traces on verifiable domains. Collectively, these strands created a natural opportunity: STaR’s disjunctive, multi-path structure precisely stresses the gap between single-path CoT strengths and the set- and path-combining requirements of algebraic closure. Building on STaR’s controlled OOD splits and the RCC-8/IA composition regimes, the present work evaluates RL-trained LRMs (e.g., o3-mini and R1-distilled Qwen) and shows that, although they can apply composition rules along a single path, they collapse when intersections across multiple paths must be aggregated—behavior that is most parsimoniously characterized as shallow simulation of algebraic closure rather than robust disjunctive reasoning.

---

*Analysis generated on: 2026-04-05T11:54:21.714498*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
