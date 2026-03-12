# Prior Work Analysis Report

## Target Paper

**Title:** Enrich-on-Graph: Query-Graph Alignment for Complex Reasoning with LLM Enriching

**arXiv ID:** [2509.20810](https://arxiv.org/abs/2509.20810)

**Abstract:** 
> Large Language Models (LLMs) exhibit strong reasoning capabilities in complex tasks. However, they still struggle with hallucinations and factual errors in knowledge-intensive scenarios like knowledge graph question answering (KGQA). We attribute this to the semantic gap between structured knowledge graphs (KGs) and unstructured queries, caused by inherent differences in their focuses and structures. Existing methods usually employ resource-intensive, non-scalable workflows reasoning on vanilla KGs, but overlook this gap. To address this challenge, we propose a flexible framework, Enrich-on-Graph (EoG), which leverages LLMs' prior knowledge to enrich KGs, bridge the semantic gap between graphs and queries. EoG enables efficient evidence extraction from KGs for precise and robust reasoning, while ensuring low computational costs, scalability, and adaptability across different methods. Furthermore, we propose three graph quality evaluation metrics to analyze query-graph alignment in KGQA task, supported by theoretical validation of our optimization objectives. Extensive experiments on two KGQA benchmark datasets indicate that EoG can effectively generate high-quality KGs and achieve the state-of-the-art performance. Our code and data are available at https://github.com/zjukg/Enrich-on-Graph.

**Innovation pattern:** Gap-Driven Reframing (confidence: high)

Secondary patterns: Representation Shift & Primitive Recasting

*Reasoning:* Identifies a concrete empirical gap (noisy KGs, costly workflows) and reframes the task by creating aligned, enriched query-graphs for LLM reasoning; also shifts input representation into unified LLM-friendly query graphs.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**KG-BERT: BERT for Knowledge Graph Completion** (2019) [[arXiv](https://arxiv.org/abs/1909.03193)]
- *Authors:* Liang Yao et al.
- *Direct Connection:* KG-BERT provided a pretrained discriminative scoring model for triple semantic plausibility, which EoG adopts as the concrete semantic-scoring component (KGC) for its Semantic Richness metric and theoretical connections to the MI objective.

### 🏷️ Inspiration

**KG-CoT: Chain-of-Thought Prompting of Large Language Models over Knowledge Graphs for Knowledge-aware Question Answering** (2024)
- *Authors:* Ruilin Zhao et al.
- *Direct Connection:* KG-CoT demonstrated that chain-of-thought-style prompting over KG-derived evidence improves faithfulness of LLM answers, motivating EoG's use of enriched, higher-quality subgraphs as the external evidence fed to LLMs to reduce hallucinations.

**StructGPT: A General Framework for Large Language Model to Reason over Structured Data** (2023) [[arXiv](https://arxiv.org/abs/2305.09645)]
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* StructGPT proposed unifying heterogeneous data formats into LLM-consumable forms for collaborative reasoning, directly inspiring EoG's parsing stage that converts both natural-language queries and KG triples into a common query format for alignment.

### 🏷️ Gap Identification

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph** (2023) [[arXiv](https://arxiv.org/abs/2307.07697)]
- *Authors:* Jiashuo Sun et al.
- *Direct Connection:* ToG framed iterative LLM-driven exploration over KG entities and relations to support multi-step reasoning but exposed the inefficiency and scalability limitations of reasoning directly over vanilla KGs, a gap EoG addresses by enriching and aligning graphs before reasoning.

**Debate on Graph: A Flexible and Reliable Reasoning Framework for Large Language Models** (2025)
- *Authors:* Jie Ma et al.
- *Direct Connection:* DoG proposed an iterative, multi-stage debate/simplification workflow for KG reasoning that demonstrates strong correctness but highlighted a bulky, resource-intensive pipeline—precisely the complexity and cost EoG reduces by shifting effort to query-aligned graph enrichment.

### 🏷️ Baseline

**Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning** (2024)
- *Authors:* Linhao Luo et al.
- *Direct Connection:* RoG introduced query-driven relational path planning that extracts relation-path subgraphs via fine-tuned LLMs and served as a primary state-of-the-art baseline whose costly fine-tuning and KG-specific path planning EoG directly aims to replace with LLM-based graph enrichment and a lightweight alignment pipeline.

### 🏷️ Extension

**QA-GNN: Reasoning with Language Models and Knowledge Graphs for Question Answering** (2021)
- *Authors:* Yasunaga et al.
- *Direct Connection:* QA-GNN showed the utility of extracting and pruning subgraphs for focused multi-hop reasoning, and EoG directly extends this pruning idea into a focus-aware multi-channel pruning scheme that combines global and local query signals.

---

## Synthesis: How Prior Work Led to This Paper

RoG, ToG and DoG demonstrated that extracting relation-paths or iteratively exploring KGs with LLMs yields strong KGQA performance but also exposed two core limitations—heavy fine-tuning or iterative workflows and poor scalability when reasoning directly over noisy vanilla KGs. KG-CoT validated that supplying KGs-orchestrated chain-of-thought evidence improves faithfulness, highlighting the value of higher-quality subgraphs as external evidence. QA-GNN operationalized focused subgraph extraction and pruning for multi-hop QA, providing concrete techniques for removing irrelevant KG portions. StructGPT showed that converting heterogeneous structured inputs into a unified, LLM-friendly query representation enables stronger alignment between models and data formats, which directly informs EoG’s parsing stage. Finally, KG-BERT supplied a concrete semantic scoring mechanism suitable for quantifying triple plausibility and thereby underpins EoG’s Semantic Richness metric and its theoretical ties to mutual information. Taken together, these works reveal an opportunity: instead of expensive iterative reasoning pipelines or costly LLM fine-tuning on KG-specific tasks, one can (1) parse queries and triples into a common format, (2) apply focused pruning inspired by QA-GNN, and (3) use LLM priors plus KG-BERT-style scoring to enrich graph structure and hierarchies so that downstream LLM reasoning is simpler, cheaper, and more faithful—precisely the intellectual pathway EoG follows.

---

*Analysis generated on: 2026-03-09T00:12:09.539819*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=17062, output=1242*
