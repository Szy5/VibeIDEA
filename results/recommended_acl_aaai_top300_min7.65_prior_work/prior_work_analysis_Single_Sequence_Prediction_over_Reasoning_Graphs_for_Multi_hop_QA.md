# Prior Work Analysis Report

## Target Paper

**Title:** Single Sequence Prediction over Reasoning Graphs for Multi-hop QA

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent generative approaches for multi-hop question answering (QA) utilize the fusion-in-decoder method to generate a single sequence output which includes both a final answer and a reasoning path taken to arrive at that answer, such as passage titles and key facts from those passages. While such models can lead to better interpretability and high quantitative scores, they often have difficulty accurately identifying the passages corresponding to key entities in the context, resulting in incorrect passage hops and a lack of faithfulness in the reasoning path. To address this, we propose a single-sequence prediction method over a local reasoning graph that integrates a graph structure connecting key entities in each context passage to relevant subsequent passages for each question. We use a graph neural network to encode this graph structure and fuse the resulting representations into the entity representations of the model. Our experiments show significant improvements in answer exact-match/F1 scores and faithfulness of grounding in the reasoning path on the HotpotQA dataset and achieve state-of-the-art numbers on the Musique dataset with only up to a 4% increase in model parameters.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering** (2021)
- *Authors:* Gautier Izacard et al.
- *Direct Connection:* This paper’s core formulation adopts FiD’s passage-wise encoding and decoder fusion as the generative backbone, which the current work directly augments by injecting graph-structured signals to address FiD’s lack of explicit cross-passage modeling for multi-hop reasoning.

**HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering** (2018)
- *Authors:* Zhilin Yang et al.
- *Direct Connection:* This dataset provides the distractor setting, supporting-fact supervision, and Wikipedia-linked passages that underpin the single-sequence reasoning target (titles+facts+answer) and supply the hyperlinks used to construct the local reasoning graph.

**MuSiQue: Multi-hop Questions via Single-hop Question Composition** (2022)
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* MuSiQue supplies a multi-hop benchmark with decompositions and intermediate answers, enabling the SIA-style reasoning path supervision and serving to assess robustness against shortcut-driven, unfaithful reasoning.

### 🏷️ Inspiration

**KG-FiD: Infusing Knowledge Graph in Fusion-in-Decoder for Open-Domain Question Answering** (2022)
- *Authors:* Donghan Yu et al.
- *Direct Connection:* Showing that infusing knowledge-graph signals into FiD improves QA directly inspired the idea here to fuse GNN-encoded graph features—built from local entity–passage links—into the FiD encoder to guide multi-hop generation.

### 🏷️ Gap Identification

**Is Multihop QA in DiRe Condition? Measuring and Reducing Disconnected Reasoning** (2020)
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* By defining the ‘disconnected reasoning’ problem and introducing the DIRE probe used for evaluation, this work directly motivated a design that enforces faithful passage hopping rather than exploiting shortcuts.

### 🏷️ Baseline

**Modeling Multi-Hop Question Answering as Single Sequence Prediction** (2022)
- *Authors:* Semih Yavuz et al.
- *Direct Connection:* The proposed method preserves PATH-FID’s single-sequence objective of generating a reasoning path (titles and supporting facts) plus the answer, but explicitly tackles PATH-FID’s reported disconnected hops by biasing generation with a local entity-to-passage graph.

### 🏷️ Related Problem

**Learning to Retrieve Reasoning Paths over Wikipedia Graph for Question Answering** (2020)
- *Authors:* Akari Asai et al.
- *Direct Connection:* By demonstrating that traversing Wikipedia’s hyperlink graph yields effective reasoning paths, this work informed the construction of per-question entity→passage graphs from in-passage links used to guide multi-hop reasoning.

---

## Synthesis: How Prior Work Led to This Paper

Fusion-in-Decoder established a powerful generative paradigm that encodes each passage independently and fuses their representations in the decoder, but it offers no explicit mechanism to model cross-passage relationships crucial for multi-hop reasoning. Building on FiD, PATH-FID trained a model to generate a single sequence that interleaves passage titles, supporting facts, and the final answer, enabling interpretable reasoning traces while retaining FiD’s independent encoding. Concurrently, the notion of ‘disconnected reasoning’ was formalized and measured by DIRE, revealing that models can achieve high answer scores while producing unfaithful hops between passages. In parallel, KG-FiD showed that injecting structured knowledge into FiD can improve reasoning, suggesting that graph signals can complement text encoders. HotpotQA supplied the distractor setting with supporting facts and hyperlink-rich contexts that naturally define a sequence target and provide linkage cues, while MuSiQue offered multi-hop questions with decompositions and intermediate answers designed to limit shortcuts. Moreover, work on retrieving reasoning paths via the Wikipedia hyperlink graph demonstrated that hyperlink structure encodes actionable chains for complex questions.
Together, these threads point to a clear opportunity: preserve the strengths of single-sequence generation while explicitly encoding cross-passage structure to prevent unfaithful hops. The natural synthesis is to construct a local entity–passage graph from contextual hyperlinks, encode it with a GNN, and fuse these node representations into the FiD encoder to bias generation toward faithful, connected paths. Supervision from HotpotQA and MuSiQue’s structured annotations makes this feasible, while DIRE provides a targeted probe to verify reductions in disconnected reasoning.

---

*Analysis generated on: 2026-04-05T12:05:42.614450*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
