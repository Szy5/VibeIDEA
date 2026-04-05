# Prior Work Analysis Report

## Target Paper

**Title:** KG-Agent: An Efficient Autonomous Agent Framework for Complex Reasoning over Knowledge Graph

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> In this paper, we aim to improve the reasoning ability of large language models (LLMs) over knowledge graphs (KGs) to answer complex questions.Inspired by existing methods that design the interaction strategy between LLMs and KG, we propose an autonomous LLM-based agent framework, called KG-Agent, which enables a small LLM to actively make decisions until finishing the reasoning process over KGs.In KG-Agent, we integrate the LLM, multifunctional toolbox, KG-based executor, and knowledge memory, and develop an iteration mechanism that autonomously selects the tool and then updates the memory for reasoning over KG.To guarantee the effectiveness, we leverage program language to formulate the multi-hop reasoning process over the KG and synthesize a code-based instruction dataset to fine-tune the base LLM.Extensive experiments demonstrate that only using 10K samples for tuning LLaMA2-7B can outperform competitive methods using larger LLMs or more data, on both in-domain and out-domain datasets.Our code and data will be publicly released.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**KQA Pro: A Dataset with Explicit Compositional Programs for Complex Question Answering over Knowledge Base** (2022)
- *Authors:* Shulin Cao et al.
- *Direct Connection:* KG-Agent synthesizes its code-based instruction data by converting KQA Pro’s executable compositional programs into stepwise KG tool invocations, directly enabling supervised tuning of the planner.

**Beyond I.I.D.: Three Levels of Generalization for Question Answering on Knowledge Bases (GrailQA)** (2021)
- *Authors:* Yu Gu et al.
- *Direct Connection:* GrailQA provides SPARQL-aligned questions and generalization splits whose logical forms are grounded to query graphs and decomposed into KG tool-call sequences for KG-Agent’s instruction synthesis and evaluation.

### 🏷️ Inspiration

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023) [[arXiv](https://arxiv.org/abs/2210.03629)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* KG-Agent adopts the ReAct-style thought–action iteration by instantiating actions as executable KG tool calls and maintaining a knowledge memory to condition subsequent decisions during multi-step reasoning.

### 🏷️ Gap Identification

**ChatDB: Augmenting LLMs with Databases as their Symbolic Memory** (2023) [[arXiv](https://arxiv.org/abs/2306.03901)]
- *Authors:* Chenxu Hu et al.
- *Direct Connection:* ChatDB showed that memory-augmented autonomous agents can coordinate multi-step decision making but relied on closed-source LLMs and lacked specialized tools for structured KG operations, directly motivating KG-Agent’s small-LLM training and KG-specific toolbox.

**Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning** (2023) [[arXiv](https://arxiv.org/abs/2310.01061)]
- *Authors:* Linhao Luo et al.
- *Direct Connection:* RoG employs pre-defined multi-round LLM–graph protocols for reasoning, whose rigidity and lack of autonomous tool choice highlighted the need for KG-Agent’s planner that adaptively selects operations and updates memory based on intermediate KG states.

### 🏷️ Baseline

**Few-shot In-Context Learning for Knowledge Base Question Answering (KB-BINDER)** (2023)
- *Authors:* Tianle Li et al.
- *Direct Connection:* KB-BINDER’s fixed in-context prompting with closed-source code models for SPARQL generation provides the primary baseline that KG-Agent surpasses by training a small open-source LLM to autonomously invoke KG tools rather than follow a static procedure.

### 🏷️ Extension

**StructGPT: A general framework for large language model to reason over structured data** (2023) [[arXiv](https://arxiv.org/abs/2305.09645)]
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* KG-Agent directly extends StructGPT’s idea of a domain-specific tool interface for structured data by replacing its fixed, human-crafted interaction plan with an autonomous tool-selection and memory-updating loop, and by designing a KG-specific multifunctional toolbox executed by a small open-source LLM.

---

## Synthesis: How Prior Work Led to This Paper

Domain-specific tool interfaces have proven crucial for allowing language models to operate over structured data: StructGPT instantiated this by prompting large models to call tools against structured backends through a fixed, human-crafted interaction plan, achieving strong performance but sacrificing adaptivity and relying on powerful APIs. In parallel, ReAct introduced a general thought–action loop where an LLM interleaves reasoning with tool invocations and tracks state, demonstrating how autonomous tool selection and stateful iteration can solve multi-step tasks. ChatDB brought memory-augmented autonomy to structured querying, showing that persistent symbolic memory helps multi-turn decision making, yet it depended on closed-source LLMs and lacked specialized operators for structured KG reasoning (e.g., relation traversal, set logic, constraints). On graphs, RoG enforced faithful multi-round LLM–graph reasoning but via pre-defined protocols, again limiting flexibility. Meanwhile, KGQA resources such as KQA Pro (with explicit compositional programs) and GrailQA (with executable SPARQL and generalization splits) provided executable logical forms that can be grounded to query graphs and decomposed into stepwise operations.
Taken together, these works revealed an opportunity: combine ReAct-like autonomous decision making and memory with a KG-specialized toolset, and train a smaller open-source LLM using supervision derived from executable KG programs. By converting the programs from KQA Pro and GrailQA into sequences of concrete tool calls, a planner can be instruction-tuned to select tools and arguments while a knowledge memory carries forward intermediate KG context. This synthesis naturally replaces rigid, pre-defined protocols (StructGPT, RoG, KB-BINDER) and avoids reliance on closed APIs (ChatDB), enabling efficient, general multi-hop KG reasoning with a compact model.

---

*Analysis generated on: 2026-04-04T22:26:55.168584*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
