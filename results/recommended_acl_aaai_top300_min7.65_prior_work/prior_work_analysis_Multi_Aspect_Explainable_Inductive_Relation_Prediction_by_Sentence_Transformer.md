# Prior Work Analysis Report

## Target Paper

**Title:** Multi-Aspect Explainable Inductive Relation Prediction by Sentence Transformer

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent studies on knowledge graphs (KGs) show that path-based methods empowered by pre-trained language models perform well in the provision of inductive and explainable relation predictions. In this paper, we introduce the concepts of relation path coverage and relation path confidence to filter out unreliable paths prior to model training to elevate the model performance. Moreover, we propose Knowledge Reasoning Sentence Transformer (KRST) to predict inductive relations in KGs. KRST is designed to encode the extracted reliable paths in KGs, allowing us to properly cluster paths and provide multi-aspect explanations. We conduct extensive experiments on three real-world datasets. The experimental results show that compared to SOTA models, KRST achieves the best performance in most transductive and inductive test cases (4 of 6), and in 11 of 12 few-shot test cases.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Inductive Relation Prediction by Subgraph Reasoning** (2020)
- *Authors:* Keshav Teru et al.
- *Direct Connection:* KRST follows GRAIL’s inductive relation prediction formulation and data splits while targeting GRAIL’s noted lack of explainability by reasoning over explicit, text-encoded paths.

### 🏷️ Inspiration

**Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks** (2019) [[arXiv](https://arxiv.org/abs/arXiv:1908.10084)]
- *Authors:* Nils Reimers et al.
- *Direct Connection:* KRST adopts Sentence-BERT’s siamese encoding and cosine similarity paradigm to separately embed triples and paths, enabling explicit similarity comparison and path clustering for multi-aspect explanations.

### 🏷️ Gap Identification

**Go for a Walk and Arrive at the Answer: Reasoning Over Paths in Knowledge Bases using Reinforcement Learning (MINERVA)** (2017) [[arXiv](https://arxiv.org/abs/arXiv:1711.05851)]
- *Authors:* Rajarshi Das et al.
- *Direct Connection:* The sparse-reward and exponential branching limitations in RL-based path reasoning highlighted by MINERVA motivate KRST’s non-RL path extraction via BFS and pre-filtering to retain only reliable reasoning paths.

### 🏷️ Baseline

**Inductive Relation Prediction by BERT** (2022)
- *Authors:* Hengrui Zha et al.
- *Direct Connection:* KRST directly builds on BERTRL’s idea of converting triples and their connecting paths into text for PLM-based scoring, but addresses BERTRL’s limitation of using all (often noisy) paths and single-path explanations by introducing path reliability filtering and replacing sequence classification with a siamese sentence-transformer similarity framework.

### 🏷️ Extension

**AMIE: Association Rule Mining under Incomplete Evidence in Ontological Knowledge Bases** (2013)
- *Authors:* Luis Galárraga et al.
- *Direct Connection:* KRST extends AMIE’s support and confidence notions for Horn rules by defining relation path coverage and relation path confidence to filter unreliable relation paths prior to training.

### 🏷️ Related Problem

**KG-BERT: BERT for Knowledge Graph Completion** (2019) [[arXiv](https://arxiv.org/abs/arXiv:1909.03193)]
- *Authors:* Liang Yao et al.
- *Direct Connection:* The textualization of entities/relations and fine-tuning of PLMs demonstrated in KG-BERT informs KRST’s use of natural language descriptions for triple scoring, which KRST augments with path conditioning and explainability.

---

## Synthesis: How Prior Work Led to This Paper

Path-centric reasoning has long leveraged the view that relation paths instantiate Horn-rule–like regularities; AMIE operationalized this by introducing support and confidence to assess rule reliability under incomplete evidence, showing that confidence-weighted rule selection can mitigate noise. Reinforcement learning methods such as MINERVA pursued path discovery directly on the graph, but exposed practical challenges—sparse rewards and exponential branching—that complicate reliable path acquisition at scale. Concurrently, PLM-based approaches demonstrated that textualizing KG components is a strong inductive signal: KG-BERT showed that BERT can score textualized triples, and BERTRL advanced this by textualizing both triples and connecting paths, using BERT sequence classification to choose a path-based explanation. However, BERTRL feeds all paths (below a length cap) to the model and largely yields single-path explanations, leaving path reliability unaddressed. In parallel, Sentence-BERT established a siamese architecture that produces sentence embeddings suitable for cosine comparison and clustering, often outperforming sequence classification on semantic similarity tasks. GRAIL defined the inductive relation prediction setting and benchmarks that isolate generalization to unseen entities, while acknowledging limited explainability.
Taken together, these works suggested a natural next step: combine inductive PLM-based textualization with explicit, confidence-inspired path filtering and a similarity-centric encoder that can compare triples against multiple paths. KRST synthesizes AMIE’s reliability principles with a BFS-based extraction strategy (avoiding RL pitfalls), then uses a Sentence-BERT–style siamese encoder and cosine embedding loss to align triples with the most semantically consistent paths, enabling multi-path, multi-aspect explanations under GRAIL’s inductive setup.

---

*Analysis generated on: 2026-04-05T11:59:36.397071*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
