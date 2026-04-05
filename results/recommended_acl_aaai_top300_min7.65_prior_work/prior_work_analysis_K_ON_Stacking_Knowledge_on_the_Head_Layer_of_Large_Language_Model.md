# Prior Work Analysis Report

## Target Paper

**Title:** K-ON: Stacking Knowledge on the Head Layer of Large Language Model

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent advancements in large language models (LLMs) have significantly improved various natural language processing (NLP) tasks. Typically, LLMs are trained to predict the next token, aligning well with many NLP tasks. However, in knowledge graph (KG) scenarios, entities are the fundamental units and identifying an entity requires at least several tokens. This leads to a granularity mismatch between KGs and natural languages. To address this issue, we propose K-ON, which integrates KG knowledge into the LLM by employing multiple head layers for next k-step prediction. K-ON can not only generate entity-level results in one step, but also enables contrastive loss against entities, which is the most powerful tool in KG representation learning. Experimental results show that K-ON outperforms state-of-the-art methods that incorporate text and even the other modalities.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space** (2019) [[arXiv](https://arxiv.org/abs/1902.10197)]
- *Authors:* Sun et al.
- *Direct Connection:* RotatE popularized entity-level contrastive training with negative entities for KG completion, providing the core training paradigm that K-ON transfers to LLMs by optimizing an entity-level contrastive loss over the full KG.

**MMKG: Multi-modal Knowledge Graphs** (2019)
- *Authors:* Liu et al.
- *Direct Connection:* MMKG introduced the DB15K benchmark used in K-ON’s evaluations, providing the multimodal KG setting where entity names span multiple tokens and highlight the token–entity granularity mismatch K-ON tackles.

### 🏷️ Inspiration

**Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads** (2024) [[arXiv](https://arxiv.org/abs/2401.10774)]
- *Authors:* Cai et al.
- *Direct Connection:* Medusa introduced the idea of attaching multiple prediction heads to an LLM to produce several future tokens in one step and used attention across heads to preserve dependencies, directly inspiring K-ON’s K distinct head layers and conditional attention to enable next-k token prediction.

**Better & Faster Large Language Models via Multi-token Prediction** (2024) [[arXiv](https://arxiv.org/abs/2404.19737)]
- *Authors:* Gloeckle et al.
- *Direct Connection:* This work showed that training LLMs with multiple score heads to predict several next tokens improves learning and efficiency, motivating K-ON’s use of per-step heads to obtain K-step token distributions that are then aggregated into entity-level scores.

### 🏷️ Gap Identification

**Exploring Large Language Models for Knowledge Graph Completion** (2023) [[arXiv](https://arxiv.org/abs/2308.13916)]
- *Authors:* Yao et al.
- *Direct Connection:* By framing LLM-based KGC as triple verification on limited candidates and reporting weak open-set performance, this paper exposed the granularity and candidate-set limitations that K-ON addresses with one-shot entity prediction and entity-level training.

**Making Large Language Models Perform Better in Knowledge Graph Completion (KoPA)** (2023) [[arXiv](https://arxiv.org/abs/2310.06671)]
- *Authors:* Zhang et al.
- *Direct Connection:* KoPA fine-tuned LLMs for triplet correctness judgments instead of open-world entity prediction, underscoring the token-level objective mismatch that K-ON resolves via multi-head next-k prediction and entity-level contrastive loss.

**KG-BERT: BERT for Knowledge Graph Completion** (2019) [[arXiv](https://arxiv.org/abs/1909.03193)]
- *Authors:* Yao et al.
- *Direct Connection:* KG-BERT encoded textual triples and scored them with a language model but relied on sequence-level classification/ranking rather than parallel entity scoring, motivating K-ON’s head-layer reparameterization to score all entities via token sequences.

---

## Synthesis: How Prior Work Led to This Paper

Multiple-decoding-head approaches such as Medusa showed that an LLM can attach several output heads to predict multiple future tokens in one step, and further proposed attention mechanisms across heads to maintain sequential dependencies. Independently, multi-token prediction work demonstrated that training with multiple score heads to anticipate several next tokens improves both efficiency and modeling quality, reinforcing the practicality of multi-head, multi-step prediction. In parallel, RotatE established the effectiveness of entity-level contrastive training with negative entities for knowledge graph completion, making entity-level discrimination the dominant paradigm in KGE. On the language-model side of KGC, KG-BERT leveraged textual encoding of triples for scoring but fundamentally operated at the sequence/token level rather than producing entity-level predictions. More recent LLM-based KGC systems, including KG-LLaMA and KoPA, framed the task as triplet verification against restricted candidate sets, documenting weak performance in open-set completion and revealing a granularity mismatch between token-level objectives and entity-level KG targets. MMKG provided the DB15K benchmark where entity names typically require multiple tokens, underscoring the mismatch between token-level generation and entity identification.
Synthesizing these threads, the natural opportunity was to combine multi-head, multi-token prediction with entity-level contrastive learning: use multiple LLM heads to produce next-k token distributions per step, aggregate them into entity-level scores, and train with entity-level negatives as in KGE. To preserve the LLM’s sequential conditioning while making parallel predictions, head-to-head attention akin to multi-head inference frameworks is introduced, and the resulting distributions are aligned to the original head via KL-based trajectory tuning. This integration resolves the token–entity granularity gap while retaining the LLM’s generative competence, enabling one-shot, entity-level scoring directly at the head layer.

---

*Analysis generated on: 2026-04-05T12:01:24.013083*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
