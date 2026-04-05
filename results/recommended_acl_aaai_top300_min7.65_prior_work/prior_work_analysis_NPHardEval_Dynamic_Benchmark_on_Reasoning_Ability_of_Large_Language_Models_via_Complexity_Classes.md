# Prior Work Analysis Report

## Target Paper

**Title:** NPHardEval: Dynamic Benchmark on Reasoning Ability of Large Language Models via Complexity Classes

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> NPHardEval: Dynamic Benchmark on Reasoning Ability of Large Language Models via Complexity Classes

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**A catalog of complexity classes** (1990)
- *Authors:* David S. Johnson
- *Direct Connection:* This work provides the formal taxonomy of P, NP-complete, and NP-hard that the benchmark directly uses to select tasks and stratify difficulty levels for a rigorously complexity-grounded evaluation.

### 🏷️ Gap Identification

**Pretraining on the test set is all you need** (2023) [[arXiv](https://arxiv.org/abs/2309.08632)]
- *Authors:* Rylan Schaeffer
- *Direct Connection:* By showing that public static benchmarks are vulnerable to memorization and overfitting, this paper directly motivates the benchmark’s monthly refresh strategy to mitigate ‘benchmark hacking’.

**Mathematical capabilities of ChatGPT** (2023) [[arXiv](https://arxiv.org/abs/2301.13867)]
- *Authors:* Simon Frieder et al.
- *Direct Connection:* This study’s reliance on manual verification for advanced reasoning tasks highlighted inefficiency and lack of standardization, prompting the use of automatic algorithmic checkers for end-to-end evaluation.

**Challenging BIG-Bench tasks and whether chain-of-thought can solve them** (2022) [[arXiv](https://arxiv.org/abs/2210.09261)]
- *Authors:* Mirac Suzgun et al.
- *Direct Connection:* By emphasizing multi-step prompting challenges without grounding in computational complexity, this work underscored the need for benchmarks centered on complexity-theoretic reasoning tasks.

**Measuring Massive Multitask Language Understanding** (2020) [[arXiv](https://arxiv.org/abs/2009.03300)]
- *Authors:* Dan Hendrycks et al.
- *Direct Connection:* As a prominent static, exam-style benchmark prone to memorization and not designed to quantify logical complexity, MMLU’s limitations motivated a complexity-based, dynamically updated alternative.

### 🏷️ Extension

**DyVal: Graph-informed dynamic evaluation of large language models** (2023) [[arXiv](https://arxiv.org/abs/2309.17167)]
- *Authors:* Kaijie Zhu et al.
- *Direct Connection:* DyVal introduced dynamic, graph-informed evaluation with periodically refreshed instances focused on polynomial-time problems, which this work extends by generalizing the dynamic mechanism to a broader set of algorithmic tasks spanning NP-complete and NP-hard.

---

## Synthesis: How Prior Work Led to This Paper

The foundations of computational complexity formalize a rigorous hierarchy of problem difficulty: Johnson’s taxonomy distinguishes P, NP-complete, and NP-hard problems and gives a principled basis for selecting tasks that inherently differ in resource requirements. Dynamic evaluation emerged as a promising direction in DyVal, which proposed graph-informed, periodically refreshed instances to test LLM reasoning but largely remained within polynomial-time settings. Empirical analyses exposed systemic weaknesses of static public benchmarks: Schaeffer demonstrated that pretraining on test sets can inflate scores and misrepresent capabilities, while Frieder and colleagues showed that graduate-level reasoning and math assessments often require manual verification, hampering scalability and consistency. Widely used reasoning suites like BIG-bench Hard focus on multi-step prompting strategies rather than complexity-grounded logic, and MMLU’s static, exam-style format emphasizes breadth of knowledge over quantified logical difficulty, both leaving gaps in measuring algorithmic reasoning depth. Together these works revealed a clear opportunity: couple the formal structure of complexity classes with dynamic, automatically verifiable evaluation to prevent benchmark hacking and to quantify reasoning across truly different hardness regimes. Building on Johnson’s framework and DyVal’s dynamic principle, the natural next step is to extend dynamism beyond polynomial-time graph tasks to a curated set of algorithmic problems that span P, NP-complete, and NP-hard, paired with deterministic solvers for automatic scoring and scheduled refreshes that resist memorization while enabling reliable longitudinal assessment of LLM reasoning.

---

*Analysis generated on: 2026-04-05T11:55:06.817635*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
