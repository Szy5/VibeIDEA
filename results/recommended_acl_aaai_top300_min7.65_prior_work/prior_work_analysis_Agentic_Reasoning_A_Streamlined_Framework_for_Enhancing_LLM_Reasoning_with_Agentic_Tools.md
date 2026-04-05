# Prior Work Analysis Report

## Target Paper

**Title:** Agentic Reasoning: A Streamlined Framework for Enhancing LLM Reasoning with Agentic Tools

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> We introduce Agentic Reasoning, a framework that enhances large language model (LLM) reasoning by integrating external tool-using agents.Agentic Reasoning dynamically leverages web search, code execution, and structured memory to address complex problems requiring deep research.A key innovation in our framework is the Mind-Map agent, which constructs a structured knowledge graph to store reasoning context and track logical relationships, ensuring coherence in long reasoning chains with extensive tool usage.Additionally, we conduct a comprehensive exploration of the Web-Search agent, leading to a highly effective search mechanism that surpasses all prior approaches.When deployed on DeepSeek-R1, our method achieves a new state-of-the-art (SOTA) among public models and delivers performance comparable to OpenAI Deep Research, the leading proprietary model in this domain.Extensive ablation studies validate the optimal selection of agentic tools and confirm the effectiveness of our Mind-Map and Web-Search agents in enhancing LLM reasoning.Our code and data are publicly available.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020) [[arXiv](https://arxiv.org/abs/2005.11401)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* Agentic Reasoning’s Web-Search agent and its querying of the Mind-Map both adopt RAG’s retrieve-then-generate paradigm to ground generation in external evidence.

**Assisting in Writing Wikipedia-like Articles from Scratch with Large Language Models (STORM) + FreshWiki** (2024) [[arXiv](https://arxiv.org/abs/2402.14207)]
- *Authors:* Yijia Shao et al.
- *Direct Connection:* STORM introduced the FreshWiki long-form, web-research writing setup that defines the deep-research problem and evaluation adopted and advanced by Agentic Reasoning.

### 🏷️ Inspiration

**Open-RAG: Enhanced Retrieval-Augmented Reasoning with Open-Source Large Language Models** (2024) [[arXiv](https://arxiv.org/abs/2410.01782)]
- *Authors:* Shayekh Bin Islam et al.
- *Direct Connection:* Open-RAG’s agentic retrieval loop—autonomously deciding when and what to retrieve during reasoning—directly inspired the Web-Search agent’s design that Agentic Reasoning refines with structured query breakdown and robust reranking.

### 🏷️ Gap Identification

**MemGPT: Towards LLMs as Operating Systems** (2023)
- *Authors:* Charles Packer et al.
- *Direct Connection:* MemGPT’s unstructured, summary-driven memory exposed brittleness in long, multi-step tasks, motivating Agentic Reasoning’s graph-structured Mind-Map to preserve logical relations and reduce drift during extended tool use.

**MemoryBank: Enhancing Large Language Models with Long-Term Memory** (2024)
- *Authors:* Wanjun Zhong et al.
- *Direct Connection:* MemoryBank demonstrated long-term retrieval from past interactions but lacked explicit relational structure, a limitation directly addressed by Agentic Reasoning’s knowledge-graph Mind-Map that encodes and queries entity-level links.

### 🏷️ Baseline

**Search-O1: Agentic Search-Enhanced Large Reasoning Models** (2025) [[arXiv](https://arxiv.org/abs/2501.05366)]
- *Authors:* Xiaoxi Li et al.
- *Direct Connection:* Search-O1 established the 'search-in-the-loop' formulation for LRMs that Agentic Reasoning explicitly improves upon via systematic query breakdown, reranking, and Mind-Map–aware context integration.

### 🏷️ Extension

**From Local to Global: A Graph RAG Approach to Query-Focused Summarization** (2024) [[arXiv](https://arxiv.org/abs/2404.16130)]
- *Authors:* Darren Edge et al.
- *Direct Connection:* The Mind-Map agent directly follows GraphRAG’s practice of building a knowledge graph and querying it with RAG, extending it into a dynamic structured memory that tracks entities and relations across long reasoning chains.

---

## Synthesis: How Prior Work Led to This Paper

Retrieval-augmented generation established the core mechanism of retrieving external evidence and conditioning generation on it, enabling language models to ground answers in sources rather than parametric memory. GraphRAG advanced this idea by converting text into a knowledge graph and using graph-aware retrieval to answer queries, showing that explicit entity and relation structure can organize and surface relevant context for complex information needs. On the search side, Search-O1 framed a practical blueprint for weaving web search into long reasoning, highlighting how iterative search during inference can lift performance on difficult questions. Complementing this, Open-RAG introduced an agentic retrieval loop in which the model autonomously decides when and what to retrieve while reasoning, demonstrating the value of retrieval decisions as part of the reasoning policy. For long-form knowledge work, STORM not only provided the FreshWiki benchmark but also presented a multi-step, web-research writing process that crystallized the deep-research problem setting. Meanwhile, memory-centric systems such as MemGPT and MemoryBank revealed that unstructured or slot-based memories often struggle to maintain coherence and logical relations across extended interactions, especially when tool calls and long chains are involved.
Taken together, these works exposed both the promise and the gaps: search must be integrated as a deliberative agentic step, retrieval should be precise and context-aware, and memory must track relations to avoid drift. Agentic Reasoning emerges as a natural synthesis—retaining RAG’s grounding, adopting agentic search decisions, and elevating memory to a graph-structured Mind-Map—while operationalizing improvements like query breakdown, reranking, and graph-informed context to create a streamlined, multi-tool reasoning loop that is both coherent and empirically stronger.

---

*Analysis generated on: 2026-04-04T22:29:59.969906*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
