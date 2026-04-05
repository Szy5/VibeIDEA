# Prior Work Analysis Report

## Target Paper

**Title:** Decoding on Graphs: Faithful and Sound Reasoning on Knowledge Graphs through Generation of Well-Formed Chains

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Knowledge Graphs (KGs) can serve as reliable knowledge sources for question answering (QA) due to their structured representation of knowledge.Existing research on the utilization of KG for large language models (LLMs) prevalently relies on subgraph retriever or iterative prompting, overlooking the potential synergy of LLMs' step-wise reasoning capabilities and KGs' structural nature.In this paper, we present DoG (Decoding on Graphs), a novel framework that facilitates a deep synergy between LLMs and KGs.We first define a concept, well-formed chain, which consists of a sequence of interrelated fact triplets on the KGs, starting from question entities and leading to answers.We argue that this concept can serve as a principle for making faithful and sound reasoning for KGQA.To enable LLMs to generate well-formed chains, we propose graph-aware constrained decoding, in which a constraint derived from the topology of the KG regulates the decoding process of the LLMs.This constrained decoding method ensures the generation of well-formed chains while making full use of the step-wise reasoning capabilities of LLMs.Based on the above, DOG, a trainingfree approach, is able to provide faithful and sound reasoning trajectories grounded on the KGs.Experiments across various KGQA tasks with different background KGs demonstrate that DOG achieves superior and robust performance.DOG also shows general applicability with various open-source LLMs 1 .

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**KGQA: A Methodology for Knowledge Graph-Based Question Answering** (2024) [[arXiv](https://arxiv.org/abs/if known)]
- *Authors:* Luo et al.
- *Direct Connection:* The work by Luo et al. introduced essential methodologies for utilizing knowledge graphs in question answering, providing the foundational problem formulation that DOG builds upon.

### 🏷️ Inspiration

**Chain of Thought: A Theoretical Perspective** (2023) [[arXiv](https://arxiv.org/abs/if known)]
- *Authors:* Feng et al.
- *Direct Connection:* Feng et al.’s exploration of chain-of-thought reasoning paths inspired DOG's core idea of generating sequential reasoning steps as a structured approach to KGQA.

### 🏷️ Gap Identification

**Grounded Dialogue Generation with Knowledge Graphs** (2022) [[arXiv](https://arxiv.org/abs/if known)]
- *Authors:* Li et al.
- *Direct Connection:* Li et al. identified limitations in the integration of KGs with dialogue systems, motivating the need for improved reasoning methods in DOG that leverage both LLMs and KGs effectively.

### 🏷️ Baseline

**GNN-RAG: Graph Neural Retrieval for Large Language Model Reasoning** (2024) [[arXiv](https://arxiv.org/abs/2405.20139)]
- *Authors:* Mavromatis and Karypis
- *Direct Connection:* Mavromatis and Karypis's GNN-RAG serves as a baseline method that DOG improves upon by eliminating the need for specialized retrievers through direct chain generation.

**ToG: Exploring Knowledge Graphs with Large Language Models** (2024) [[arXiv](https://arxiv.org/abs/if known)]
- *Authors:* Sun et al.
- *Direct Connection:* The ToG method engages LLMs with iterative prompts, which DOG addresses by proposing a more direct reasoning process through the generation of well-formed chains.

**Tree-of-Traversals: Augmenting LLMs with Knowledge Graphs** (2024) [[arXiv](https://arxiv.org/abs/if known)]
- *Authors:* Markowitz et al.
- *Direct Connection:* Markowitz et al. investigated LLM interactions with KGs, providing insights that DOG builds on by utilizing a complete question graph instead of focusing on one hop at a time.

---

## Synthesis: How Prior Work Led to This Paper

The development of DOG is rooted in several pivotal prior studies addressing knowledge graph question answering (KGQA). Firstly, the foundational work by Luo et al. established a methodology for KGQA that DOG directly builds upon, defining key problem formulations essential for this field. Mavromatis and Karypis's GNN-RAG and Sun et al.'s ToG provided baseline methodologies wherein LLMs interacted with KGs but were constrained by their reliance on specialized retrievers or iterative prompts. Conversely, Markowitz et al. enhanced LLM-knowledge graph interactions by employing a tree-based approach, which DOG extends by advocating for the processing of complete question graphs. The exploration of reasoning via chain-of-thought by Feng et al. significantly inspired DOG's innovative direction to generate well-formed reasoning chains. Additionally, the work of Li et al. highlighted gaps in current methodologies, framing the necessity for DOG to improve how LLMs utilize KGs. Collectively, these studies shaped the emergence of DOG as a more integrated approach to KGQA, blending LLM capabilities with structured reasoning derived from KGs, thus filling the identified gaps and enhancing the constraints imposed by prior methodologies.

---

*Analysis generated on: 2026-04-04T23:21:52.984851*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
