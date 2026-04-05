# Prior Work Analysis Report

## Target Paper

**Title:** Improving Chain-of-Thought Reasoning via Quasi-Symbolic Abstractions

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Chain-of-Thought (CoT) represents a common strategy for reasoning in Large Language Models (LLMs) by decomposing complex tasks into intermediate inference steps.However, explanations generated via CoT are susceptible to content biases that negatively affect their robustness and faithfulness.To mitigate existing limitations, recent work has proposed the use of logical formalisms coupled with external symbolic solvers.However, fully symbolically formalised approaches introduce the bottleneck of requiring a complete translation from natural language to formal languages, a process that affects efficiency and flexibility.To achieve a trade-off, this paper investigates methods to disentangle content from logical reasoning without a complete formalisation.In particular, we present QuaSAR (for Quasi-Symbolic Abstract Reasoning), a variation of CoT that guides LLMs to operate at a higher level of abstraction via quasi-symbolic explanations.Our framework leverages the capability of LLMs to formalise only relevant variables and predicates, enabling the coexistence of symbolic elements with natural language.We show the impact of QuaSAR for in-context learning and for constructing demonstrations to improve the reasoning capabilities of smaller models.Our experiments show that quasi-symbolic abstractions can improve CoTbased methods by up to 8% accuracy, enhancing robustness and consistency on challenging adversarial variations on both natural language (i.e.MMLU-Redux) and symbolic reasoning tasks (i.e., GSM-Symbolic).

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This work introduced the step-by-step CoT paradigm that QuaSAR directly modifies by inserting explicit abstraction and semi-formalisation stages into the reasoning chain.

### 🏷️ Inspiration

**Faithful Chain-of-Thought Reasoning** (2023)
- *Authors:* Qing Lyu et al.
- *Direct Connection:* By diagnosing content biases and unfaithful rationales in free-form CoT and advocating structured, faithful reasoning, this paper directly motivated QuaSAR’s use of structured instructions to disentangle reasoning from content via quasi-symbolic steps.

**Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models** (2024)
- *Authors:* Huaixiu Steven Zheng et al.
- *Direct Connection:* This work provided the key insight that operating at a higher level of abstraction improves LLM reasoning, directly inspiring QuaSAR’s explicit Abstraction and Formalisation stages.

### 🏷️ Gap Identification

**LeanReasoner: Boosting Complex Logical Reasoning with Lean** (2024) [[arXiv](https://arxiv.org/abs/2403.13312)]
- *Authors:* Dongwei Jiang et al.
- *Direct Connection:* This work demonstrated strong logic performance via external proof assistants but highlighted the bottleneck of full translation to formal systems, a limitation QuaSAR addresses by avoiding complete formalisation while retaining symbolic structure.

**Verification and Refinement of Natural Language Explanations through LLM-Symbolic Theorem Proving** (2024)
- *Authors:* Xin Quan et al.
- *Direct Connection:* By showing verifier-in-the-loop pipelines that improve correctness at the cost of solver dependence and translation overhead, this paper underscored the practical inefficiency QuaSAR sidesteps with in-model quasi-symbolic reasoning.

### 🏷️ Baseline

**CoMAT: Chain of Mathematically Annotated Thought Improves Mathematical Reasoning** (2024)
- *Authors:* Joshua Ong Jun Leang et al.
- *Direct Connection:* As a primary comparison point using formal mathematical annotations to guide CoT, CoMAT’s multi-stage formalism set the benchmark that QuaSAR seeks to surpass with a single-step, lighter-weight quasi-symbolic prompt.

---

## Synthesis: How Prior Work Led to This Paper

Step-by-step reasoning with large language models was catalyzed by Chain-of-Thought prompting, which established that explicit intermediate steps can unlock latent reasoning abilities. Subsequent scrutiny revealed weaknesses in free-form rationales: Faithful Chain-of-Thought identified content biases and unfaithful explanations, arguing for structured constraints to separate reasoning from domain content. Parallel efforts sought stronger logical guarantees by embracing formal systems; LeanReasoner integrated LLMs with the Lean proof assistant, demonstrating the benefits of fully symbolic pipelines while exposing the overhead and brittleness of complete translations to formal languages. Similarly, verifier-in-the-loop approaches that refine natural language explanations via theorem provers improved correctness yet incurred significant solver dependence and translation costs. In mathematical domains, CoMAT showed that annotating thoughts with formal mathematical constructs can guide models toward more reliable solutions, albeit through multi-stage formalization and higher prompting costs. Complementing these, Take a Step Back showed that abstraction itself—stepping away from concrete content—enhances reasoning by fostering generalizable patterns.
These strands collectively point to a gap: we need the faithfulness and robustness of symbolic guidance without the inefficiencies of full formalization and external solvers. The natural next step is to combine CoT’s stepwise reasoning with explicit yet lightweight abstraction, using just enough symbolic structure to mitigate content effects. By formalizing only relevant variables and predicates and blending them with natural language, the current work synthesizes these insights into a single-prompt, quasi-symbolic protocol that retains flexibility, improves robustness, and reduces costs relative to solver-dependent or fully formal approaches.

---

*Analysis generated on: 2026-04-05T12:00:08.990203*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
