# Prior Work Analysis Report

## Target Paper

**Title:** Deliberate Reasoning in Language Models as Structure-Aware Planning with an Accurate World Model

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Enhancing the reasoning capabilities of language models (LMs) remains a key challenge, especially for tasks that require complex, multistep decision-making where existing Chain-of-Thought (CoT) approaches struggle with consistency and verification.In this paper, we propose a novel reasoning framework, referred to as Structure-aware Planning with an Accurate World Model (SWAP), that integrates structured knowledge representation with learned planning.Unlike prior methods that rely purely on natural language reasoning, SWAP leverages entailment graphs to encode structured dependencies and enable symbolic verification of intermediate steps.To systematically construct and update the graph, SWAP employs a policy model to propose candidate expansions and a world model to predict structural updates.To improve accuracy, the world model generates multiple alternative updates, and a discriminator re-ranks them based on plausibility.To encourage diverse exploration, we introduce Diversity-based Modelling (DM), which samples candidates from the remaining probability mass after removing previously sampled candidates from the original policy distribution.Additionally, SWAP improves the discrimination accuracy through Contrastive Ranking (CR), which directly compares candidates within prompts and incorporates metaknowledge to improve ranking quality.We evaluate SWAP across diverse reasoning-intensive benchmarks including math reasoning, logical reasoning, and coding tasks.Extensive experiments demonstrate that SWAP significantly improves upon the base models and consistently outperforms existing reasoning methods 1 .

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Explaining Answers with Entailment Trees** (2021) [[arXiv](https://arxiv.org/abs/2104.08661)]
- *Authors:* Bhavana Dalvi et al.
- *Direct Connection:* This work introduced entailment graphs/trees as a structured representation linking premises to conclusions, which SWAP directly adopts as the world state to enable symbolic verification and structure-aware reasoning.

### 🏷️ Gap Identification

**Let’s Verify Step by Step** (2023) [[arXiv](https://arxiv.org/abs/2305.20050)]
- *Authors:* Hunter Lightman et al.
- *Direct Connection:* This paper popularized process reward models for stepwise verification, whose limitation of reducing rich decisions to scalar scores is explicitly addressed in SWAP by replacing PRM scoring with contrastive ranking between candidates.

**When is tree search useful for LLM planning? It depends on the discriminator** (2024) [[arXiv](https://arxiv.org/abs/2402.10890)]
- *Authors:* Ziru Chen et al.
- *Direct Connection:* By showing that planning performance hinges on discriminator quality and that prompting the same LM is often insufficient, this work directly motivates SWAP’s trained contrastive discriminator with meta-knowledge for reliable candidate selection.

**Can LLMs reason in the wild with programs?** (2024)
- *Authors:* Yuan Yang et al.
- *Direct Connection:* This study demonstrated that program-based and formal logic approaches often lack expressiveness and generalization, motivating SWAP’s semi-formal entailment-graph formulation that blends symbolic verification with flexible natural language reasoning.

### 🏷️ Baseline

**Tree of Thoughts: Deliberate Problem Solving with Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.10601)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* ToT established deliberate multi-step search over reasoning paths, and SWAP builds on this planning paradigm while addressing ToT’s unstructured states by introducing entailment-graph states and a more accurate world model for state simulation.

### 🏷️ Extension

**Reasoning with Language Model is Planning with World Model** (2023) [[arXiv](https://arxiv.org/abs/2305.14992)]
- *Authors:* Shibo Hao et al.
- *Direct Connection:* RAP framed LM reasoning as planning with a learned world model, which SWAP extends by making the world model more accurate via multi-sampled state predictions and discriminator re-ranking and by operating over structured entailment graphs rather than raw text.

### 🏷️ Related Problem

**Diverse Beam Search: Decoding Diverse Solutions from Neural Sequence Models** (2016) [[arXiv](https://arxiv.org/abs/1610.02424)]
- *Authors:* Ashwin K. Vijayakumar et al.
- *Direct Connection:* Diverse Beam Search foregrounded the importance of diversity in decoding but is impractical for long-form reasoning, directly motivating SWAP’s Diversity-based Modeling that promotes diversity by subtracting a semantic-equivalence distribution from the policy.

---

## Synthesis: How Prior Work Led to This Paper

Entailment trees were introduced to explicitly capture how premises support intermediate claims and final conclusions, providing a structured graph representation and an avenue for symbolic verification. Deliberate search over reasoning paths was later articulated as tree-based exploration, though typically over unstructured text and with heuristic selection. Planning with a learned world model framed reasoning as simulating next states, but early implementations relied on prompting the same LM for dynamics and struggled on complex tasks. Stepwise verification via process reward models brought supervision to intermediate reasoning steps, yet compressed rich decisions into single scores and introduced calibration issues. Subsequent analyses established that the success of planning critically depends on a strong discriminator and that naive prompt-based judges are insufficient. Parallel work on program-based and purely formal solvers revealed limited expressiveness and generalization, leaving room for semi-formal structures. Meanwhile, diversity-seeking decoding like Diverse Beam Search highlighted the value of exploration but proved unwieldy for long-form reasoning.
Bringing these strands together, the next step was to marry a flexible but verifiable structure with learned planning and stronger selection. SWAP instantiates entailment graphs as the state space for planning, improves world-model accuracy by multi-sampling and re-ranking predicted structural updates, replaces scalar PRM scoring with contrastive ranking conditioned on meta-knowledge, and scales exploration through diversity modeling that subtracts paraphrase-like mass from the policy distribution. This synthesis directly addresses the lack of verifiable structure, weak discriminators, and inadequate diversity in prior planning frameworks while retaining the flexibility that formal program-based methods lack.

---

*Analysis generated on: 2026-04-05T11:53:57.915211*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
