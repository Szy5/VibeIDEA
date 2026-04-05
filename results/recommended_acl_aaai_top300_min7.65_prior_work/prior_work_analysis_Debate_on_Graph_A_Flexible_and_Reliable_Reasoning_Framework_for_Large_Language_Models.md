# Prior Work Analysis Report

## Target Paper

**Title:** Debate on Graph: A Flexible and Reliable Reasoning Framework for Large Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLMs) may suffer from hallucinations in real-world applications due to the lack of relevant knowledge. In contrast, knowledge graphs encompass extensive, multi-relational structures that store a vast array of symbolic facts. Consequently, integrating LLMs with knowledge graphs has been extensively explored, with Knowledge Graph Question Answering (KGQA) serving as a critical touchstone for the integration. This task requires LLMs to answer natural language questions by retrieving relevant triples from knowledge graphs. However, existing methods face two significant challenges: *excessively long reasoning paths distracting from the answer generation*, and *false-positive relations hindering the path refinement*. In this paper, we propose an iterative interactive KGQA framework that leverages the interactive learning capabilities of LLMs to perform reasoning and Debating over Graphs (DoG). Specifically, DoG employs a subgraph-focusing mechanism, allowing LLMs to perform answer trying after each reasoning step, thereby mitigating the impact of lengthy reasoning paths. On the other hand, DoG utilizes a multi-role debate team to gradually simplify complex questions, reducing the influence of false-positive relations. This debate mechanism ensures the reliability of the reasoning process. Experimental results on five public datasets demonstrate the effectiveness and superiority of our architecture. Notably, DoG outperforms the state-of-the-art method ToG by 23.7% and 9.1% in accuracy on WebQuestions and GrailQA, respectively. Furthermore, the integration experiments with various LLMs on the mentioned datasets highlight the flexibility of DoG.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**GrailQA: A Human-Composed Benchmark for Generalization in Knowledge Base Question Answering** (2021)
- *Authors:* Gu et al.
- *Direct Connection:* DoG targets the KGQA formulation and compositional generalization challenges crystallized in GrailQA, which motivate mechanisms to control path length and reduce spurious relation matches.

### 🏷️ Inspiration

**ReAct: Synergizing Reasoning and Acting in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2210.03629)]
- *Authors:* Yao et al.
- *Direct Connection:* DoG’s iterative loop that interleaves reasoning with graph actions (expanding/focusing subgraphs) and immediate answer attempts is directly inspired by ReAct’s reasoning–action interleaving framework.

**Least-to-Most Prompting Enables Complex Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2205.10625)]
- *Authors:* Zhou et al.
- *Direct Connection:* DoG’s multi-role team that decomposes and simplifies complex KG questions draws on least-to-most prompting’s principle of breaking problems into incrementally solvable subproblems.

### 🏷️ Baseline

**Think-on-Graph: Deep and Interpretable Graph Reasoning with Large Language Models** (2023)
- *Authors:* Zhang et al.
- *Direct Connection:* DoG directly builds on and addresses Think-on-Graph’s interactive KGQA paradigm, specifically mitigating its tendency to explore overly long, noisy reasoning chains with spurious relations by introducing subgraph focusing and a debate-based pruning mechanism.

### 🏷️ Extension

**Tree of Thoughts: Deliberate Problem Solving with Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.10601)]
- *Authors:* Yao et al.
- *Direct Connection:* DoG adapts Tree-of-Thoughts’ state-space search and intermediate evaluation to graph traversal by letting LLMs try answers after each hop and use debate to assess and prune candidate reasoning branches.

**Multi-Agent Debate Improves Reasoning in Large Language Models** (2023)
- *Authors:* Du et al.
- *Direct Connection:* DoG extends multi-agent debate by assigning specialized roles to critique candidate relations and paths on a KG, using debate outcomes to suppress false-positive relations during reasoning.

### 🏷️ Related Problem

**PullNet: Open Domain Question Answering with Iterative Retrieval on Knowledge Bases and Text** (2019) [[arXiv](https://arxiv.org/abs/1904.09537)]
- *Authors:* Sun et al.
- *Direct Connection:* DoG generalizes PullNet’s iterative subgraph construction idea by making the subgraph expansion LLM-driven and debate-controlled to maintain a focused, high-precision subgraph for reasoning.

---

## Synthesis: How Prior Work Led to This Paper

Think-on-Graph demonstrated that large language models can drive knowledge graph question answering by iteratively exploring paths on a KG, but its expansive path-growth strategy often yields long, noisy chains with spurious relations that obscure the answer. Tree of Thoughts introduced deliberate state-space search with intermediate evaluations, showing that reasoning paths can be generated and pruned as a structured search process rather than a single linear chain. ReAct showed that interleaving “thinking” steps with “acting” steps—tool calls or environment interactions—improves reliability by grounding intermediate reasoning in actions and immediate feedback. Least-to-most prompting provided a principled way to convert complex queries into manageable subproblems solved in sequence, reducing reasoning burden and error propagation. Multi-agent debate demonstrated that coordinating multiple LLM roles to critique and defend solutions can improve factuality and robustness by surfacing and resolving contradictions. From the KGQA side, PullNet highlighted that iterative subgraph construction and focusing can keep reasoning localized to relevant graph regions, limiting noise. GrailQA formalized a KGQA setting with compositional generalization that stresses multi-hop reasoning while penalizing reliance on superficial cues. Together, these works reveal a gap: interactive KG reasoning needs both principled search control and robust error-checking to avoid long, spurious paths. The natural next step is to merge deliberate search and action loops with debate-driven adjudication, applied to iterative subgraph focusing. By letting agents decompose questions, expand and prune subgraphs, and attempt answers at each hop while debating relation plausibility, the approach directly addresses path-length distraction and false-positive relations in KGQA.

---

*Analysis generated on: 2026-04-04T22:35:43.126426*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
