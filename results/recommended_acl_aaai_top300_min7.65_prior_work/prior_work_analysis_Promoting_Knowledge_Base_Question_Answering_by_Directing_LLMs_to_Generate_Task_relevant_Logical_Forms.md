# Prior Work Analysis Report

## Target Paper

**Title:** Promoting Knowledge Base Question Answering by Directing LLMs to Generate Task-relevant Logical Forms

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Knowledge base question answering (KBQA) refers to the system that produces answers to user queries by reasoning with a large-scale structured knowledge base. Advanced works have achieved great success either by generating logical forms (LF) or directly generating answers. Although the former typically yields better performance, these generated LF could be inaccurate, e.g., non-executable. In this regard, large language models (LLMs) have shown exciting potential for accurate generation. However, it is challenging to fine-tune LLMs to generate LF. This is because the context retrieved for prediction typically leads to an excessive number of reasoning paths. In this context, LLMs can generate numerous LF corresponding to these reasoning paths, but a few LF can result in correct answers. Thus, fine-tuning LLMs to generate answer-relevant LF would conflict with the prior knowledge of the LLMs. In this work, we propose a novel learning framework, FM-KBQA, to fine-tune LLMs using multi-task learning for KBQA. Specifically, we propose to fine-tune LLMs using an additional objective: generating the index of reasoning paths that lead to correct answers. This will direct LLMs to pay attention to answer-relevant paths among numerous reasoning paths by completing a simple task where the selected reasoning paths can be supplementary for non-executable LF. Directly generating answers can make LLMs pay attention to the answer-relevant reasoning paths, but it is much more challenging than generating the index of reasoning paths. To verify FM-KBQA's effectiveness, we conduct experiments on mainstream benchmarks, such as WebQuestionsSP (WQSP) and ComplexWebQuestions (CWQ). Extensive evaluations across two public benchmark datasets underscore the superiority of FM-KBQA over current state-of-the-art methods.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**PullNet: Open domain question answering with iterative retrieval on knowledge bases and text** (2019) [[arXiv](https://arxiv.org/abs/1904.09537)]
- *Authors:* Sun et al.
- *Direct Connection:* PullNet lays the foundation for leveraging iterative retrieval in KBQA, which is essential for understanding the importance of reasoning paths when generating logical forms in the current framework.

### 🏷️ Inspiration

**ReTraCk: A flexible and efficient framework for knowledge base question answering** (2021) [[arXiv](https://arxiv.org/abs/2104.08762)]
- *Authors:* Chen et al.
- *Direct Connection:* ReTraCk emphasizes the importance of semantic checkers in generating accurate logical forms, which inspires the current study's approach to fine-tuning LLMs with a focus on answer relevancy.

### 🏷️ Gap Identification

**Decaf: Joint decoding of answers and logical forms for question answering over knowledge bases** (2022) [[arXiv](https://arxiv.org/abs/2210.00063)]
- *Authors:* Yu et al.
- *Direct Connection:* The work highlights the challenges of generating joint answers and logical forms, which this paper addresses by proposing a framework that allows LLMs to focus on answer-relevant reasoning paths, thus mitigating issues with non-executable logical forms.

**Think-on-graph: Deep and responsible reasoning of large language model with knowledge graph** (2023) [[arXiv](https://arxiv.org/abs/2307.07697)]
- *Authors:* Sun et al.
- *Direct Connection:* This paper addresses reasoning on knowledge graphs but does not provide efficient means for focusing on specific reasoning paths, which the current work aims to improve by directing LLMs to generate relevant logical forms.

### 🏷️ Baseline

**ChatKBQA: A Generate-then-Retrieve Framework for Knowledge Base Question Answering with Fine-tuned Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2310.08975)]
- *Authors:* Luo et al.
- *Direct Connection:* This paper presents a generate-then-retrieve framework for KBQA that the current work improves upon by adding an additional multi-task learning objective to better focus on the correct reasoning paths.

### 🏷️ Extension

**UniKGQA: Unified retrieval and reasoning for solving multi-hop question answering over knowledge graph** (2022) [[arXiv](https://arxiv.org/abs/2212.00959)]
- *Authors:* Jiang et al.
- *Direct Connection:* UniKGQA introduces a unified architecture that combines retrieval and reasoning strategies, which this paper extends by implementing a focused objective directing LLMs towards generating executable logical forms.

### 🏷️ Related Problem

**Reasoning on graphs: Faithful and interpretable large language model reasoning** (2023) [[arXiv](https://arxiv.org/abs/2310.01061)]
- *Authors:* Luo et al.
- *Direct Connection:* This paper explores reasoning with graphs in LLMs, which informs the current approach that enhances reasoning accuracy by guiding LLMs to focus on answer-relevant reasoning paths.

---

## Synthesis: How Prior Work Led to This Paper

The research landscape preceding this paper includes significant contributions to the realm of knowledge base question answering (KBQA), notably works like Decaf, which highlight the challenges around generating coherent answers alongside logical forms, setting the stage for the current work's dual-focus enhancement. ReTraCk elucidates the necessity for semantic consistency in generated logical forms, underscoring the need for frameworks that ensure the asker's query aligns with the generated result; this influenced the methodology currently adopted for leveraging multi-task learning in LLM fine-tuning. Furthermore, ChatKBQA's generate-then-retrieve paradigm provides a baseline that this work seeks to enhance, directing LLMs more effectively towards correct reasoning paths. The emphasis on KA queries and the inherent reasoning nature of knowledge graphs explored in Think-on-graph casts light on the limitations faced when reasoning with excessive non-relevant paths, which this research addresses by refining the focus. The integration of Unikgqa's unified framework informs the efficiency maximization within retrieval and reasoning that the current multi-task learning strategy aims for. Collectively, these papers illuminate gaps and establish a foundational narrative which the current paper adeptly builds upon, leading to a nuanced and innovative contribution in KBQA.

---

*Analysis generated on: 2026-04-04T23:21:53.291145*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
