# Prior Work Analysis Report

## Target Paper

**Title:** Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning

**arXiv ID:** [2310.01061](https://arxiv.org/abs/2310.01061)

**Abstract:** 
> Large language models (LLMs) have demonstrated impressive reasoning abilities in complex tasks. However, they lack up-to-date knowledge and experience hallucinations during reasoning, which can lead to incorrect reasoning processes and diminish their performance and trustworthiness. Knowledge graphs (KGs), which capture vast amounts of facts in a structured format, offer a reliable source of knowledge for reasoning. Nevertheless, existing KG-based LLM reasoning methods only treat KGs as factual knowledge bases and overlook the importance of their structural information for reasoning. In this paper, we propose a novel method called reasoning on graphs (RoG) that synergizes LLMs with KGs to enable faithful and interpretable reasoning. Specifically, we present a planning-retrieval-reasoning framework, where RoG first generates relation paths grounded by KGs as faithful plans. These plans are then used to retrieve valid reasoning paths from the KGs for LLMs to conduct faithful reasoning. Furthermore, RoG not only distills knowledge from KGs to improve the reasoning ability of LLMs through training but also allows seamless integration with any arbitrary LLMs during inference. Extensive experiments on two benchmark KGQA datasets demonstrate that RoG achieves state-of-the-art performance on KG reasoning tasks and generates faithful and interpretable reasoning results.

**Innovation pattern:** Modular Pipeline Composition (confidence: high)

Secondary patterns: Representation Shift & Primitive Recasting, Cross-Domain Synthesis

*Reasoning:* Designs a separate planning module + FiD-style fusion of retrieved reasoning-paths (modular pipeline), while recasting primitives as relation-path plans and combining LLM planning with KG retrieval.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Inspiration

**Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by large language models** (2023) [[arXiv](https://arxiv.org/abs/2305.04091)]
- *Authors:* Keheng Wang et al.
- *Direct Connection:* Introduced the plan-and-solve paradigm of prompting LLMs to first generate a plan and then execute stepwise reasoning, directly inspiring RoG's use of an explicit planning stage (relation-path plans) before retrieval and reasoning.

**Subgraph retrieval enhanced model for multi-hop knowledge base question answering** (2022)
- *Authors:* Jing Zhang et al.
- *Direct Connection:* Demonstrated the value of relation-path based retrieval and subgraph/shortest-path supervision for multi-hop KGQA, motivating RoG to use relation paths (shortest-paths) as supervision and retrieval guides for faithful planning.

**Knowledge-driven CoT: Exploring faithful reasoning in LLMs for knowledge-intensive question answering** (2023) [[arXiv](https://arxiv.org/abs/2308.13259)]
- *Authors:* Keheng Wang et al.
- *Direct Connection:* Showed that retrieving and integrating external KG knowledge can produce more faithful chain-of-thoughts, directly motivating RoG's objective of distilling KG-structured knowledge into LLM planning and using KG retrieval to reduce hallucination.

### 🏷️ Baseline

**Unikgqa: Unified retrieval and reasoning for solving multi-hop question answering over knowledge graph** (2022)
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* Unified graph retrieval and LLM-based reasoning as a single system for KGQA and serves as a primary state-of-the-art baseline that RoG improves upon by explicitly exploiting relation-path structure as faithful plans.

**DECAF: Joint decoding of answers and logical forms for question answering over knowledge bases** (2022)
- *Authors:* Donghan Yu et al.
- *Direct Connection:* Combined semantic parsing and LLM reasoning to produce executable queries and answers, representing the competing paradigm (semantic parsing + LLM) whose limitations (non-executable queries / faithfulness) RoG targets with relation-path grounded plans.

### 🏷️ Extension

**Leveraging passage retrieval with generative models for open domain question answering (Fusion-in-Decoder)** (2021)
- *Authors:* Gautier Izacard et al.
- *Direct Connection:* Presented the FiD retrieval-into-generator architecture for fusing multiple retrieved passages into a generative model, which RoG directly adopts and extends as its retrieval–reasoning module to aggregate multiple KG reasoning-paths for answer generation.

---

## Synthesis: How Prior Work Led to This Paper

Recent advances established two complementary technical threads relevant to RoG: explicit planning prompts for LLMs and retrieval-augmented generation. The plan-and-solve work provided the concrete paradigm of eliciting a plan from an LLM before execution, which directly motivated designing a separate planning module that outputs relation-path plans. On the retrieval side, Izacard & Grave’s Fusion-in-Decoder concretely showed how multiple retrieved contexts can be fused by a generator, and RoG re-purposes this FiD-style fusion to aggregate multiple reasoning-path instances retrieved from a KG. Prior KGQA systems—UniKGQA and DECAF—demonstrated strong unified retrieval/reasoning and joint logical-form/answer decoding baselines but also revealed limitations (treating KGs mainly as flat facts or producing non-executable queries). Work on subgraph/relation-path retrieval (Zhang et al., 2022) established shortest-path/relation-path supervision as an effective signal for multi-hop KGQA, which RoG leverages as ground-truth plans; and knowledge-driven CoT methods showed that injecting KG evidence into reasoning reduces hallucination, guiding RoG’s decision to distill KG structure into planning and to retrieve KG paths during inference. Together, these threads exposed a natural gap: combine plan-based LLM prompting with relation-path–grounded retrieval and FiD-style fusion so plans are both faithful and interpretable; RoG synthesizes these precise elements by training LLMs to produce KG-grounded relation-path plans, retrieving matching graph paths, and reasoning with a FiD-inspired fusion to yield faithful, interpretable KGQA.

---

*Analysis generated on: 2026-03-09T00:08:19.500407*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=16263, output=1128*
