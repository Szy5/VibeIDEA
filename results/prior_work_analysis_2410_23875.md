# Prior Work Analysis Report

## Target Paper

**Title:** Plan-on-Graph: Self-Correcting Adaptive Planning of Large Language Model on Knowledge Graphs

**arXiv ID:** [2410.23875](https://arxiv.org/abs/2410.23875)

**Abstract:** 
> Large Language Models (LLMs) have shown remarkable reasoning capabilities on complex tasks, but they still suffer from out-of-date knowledge, hallucinations, and opaque decision-making. In contrast, Knowledge Graphs (KGs) can provide explicit and editable knowledge for LLMs to alleviate these issues. Existing paradigm of KG-augmented LLM manually predefines the breadth of exploration space and requires flawless navigation in KGs. However, this paradigm cannot adaptively explore reasoning paths in KGs based on the question semantics and self-correct erroneous reasoning paths, resulting in a bottleneck in efficiency and effect. To address these limitations, we propose a novel self-correcting adaptive planning paradigm for KG-augmented LLM named Plan-on-Graph (PoG), which first decomposes the question into several sub-objectives and then repeats the process of adaptively exploring reasoning paths, updating memory, and reflecting on the need to self-correct erroneous reasoning paths until arriving at the answer. Specifically, three important mechanisms of Guidance, Memory, and Reflection are designed to work together, to guarantee the adaptive breadth of self-correcting planning for graph reasoning. Finally, extensive experiments on three real-world datasets demonstrate the effectiveness and efficiency of PoG.

**Innovation pattern:** Gap-Driven Reframing (confidence: high)

Secondary patterns: Representation Shift & Primitive Recasting

*Reasoning:* Identifies a concrete gap in prior LLM-on-graph methods (fixed breadth, unidirectional paths) and reframes the problem toward adaptive planning and self-correction; also shifts path-extension primitives/agent actions, i.e., a representation/primitive recasting.

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022)
- *Authors:* Jason Wei et al.
- *Direct Connection:* Chain‑of‑Thought established the practical technique of prompting LLMs to produce intermediate reasoning steps and decomposition, which PoG leverages to prompt decomposition into sub‑objectives that guide targeted, condition‑aware KG exploration.

### 🏷️ Inspiration

**StructGPT: A General Framework for Large Language Model to Reason over Structured Data** (2023)
- *Authors:* Jinhao Jiang et al.
- *Direct Connection:* StructGPT established the paradigm of using LLMs as controllers to select and extend structured paths (entities/relations) over graphs/tables, which PoG builds on by adding explicit task decomposition, persistent subgraph memory, and reflection-based corrections for adaptive KG navigation.

**Reflexion: Language Agents with Verbal Reinforcement Learning** (2024)
- *Authors:* Noah Shinn et al.
- *Direct Connection:* Reflexion introduced a verbal self‑feedback loop for agents to diagnose and learn from mistakes, a concept PoG adapts into its Reflection mechanism to evaluate sufficiency of retrieved KG evidence and decide when and where to backtrack on reasoning paths.

**Self-Refine: Iterative Refinement with Self-Feedback** (2024)
- *Authors:* Aman Madaan et al.
- *Direct Connection:* Self‑Refine demonstrated iterative LLM-driven refinement of outputs using its own feedback, directly informing PoG’s design of repeated cycles of exploration → memory update → reflection to progressively correct and refine KG-based reasoning.

**Graph of Thoughts: Solving Elaborate Problems with Large Language Models** (2024)
- *Authors:* Maciej Besta et al.
- *Direct Connection:* Graph‑of‑Thought articulated graph‑structured multi‑step planning and non‑linear search for LLMs, motivating PoG’s explicit maintenance of a retrieved subgraph and structured reasoning paths that support branching exploration and corrective backtracking.

### 🏷️ Baseline

**Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph** (2024)
- *Authors:* Jiashuo Sun et al.
- *Direct Connection:* PoG directly addresses ToG’s core limitation of fixed‑breadth, unidirectional KG exploration by replacing that static exploration policy with adaptive breadth selection and a reflection-driven backtracking/self-correction mechanism.

---

## Synthesis: How Prior Work Led to This Paper

Recent work treated LLMs as controllers over structured data and graphs and exposed both the opportunities and shortcomings that PoG addresses. Think‑on‑Graph (ToG) concretely operationalized LLM‑driven KG exploration but relied on a fixed exploration breadth and unidirectional path extension, highlighting the need for adaptive planning and error recovery; StructGPT formalized the idea of using LLMs to select and extend structured paths (entities/relations), supplying the core agent‑on‑structured‑data paradigm that PoG extends. Concurrent advances in LLM self‑correction—Reflexion’s verbal reinforcement loop and Self‑Refine’s iterative self‑feedback—showed how agents can diagnose and refine trajectories, directly inspiring PoG’s Reflection loop that decides when to backtrack and which entities to re‑explore. Chain‑of‑Thought introduced decompositional prompting and intermediate reasoning steps, which PoG adopts as sub‑objective decomposition (Guidance) to focus retrieval; Graph‑of‑Thought framed non‑linear, graph‑structured planning for LLMs and motivates PoG’s explicit subgraph and path memory to support branching and correction. Together these works expose a clear gap: LLM‑driven KG reasoning needed adaptive breadth control, persistent graph memory, and an explicit self‑correction mechanism; PoG synthesizes the decomposition and structured‑data selection paradigm with iterative self‑feedback and graph‑aware memory to realize adaptive, self‑correcting planning over knowledge graphs.

---

*Analysis generated on: 2026-03-08T23:57:59.224971*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=15452, output=1081*
