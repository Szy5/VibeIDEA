# Prior Work Analysis Report

## Target Paper

**Title:** Multimodal Reasoning with Multimodal Knowledge Graph

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Multimodal reasoning with large language models (LLMs) often suffers from hallucinations and the presence of deficient or outdated knowledge within LLMs.Some approaches have sought to mitigate these issues by employing textual knowledge graphs, but their singular modality of knowledge limits comprehensive cross-modal understanding.In this paper, we propose the Multimodal Reasoning with Multimodal Knowledge Graph (MR-MKG) method, which leverages multimodal knowledge graphs (MMKGs) to learn rich and semantic knowledge across modalities, significantly enhancing the multimodal reasoning capabilities of LLMs.In particular, a relation graph attention network is utilized for encoding MMKGs and a cross-modal alignment module is designed for optimizing image-text alignment.A MMKGgrounded dataset is constructed to equip LLMs with initial expertise in multimodal reasoning through pretraining.Remarkably, MR-MKG achieves superior performance while training on only a small fraction of parameters, approximately 2.25% of the LLM's parameter size.Experimental results on multimodal question answering and multimodal analogy reasoning tasks demonstrate that our MR-MKG method outperforms previous state-of-the-art models.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**MMKG: Multi-Modal Knowledge Graphs** (2019)
- *Authors:* Ye Liu et al.
- *Direct Connection:* This work introduced and released MMKGs that associate entities with images across KBs (Freebase, DBpedia, YAGO), providing the exact multimodal KG resource MR-MKG retrieves from to supply image-linked triples for ScienceQA and to ground multimodal reasoning.

**Multimodal Analogical Reasoning over Knowledge Graphs** (2022)
- *Authors:* Ningyu Zhang et al.
- *Direct Connection:* This work defined the multimodal analogical reasoning task and released MARS/MarKG, which MR-MKG uses as the problem setup and MMKG source for its analogy experiments and evaluations.

### 🏷️ Inspiration

**Image-embodied Knowledge Representation Learning** (2017)
- *Authors:* Ruobing Xie et al.
- *Direct Connection:* By demonstrating that integrating entity images into KG embeddings improves downstream reasoning, this paper directly motivated MR-MKG’s design choice to treat visual signals as first-class knowledge within a KG and to leverage them during reasoning.

**Retrieve-Rewrite-Answer: A KG-to-Text Enhanced LLMs Framework for Knowledge Graph Question Answering** (2023) [[arXiv](https://arxiv.org/abs/2309.11206)]
- *Authors:* Yike Wu et al.
- *Direct Connection:* This paper’s pipeline of retrieving KG subgraphs and injecting them into LLM prompts inspired MR-MKG’s retrieval-and-injection strategy, which is generalized from textual verbalization to embedding-level integration of multimodal KG evidence.

### 🏷️ Gap Identification

**KAM-CoT: Knowledge Augmented Multimodal Chain-of-Thoughts Reasoning** (2024)
- *Authors:* Debjyoti Mondal et al.
- *Direct Connection:* By augmenting multimodal reasoning with text-based KGs yet remaining constrained by single-modality knowledge, this study highlights the key limitation MR-MKG addresses by exploiting multimodal KGs and adding explicit cross-modal alignment.

### 🏷️ Extension

**Relation-aware Graph Attention Networks with Relational Position Encodings for Emotion Recognition in Conversations** (2020)
- *Authors:* Taichi Ishiwatari et al.
- *Direct Connection:* MR-MKG adopts and extends RGAT as its KG encoder to embed retrieved MMKG subgraphs, leveraging relation-aware attention to preserve graph structure and relation semantics before mapping into the LLM.

**Graph Neural Prompting with Large Language Models** (2023)
- *Authors:* Yijun Tian et al.
- *Direct Connection:* Their finding that raw KG triples introduce noise and proposal to use GNNs to extract salient graph representations is directly extended in MR-MKG by encoding MMKG subgraphs with RGAT and feeding the compact embeddings to the LLM.

---

## Synthesis: How Prior Work Led to This Paper

Multimodal knowledge graphs gained traction when MMKG established entity-level alignments with images across canonical KBs, enabling retrieval of visually grounded triples instead of text-only facts. Earlier, IKRL showed that augmenting entity representations with images yields stronger knowledge embeddings, highlighting that visual content can be a knowledge-bearing signal rather than mere illustration. For encoding graph structure and relation semantics, RGAT introduced relation-aware attention and relational position encodings, demonstrating superior capacity to preserve relational patterns in graph representations. In parallel, KG-to-LLM augmentation advanced through a retrieve-and-inject paradigm that transformed retrieved subgraphs into prompts for LLMs, while subsequent work warned that dumping raw triples is noisy and proposed graph neural prompting to distill salient subgraph information before interfacing with LLMs. Finally, the MARS/MarKG benchmark framed multimodal analogical reasoning directly on multimodal KGs, and KAM-CoT demonstrated the promise of knowledge-augmented multimodal CoT while revealing the limitations of text-only KGs for cross-modal reasoning.
Together, these threads exposed a natural opportunity: combine the retrieve-and-inject LLM paradigm with graph neural encoding, but source knowledge from truly multimodal KGs and explicitly align images and text at the entity level. Building on MMKG and MarKG as resources, and on IKRL’s insight that images enrich entity semantics, a relation-aware GNN (RGAT) is used to embed retrieved MMKG subgraphs; alignment is reinforced via an image–text matching objective within the graph; and compact knowledge and visual adapters inject these embeddings into frozen LLMs. This synthesis addresses the noise and modality gaps flagged by GNP and KAM-CoT, yielding a parameter-efficient way to ground multimodal reasoning in MMKG evidence.

---

*Analysis generated on: 2026-04-05T12:07:20.832338*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
