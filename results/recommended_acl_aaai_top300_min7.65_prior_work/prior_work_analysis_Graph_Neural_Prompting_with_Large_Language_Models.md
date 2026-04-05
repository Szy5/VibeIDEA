# Prior Work Analysis Report

## Target Paper

**Title:** Graph Neural Prompting with Large Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) have shown remarkable generalization capability with exceptional performance in various language modeling tasks. However, they still exhibit inherent limitations in precisely capturing and returning grounded knowledge. While existing work has explored utilizing knowledge graphs (KGs) to enhance language modeling via joint training and customized model architectures, applying this to LLMs is problematic owing to their large number of parameters and high computational cost. Therefore, how to enhance pre-trained LLMs using grounded knowledge, e.g., retrieval-augmented generation, remains an open question. In this work, we propose Graph Neural Prompting (GNP), a novel plug-and-play method to assist pre-trained LLMs in learning beneficial knowledge from KGs. GNP encompasses various designs, including a standard graph neural network encoder, a cross-modality pooling module, a domain projector, and a self-supervised link prediction objective. Extensive experiments on multiple datasets demonstrate the superiority of GNP on both commonsense and biomedical reasoning tasks across different LLM sizes and settings. Code is available at https://github.com/meettyj/GNP.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020) [[arXiv](https://arxiv.org/abs/2005.11401)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* GNP follows the RAG principle of augmenting generation with retrieved external knowledge, replacing document retrieval/concatenation with KG subgraph retrieval and a learned graph-derived prompt that conditions the LLM.

### 🏷️ Inspiration

**QA-GNN: Reasoning with Language Models and Knowledge Graphs for Question Answering** (2021) [[arXiv](https://arxiv.org/abs/2104.06378)]
- *Authors:* Michihiro Yasunaga et al.
- *Direct Connection:* GNP draws on QA-GNN’s question-conditioned KG reasoning—retrieving a local subgraph and using a graph encoder—but retools it into cross-modality pooling that attends to input tokens to select relevant nodes for forming a prompt vector.

### 🏷️ Gap Identification

**GreaseLM: Graph REASoning Enhanced Language Models for Question Answering** (2022)
- *Authors:* Xinyue Zhang et al.
- *Direct Connection:* By showing that tight GNN–LM fusion with joint training boosts QA but requires bespoke architectures, GreaseLM motivates GNP’s plug-and-play alternative that distills KG reasoning into a compact prompt usable with frozen LLMs.

**Deep Bidirectional Language-Knowledge Graph Pretraining (DRAGON)** (2022)
- *Authors:* Michihiro Yasunaga et al.
- *Direct Connection:* DRAGON’s heavy joint pretraining over text and KGs—and its retrieval/ranking protocols—highlight both the benefits of KG-text fusion and the impracticality for LLMs, directly motivating GNP’s lightweight KG-to-LLM prompting approach and subgraph retrieval strategy.

### 🏷️ Baseline

**Knowledge-Augmented Language Model Prompting for Zero-Shot Knowledge Graph Question Answering** (2023)
- *Authors:* Juyong Baek et al.
- *Direct Connection:* KAPING’s direct injection of retrieved KG triples into LLM prompts is the primary baseline GNP improves upon by learning to denoise and compress KG evidence via GNN encoding and cross-modality pooling before conditioning the LLM.

### 🏷️ Extension

**The Power of Scale for Parameter-Efficient Prompt Tuning** (2021) [[arXiv](https://arxiv.org/abs/2104.08691)]
- *Authors:* Brian Lester et al.
- *Direct Connection:* GNP adopts the frozen-LLM soft-prompting paradigm of Prompt Tuning and extends it by generating instance-specific soft prompts from KG-encoded representations instead of learning a static dataset-level vector.

---

## Synthesis: How Prior Work Led to This Paper

Soft prompt tuning established that frozen language models can be steered by learned continuous prompts, demonstrating a parameter-efficient alternative to full fine-tuning. Retrieval-augmented generation further showed that conditioning generators on retrieved external knowledge can markedly improve knowledge-intensive tasks, typically by fetching and concatenating relevant passages. Concurrently, knowledge-graph QA methods revealed that question-specific subgraph retrieval and graph encoders can scaffold complex reasoning: QA-GNN retrieves local KG neighborhoods and uses a graph network to focus on question-relevant entities, while GreaseLM tightly fuses a GNN with a language model through joint training to propagate graph reasoning signals into text representations. DRAGON extended this trajectory with deep bidirectional pretraining across KGs and text, alongside retrieval and ranking schemes, evidencing strong gains but also imposing substantial architectural complexity and training cost. In contrast, KAPING exemplified a lightweight approach for LLMs by directly inserting retrieved KG triples into prompts, but it exposed a practical pitfall—noisy and extraneous KG content can degrade performance when injected verbatim.
Collectively, these works revealed a clear opportunity: harness KG structure for LLMs without heavy joint training or brittle triple concatenation, and do so in a prompt-based, frozen-LLM setting. Building on soft prompting and RAG’s retrieval ethos, and leveraging question-conditioned KG selection from QA-GNN, the current work synthesizes a GNN encoder, token-guided cross-modality pooling to highlight salient nodes, a domain projector aligning graph and text spaces, and a self-supervised link-prediction objective—yielding a compact, instance-level graph neural prompt that robustly conditions LLMs with grounded KG knowledge.

---

*Analysis generated on: 2026-04-05T11:37:36.593705*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
