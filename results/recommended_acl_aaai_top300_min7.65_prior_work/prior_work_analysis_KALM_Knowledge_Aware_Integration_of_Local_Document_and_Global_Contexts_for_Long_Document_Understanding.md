# Prior Work Analysis Report

## Target Paper

**Title:** KALM: Knowledge-Aware Integration of Local, Document, and Global Contexts for Long Document Understanding

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> With the advent of pre-trained language models (LMs), increasing research efforts have been focusing on infusing commonsense and domain-specific knowledge to prepare LMs for downstream tasks. These works attempt to leverage knowledge graphs, the de facto standard of symbolic knowledge representation, along with pre-trained LMs. While existing approaches leverage external knowledge, it remains an open question how to jointly incorporate knowledge graphs represented in varying contexts — from local (e.g., sentence), document-level, to global knowledge, to enable knowledge-rich and interpretable exchange across contexts. In addition, incorporating varying contexts can especially benefit long document understanding tasks that leverage pre-trained LMs, typically bounded by the input sequence length. In light of these challenges, we propose KALM, a language model that jointly leverages knowledge in local, document-level, and global contexts for long document understanding. KALM firstly encodes long documents and knowledge graphs into the three knowledge-aware context representations. KALM then processes each context with context-specific layers. These context-specific layers are followed by a ContextFusion layer that facilitates knowledge exchange to derive an overarching document representation. Extensive experiments demonstrate that KALM achieves state-of-the-art performance on three long document understanding tasks across 6 datasets/settings. Further analyses reveal that the three knowledge-aware contexts are complementary and they all contribute to model performance, while the importance and information exchange patterns of different contexts vary on different tasks and datasets.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Inspiration

**QA-GNN: Reasoning with Language Models and Knowledge Graphs for Question Answering** (2021) [[arXiv](https://arxiv.org/abs/2104.06378)]
- *Authors:* Yasunaga et al.
- *Direct Connection:* KALM adopts QA-GNN’s core insight of extracting and encoding a small k-hop (k=2) KG subgraph to supply global knowledge, using it as the global context that is then integrated with textual representations.

**Investigating the Effect of Background Knowledge on Natural Questions** (2021)
- *Authors:* Balachandran et al.
- *Direct Connection:* KALM leverages the finding that adding entity descriptions improves LM understanding by concatenating KG-derived textual descriptions to paragraphs to form its local knowledge-aware context.

### 🏷️ Gap Identification

**Compare to the Knowledge: Graph Neural Fake News Detection with External Knowledge** (2021)
- *Authors:* Hu et al.
- *Direct Connection:* While CompareNet shows the value of document-level heterogeneous graphs with external knowledge, it primarily fuses text and KG via simple aggregation; KALM addresses this limitation by enabling explicit information flow and exchange across multiple contexts via ContextFusion.

**KEPLER: A Unified Model for Knowledge Embedding and Pre-trained Language Representation** (2021)
- *Authors:* Wang et al.
- *Direct Connection:* KEPLER’s sentence-level KG triple–aware pretraining illustrates local knowledge infusion but is tailored to short texts and model pretraining; KALM explicitly targets long documents by integrating local knowledge with document and global contexts rather than relying on pretraining alone.

### 🏷️ Baseline

**GreaseLM: Graph Reasoning Enhanced Language Models** (2021)
- *Authors:* Zhang et al.
- *Direct Connection:* KALM directly builds on GreaseLM’s paradigm of encoding a k-hop KG subgraph with a GNN and fusing it with LM representations (via MInt), but generalizes this fusion to three contexts and replaces MInt with a ContextFusion layer that enables bidirectional exchange across local, document, and global representations.

### 🏷️ Extension

**KGAP: Knowledge Graph Augmented Political Perspective Detection in News Media** (2021) [[arXiv](https://arxiv.org/abs/2108.03861)]
- *Authors:* Feng et al.
- *Direct Connection:* KALM extends document-graph based knowledge infusion from KGAP by introducing knowledge coreference edges between paragraphs and a knowledge-guided attention GNN to enable cross-paragraph, KG-driven message passing.

---

## Synthesis: How Prior Work Led to This Paper

Graph–language fusion methods showed how to combine language models with knowledge graphs: GreaseLM encoded k-hop KG subgraphs with GNNs and introduced a modality interaction module to fuse them with LM token representations, while QA-GNN demonstrated that a compact 2-hop subgraph centered on mentioned entities suffices to inject relevant global knowledge for reasoning. Document-level knowledge integration progressed through graph-based approaches like KGAP and CompareNet, which constructed document graphs linking text spans with KG entities and relations to propagate signals across a document. These document-graph methods, however, typically used simple aggregation or one-shot fusion and did not explicitly model repeated, cross-paragraph entity overlap as a guiding signal for message passing. At the sentence/local level, KEPLER showed that aligning LMs with KG triples during pretraining can infuse factual knowledge, and Balachandran et al. found that appending entity descriptions to inputs benefits downstream understanding, but such techniques were largely tailored to short inputs and did not address inter-paragraph structure or global KG reasoning.
Taken together, this landscape suggested an opportunity: combine the strengths of local augmentation, document-graph reasoning, and global KG subgraphs, while enabling dynamic exchange among them. KALM synthesizes these threads by (i) forming a local context via appending entity descriptions, (ii) constructing a document-level graph with knowledge coreference edges so cross-paragraph links follow shared KG entities, and (iii) adopting a 2-hop KG subgraph for global context; it then replaces prior concatenation/MInt-style fusion with a ContextFusion layer that lets the three contexts attend to and inform one another, providing a unified, knowledge-rich representation tailored to long document understanding.

---

*Analysis generated on: 2026-04-05T11:57:24.555308*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
