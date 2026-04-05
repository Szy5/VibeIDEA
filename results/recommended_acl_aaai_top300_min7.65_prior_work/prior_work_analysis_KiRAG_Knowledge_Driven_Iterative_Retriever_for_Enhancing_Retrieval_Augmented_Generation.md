# Prior Work Analysis Report

## Target Paper

**Title:** KiRAG: Knowledge-Driven Iterative Retriever for Enhancing Retrieval-Augmented Generation

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Iterative retrieval-augmented generation(iRAG) models offer an effective approach for multihop question answering (QA).However, their retrieval processes face two key challenges: (1) they can be disrupted by irrelevant documents or factually inaccurate chain-of-thoughts; (2) their retrievers are not designed to dynamically adapt to the evolving information needs in multi-step reasoning, making it difficult to identify and retrieve the missing information required at each iterative step.Therefore, we propose KiRAG 1 , which uses a knowledge-driven iterative retriever model to enhance the retrieval process of iRAG.Specifically, KiRAG decomposes documents into knowledge triples and performs iterative retrieval with these triples to enable a factually reliable retrieval process.Moreover, KiRAG integrates reasoning into the retrieval process to dynamically identify and retrieve knowledge that bridges information gaps, effectively adapting to the evolving information needs.Empirical results show that KiRAG significantly outperforms existing iRAG models, with an average improvement of 9.40% in R@3 and 5.14% in F1 on multi-hop QA datasets.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**TRACE the evidence: Constructing knowledge-grounded reasoning chains for retrieval-augmented generation** (2024)
- *Authors:* Jinyuan Fang et al.
- *Direct Connection:* KiRAG uses TRACE’s triple-grounded reasoning chains to construct silver supervision for its Reasoning Chain Aligner and adopts the notion of evidence chains as sequences of knowledge triples.

**HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering** (2018) [[arXiv](https://arxiv.org/abs/1809.09600)]
- *Authors:* Zhilin Yang et al.
- *Direct Connection:* HotpotQA defines the multi-hop QA setting requiring stepwise aggregation of evidence across documents, the core problem formulation and evaluation setting on which KiRAG is developed and assessed.

### 🏷️ Inspiration

**REANO: Optimising retrieval-augmented reader models through knowledge graph generation** (2024)
- *Authors:* Jinyuan Fang et al.
- *Direct Connection:* REANO’s finding that generating and leveraging document-grounded knowledge triples improves factuality directly motivates KiRAG’s decomposition of documents into triples for more faithful retrieval.

**From Local to Global: A Graph RAG Approach to Query-Focused Summarization** (2024) [[arXiv](https://arxiv.org/abs/2404.16130)]
- *Authors:* Darren Edge et al.
- *Direct Connection:* Edge et al. showed LLMs can extract document-grounded knowledge triples to build a graph index, which KiRAG adopts as an offline KG corpus for efficient, fact-grounded candidate generation.

### 🏷️ Baseline

**Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions** (2023)
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* KiRAG retains IRCoT’s iterative retrieve–reason loop but directly replaces IRCoT’s LLM-generated chain-of-thought guidance with document-grounded knowledge triples to drive each retrieval step.

### 🏷️ Extension

**Boosting Language Models’ Reasoning with Chain-of-Knowledge Prompting** (2024)
- *Authors:* Jianing Wang et al.
- *Direct Connection:* KiRAG extends Chain-of-Knowledge prompting by having an LLM-based Constructor assemble the next triple in a triple-based reasoning chain from candidate triples, replacing free-form CoT with grounded CoK during iterative retrieval.

### 🏷️ Related Problem

**DRAGIN: Dynamic Retrieval Augmented Generation Based on the Real-Time Information Needs of Large Language Models** (2024)
- *Authors:* Weihang Su et al.
- *Direct Connection:* Addressing the same need to adapt retrieval to evolving information needs, DRAGIN motivates KiRAG’s trained Reasoning Chain Aligner for selecting the next-step evidence without relying on free-form LLM thoughts.

---

## Synthesis: How Prior Work Led to This Paper

Interleaving retrieval with chain-of-thought (CoT) reasoning, IRCoT demonstrated that iteratively generating intermediate thoughts can guide multi-step retrieval for knowledge-intensive questions, but its reliance on free-form CoT leaves it vulnerable to hallucinations. TRACE introduced knowledge-grounded reasoning chains composed of document-extracted triples, establishing a way to represent evidence as sequences of ⟨head, relation, tail⟩ facts and producing supervision for building such chains. REANO showed that generating and leveraging document-grounded triples improves factual fidelity in RAG, highlighting the advantage of operating on structured, verifiable units rather than noisy sentences. Chain-of-Knowledge prompting further argued for replacing free-form CoT with triple-based CoK to enhance faithfulness in reasoning. Complementing these ideas, Edge et al. demonstrated that LLMs can reliably extract knowledge triples from text to construct a graph index, enabling efficient graph-centric retrieval over document content. In parallel, DRAGIN emphasized that retrieval should adapt dynamically to evolving information needs across steps, framing the need for mechanisms that decide what to fetch next as reasoning progresses. HotpotQA formalized the multi-hop QA task that demands sequential evidence gathering across documents.
Together, these works surfaced both the opportunity and the path forward: use triple-grounded chains to avoid hallucinated guidance, and adapt retrieval to evolving information needs. KiRAG synthesizes this by extracting document-grounded triples to build an offline KG corpus, training a bi-encoder aligner (supervised with TRACE-style chains) to select the next triple that bridges current evidence gaps, and using a CoK-style Constructor to extend a triple chain rather than free-form thoughts. This yields a knowledge-driven iterative retriever that remains factual while dynamically steering retrieval toward the missing pieces required for multi-hop QA.

---

*Analysis generated on: 2026-04-05T12:06:45.950296*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
