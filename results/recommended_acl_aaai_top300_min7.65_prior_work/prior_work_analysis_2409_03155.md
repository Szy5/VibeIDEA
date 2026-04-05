# Prior Work Analysis Report

## Target Paper

**Title:** Debate on Graph: a Flexible and Reliable Reasoning Framework for Large Language Models

**arXiv ID:** [2409.03155](https://arxiv.org/abs/2409.03155)

**Abstract:** 
> Large Language Models (LLMs) may suffer from hallucinations in real-world applications due to the lack of relevant knowledge. In contrast, knowledge graphs encompass extensive, multi-relational structures that store a vast array of symbolic facts. Consequently, integrating LLMs with knowledge graphs has been extensively explored, with Knowledge Graph Question Answering (KGQA) serving as a critical touchstone for the integration. This task requires LLMs to answer natural language questions by retrieving relevant triples from knowledge graphs. However, existing methods face two significant challenges: \textit{excessively long reasoning paths distracting from the answer generation}, and \textit{false-positive relations hindering the path refinement}. In this paper, we propose an iterative interactive KGQA framework that leverages the interactive learning capabilities of LLMs to perform reasoning and Debating over Graphs (DoG). Specifically, DoG employs a subgraph-focusing mechanism, allowing LLMs to perform answer trying after each reasoning step, thereby mitigating the impact of lengthy reasoning paths. On the other hand, DoG utilizes a multi-role debate team to gradually simplify complex questions, reducing the influence of false-positive relations. This debate mechanism ensures the reliability of the reasoning process. Experimental results on five public datasets demonstrate the effectiveness and superiority of our architecture. Notably, DoG outperforms the state-of-the-art method ToG by 23.7\% and 9.1\% in accuracy on WebQuestions and GrailQA, respectively. Furthermore, the integration experiments with various LLMs on the mentioned datasets highlight the flexibility of DoG. Code is available at \url{https://github.com/reml-group/DoG}.

**Innovation pattern:** Modular Pipeline Composition (confidence: high)

Secondary patterns: Representation Shift & Primitive Recasting

*Reasoning:* The paper decomposes KGQA into explicit modules/interfaces (retrieval, relation selection, graph retrieval, inference) and builds invoke–reason–generate pipelines, while also relying on linearization/representation of structured data for LLMs.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**StructGPT: A General Framework for Large Language Model to Reason over Structured Data** (2023)
- *Authors:* Jiang et al.
- *Direct Connection:* StructGPT introduced the interface-driven linearization and iterative invoke–reason–generate pattern for LLMs to operate over structured data, providing the interface design and stepwise reasoning template that DoG adopts and extends with subgraph-focused answer-trying.

**UniKGQA: Unified Retrieval and Reasoning for Solving Multi-hop Question Answering Over Knowledge Graph** (2023)
- *Authors:* Jiang et al.
- *Direct Connection:* UniKGQA proposed unified retrieval-plus-propagation mechanisms for multi‑hop KGQA (identifying initial entity then iteratively expanding/re‑scoring paths), which is the iterative inference formulation DoG builds upon and refines with answer-trying and simplification to avoid path drift.

### 🏷️ Inspiration

**KG-GPT: A General Framework for Reasoning on Knowledge Graphs Using Large Language Models** (2023)
- *Authors:* Kim et al.
- *Direct Connection:* KG-GPT formalized the decomposition of KGQA into segmentation, graph retrieval, and inference with LLMs, inspiring DoG’s modular two-interface KG invocation (get_relations, triple_filling) and its emphasis on precise relation selection before expansion.

**Improving factuality and reasoning in language models through multiagent debate** (2023)
- *Authors:* Du et al.
- *Direct Connection:* Du et al. demonstrated that multi‑agent debate improves factuality and reasoning by having agents propose and critique solutions, directly motivating DoG’s use of a multi‑role debate team (expert, critic, linguist) to reliably simplify subquestions and reduce false-positive relation effects.

**ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate** (2023)
- *Authors:* Chan et al.
- *Direct Connection:* ChatEval showed concrete prompting patterns and one-by-one discussion strategies for multi-agent debate to produce higher-quality judgments, which DoG borrows to structure its sequential role interactions and ensure consistency during question simplification.

### 🏷️ Baseline

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph** (2024)
- *Authors:* Sun et al.
- *Direct Connection:* ToG established the recent paradigm of treating an LLM as an interactive agent that performs deep iterative path search and uses retrieved multi-hop evidence to generate answers, and DoG explicitly targets the same KGQA setting while addressing ToG’s problems of overly long evidence chains and false‑positive relation expansion.

---

## Synthesis: How Prior Work Led to This Paper

StructGPT and UniKGQA established the practical interface and iterative retrieval–reasoning formulation for LLMs over structured knowledge: StructGPT supplied the linearization and invoke–reason–generate interface design for applying LLMs to structured data, while UniKGQA formalized the iterative identification of initial entities and propagation-based multi-hop retrieval that underpins KGQA workflows. KG-GPT complemented these by partitioning KGQA into segmentation, graph retrieval, and inference stages and emphasizing accurate relation selection before expansion, which informed DoG’s two explicit KG invocation interfaces (get_relations and triple_filling). Building on that iterative agent-style paradigm, ToG implemented deep agentic reasoning on graphs and used multi-path evidence for final answers, exposing two practical failure modes—long distracting evidence chains and false‑positive relation expansion—that DoG explicitly targets. Parallel lines of work on multi-agent debate and role prompting (e.g., Du et al. and ChatEval) provided the methodological insight that multiple specialized LLM roles plus ordered, critique-based exchanges improve factuality and decision robustness. Together these specific techniques—interface-driven iterative reasoning, modular graph retrieval and relation filtering, and structured multi‑agent debate—revealed a gap: existing agentic KGQA methods aggregate long paths and propagate spurious relations before answering; synthesizing subgraph-focused answer-trying with a sequential multi-role debate for question simplification was therefore a natural next step to reduce path distraction and false-positive propagation and to make stepwise KG reasoning both flexible and reliable.

---

*Analysis generated on: 2026-03-09T00:11:01.438687*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=16129, output=1115*
