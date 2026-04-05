# Prior Work Analysis Report

## Target Paper

**Title:** BELLE: A Bi-Level Multi-Agent Reasoning Framework for Multi-Hop Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Multi-hop question answering (QA) involves finding multiple relevant passages and performing step-by-step reasoning to answer complex questions.Previous works on multi-hop QA employ specific methods from different modeling perspectives based on large language models (LLMs), regardless of question types.In this paper, we first conduct an in-depth analysis of public multi-hop QA benchmarks, categorizing questions into four types and evaluating five types of cutting-edge methods: Chainof-Thought (CoT), Single-step, Iterative-step, Sub-step, and Adaptive-step.We find that different types of multi-hop questions exhibit varying degrees of sensitivity to different types of methods.Thus, we propose a Bi-levEL muLti-agEnt reasoning (BELLE) framework to address multi-hop QA by specifically focusing on the correspondence between question types and methods, with each type of method regarded as an "operator" by prompting LLMs differently.The first level of BELLE includes multiple agents that debate to formulate an executable plan of combined "operators" to address the multi-hop QA task comprehensively.During the debate, in addition to the basic roles of affirmative debater, negative debater, and judge, at the second level, we further leverage fast and slow debaters to monitor whether changes in viewpoints are reasonable.Extensive experiments demonstrate that BELLE significantly outperforms strong baselines in various datasets.Additionally, the model consumption of BELLE is higher cost-effectiveness than that of single models in more complex multihop QA scenarios.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This work provides the step-by-step reasoning paradigm that BELLE treats as a closed-book “operator” and selects when external retrieval is unnecessary.

**Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions** (2023) [[arXiv](https://arxiv.org/abs/2305.12117)]
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* It introduces the iterative retrieval–reasoning procedure that BELLE directly invokes as its iterative-step operator for complex inference questions.

**Successive Prompting for Decomposing Complex Questions** (2022)
- *Authors:* Dheeru Dua et al.
- *Direct Connection:* This paper establishes the sub-question decomposition strategy that BELLE uses as its sub-step operator to break multi-hop questions into solvable parts.

**MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries** (2024) [[arXiv](https://arxiv.org/abs/2401.15391)]
- *Authors:* Yixuan Tang and Yi Yang
- *Direct Connection:* It defines the four-way question-type taxonomy (Inference, Comparison, Temporal, Null) that BELLE adopts to condition planning and operator selection.

**Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate** (2024)
- *Authors:* Tian Liang et al.
- *Direct Connection:* This work provides the basic affirmative/negative/judge debate setup upon which BELLE builds its planning procedure for selecting operators.

### 🏷️ Inspiration

**Agents Thinking Fast and Slow: A Talker-Reasoner Architecture** (2024) [[arXiv](https://arxiv.org/abs/2410.08328)]
- *Authors:* Konstantina Christakopoulou et al.
- *Direct Connection:* The fast/slow separation of reasoning directly inspires BELLE’s fast and slow debater roles that evaluate current operator choices and integrate historical debate summaries.

### 🏷️ Gap Identification

**Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity** (2024)
- *Authors:* Soyeong Jeong et al.
- *Direct Connection:* Adaptive-RAG’s classifier adapts retrieval depth within a single pipeline, highlighting the limitation that BELLE addresses by routing and composing across multiple operator families based on question types.

---

## Synthesis: How Prior Work Led to This Paper

Step-by-step prompting demonstrated that large language models can carry out explicit reasoning chains, establishing a closed-book operator that answers many questions without retrieval. For knowledge-intensive multi-step tasks, interleaving retrieval with chain-of-thought showed how iterative retrieval conditioned on intermediate reasoning improves factual grounding, while successive prompting introduced a practical mechanism to decompose a complex question into sub-questions solvable in stages. Adaptive-RAG advanced the idea of question-contingent reasoning by learning to modulate retrieval effort using a complexity classifier, but its adaptation remains confined to a single retrieval pipeline. In parallel, MultiHop-RAG formalized a four-type taxonomy—Inference, Comparison, Temporal, and Null—revealing that multi-hop questions vary systematically and suggesting that different procedural tools may suit different types. On the control side, multi-agent debate works crystallized an affirmative/negative/judge interaction pattern that can guide decision making, and the talker–reasoner (fast/slow) split illuminated how near-term deliberation can be complemented by slower, memory-based reflection. Collectively, these insights exposed a gap: despite diverse operators and emerging adaptive and debate mechanisms, there was no planner that selects and composes across operator families conditioned on question type and debate history. The natural next step is a planner that first recognizes question type, then uses a structured debate—augmented with fast evaluation and slow memory—to produce an execution plan that composes operators like sub-step decomposition, single- or iterative-step retrieval, and CoT where appropriate, yielding both higher accuracy and better cost-effectiveness for multi-hop QA.

---

*Analysis generated on: 2026-04-05T11:59:15.441642*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
