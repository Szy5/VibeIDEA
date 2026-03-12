# Prior Work Analysis Report

## Target Paper

**Title:** FiTs: Fine-grained Two-stage Training for Knowledge-aware Question Answering

**arXiv ID:** [2302.11799](https://arxiv.org/abs/2302.11799)

**Abstract:** 
> Knowledge-aware question answering (KAQA) requires the model to answer questions over a knowledge base, which is essential for both open-domain QA and domain-specific QA, especially when language models alone cannot provide all the knowledge needed. Despite the promising result of recent KAQA systems which tend to integrate linguistic knowledge from pre-trained language models (PLM) and factual knowledge from knowledge graphs (KG) to answer complex questions, a bottleneck exists in effectively fusing the representations from PLMs and KGs because of (i) the semantic and distributional gaps between them, and (ii) the difficulties in joint reasoning over the provided knowledge from both modalities. To address the above two problems, we propose a Fine-grained Two-stage training framework (FiTs) to boost the KAQA system performance: The first stage aims at aligning representations from the PLM and the KG, thus bridging the modality gaps between them, named knowledge adaptive post-training. The second stage, called knowledge-aware fine-tuning, aims to improve the model's joint reasoning ability based on the aligned representations. In detail, we fine-tune the post-trained model via two auxiliary self-supervised tasks in addition to the QA supervision. Extensive experiments demonstrate that our approach achieves state-of-the-art performance on three benchmarks in the commonsense reasoning (i.e., CommonsenseQA, OpenbookQA) and medical question answering (i.e., MedQA-USMILE) domains.

**Innovation pattern:** Modular Pipeline Composition (confidence: high)

Secondary patterns: Cross-Domain Synthesis, Inject Structural Inductive Bias

*Reasoning:* Presents a two-stage, modular LM+GNN pipeline (retrieval, KG subgraph, intermediate fusion) and training schedule; draws on cross-domain synthesis (LMs + GNNs) and injects structural KG inductive bias (TransE-inspired regularization).

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**QA-GNN: Reasoning with Language Models and Knowledge Graphs for Question Answering** (2021)
- *Authors:* Makoto Yasunaga et al.
- *Direct Connection:* The paper follows QA-GNN's retrieval pipeline and relevance-scoring procedure for assembling KG subgraphs per QA example, using that formulation as the working problem setup for joint LM+KG reasoning.

**CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge** (2019)
- *Authors:* Alon Talmor et al.
- *Direct Connection:* CommonsenseQA provides the primary task/dataset formulation (knowledge-aware multiple-choice QA) used to evaluate and drive the methodological choices for retrieval, fusion, and fine-tuning objectives.

### 🏷️ Inspiration

**Translating Embeddings for Modeling Multi-relational Data (TransE)** (2013)
- *Authors:* Antoine Bordes et al.
- *Direct Connection:* The knowledge-backbone regularization objective directly draws on TransE's translation-in-embedding-space idea, motivating the paper's constraint that head + relation ≈ tail in the fused representation space.

**Mind the gap: Understanding the modality gap in multi-modal contrastive representation learning** (2022) [[arXiv](https://arxiv.org/abs/2203.02053)]
- *Authors:* Wenjia Liang et al.
- *Direct Connection:* This analysis of semantic and distributional gaps across modalities motivates the paper's central claim about LM vs. KG representation mismatch and underpins the design of the knowledge-adaptive contrastive post-training to explicitly align modalities.

### 🏷️ Gap Identification

**KagNet: Knowledge-Aware Graph Networks for Commonsense Reasoning** (2019)
- *Authors:* Boyi Lin et al.
- *Direct Connection:* KagNet exemplifies prior LM+KG approaches that inject graph knowledge into language encoders in a largely one-way manner, a limitation FiTs explicitly calls out and seeks to address by improving bidirectional alignment and joint reasoning.

### 🏷️ Baseline

**GreaseLM: Graph REASoning Enhanced Language Models for Question Answering** (2022) [[arXiv](https://arxiv.org/abs/2201.08860)]
- *Authors:* Xingcheng Zhang et al.
- *Direct Connection:* GreaseLM is the backbone the paper adopts and improves upon—providing the intermediate-layer LM+GNN modality-interaction architecture that FiTs retains while targeting its lack of pre-fusion adaptation, making GreaseLM the primary system the work seeks to outperform.

---

## Synthesis: How Prior Work Led to This Paper

GreaseLM established the concrete LM+GNN intermediate-layer fusion architecture and two-way interaction mechanism that this line of work builds upon, making it the salient reference architecture and comparative baseline; QA-GNN supplied the practical retrieval and KG subgraph construction procedure used to formulate inputs and relevance scoring; KagNet and similar one-way augmentation methods highlighted the limitations of treating one modality as merely auxiliary and exposed the need for tighter semantic alignment and reciprocal fusion; TransE provided the specific modeling insight—treating relations as translations in embedding space—that directly inspired the knowledge-backbone regularization (head + relation ≈ tail) used as a self-supervised fine-tuning term; empirical analyses like “Mind the gap” documented modality semantic and distributional mismatches, motivating a contrastive alignment objective to reduce semantic and distributional gaps between text-entity and graph-node embeddings; and CommonsenseQA defined the knowledge-aware multiple-choice QA evaluation setup that grounded the design choices. Together, these works created a clear opportunity: existing LM+KG systems possess powerful fusion layers but lack an initialization and auxiliary objectives that (a) align modality representations before fusion and (b) regularize joint reasoning with self-supervised signals; synthesizing retrieval/formulation from QA-GNN, the fusion backbone of GreaseLM, contrastive alignment motivations, and relation-translation priors naturally led to a two-stage recipe—knowledge-adaptive post-training plus knowledge-aware fine-tuning—that directly addresses the identified gaps and improves downstream KAQA performance.

---

*Analysis generated on: 2026-03-09T00:19:29.944636*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=14296, output=1092*
