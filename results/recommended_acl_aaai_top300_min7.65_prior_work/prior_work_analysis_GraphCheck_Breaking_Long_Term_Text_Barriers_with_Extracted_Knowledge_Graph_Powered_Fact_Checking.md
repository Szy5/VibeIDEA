# Prior Work Analysis Report

## Target Paper

**Title:** GraphCheck: Breaking Long-Term Text Barriers with Extracted Knowledge Graph-Powered Fact-Checking

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) are widely used, but they often generate subtle factual errors, especially in long-form text. These errors are fatal in some specialized domains such as medicine. Existing fact-checking with grounding documents methods face two main challenges: (1) they struggle to understand complex multihop relations in long documents, often overlooking subtle factual errors; (2) most specialized methods rely on pairwise comparisons, requiring multiple model calls, leading to high resource and computational costs. To address these challenges, we propose <b><i>GraphCheck</i></b> , a fact-checking framework that uses extracted knowledge graphs to enhance text representation. Graph Neural Networks further process these graphs as a soft prompt, enabling LLMs to incorporate structured knowledge more effectively. Enhanced with graph-based reasoning, GraphCheck captures multihop reasoning chains that are often overlooked by existing methods, enabling precise and efficient fact-checking in a single inference call. Experimental results on seven benchmarks spanning both general and medical domains demonstrate up to a 7.1% overall improvement over baseline models. Notably, GraphCheck outperforms existing specialized fact-checkers and achieves comparable performance with state-of-the-art LLMs, such as DeepSeek-V3 and OpenAI-o1, with significantly fewer parameters.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**MiniCheck** (2024)
- *Authors:* Jiabin Tang et al.
- *Direct Connection:* MiniCheck provided the document–claim–label pairs that GraphCheck uses to synthesize graph training data for its GNN and exemplified the fine-grained, multi-call checking paradigm whose inefficiency GraphCheck remedies.

### 🏷️ Inspiration

**G-Retriever: Retrieval-Augmented Generation for Textual Graph Understanding and Question Answering** (2024) [[arXiv](https://arxiv.org/abs/2402.07630)]
- *Authors:* Xiaoxin He et al.
- *Direct Connection:* G-Retriever demonstrated that LLMs can utilize graph evidence when textualized, inspiring GraphCheck to replace verbose graph text with a projector that aligns GNN-derived graph embeddings to the LLM space for more efficient integration.

### 🏷️ Gap Identification

**FactScore: Fine-Grained Atomic Evaluation of Factual Precision in Long Form Text Generation** (2023) [[arXiv](https://arxiv.org/abs/2305.14251)]
- *Authors:* Sewon Min et al.
- *Direct Connection:* By showing that decomposing long-form outputs into atomic facts and verifying each one separately improves faithfulness but requires many verifier calls, FactScore directly motivates GraphCheck’s single-call alternative that captures multi-hop relations via whole-graph reasoning.

**GraphEval: A Knowledge-Graph Based LLM Hallucination Evaluation Framework** (2024) [[arXiv](https://arxiv.org/abs/2407.10793)]
- *Authors:* Hannah Sansford et al.
- *Direct Connection:* GraphEval verifies extracted triples with pairwise NLI but ignores global graph topology, a limitation GraphCheck overcomes by encoding the full claim/document graphs with a GNN and leveraging their structure for multihop reasoning.

### 🏷️ Baseline

**ACUEval: Atomic Content Unit-based Evaluation for Factual Consistency** (2024)
- *Authors:* Ziqing Wan et al.
- *Direct Connection:* ACUEval operationalizes per-unit extraction and pairwise verification for long texts, serving as a primary baseline whose multi-call inefficiency GraphCheck addresses by encoding the entire claim and document graphs and deciding in one pass.

### 🏷️ Extension

**FactGraph: Evaluating Factuality in Summarization with Semantic Graph Representations** (2022) [[arXiv](https://arxiv.org/abs/2204.06508)]
- *Authors:* Leonardo F. R. Ribeiro et al.
- *Direct Connection:* FactGraph established that combining graph encoders with text features aids factuality judgments, which GraphCheck extends by injecting learned GNN graph embeddings as a soft prompt into an LLM verifier and comparing claim vs. document graphs.

### 🏷️ Related Problem

**AMRFact: Enhancing Summarization Factuality Evaluation with AMR-Driven Negative Samples Generation** (2024)
- *Authors:* Haoyi Qiu et al.
- *Direct Connection:* AMRFact leveraged structured AMR graphs to strengthen factuality evaluation signals, reinforcing the core insight GraphCheck adopts—structured semantic graphs support better detection of subtle inconsistencies than raw text alone.

---

## Synthesis: How Prior Work Led to This Paper

Fine-grained fact-checking emerged as a response to subtle errors in long-form generation. FactScore showed that breaking text into atomic facts and verifying each item increases precision but at the cost of many verification calls. ACUEval systematized this idea via Atomic Content Units and pairwise verification, further demonstrating effectiveness yet highlighting inefficiency at scale. In parallel, graph-centric approaches began to surface: GraphEval extracted triples and assessed them with NLI on a per-triple basis, making the process sensitive to local errors while missing global topology. Earlier, FactGraph established that semantic graphs combined with textual features improve factuality decisions, though it relied on pre-LLM architectures and shallow fusion. G-Retriever then demonstrated that LLMs can benefit from graph evidence by prompting with textualized graphs, while AMRFact underlined that structured representations like AMR can better capture factual relations than raw text alone. MiniCheck, finally, contributed large-scale document–claim–label pairs that operationalized fine-grained checking and provided the supervision GraphCheck uses to synthesize graph training data.
Building on these strands, a gap became clear: atomic, per-unit methods are accurate but computationally expensive, and triple-wise graph checks miss multihop dependencies and global structure; textual graph prompting risks long, noisy inputs. The natural next step was to encode full claim and document graphs, align them with LLM representations, and decide once. GraphCheck synthesizes these insights by extracting KGs, encoding them with a trainable GNN, projecting the embeddings into the LLM as a soft prompt, and performing a single-pass, multihop-aware comparison—achieving fine-grained accuracy with markedly improved efficiency, especially on long documents and specialized domains.

---

*Analysis generated on: 2026-04-05T12:05:52.009415*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
