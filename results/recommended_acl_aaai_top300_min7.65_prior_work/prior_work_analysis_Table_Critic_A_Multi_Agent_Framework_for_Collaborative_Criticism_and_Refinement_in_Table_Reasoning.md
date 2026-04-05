# Prior Work Analysis Report

## Target Paper

**Title:** Table-Critic: A Multi-Agent Framework for Collaborative Criticism and Refinement in Table Reasoning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Despite the remarkable capabilities of large language models (LLMs) in various reasoning tasks, they still struggle with table reasoning tasks, particularly in maintaining consistency throughout multi-step reasoning processes.While existing approaches have explored various decomposition strategies, they often lack effective mechanisms to identify and correct errors in intermediate reasoning steps, leading to cascading error propagation.To address these issues, we propose Table-Critic, a novel multi-agent framework that facilitates collaborative criticism and iterative refinement of the reasoning process until convergence to correct solutions.Our framework consists of four specialized agents: a Judge for error identification, a Critic for comprehensive critiques, a Refiner for process improvement, and a Curator for pattern distillation.To effectively deal with diverse and unpredictable error types, we introduce a self-evolving template tree that systematically accumulates critique knowledge through experience-driven learning and guides future reflections.Extensive experiments have demonstrated that Table-Critic achieves substantial improvements over existing methods, achieving superior accuracy and error correction rates while maintaining computational efficiency and lower solution degradation rate.The code is available at https: //github.com/Peiying-Yu/Table-Critic.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Compositional semantic parsing on semi-structured tables** (2015) [[arXiv](https://arxiv.org/abs/1508.00305)]
- *Authors:* Panupong Pasupat and Percy Liang
- *Direct Connection:* WikiTableQuestions defines the compositional table reasoning setting and evaluation protocol that Table-Critic targets with iterative critique and refinement.

**TabFact: A large-scale dataset for table-based fact verification** (2020)
- *Authors:* Wenhu Chen et al.
- *Direct Connection:* TabFact provides the table-based fact verification formulation used to test whether critique patterns generalize across verification-style reasoning.

### 🏷️ Inspiration

**Self-Refine: Iterative refinement with self-feedback** (2023)
- *Authors:* Aman Madaan et al.
- *Direct Connection:* Table-Critic’s multi-turn refinement loop is inspired by Self-Refine’s iterative self-feedback paradigm, but operationalizes it with structured roles and template-guided critiques for more reliable corrections.

### 🏷️ Gap Identification

**Large language models are versatile decomposers: Decomposing evidence and questions for table-based reasoning** (2023)
- *Authors:* Yunhu Ye et al.
- *Direct Connection:* Dater’s sub-table decomposition improves table reasoning but lacks mechanisms to detect and fix intermediate-step errors, a gap Table-Critic explicitly fills with targeted criticism and revision between steps.

**Binding language models in symbolic languages** (2022) [[arXiv](https://arxiv.org/abs/2210.02875)]
- *Authors:* Zhoujun Cheng et al.
- *Direct Connection:* Binder decomposes questions into executable programs but provides no systematic critique of intermediate reasoning, motivating Table-Critic’s design to identify first-step errors and prevent cascading failures.

### 🏷️ Baseline

**Chain-of-Table: Evolving tables in the reasoning chain for table understanding** (2024)
- *Authors:* Zilong Wang et al.
- *Direct Connection:* Table-Critic builds directly on Chain-of-Table to produce initial evolving sub-table reasoning chains and explicitly addresses its core limitation—no mechanism to critique and repair intermediate steps—by layering agent-guided criticism and refinement on top.

### 🏷️ Extension

**Critic-CoT: Boosting the reasoning abilities of large language model via chain-of-thoughts critic** (2024) [[arXiv](https://arxiv.org/abs/2408.16326)]
- *Authors:* Xin Zheng et al.
- *Direct Connection:* Table-Critic extends Critic-CoT’s single-critic self-reflection by introducing role-specialized agents (Judge, Critic, Refiner, Curator) and error-type routing to focus feedback on the first incorrect step and reduce solution degradation.

---

## Synthesis: How Prior Work Led to This Paper

Dynamic decomposition methods for table reasoning established the practice of building stepwise solutions over tables but left a gap in intermediate error control. Chain-of-Table operationalized reasoning as evolving sub-tables, yielding transparent chains that nonetheless lacked a way to identify and repair wrong steps before they propagated. Dater similarly decomposed questions and evidence via sub-table operations without built-in mechanisms to critique intermediate steps, while Binder used program-execution decomposition (SQL/Python) but offered no systematic diagnosis of step-level mistakes. In parallel, self-reflection work proposed iterative self-improvement: Self-Refine demonstrated that LLMs can revise solutions via self-feedback, and Critic-CoT introduced an explicit chain-of-thought critic, though a single-critic loop can be unreliable and degrade correct solutions. These developments played out on established problem settings defined by WikiTableQuestions (compositional multi-step table QA) and TabFact (table-based fact verification), which stress both multi-step consistency and error containment. Collectively, this body of work revealed a clear opportunity: decomposition produces interpretable steps, but without robust, targeted error diagnosis and correction, mistakes cascade. The next step was to structure self-improvement around roles and reusable critique knowledge. Building on Chain-of-Table’s chains, the new approach generalizes Critic-CoT’s self-critique into a multi-agent loop that focuses on the first erroneous step and iterates until convergence, while a self-evolving template tree distills and routes critique patterns by error type, stabilizing revisions across tasks like WikiTableQuestions and TabFact.

---

*Analysis generated on: 2026-04-05T11:57:58.381582*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
