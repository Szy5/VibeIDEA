# Prior Work Analysis Report

## Target Paper

**Title:** Towards Complex Scenarios: Building End-to-End Task-Oriented Dialogue System across Multiple Knowledge Bases

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> With the success of the sequence-to-sequence model, end-to-end task-oriented dialogue systems (EToDs) have obtained remarkable progress. However, most existing EToDs are limited to single KB settings where dialogues can be supported by a single KB, which is still far from satisfying the requirements of some complex applications (multi-KBs setting). In this work, we first empirically show that the existing single-KB EToDs fail to work on multi-KB settings that require models to reason across various KBs. To solve this issue, we take the first step to consider the multi-KBs scenario in EToDs and introduce a KB-over-KB Heterogeneous Graph Attention Network (KoK-HAN) to facilitate model to reason over multiple KBs. The core module is a triple-connection graph interaction layer that can model different granularity levels of interaction information across different KBs (i.e., intra-KB connection, inter-KB connection and dialogue-KB connection). Experimental results confirm the superiority of our model for multiple KBs reasoning.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Key-Value Retrieval Networks for Task-Oriented Dialogue** (2017) [[arXiv](https://arxiv.org/abs/1705.05414)]
- *Authors:* Mihail Eric et al.
- *Direct Connection:* The paper adopts the KB triplet (subject, relation, object) representation and attention-based KB querying introduced by Key-Value Retrieval Networks to construct KoK-HAN’s KB entity nodes and form the basis for knowledge retrieval.

**CrossWOZ: A Large-Scale Chinese Cross-Domain Task-Oriented Dialogue Dataset** (2020)
- *Authors:* Qian Zhu et al.
- *Direct Connection:* CrossWOZ provides cross-domain dialogues and KBs from which the authors curate multi-KB cases, establishing the problem setting and evaluation bedrock for cross-KB reasoning.

**RiSAWOZ: A Large-Scale Multi-Domain Wizard-of-Oz Dataset with Rich Semantic Annotations for Task-Oriented Dialogue Modeling** (2020)
- *Authors:* Jun Quan et al.
- *Direct Connection:* RiSAWOZ supplies multi-domain dialogues with associated KBs that the authors equip to create multi-KB scenarios, serving as a second foundational testbed for evaluating cross-KB reasoning.

### 🏷️ Inspiration

**GraphDialog: Integrating Graph Knowledge into End-to-End Task-Oriented Dialogue Systems** (2020)
- *Authors:* Shuai Yang et al.
- *Direct Connection:* GraphDialog’s use of graph neural networks to propagate messages between dialogue tokens and KB entities directly inspires KoK-HAN’s graph-based reasoning, which is generalized here into a heterogeneous graph with intra- and inter-KB edges.

### 🏷️ Gap Identification

**Dynamic Fusion Network for Multi-Domain End-to-end Task-Oriented Dialog** (2020)
- *Authors:* Libo Qin et al.
- *Direct Connection:* DF-Net’s domain-aware fusion improves multi-domain single-KB querying but lacks mechanisms to model dependencies across KBs, a limitation explicitly targeted by KoK-HAN’s inter-KB graph connections.

### 🏷️ Baseline

**An Interpretable Neuro-Symbolic Reasoning Framework for Task-Oriented Dialogue Generation** (2022)
- *Authors:* Shuai Yang et al.
- *Direct Connection:* As the strongest explicit reasoning baseline in single-KB settings, this approach’s significant performance drop under multi-KB scenarios in the authors’ experiments motivates KoK-HAN’s cross-KB graph reasoning design.

### 🏷️ Extension

**Global-to-Local Memory Pointer Networks for Task-Oriented Dialogue** (2019) [[arXiv](https://arxiv.org/abs/1901.04713)]
- *Authors:* Chien-Sheng Wu et al.
- *Direct Connection:* KoK-HAN directly extends GLMP’s sketch-tagged decoder and pointer-based lexicalization by querying over heterogeneous graph node outputs instead of a flat memory, enabling entity grounding from multiple KBs.

---

## Synthesis: How Prior Work Led to This Paper

Key-Value Retrieval Networks introduced representing KB entries as (subject, relation, object) triplets and attending over them, establishing how end-to-end systems can interface with structured KBs. Building on this, Global-to-Local Memory Pointer Networks equipped task-oriented dialogue with a sketch-tagged decoder and pointer-based lexicalization, allowing responses to mix generated words and copied entities guided by the dialogue context. GraphDialog demonstrated that graph neural networks can integrate dialogue tokens and KB entities, using message passing to capture relational structure beyond flat memory lookup. Dynamic Fusion Network addressed multi-domain dialogue by dynamically leveraging domain features to retrieve from a single KB, highlighting domain-aware querying but not cross-KB dependency modeling. An interpretable neuro-symbolic framework further elevated explicit reasoning for single-KB grounded generation, yet its design and empirical strengths remained bound to one KB per dialogue. CrossWOZ and RiSAWOZ provided cross-domain dialogue corpora with associated KBs that naturally instantiate scenarios requiring knowledge chaining across domains.
Taken together, these works revealed a gap: strong single-KB retrieval and explicit reasoning mechanisms, even with domain-aware fusion, struggle to reason across multiple KBs. The natural next step was to retain the proven sketch-pointer decoding paradigm while replacing flat KB access with graph-based reasoning that preserves KB structure and enables cross-KB message flow. By introducing a heterogeneous graph with intra-KB edges to capture high-order row structure, inter-KB edges via global nodes to pass information across KBs, and dialogue–KB co-occurrence connections to ground entity access, the new approach synthesizes these insights into a unified framework for multi-KB end-to-end dialogue.

---

*Analysis generated on: 2026-04-05T12:08:08.438616*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
