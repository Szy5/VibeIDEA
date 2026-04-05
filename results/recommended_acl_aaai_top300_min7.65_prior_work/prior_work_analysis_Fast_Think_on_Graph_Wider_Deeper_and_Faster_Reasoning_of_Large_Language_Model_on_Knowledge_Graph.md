# Prior Work Analysis Report

## Target Paper

**Title:** Fast Think-on-Graph: Wider, Deeper and Faster Reasoning of Large Language Model on Knowledge Graph

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Graph Retrieval Augmented Generation (GRAG) is a novel paradigm that takes the naive RAG system a step further by integrating graph information, such as knowledge graph (KGs), into large-scale language models (LLMs) to mitigate hallucination. However, existing GRAG still encounter limitations: 1) simple paradigms usually fail with the complex problems due to the narrow and shallow correlations capture from KGs 2) methods of strong coupling with KGs tend to be high computation cost and time consuming if the graph is dense. In this paper, we propose the Fast Think-on-Graph (FastToG), an innovative paradigm for enabling LLMs to think ``community by community" within KGs. To do this, FastToG employs community detection for deeper correlation capture and two stages community pruning - coarse and fine pruning for faster retrieval. Furthermore, we also develop two Community-to-Text methods to convert the graph structure of communities into textual form for better understanding by LLMs. Experimental results demonstrate the effectiveness of FastToG, showcasing higher accuracy, faster reasoning, and better explainability compared to the previous works.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Fast Unfolding of Communities in Large Networks** (2008)
- *Authors:* V. D. Blondel et al.
- *Direct Connection:* The Louvain method’s modularity objective provides both the practical community detection mechanism on local subgraphs and the modularity score used for FastToG’s coarse community pruning.

**Knowledge Prompting in Pre-trained Language Model for Natural Language Understanding** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2210.08536)]
- *Authors:* J. Wang et al.
- *Direct Connection:* This work formalized multi-hop (d>1) knowledge prompting with entity–relation chains, a depth-oriented retrieval idea that FastToG adapts from nodes to communities to achieve n-d reasoning.

### 🏷️ Inspiration

**From Local to Global: A Graph RAG Approach to Query-Focused Summarization** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2404.16130)]
- *Authors:* D. Edge et al.
- *Direct Connection:* By showing that community detection can serve as an effective retrieval unit and that community summaries improve utility for LLMs, this paper inspired FastToG’s choice of communities as the basic reasoning unit and its community-to-text conversion.

**Large Language Models are Zero-Shot Reasoners** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2205.11916)]
- *Authors:* T. Kojima et al.
- *Direct Connection:* The step-by-step chain-of-thought prompting directly motivates FastToG’s “think community by community” design, treating successive communities as the intermediate reasoning steps.

### 🏷️ Gap Identification

**Large Language Models are Not Robust Multiple Choice Selectors** (2023)
- *Authors:* C. Zheng et al.
- *Direct Connection:* Evidence that LLMs exhibit selection bias and instability when choosing from many options directly motivated FastToG’s modularity-based coarse pruning to shrink candidate communities before LLM selection.

### 🏷️ Baseline

**Knowledge Graph Prompting for Multi-Document Question Answering** (2024)
- *Authors:* Y. Wang et al.
- *Direct Connection:* As a representative n-w GraphRAG that expands breadth via prompted neighbor exploration, KGP serves as a primary baseline that FastToG outperforms by replacing ad hoc neighbor expansion with community-based retrieval.

### 🏷️ Extension

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model with Knowledge Graph** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2307.07697)]
- *Authors:* J. Sun et al.
- *Direct Connection:* This work’s entity–relation chain-of-thought with LLM-driven pruning and beam search is directly generalized by FastToG into community-level chains, replacing node-by-node expansion and scoring-based pruning with modularity-guided coarse pruning and LLM fine selection to reduce depth and calls.

---

## Synthesis: How Prior Work Led to This Paper

Entity–relation chain-of-thought for knowledge-graph reasoning was concretely instantiated by Think-on-Graph, which coupled LLMs with multi-hop chains and used LLM-based scoring and beam search to guide expansions; this established a depth-first GraphRAG blueprint but incurred many LLM calls. In parallel, GraphRAG demonstrated that graph communities are effective retrieval units and that summarizing cluster-level structure into text improves LLM usability, offering a width-oriented approach grounded in community detection. The broader idea that large models benefit from explicit intermediate steps was crystallized by zero-shot chain-of-thought prompting, which suggested treating structured steps as thinking waypoints. At the graph algorithm level, the Louvain method provided both a scalable community detection routine and the modularity objective, a principled quality measure for selecting well-formed communities. Knowledge Graph Prompting showed that expanding neighborhood breadth can improve coverage but often relies on adjacent-node exploration that can be noisy or shallow. Meanwhile, evidence that LLMs are unreliable multiple-choice selectors under large candidate sets highlighted the risk of relying solely on LLM choice for pruning. Finally, knowledge prompting with multi-hop chains established the value of d>1 retrieval paths for capturing deeper relations.
Synthesizing these insights, the current work treats communities themselves as the chain-of-thought steps, merging width (community-level context) with depth (multi-step chains). It performs local community detection to avoid full-graph partitioning, uses modularity for coarse pruning to tame candidate explosion and LLM selection bias, and then applies LLM-based fine selection and community-to-text conversion to feed concise, structured evidence to the model—naturally extending chain-of-thought and GraphRAG principles into a unified, faster n-w n-d paradigm.

---

*Analysis generated on: 2026-04-05T12:01:16.803355*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
