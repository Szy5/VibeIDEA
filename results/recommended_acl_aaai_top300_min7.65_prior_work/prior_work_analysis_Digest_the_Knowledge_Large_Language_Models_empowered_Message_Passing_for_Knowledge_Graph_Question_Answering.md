# Prior Work Analysis Report

## Target Paper

**Title:** Digest the Knowledge: Large Language Models empowered Message Passing for Knowledge Graph Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Despite their success, large language models (LLMs) suffer from notorious hallucination issue.By introducing external knowledge stored in knowledge graphs (KGs), existing methods use paths as the medium to represent the graph information sent into LLMs.However, paths only contain limited graph structure information and are unorganized with redundant sequentially appearing keywords, which are difficult for LLMs to digest.We aim to find a suitable medium that captures the essence of structural knowledge in KGs.Inspired by Neural Message Passing in Graph Neural Networks, we propose Language Message Passing (LMP), which first learns a concise facts graph by iteratively aggregating neighbor entities and transforming them into semantic facts, and then performs Topological Readout that encodes the graph structure information into multi-level lists of texts to augment LLMs.Our method serves as a brand-new innovative framework that brings a new perspective into KG-enhanced LLMs, and also offers humanlevel semantic explainability with significant performance improvements over existing methods on all five knowledge graph question answering datasets.Our code is available at https://github.com/wanjunhong0/LMP.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Inspiration

**Neural Message Passing for Quantum Chemistry** (2017) [[arXiv](https://arxiv.org/abs/1704.01212)]
- *Authors:* Justin Gilmer et al.
- *Direct Connection:* The core idea of iteratively aggregating and transforming neighborhood information in a message passing framework directly inspires implementing an LLM-driven, text-space message passing to build a concise 'facts graph'.

**How Powerful are Graph Neural Networks?** (2019) [[arXiv](https://arxiv.org/abs/1810.00826)]
- *Authors:* Keyulu Xu et al.
- *Direct Connection:* The concept of graph-level Readout functions for summarizing structure motivates the Topological Readout that encodes depth and width via DFS-numbered, multi-level textual lists.

### 🏷️ Gap Identification

**Retrieve-Rewrite-Answer: A KG-to-Text Enhanced LLMs Framework for Knowledge Graph Question Answering** (2023) [[arXiv](https://arxiv.org/abs/2309.11206)]
- *Authors:* Yike Wu et al.
- *Direct Connection:* By showing raw keyword triples are awkward for LLMs and advocating KG-to-text rewriting, it directly motivates transforming aggregated neighborhoods into concise, question-focused semantic facts.

**HARP: Hierarchical Representation Learning for Networks** (2018) [[arXiv](https://arxiv.org/abs/1706.07845)]
- *Authors:* Haochen Chen et al.
- *Direct Connection:* Its observation that path-level traversals capture depth but miss hierarchical overviews motivates moving beyond paths to a condensed, structured representation that preserves multi-level graph organization.

### 🏷️ Baseline

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model with Knowledge Graph** (2024) [[arXiv](https://arxiv.org/abs/unknown)]
- *Authors:* Jiashuo Sun et al.
- *Direct Connection:* As a primary path-based KG-to-LLM baseline, it retrieves and feeds raw paths/triples to LLMs, whose structural and semantic limitations are explicitly addressed by replacing paths with a message-passing-derived facts graph.

### 🏷️ Extension

**Hierarchical Graph Representation Learning with Differentiable Pooling** (2018) [[arXiv](https://arxiv.org/abs/1806.08804)]
- *Authors:* Zhitao Ying et al.
- *Direct Connection:* The pooling notion of coarsening nodes into higher-level units is directly extended by merging l-hop neighbor entities into hyper-entities whose text descriptions are summarized semantic facts.

**Inductive Representation Learning on Large Graphs** (2017) [[arXiv](https://arxiv.org/abs/1706.02216)]
- *Authors:* Will Hamilton et al.
- *Direct Connection:* GraphSAGE’s neighbor sampling to control breadth informs the sampling step that selects top-K l-hop relations per layer to keep LLM-based message passing tractable and focused.

---

## Synthesis: How Prior Work Led to This Paper

Neural Message Passing established the practice of iteratively aggregating and transforming neighborhood information to derive informative, higher-level graph representations, while later work emphasized explicit Readout functions for producing graph-level summaries. Complementary advances demonstrated how to coarsen graphs via differentiable pooling, merging fine-grained nodes into higher-level constructs, and how neighbor sampling controls computational breadth during message passing. In parallel, knowledge-graph–enhanced LLM systems operationalized retrieval as paths: methods like Think-on-Graph extract and feed raw triples or paths to LLMs for reasoning. However, evidence accumulated that keyword-based triples and paths are semantically awkward for language models, motivating KG-to-text rewriting to better align with LLMs, and theoretical insights on representation learning highlighted that paths capture depth but fail to provide a hierarchical overview of graph structure. Together, these works delineated both a set of powerful graph-structuring primitives and the shortcomings of path-based KG augmentation for LLMs.
Synthesizing these insights naturally suggested replacing path extraction with a message passing–style pipeline executed in text: sample salient l-hop neighborhoods (as in neighbor sampling), aggregate and transform them into concise semantic statements (aligned with KG-to-text), pool them into hyper-entities (inspired by DiffPool), and apply a readout-like procedure that preserves topology by encoding depth and width into hierarchical multi-level lists. This combination yields a compact, human-interpretable facts graph that captures structure beyond paths and produces LLM-digestible inputs, directly addressing the limitations surfaced by path-centric KG-LLM methods.

---

*Analysis generated on: 2026-04-05T11:53:21.468928*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
