# Prior Work Analysis Report

## Target Paper

**Title:** Question Calibration and Multi-Hop Modeling for Temporal Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Many models that leverage knowledge graphs (KGs) have recently demonstrated remarkable success in question answering (QA) tasks. In the real world, many facts contained in KGs are time-constrained thus temporal KGQA has received increasing attention. Despite the fruitful efforts of previous models in temporal KGQA, they still have several limitations. (I) They adopt pre-trained language models (PLMs) to obtain question representations, while PLMs tend to focus on entity information and ignore entity transfer caused by temporal constraints, and finally fail to learn specific temporal representations of entities. (II) They neither emphasize the graph structure between entities nor explicitly model the multi-hop relationship in the graph, which will make it difficult to solve complex multi-hop question answering. To alleviate this problem, we propose a novel Question Calibration and Multi-Hop Modeling (QC-MHM) network. Specifically, We first calibrate the question representation by fusing the question and the time-constrained concepts in KG. Then, we construct the GNN layer to complete multi-hop message passing. Finally, the question representation is combined with the embedding output by the GNN to generate the final prediction. Empirical results verify that the proposed model achieves better performance than the state-of-the-art models in the benchmark dataset. Notably, the Hits@1 and Hits@10 results of QC-MHM on the CronQuestions dataset's complex questions are absolutely improved by 5.1% and 1.2% compared to the best-performing baseline. Moreover, QC-MHM can generate interpretable and trustworthy predictions.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Question Answering Over Temporal Knowledge Graphs** (2021)
- *Authors:* Amanpreet Saxena et al.
- *Direct Connection:* This work formalized temporal KGQA with a PLM+temporal-KG-embedding pipeline and introduced the CronQuestions dataset used here, providing the task setup and baseline architecture that the new model builds upon and seeks to overcome.

**Complex Temporal Question Answering on Knowledge Graphs** (2021)
- *Authors:* Zhen Jia et al.
- *Direct Connection:* This paper introduced the TimeQuestions benchmark with explicit/implicit/temporal/ordinal categories, providing the second evaluation setting and concretely motivating techniques that better capture temporal signals in questions.

### 🏷️ Inspiration

**Time-aware Multiway Adaptive Fusion Network for Temporal KGQA** (2022)
- *Authors:* Fang Fang and Yang Liu
- *Direct Connection:* By extracting KG SPOs relevant to the question and fusing them via multi-way attention, TMA directly inspired the question calibration module that retrieves top SPOs and performs multi-view attention with adaptive gating to infuse time-constrained KG context into question representations.

**Multiway Attention Networks for Modeling Sentence Pairs** (2018)
- *Authors:* Chenguang Tan et al.
- *Direct Connection:* Its multiway attention mechanisms for sentence-pair alignment directly inspired the multi-view (concat/dot/minus) attention module used to align token-level question features with retrieved SPOs during question calibration.

### 🏷️ Gap Identification

**Improving Time Sensitivity for Question Answering over Temporal Knowledge Graphs** (2022)
- *Authors:* Chi Shang et al.
- *Direct Connection:* Although it enhances time sensitivity via time estimation and contrastive learning, this work does not explicitly model graph structure or multi-hop paths, a limitation explicitly addressed by introducing multi-hop message passing with path-level attention.

**TwiRGCN: Temporally Weighted Graph Convolution for Question Answering over Temporal Knowledge Graphs** (2022) [[arXiv](https://arxiv.org/abs/2210.06281)]
- *Authors:* Anshul Sharma et al.
- *Direct Connection:* This GCN-based TKGQA approach weights edges temporally but operates with one-hop neighborhood aggregation, motivating the development of an attention-based diffusion mechanism that aggregates multi-hop paths within a single layer and yields interpretable reasoning paths.

### 🏷️ Extension

**Tensor Decompositions for Temporal Knowledge Base Completion** (2020)
- *Authors:* Timothée Lacroix et al.
- *Direct Connection:* The method adopts TComplEx to initialize entity/relation/timestamp embeddings and directly extends it by injecting temporal order via sinusoidal position encodings and an auxiliary time-order prediction loss to make timestamp embeddings order-aware.

---

## Synthesis: How Prior Work Led to This Paper

Question answering over temporal knowledge graphs was formalized by Saxena et al., who paired pre-trained language models with temporal KG embeddings and released the CronQuestions benchmark, establishing the dominant pipeline and evaluation setting. For the embedding backbone, Lacroix et al.’s TComplEx provided a strong time-aware KG completion model to produce entity, relation, and timestamp vectors. To inject KG-derived context into question understanding, Fang and Liu’s TMA demonstrated that selecting question-relevant SPOs from the KG and fusing them with multi-way attention can enrich question representations in temporal KGQA. Shang et al. improved time sensitivity by estimating timestamps and applying contrastive objectives to time words, highlighting the importance of temporal cues in language, while Sharma et al. introduced temporally weighted graph convolution for TKGQA, evidencing the value of graph structure but still relying on one-hop neighborhoods. Complementing these, Jia et al.’s TimeQuestions dataset emphasized challenging explicit, implicit, temporal, and ordinal reasoning types that stress both temporal comprehension and complex reasoning. At the sentence-pair modeling level, Tan et al.’s multiway attention networks supplied a practical blueprint for multi-view alignment between text sequences.
Collectively, these works exposed a gap: PLM-centric temporal QA underutilizes KG structure and temporal ordering, and GNN-based approaches often fail to model multi-hop relational paths explicitly. Building on the CronKGQA/TComplEx pipeline and the datasets from CronQuestions and TimeQuestions, it was natural to calibrate questions with KG SPOs using multi-view attention inspired by TMA and Tan, while extending TComplEx to encode time order and addressing one-hop limitations by designing a path-attentive, diffusion-style multi-hop aggregation. This synthesis directly targets complex temporal queries by aligning language with time-constrained KG context and enabling interpretable multi-hop reasoning.

---

*Analysis generated on: 2026-04-05T12:05:22.849458*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
