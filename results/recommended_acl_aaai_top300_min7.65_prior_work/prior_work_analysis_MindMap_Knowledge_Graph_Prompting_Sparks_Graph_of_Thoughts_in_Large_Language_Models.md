# Prior Work Analysis Report

## Target Paper

**Title:** MindMap: Knowledge Graph Prompting Sparks Graph of Thoughts in Large Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) have achieved remarkable performance in natural language understanding and generation tasks.However, they often suffer from limitations such as difficulty in incorporating new knowledge, generating hallucinations, and explaining their reasoning process.To address these challenges, we propose a novel prompting pipeline, named MindMap, that leverages knowledge graphs (KGs) to enhance LLMs' inference and transparency.Our method enables LLMs to comprehend KG inputs and infer with a combination of implicit and external knowledge.Moreover, our method elicits the mind map of LLMs, which reveals their reasoning pathways based on the ontology of knowledge.We evaluate our method on diverse question & answering tasks, especially in medical domains, and show significant improvements over baselines.We also introduce a new hallucination evaluation benchmark and analyze the effects of different components of our method.Our results demonstrate the effectiveness and robustness of our method in merging knowledge from LLMs and KGs for combined inference.To reproduce our results and extend the framework further, we make our codebase available at https://github.com/wylwilling/MindMap.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**K-BERT: Enabling language representation with knowledge graph** (2020) [[arXiv](https://arxiv.org/abs/N/A)]
- *Authors:* Weijie Liu et al.
- *Direct Connection:* K-BERT introduced the integration of KGs with language models, which provided a foundational understanding for MindMap's advancement of reasoning with graphical inputs.

### 🏷️ Inspiration

**Knowledge-augmented language model prompting for zero-shot knowledge graph question answering** (2023) [[arXiv](https://arxiv.org/abs/2306.04136)]
- *Authors:* Jinheon Baek et al.
- *Direct Connection:* This paper inspired the concept of using KGs to formulate prompts for language models, which served as a key pivot for MindMap's novel prompting technique.

### 🏷️ Gap Identification

**QA-GNN: Reasoning with language models and knowledge graphs for question answering** (2021) [[arXiv](https://arxiv.org/abs/N/A)]
- *Authors:* Michihiro Yasunaga et al.
- *Direct Connection:* This work identified limitations in the combinative reasoning of language models and KGs, which MindMap addresses by proposing a synergistic inference method.

### 🏷️ Baseline

**Retrieval-augmented generation for knowledge-intensive NLP tasks** (2020) [[arXiv](https://arxiv.org/abs/N/A)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* This work laid the foundation for using retrieval-augmented approaches in language models, which MindMap builds upon by integrating knowledge graphs (KGs) for enhanced inference.

### 🏷️ Extension

**GreaseLM: Graph reasoning enhanced language models** (2022) [[arXiv](https://arxiv.org/abs/N/A)]
- *Authors:* Xikun Zhang et al.
- *Direct Connection:* MindMap extends the techniques from GreaseLM by specifically enhancing LLMs’ ability to interact with KGs, thereby improving reasoning capabilities.

### 🏷️ Related Problem

**Exploring the potential of large language models (LLMs) in learning on graphs** (2023) [[arXiv](https://arxiv.org/abs/2307.03393)]
- *Authors:* Zhikai Chen et al.
- *Direct Connection:* This paper explores the intersection of LLMs and graph structures, informing MindMap's approach to engaging LLMs with complex evidence from KGs.

---

## Synthesis: How Prior Work Led to This Paper

Prior works in the area of knowledge graphs and language model integration set important milestones relevant to the innovation of MindMap. For instance, the foundational idea from Lewis et al. (2020) on retrieval-augmented generation inspired the use of external knowledge to enhance language model performance. Building on this, Baek et al. (2023) demonstrated the effectiveness of prompting LLMs using KGs for question answering, which motivated the specific prompting enhancements in MindMap. The introduction of K-BERT by Liu et al. (2020) provided critical insights into the language representation improvements achieved when integrating KGs, which MindMap extends through a more sophisticated reasoning framework. Yasunaga et al. (2021) pinpointed key limitations in existing models’ reasoning capabilities with KGs, opening a pathway that MindMap effectively navigates by introducing synergistic inference techniques. Furthermore, the exploration of LLMs in graph contexts by Chen et al. (2023) showcases the potential for LLMs to tackle complex queries by synthesizing information from diverse graph structures. Collectively, these works highlight a natural progression towards MindMap's innovative integration of KGs with LLMs, addressing existing gaps and enhancing the reasoning process.

---

*Analysis generated on: 2026-04-04T23:22:05.396094*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
