# Prior Work Analysis Report

## Target Paper

**Title:** Graph Neural Prompting with Large Language Models

**arXiv ID:** [2309.15427](https://arxiv.org/abs/2309.15427)

**Abstract:** 
> Large language models (LLMs) have shown remarkable generalization capability with exceptional performance in various language modeling tasks. However, they still exhibit inherent limitations in precisely capturing and returning grounded knowledge. While existing work has explored utilizing knowledge graphs (KGs) to enhance language modeling via joint training and customized model architectures, applying this to LLMs is problematic owing to their large number of parameters and high computational cost. Therefore, how to enhance pre-trained LLMs using grounded knowledge, e.g., retrieval-augmented generation, remains an open question. In this work, we propose Graph Neural Prompting (GNP), a novel plug-and-play method to assist pre-trained LLMs in learning beneficial knowledge from KGs. GNP encompasses various designs, including a standard graph neural network encoder, a cross-modality pooling module, a domain projector, and a self-supervised link prediction objective. Extensive experiments on multiple datasets demonstrate the superiority of GNP on both commonsense and biomedical reasoning tasks across different LLM sizes and settings. Code is available at https://github.com/meettyj/GNP.

**Innovation pattern:** Cross-Domain Synthesis (confidence: high)

Secondary patterns: Modular Pipeline Composition

*Reasoning:* The work fuses GNN/KG retrieval techniques with frozen LLM prompt‑tuning—a deliberate cross‑domain hybridization—while repurposing a modular pipeline (entity linking, subgraph retrieval, GNN encoding) to produce prompts.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020) [[arXiv](https://arxiv.org/abs/arXiv:2005.11401)]
- *Authors:* Lewis et al.
- *Direct Connection:* Formalized the paradigm of retrieving external knowledge to augment a language model’s output, which GNP adopts at the knowledge-graph level by retrieving subgraphs and converting retrieved facts into prompts instead of raw text context.

**Embedding Entities and Relations for Learning and Inference in Knowledge Bases (DistMult)** (2015) [[arXiv](https://arxiv.org/abs/arXiv:1412.6575)]
- *Authors:* Yang et al.
- *Direct Connection:* Introduced the DistMult scoring function for relation prediction widely used for KG link prediction, which GNP directly adopts as the self‑supervised scoring objective to refine node embeddings and capture relational structure in the learned prompts.

### 🏷️ Inspiration

**The Power of Scale for Parameter-Efficient Prompt Tuning** (2021) [[arXiv](https://arxiv.org/abs/arXiv:2104.08691)]
- *Authors:* Lester et al.
- *Direct Connection:* Introduced soft, learnable prompt vectors for frozen large language models, a specific mechanism GNP generalizes by producing instance-level soft prompts derived from encoded subgraphs rather than dataset-level token embeddings.

**QA‑GNN: Reasoning with Language Models and Knowledge Graphs for Question Answering** (2021)
- *Authors:* Yasunaga et al.
- *Direct Connection:* Demonstrated retrieving subgraphs and using GNNs to perform multi-hop reasoning over KGs for QA, a pipeline GNP reuses (entity linking, two‑hop subgraph retrieval, GNN encoding) but redirects the GNN output into soft prompts for pre‑trained LLMs.

### 🏷️ Gap Identification

**GreaseLM: Graph REASoning Enhanced Language Models for Question Answering** (2022)
- *Authors:* Zhang et al.
- *Direct Connection:* Showed the benefits of fusing graph structure with language models via joint architectures and pretraining, and in doing so exposed the heavy computation and joint‑training limitations that motivated GNP’s plug‑and‑play prompt approach instead of fusion pretraining.

**Knowledge-Augmented Language Model Prompting for Zero-Shot Knowledge Graph Question Answering (KAPING)** (2023)
- *Authors:* Baek, Aji, and Saffari
- *Direct Connection:* Proposed directly injecting retrieved KG triples into LLM prompts and empirically observed noise and brittleness, a practical failure mode GNP addresses by learning condensed, relevance‑weighted graph prompts via cross‑modality pooling and a domain projector.

---

## Synthesis: How Prior Work Led to This Paper

Work on soft prompt learning established that frozen LLMs can be steered by learned continuous vectors, and the prompt‑tuning literature provided the concrete mechanism GNP adapts to carry structured knowledge. Retrieval‑augmented generation formalized the utility of fetching external evidence to supplement language models, which motivated retrieving KG subgraphs as the knowledge source. Prior graph+language efforts (e.g., QA‑GNN) demonstrated the concrete pipeline of entity linking, local subgraph retrieval, and GNN encoding for question answering—elements GNP reuses but repurposes to produce prompts rather than to jointly train or fuse models. At the same time, fusion and joint pretraining methods (GreaseLM, related joint KG–LM pretraining) highlighted strong gains but also expensive joint training and architectural coupling, exposing a gap for a plug‑and‑play alternative. Practical KG→LLM prompt attempts like KAPING further showed that naively dumping triples into prompts is noisy, motivating GNP’s cross‑modality pooling and domain projector. Finally, classical KG scoring (DistMult) supplied the off‑the‑shelf self‑supervised objective GNP uses to sharpen relation awareness in node embeddings. Together, these works pointed to the natural next step: convert retrieved subgraphs into compact, relevance‑aware soft prompts (bridging graph and text domains) so pre‑trained LLMs can leverage KG structure without costly joint retraining.

---

*Analysis generated on: 2026-03-09T00:18:26.450961*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=15724, output=1112*
