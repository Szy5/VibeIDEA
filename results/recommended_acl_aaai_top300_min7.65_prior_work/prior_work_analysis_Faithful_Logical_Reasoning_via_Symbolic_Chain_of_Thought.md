# Prior Work Analysis Report

## Target Paper

**Title:** Faithful Logical Reasoning via Symbolic Chain-of-Thought

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> While the recent Chain-of-Thought (CoT) technique enhances the reasoning ability of large language models (LLMs) with the theory of mind, it might still struggle in handling logical reasoning that relies much on symbolic expressions and rigid deducing rules.To strengthen the logical reasoning capability of LLMs, we propose a novel Symbolic Chain-of-Thought, namely SymbCoT, a fully LLM-based framework that integrates symbolic expressions and logic rules with CoT prompting.Technically, building upon an LLM, SymbCoT 1) first translates the natural language context into the symbolic format, and then 2) derives a step-by-step plan to solve the problem with symbolic logical rules, 3) followed by a verifier to check the translation and reasoning chain.Via thorough evaluations on 5 standard datasets with both First-Order Logic and Constraint Optimization symbolic expressions, SymbCoT shows striking improvements over the CoT method consistently, meanwhile refreshing the current stateof-the-art performances.We further demonstrate that our system advances in more faithful, flexible, and explainable logical reasoning.To our knowledge, this is the first to combine symbolic expressions and rules into CoT for logical reasoning with LLMs.Code is open at https://github.com/Aiden0526/SymbCoT.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This paper established the step-by-step reasoning paradigm that SymbCoT directly extends by expressing intermediate steps in formal symbolic logic rather than purely natural-language rationales.

**FOLIO: Natural Language Reasoning with First-Order Logic** (2022) [[arXiv](https://arxiv.org/abs/2209.00840)]
- *Authors:* Simeng Han et al.
- *Direct Connection:* FOLIO defined the NL-to-FOL reasoning setup with T/F/U judgments that directly shapes SymbCoT’s translation target, inference space, and verification of faithfulness.

### 🏷️ Inspiration

**Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.04091)]
- *Authors:* Lei Wang et al.
- *Direct Connection:* Its explicit plan-then-solve decomposition directly motivates SymbCoT’s Planner and Solver modules, which operationalize the plan via formal inference rules over symbolic representations.

**Code Prompting: A Neural Symbolic Method for Complex Reasoning in Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.18507)]
- *Authors:* Yi Hu et al.
- *Direct Connection:* Demonstrating that structured, program-like intermediate representations improve reliability, this work inspires SymbCoT’s use of symbolic logic expressions as the structured form of chain-of-thought.

**MathPrompter: Mathematical Reasoning Using Large Language Models** (2023)
- *Authors:* Shima Imani et al.
- *Direct Connection:* Showing that equations as intermediate steps steer LLM reasoning, MathPrompter motivates SymbCoT’s use of FOL/CO formulas and explicit rule application to guide faithful logical deduction.

### 🏷️ Gap Identification

**Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning** (2023) [[arXiv](https://arxiv.org/abs/2305.12295)]
- *Authors:* Liangming Pan et al.
- *Direct Connection:* By using LLMs only as translators and delegating reasoning to external provers, Logic-LM exposed brittleness to translation errors and limited LLM reasoning, gaps SymbCoT addresses with a fully LLM-based translation–reasoning pipeline plus verification.

### 🏷️ Related Problem

**LINC: A Neurosymbolic Approach for Logical Reasoning by Combining Language Models with First-Order Logic Provers** (2023)
- *Authors:* Theo Olausson et al.
- *Direct Connection:* LINC’s LM-to-prover workflow showed the promise and limitations of external theorem proving—strict formatting and information loss—which SymbCoT avoids by internalizing both symbolic translation and reasoning with an LLM and adding a verifier.

---

## Synthesis: How Prior Work Led to This Paper

Step-by-step prompting emerged as a powerful technique with Chain-of-Thought, which taught language models to externalize intermediate reasoning in natural language. Plan-and-Solve further refined this by separating high-level planning from execution, making complex problems tractable through explicit subgoal decomposition. Parallel work showed that structured intermediate representations can be even more reliable: Code Prompting framed thoughts as pseudo-code to align with task structure, while MathPrompter used equations as the medium of thought for math, both highlighting that the form of intermediate steps matters for correctness. In neurosymbolic reasoning, Logic-LM and LINC mapped natural language into formal logic and delegated deduction to external provers, achieving strong performance but revealing fragility to translation syntax, potential information loss, and limited explainability since the core reasoning lived outside the LM. Datasets like FOLIO crystallized a concrete setting—translate NL to FOL and determine true/false/unknown—establishing the representational and evaluative scaffold for studying faithful logical reasoning.
Taken together, these threads suggested a clear opportunity: keep the interpretive strengths of LMs and the rigor of symbolic rules, but enact both translation and deduction within the model, and structure the thought process to match the logic of the task. Building on CoT’s stepwise paradigm and Plan-and-Solve’s decomposition, and inspired by code/equation-style reasoning, the current work integrates symbolic expressions directly into the chain of thought, executes rule-based inference inside the LM, and adds a verifier to audit both translation and logical steps. This synthesis addresses the brittle translator-to-prover gap while preserving precision and faithfulness demanded by formal logical reasoning.

---

*Analysis generated on: 2026-04-05T11:56:52.486934*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
