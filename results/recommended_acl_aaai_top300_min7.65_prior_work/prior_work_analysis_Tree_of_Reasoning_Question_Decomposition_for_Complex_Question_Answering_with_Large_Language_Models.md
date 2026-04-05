# Prior Work Analysis Report

## Target Paper

**Title:** Tree-of-Reasoning Question Decomposition for Complex Question Answering with Large Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) have recently demonstrated remarkable performance across various Natual Language Processing tasks. In the field of multi-hop reasoning, the Chain-of-thought (CoT) prompt method has emerged as a paradigm, using curated stepwise reasoning demonstrations to enhance LLM's ability to reason and produce coherent rational pathways. To ensure the accuracy, reliability, and traceability of the generated answers, many studies have incorporated information retrieval (IR) to provide LLMs with external knowledge. However, existing CoT with IR methods decomposes questions into sub-questions based on a single compositionality type, which limits their effectiveness for questions involving multiple compositionality types. Additionally, these methods suffer from inefficient retrieval, as complex questions often contain abundant information, leading to the retrieval of irrelevant information inconsistent with the query's intent. In this work, we propose a novel question decomposition framework called TRQA for multi-hop question answering, which addresses these limitations. Our framework introduces a reasoning tree (RT) to represent the structure of complex questions. It consists of four components: the Reasoning Tree Constructor (RTC), the Question Generator (QG), the Retrieval and LLM Interaction Module (RAIL), and the Answer Aggregation Module (AAM). Specifically, the RTC predicts diverse sub-question structures to construct the reasoning tree, allowing a more comprehensive representation of complex questions. The QG generates sub-questions for leaf-node in the reasoning tree, and we explore two methods for QG: prompt-based and T5-based approaches. The IR module retrieves documents aligned with sub-questions, while the LLM formulates answers based on the retrieved information. Finally, the AAM aggregates answers along the reason tree, producing a definitive response from bottom to top.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Unsupervised Multi-hop Question Answering by Question Generation** (2020) [[arXiv](https://arxiv.org/abs/2010.12623)]
- *Authors:* Liangming Pan et al.
- *Direct Connection:* Pan et al.’s taxonomy of nest-type versus branch-type sub-question relations directly underpins TRQA’s [NEST] and [BRANCH] operators for representing multi-compositional structure in its reasoning tree.

### 🏷️ Inspiration

**Question Decomposition Tree for Answering Complex Questions over Knowledge Bases** (2023) [[arXiv](https://arxiv.org/abs/2306.07597)]
- *Authors:* Xiaofeng Huang et al.
- *Direct Connection:* Huang et al. showed that modeling questions as a decomposition tree improves handling compositionality, which TRQA generalizes by learning a dependency-parse–driven reasoning tree and using it to steer per-node IR and answer aggregation beyond KB-QA.

**EDG-Based Question Decomposition for Complex Question Answering over Knowledge Bases** (2021)
- *Authors:* Xiting Hu et al.
- *Direct Connection:* Hu et al.’s syntax-guided (constituency) decomposition into an entity-centric graph motivated TRQA’s parse-guided approach, which replaces EDG’s hand-crafted rules with a T5 model predicting [NEST]/[BRANCH] over dependency parses to improve coverage.

**Plan-and-Solve Prompting: Improving Zero-shot Chain-of-Thought Reasoning by Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.04091)]
- *Authors:* L. Wang et al.
- *Direct Connection:* Plan-and-Solve’s decoupling of planning from solving directly inspires TRQA’s architecture, where RTC first plans a global tree and QG+RAIL subsequently solve sub-questions along that plan.

**Search-in-the-Chain: Towards the Accurate, Credible and Traceable Content Generation for Complex Knowledge-intensive Tasks** (2023) [[arXiv](https://arxiv.org/abs/2304.14732)]
- *Authors:* Shuai Xu et al.
- *Direct Connection:* Search-in-the-Chain’s interleaving of retrieval with reasoning to enhance credibility and attribution motivates TRQA’s per-node retrieval logging and bottom-up aggregation for traceable, verifiable multi-hop answers.

### 🏷️ Baseline

**Measuring and Narrowing the Compositionality Gap in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2210.03350)]
- *Authors:* Ofir Press et al.
- *Direct Connection:* Self-Ask’s iterative sub-question generation with retrieval is the primary stepwise baseline that TRQA surpasses by replacing the linear sequence with a globally planned reasoning tree that captures both nested and branching dependencies.

**Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP** (2022) [[arXiv](https://arxiv.org/abs/2212.14024)]
- *Authors:* Omar Khattab et al.
- *Direct Connection:* DSP’s tight composition of prompting and search informs TRQA’s Retrieval-and-LLM Interaction, which instead organizes retrieval calls along an explicit reasoning tree to improve accuracy and traceability at each node.

---

## Synthesis: How Prior Work Led to This Paper

Prior work established two crucial ingredients for complex QA. First, Pan et al. formalized compositionality by distinguishing nest-type and branch-type dependencies among sub-questions, highlighting that both must be handled. Second, several lines of research explored structure-aware decomposition: Huang et al. introduced a Question Decomposition Tree for KB-QA, demonstrating that tree representations better capture compositional diversity than linear chains, while Hu et al. showed that syntactic analyses can guide decomposition by transforming parse structures into question segments—though via hand-crafted EDG rules with coverage limits. On the prompting side, Self-Ask operationalized iterative sub-questioning with retrieval, and DSP tightly coupled prompting with search for knowledge-intensive tasks; both improved correctness but remained fundamentally sequential. Plan-and-Solve further separated planning from solving in zero-shot CoT, and Search-in-the-Chain advocated inserting retrieval into the reasoning process to boost accuracy and traceability, yet these methods still organized reasoning as a linear chain. Collectively these works revealed that multi-hop QA needs (i) explicit modeling of both nest and branch compositions, (ii) a global plan rather than purely local step-wise decisions, (iii) parse-informed decomposition to ground structure, and (iv) retrieval intertwined with reasoning for attribution. TRQA synthesizes these insights by learning a dependency-parse–driven reasoning tree that encodes [NEST]/[BRANCH] relations, adopting a plan-then-solve workflow where sub-questions are generated for leaf nodes, retrieval is executed per node to align evidence with intent, and answers are aggregated bottom-up along the tree, thereby addressing linear-chain limitations, reducing irrelevant retrieval, and improving traceability.

---

*Analysis generated on: 2026-04-05T11:39:00.150946*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
