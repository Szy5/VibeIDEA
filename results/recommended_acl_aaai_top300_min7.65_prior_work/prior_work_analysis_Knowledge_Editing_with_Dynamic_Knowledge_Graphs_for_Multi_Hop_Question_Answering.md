# Prior Work Analysis Report

## Target Paper

**Title:** Knowledge Editing with Dynamic Knowledge Graphs for Multi-Hop Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Multi-hop question answering (MHQA) poses a significant challenge for large language models (LLMs) due to the extensive knowledge demands involved. Knowledge editing, which aims to precisely modify the LLMs to incorporate specific knowledge without negatively impacting other unrelated knowledge, offers a potential solution for addressing MHQA challenges with LLMs. However, current solutions struggle to effectively resolve issues of knowledge conflicts. Most parameter-preserving editing methods are hindered by inaccurate retrieval and overlook secondary editing issues, which can introduce noise into the reasoning process of LLMs. In this paper, we introduce KEDKG, a novel knowledge editing method that leverages a dynamic knowledge graph for MHQA, designed to ensure the reliability of answers. KEDKG involves two primary steps: dynamic knowledge graph construction and knowledge graph augmented generation. Initially, KEDKG autonomously constructs a dynamic knowledge graph to store revised information while resolving potential knowledge conflicts. Subsequently, it employs a fine-grained retrieval strategy coupled with an entity and relation detector to enhance the accuracy of graph retrieval for LLM generation. Experimental results on benchmarks show that KEDKG surpasses previous state-of-the-art models, delivering more accurate and reliable answers in environments with dynamic information.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Inspiration

**Can We Edit Factual Knowledge by In-Context Learning?** (2023) [[arXiv](https://arxiv.org/abs/2309.00144)]
- *Authors:* Zheng et al.
- *Direct Connection:* This paper's exploration of knowledge incorporation through in-context learning serves as inspiration for KEDKG's structured approach using dynamic knowledge graphs to enhance multi-hop reasoning.

### 🏷️ Gap Identification

**Editing Factual Knowledge in Language Models** (2021) [[arXiv](https://arxiv.org/abs/2110.00702)]
- *Authors:* De Cao et al.
- *Direct Connection:* This work highlights issues like catastrophic forgetting related to factual edits, which KEDKG addresses by ensuring that knowledge updates do not interfere with previously stored information.

**Mass-Editing Memory in a Transformer** (2023) [[arXiv](https://arxiv.org/abs/2302.05078)]
- *Authors:* Meng et al.
- *Direct Connection:* KEDKG specifically responds to the limitations of mass editing in knowledge incorporation by innovating a dynamic approach to conflict resolution in stored knowledge.

### 🏷️ Baseline

**PokeMQA: Programmable knowledge editing for Multi-hop Question Answering** (2024) [[arXiv](https://arxiv.org/abs/22404.00492)]
- *Authors:* Gu et al.
- *Direct Connection:* KEDKG improves upon PokeMQA by constructing a dynamic knowledge graph to handle knowledge edits more effectively, addressing the limitations of retrieval accuracy in multi-hop question answering.

**MeLLo: Multi-hop Knowledge Editing for Language Models** (2023) [[arXiv](https://arxiv.org/abs/2310.00782)]
- *Authors:* Zhong et al.
- *Direct Connection:* KEDKG builds upon the MeLLo framework by integrating a dynamic knowledge graph that allows for enhanced retrieval practices, specific to handling conflicts that arise during editing.

### 🏷️ Extension

**Locating and editing factual associations in GPT** (2022) [[arXiv](https://arxiv.org/abs/2204.07865)]
- *Authors:* Meng et al.
- *Direct Connection:* KEDKG extends the concept of targeted editing from this work by implementing a comprehensive dynamic knowledge graph that efficiently manages edits and secondary conflicts.

---

## Synthesis: How Prior Work Led to This Paper

Prior works such as PokeMQA and MeLLo set foundational approaches for knowledge editing in multi-hop question answering, but KEDKG significantly enhances these frameworks by implementing dynamic knowledge graphs that adaptively resolve conflicts arising from sequential edits. Additionally, the limitations highlighted by De Cao et al. regarding catastrophic forgetting and by Meng et al. related to mass editing inspire KEDKG's design choice of ensuring coherence and reliability in knowledge updates. Furthermore, the method of locating and editing factual associations detailed by Meng et al. reflects the need for a systematic approach to dynamic edits, which KEDKG successfully addresses. The insights gained from Zheng et al. regarding in-context learning influence KEDKG's architecture, enabling it to facilitate more sophisticated reasoning processes within large language models. Collectively, these works reveal a landscape of challenges and opportunities that KEDKG effectively navigates, illustrating a clear progression towards a more reliable and accurate MHQA capability.

---

*Analysis generated on: 2026-04-04T23:22:00.497661*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
