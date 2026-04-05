# Prior Work Analysis Report

## Target Paper

**Title:** Dynamic Heterogeneous-Graph Reasoning with Language Models and Knowledge Representation Learning for Commonsense Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recently, knowledge graphs (KGs) have won noteworthy success in commonsense question answering. Existing methods retrieve relevant subgraphs in the KGs through key entities and reason about the answer with language models (LMs) and graph neural networks. However, they ignore (i) optimizing the knowledge representation and structure of subgraphs and (ii) deeply fusing heterogeneous QA context with subgraphs. In this paper, we propose a dynamic heterogeneous-graph reasoning method with LMs and knowledge representation learning (DHLK), which constructs a heterogeneous knowledge graph (HKG) based on multiple knowledge sources and optimizes the structure and knowledge representation of the HKG using a two-stage pruning strategy and knowledge representation learning (KRL). It then performs joint reasoning by LMs and Relation Mask Self-Attention (RMSA). Specifically, DHLK filters key entities based on the dictionary vocabulary to achieve the first-stage pruning while incorporating the paraphrases in the dictionary into the subgraph to construct the HKG. Then, DHLK encodes and fuses the QA context and HKG using LM, and dynamically removes irrelevant KG entities based on the attention weights of LM for the second-stage pruning. Finally, DHLK introduces KRL to optimize the knowledge representation and perform answer reasoning on the HKG by RMSA.We evaluate DHLK at CommonsenseQA and OpenBookQA, and show its improvement on existing LM and LM+KG methods.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Translating Embeddings for Modeling Multi-relational Data** (2013)
- *Authors:* Antoine Bordes et al.
- *Direct Connection:* DHLK uses TransE’s margin-based KRL objective to optimize entity and relation representations of its heterogeneous subgraph prior to attention-based reasoning.

**WordNet: A Lexical Database for English** (1995)
- *Authors:* George A. Miller
- *Direct Connection:* WordNet provides paraphrases and lexical groupings that DHLK leverages both to identify multiword key entities for first-stage pruning and to add paraphrase nodes (DefAs edges) when constructing its heterogeneous knowledge graph.

### 🏷️ Inspiration

**K-BERT: Enabling Language Representation with Knowledge Graph** (2020)
- *Authors:* Weijie Liu et al.
- *Direct Connection:* K-BERT introduced the visible-matrix masking strategy to inject KG tokens into a Transformer without corrupting sentence semantics, which DHLK directly adopts to fuse QA text and KG nodes via Mask Self-Attention during LM encoding.

**Relational Graph Attention Network for Aspect-based Sentiment Analysis** (2020)
- *Authors:* Kai Wang et al.
- *Direct Connection:* RGAT introduced relation-aware attention by incorporating relation embeddings into attention computations, directly inspiring DHLK’s Relation Mask Self-Attention (RMSA) for joint entity–relation reasoning on the pruned HKG.

### 🏷️ Gap Identification

**JointLK: Joint Reasoning with Language Models and Knowledge Graphs for Commonsense Question Answering** (2022)
- *Authors:* Yueqing Sun et al.
- *Direct Connection:* JointLK’s bidirectional attention fuses text and KG after separate encodings and uses an external pruning module, highlighting the gap that DHLK addresses with in-encoder fusion via masks and attention-based dynamic entity pruning.

### 🏷️ Extension

**QA-GNN: Reasoning with Language Models and Knowledge Graphs for Commonsense Question Answering** (2021)
- *Authors:* Michihiro Yasunaga et al.
- *Direct Connection:* DHLK follows QA-GNN’s two-hop ConceptNet subgraph retrieval based on key entities and extends its idea of LM-estimated entity importance into a dynamic pruning mechanism driven by LM attention weights.

**KagNet: Knowledge-Aware Graph Networks for Commonsense Reasoning** (2019)
- *Authors:* Bill Yuchen Lin et al.
- *Direct Connection:* KagNet formalized path-centric reasoning and GRU encoding of conceptual paths between question and choice entities, which DHLK reuses in its KG2QA module to inject selected path evidence into the QA representation.

---

## Synthesis: How Prior Work Led to This Paper

Visible-matrix masking from K-BERT showed how to inject knowledge tokens into a Transformer while constraining cross-token visibility, preserving sentence semantics as external facts are fused into self-attention. QA-GNN established a pragmatic pipeline for commonsense QA by retrieving two-hop subgraphs from ConceptNet using key entities and estimating entity importance with language models to guide reasoning over the subgraph. JointLK advanced cross-modal fusion with bidirectional attention and introduced explicit subgraph pruning, but maintained separate encoders for text and graphs, limiting deeper token-level interaction. KagNet framed path-centric reasoning by defining question-to-choice conceptual paths and encoding them with a GRU so path evidence could influence answer selection. Relation-aware attention, as instantiated in RGAT, demonstrated that injecting relation embeddings into attention weights improves relational reasoning over graphs. TransE provided a simple and scalable KRL objective to learn entity and relation embeddings for triple-based knowledge. WordNet supplied high-quality lexical paraphrases and multiword expressions that can be linked to KG concepts, indicating the value of dictionary resources in augmenting commonsense knowledge.
Collectively, these works exposed both the promise and limitations of LM+KG methods: effective subgraph retrieval and path reasoning exist, but fusion is often shallow and subgraphs remain noisy. The natural next step is to fuse KG and text inside the LM via visibility masks (à la K-BERT), refine subgraphs dynamically using LM attention, and improve signal with dictionary-derived paraphrases. Building on QA-GNN’s retrieval and KagNet’s path encoding, while adopting RGAT-style relation-aware attention and TransE-based KRL, DHLK unifies these ideas into dynamic heterogeneous-graph reasoning that deepens fusion and denoises knowledge for stronger commonsense QA.

---

*Analysis generated on: 2026-04-05T11:56:58.563546*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
