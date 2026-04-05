# Prior Work Analysis Report

## Target Paper

**Title:** FiTs: Fine-Grained Two-Stage Training for Knowledge-Aware Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Knowledge-aware question answering (KAQA) requires the model to answer questions over a knowledge base, which is essential for both open-domain QA and domain-specific QA, especially when language models alone cannot provide all the knowledge needed. Despite the promising result of recent KAQA systems which tend to integrate linguistic knowledge from pre-trained language models (PLM) and factual knowledge from knowledge graphs (KG) to answer complex questions, a bottleneck exists in effectively fusing the representations from PLMs and KGs because of (i) the semantic and distributional gaps between them, and (ii) the difficulties in joint reasoning over the provided knowledge from both modalities. To address the above two problems, we propose a Fine-grained Two-stage training framework (FiTs) to boost the KAQA system performance: The first stage aims at aligning representations from the PLM and the KG, thus bridging the modality gaps between them, named knowledge adaptive post-training. The second stage, called knowledge-aware fine-tuning, aims to improve the model's joint reasoning ability based on the aligned representations. In detail, we fine-tune the post-trained model via two auxiliary self-supervised tasks in addition to the QA supervision. Extensive experiments demonstrate that our approach achieves state-of-the-art performance on three benchmarks in the commonsense reasoning (i.e., CommonsenseQA, OpenbookQA) and medical question answering (i.e., MedQA-USMILE) domains.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**QA-GNN: Reasoning with Language Models and Knowledge Graphs for Question Answering** (2021) [[arXiv](https://arxiv.org/abs/2104.06378)]
- *Authors:* M. Yasunaga et al.
- *Direct Connection:* FiTs follows QA-GNN’s IR-based KAQA setup and entity-retrieval procedure to construct KG subgraphs and uses attentive pooling over KG nodes in the scoring head as the base for its two-stage training.

### 🏷️ Inspiration

**Translating embeddings for modeling multi-relational data** (2013)
- *Authors:* A. Bordes et al.
- *Direct Connection:* FiTs’s knowledge backbone regularization borrows the TransE insight by enforcing a translation-like constraint (eh + er ≈ et) on KG triples within the joint embedding space to encourage structured reasoning.

### 🏷️ Gap Identification

**Mind the gap: Understanding the modality gap in multi-modal contrastive representation learning** (2022) [[arXiv](https://arxiv.org/abs/2203.02053)]
- *Authors:* W. Liang et al.
- *Direct Connection:* The documented semantic and distributional ‘modality gap’ between modalities directly motivated FiTs’s contrastive knowledge-adaptive post-training to align PLM and KG representations before joint reasoning.

**Beyond IID: three levels of generalization for question answering on knowledge bases** (2021)
- *Authors:* Y. Gu et al.
- *Direct Connection:* This work’s observation that KAQA models struggle with noisy or shifted evidence motivated FiTs’s self-supervised Knowledge Source Distinction objective to explicitly teach the model to identify relevant versus irrelevant KG entities.

### 🏷️ Baseline

**Scalable Multi-Hop Relational Reasoning for Knowledge-Aware Question Answering (MHGRN)** (2020)
- *Authors:* Y. Feng et al.
- *Direct Connection:* As a strong LM+KG multi-hop reasoning baseline, MHGRN underscored the need for more effective PLM–KG fusion and robust joint reasoning, which FiTs achieves via representation pre-alignment and auxiliary regularization.

### 🏷️ Extension

**GreaseLM: Graph REASoning Enhanced Language Models for Question Answering** (2022) [[arXiv](https://arxiv.org/abs/2201.08860)]
- *Authors:* X. Zhang et al.
- *Direct Connection:* FiTs retains GreaseLM’s LM–GNN cross-modality encoder and extends it with a knowledge-adaptive post-training stage and auxiliary fine-tuning losses to pre-align PLM–KG representations and strengthen joint reasoning that GreaseLM left unadapted.

---

## Synthesis: How Prior Work Led to This Paper

Graph-augmented QA systems have evolved from augmenting language models with retrieved knowledge graphs to tightly coupling both modalities. QA-GNN formalized an IR-based KAQA pipeline that retrieves entity-centric subgraphs and attentively pools graph features into the answer scorer, establishing the practical framework many LM+KG systems follow. GreaseLM advanced this paradigm by introducing two-way interaction layers between a pre-trained LM and a GNN, mixing an interaction token and node representation so information flows across modalities rather than only one way. Yet empirical analyses of multi-modal contrastive learning revealed a deeper issue: modality gaps where semantically aligned items reside in disparate, narrow cones across embedding spaces, hindering fusion and transfer. Concurrently, multi-hop graph reasoners like MHGRN showed that even with strong graph aggregation, leveraging noisy, imperfectly retrieved KGs remains challenging. At the knowledge representation level, TransE offered a simple but powerful insight—relations can be modeled as translations—providing a geometric constraint for triple coherence. Finally, studies on KAQA generalization highlighted that models degrade under distribution shifts and when faced with irrelevant or insufficient evidence, underscoring the need for mechanisms that explicitly distinguish useful from noisy knowledge.
Building on this landscape, the next step was to pre-align PLM and KG spaces before cross-modal mixing while regularizing reasoning over retrieved triples and teaching models to filter knowledge. FiTs synthesizes these insights by adding a contrastive, knowledge-adaptive post-training stage to close semantic and distributional gaps, and by introducing two self-supervised fine-tuning objectives: a TransE-inspired backbone regularizer to preserve triple structure and a knowledge source distinction classifier to separate question-linked, answer-linked, peripheral, and irrelevant entities. Coupled with QA-GNN-style retrieval and GreaseLM’s interaction backbone, this two-stage design naturally addresses both modality mismatch and noisy evidence in KAQA.

---

*Analysis generated on: 2026-04-05T11:53:30.461578*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
