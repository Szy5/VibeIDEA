# Prior Work Analysis Report

## Target Paper

**Title:** Can We Further Elicit Reasoning in LLMs? Critic-Guided Planning with Retrieval-Augmentation for Solving Challenging Tasks

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models excel at problemsolving but often struggle with complex reasoning and factual accuracy.While chainof-thought and retrieval-augmented generation help break down problems and retrieve knowledge, they still falter on challenging tasks like competitive programming due to frequent reasoning errors and irrelevant retrieval.To address this, we introduce Critic-guided planning with Retrieval-augmentation, CR-Planner, a novel framework that leverages fine-tuned critic models to guide both reasoning and retrieval processes through planning.CR-Planner iteratively selects and executes sub-goals, guided by critic models.A sub-goal critic identifies promising sub-goals from reasoning, query generation, and retrieval, while an execution critic evaluates outputs of sub-goal executions.We employ Monte Carlo Tree Search to collect data for critic training, allowing systematic exploration of action sequences and effective navigation toward the final answer.We evaluate CR-Planner on challenging domain-knowledgeintensive and reasoning-heavy tasks, including competitive programming, theorem-driven math reasoning, and complex domain retrieval problems.It significantly outperforms baselines, demonstrating effectiveness in both reasoning and retrieval.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* Established step-by-step rationale generation (CoT), providing the REASON sub-goal abstraction whose candidates CR-Planner scores and selects with an execution critic.

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2210.03629)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* Introduced interleaving reasoning with tool use/retrieval at each step, forming the blueprint for CR-Planner’s alternating REASON–GENQUERY–RETRIEVE sub-goals.

**Retrieval-Augmented Generation for Knowledge-Intensive NLP** (2020) [[arXiv](https://arxiv.org/abs/arXiv:2005.11401)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* Defined the RAG paradigm and its core subtasks (query generation and document selection) that CR-Planner jointly optimizes via critics rather than tuning each in isolation.

**A Survey of Monte Carlo Tree Search Methods** (2012)
- *Authors:* Cameron Browne et al.
- *Direct Connection:* Provided the MCTS framework that CR-Planner uses to simulate trajectories and backpropagate long-term rewards to construct training data for its critic models.

### 🏷️ Inspiration

**Tree of Thoughts: Deliberate Problem Solving with Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2305.10601)]
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* Proposed planning as search over intermediate thoughts with self-evaluation, directly inspiring CR-Planner’s sub-goal planning and value-based selection across multi-step reasoning paths.

### 🏷️ Gap Identification

**Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection** (2024)
- *Authors:* Akari Asai et al.
- *Direct Connection:* Showed how fine-tuning a base LLM to decide when/how to retrieve with reflection tokens aids simple tasks but requires base-model training and struggles on complex problems—limitations CR-Planner addresses by training external critics and targeting harder domains.

### 🏷️ Extension

**Let’s Verify Step by Step** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2305.20050)]
- *Authors:* Hunter Lightman et al.
- *Direct Connection:* Demonstrated process supervision using a value model to predict future rewards of reasoning steps; CR-Planner extends this by training domain-specific critics as value functions for both reasoning and retrieval to guide planning.

---

## Synthesis: How Prior Work Led to This Paper

Step-by-step rationale prompting established that large language models could be guided through intermediate reasoning, with Chain-of-Thought introducing explicit rationales that shape a natural REASON sub-goal. Tree of Thoughts then moved beyond linear chains by casting problem solving as search over intermediate thoughts with self-evaluation, bringing a planning-centric perspective to multi-step reasoning. In parallel, ReAct interleaved reasoning with tool interactions, showing that query generation and retrieval can be woven into the reasoning loop at each step. Retrieval-Augmented Generation formalized this retrieval–generation paradigm and clarified the subcomponents—query construction and document selection—that must be coordinated for knowledge-intensive tasks. Self-RAG advanced this integration by fine-tuning models to decide when and how to retrieve and to critique their own outputs via reflection tokens, but it remained tied to base-model training and was most effective on simpler multi-hop tasks. Process supervision via a value model, exemplified by Let’s Verify Step by Step, introduced step-level reward estimation to steer reasoning trajectories. Finally, Monte Carlo Tree Search offered a principled way to explore action sequences and propagate simulated long-term rewards, enabling data collection for training value estimators.
Together, these works revealed that effective solutions require planning over both reasoning and retrieval actions, step-level evaluation of intermediate options, and mechanisms to assess long-term impact—not just local improvements to individual subtasks. The convergence of planning (ToT/ReAct), retrieval-aware reasoning (RAG/Self-RAG), and value-based process supervision (RAP), combined with MCTS for trajectory generation, naturally led to a framework that trains small, domain-specific critics as value functions to select sub-goals and executions—yielding a unified, critic-guided planner for complex, knowledge-intensive reasoning.

---

*Analysis generated on: 2026-04-05T11:53:18.722627*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
