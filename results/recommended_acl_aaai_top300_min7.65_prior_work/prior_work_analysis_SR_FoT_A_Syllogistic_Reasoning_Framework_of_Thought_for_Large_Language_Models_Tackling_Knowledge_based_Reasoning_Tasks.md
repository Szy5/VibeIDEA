# Prior Work Analysis Report

## Target Paper

**Title:** SR-FoT: A Syllogistic-Reasoning Framework of Thought for Large Language Models Tackling Knowledge-based Reasoning Tasks

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Deductive reasoning is a crucial logical capability that assists us in solving complex problems based on existing knowledge. Although augmented by Chain-of-Thought prompts, Large Language Models (LLMs) might not follow the correct reasoning paths. Enhancing the deductive reasoning abilities of LLMs, and leveraging their extensive built-in knowledge for various reasoning tasks, remains an open question. Attempting to mimic the human deductive reasoning paradigm, we propose a multi-stage Syllogistic-Reasoning Framework of Thought (SR-FoT) that enables LLMs to perform syllogistic deductive reasoning to handle complex knowledge-based reasoning tasks. Our SR-FoT begins by interpreting the question and then uses the interpretation and the original question to propose a suitable major premise. It proceeds by generating and answering minor premise questions in two stages to match the minor premises. Finally, it guides LLMs to use the previously generated major and minor premises to perform syllogistic deductive reasoning to derive the answer to the original question. Extensive and thorough experiments on knowledge-based reasoning tasks have demonstrated the effectiveness and advantages of our SR-FoT.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Strategies in syllogistic reasoning** (1999)
- *Authors:* Monica Bucciarelli et al.
- *Direct Connection:* This work provides the classic syllogistic schema—major premise, minor premise, conclusion—that SR-FoT operationalizes by mapping each component to a dedicated prompt stage.

### 🏷️ Inspiration

**Sparks of Artificial General Intelligence: Early experiments with GPT-4** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2303.12712)]
- *Authors:* Sébastien Bubeck et al.
- *Direct Connection:* Observations that GPT-4 can autonomously pose and answer sub-questions directly motivate SR-FoT’s two-step minor-premise module: posing a minor premise question and then answering it.

### 🏷️ Gap Identification

**Hence, Socrates is mortal: A Benchmark for Natural Language Syllogistic Reasoning** (2023)
- *Authors:* Yuxuan Wu et al.
- *Direct Connection:* By evaluating syllogistic reasoning with given premises, this benchmark highlights that prior work focused on testing rather than generating and applying premises in natural language, a gap SR-FoT addresses.

**Language models don’t always say what they think: unfaithful explanations in chain-of-thought prompting** (2024)
- *Authors:* Miles Turpin et al.
- *Direct Connection:* Evidence that CoT explanations can be unfaithful motivates SR-FoT’s constrained per-stage visibility and syllogistic structure to increase reasoning rigor and faithfulness.

### 🏷️ Baseline

**Chain-of-thought prompting elicits reasoning in large language models** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* SR-FoT explicitly targets CoT’s lack of deductive rigor and uses CoT-style stepwise reasoning within its minor-premise answering stage while benchmarking against CoT as the principal baseline.

### 🏷️ Extension

**Self-consistency improves chain of thought reasoning in language models** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* The authors directly adapt self-consistency sampling from SC-CoT to aggregate multiple syllogistic runs in their SC-SR-FoT variant, extending the technique to their deductive framework.

### 🏷️ Related Problem

**Least-to-Most Prompting Enables Complex Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2205.10625)]
- *Authors:* Denny Zhou et al.
- *Direct Connection:* Showing that decomposing problems improves reasoning informs SR-FoT’s staged design, which instantiates decomposition through syllogistic roles rather than generic subproblems.

---

## Synthesis: How Prior Work Led to This Paper

Classic work on human deductive reasoning established syllogism as a structured process with a major premise, a minor premise, and a conclusion, clarifying how universal rules can be applied to specific instances to yield rigorous inferences. Chain-of-Thought prompting showed that large language models can be steered into multi-step reasoning, and self-consistency sampling further improved reliability by aggregating multiple reasoning paths. However, subsequent analyses found that Chain-of-Thought explanations can be unfaithful, underscoring a lack of rigor and raising concerns about hallucination and error accumulation. Structured prompting methods such as Least-to-Most demonstrated that decomposing tasks into subproblems enhances performance, though they did not tie substeps to formal logical roles. In parallel, a syllogistic benchmark in natural language assessed LLMs on problems with provided premises, highlighting evaluation progress but also the absence of methods that autonomously generate and then use premises. Finally, early experiments with GPT-4 revealed that models can pose and answer their own sub-questions, suggesting a practical mechanism for eliciting missing intermediate facts.
Collectively, these works reveal both the value of decomposition and the need for logically grounded, faithful reasoning. SR-FoT synthesizes these insights by instantiating a multi-stage pipeline aligned with syllogistic roles, autonomously posing and answering a minor-premise question to obtain the specific fact needed to apply a major premise, and constraining each stage’s visible inputs to curb distraction and hallucination. It further extends self-consistency sampling to aggregate syllogistic trajectories, naturally advancing from prior CoT-style reasoning toward more rigorous, premise-driven deduction for knowledge-based tasks.

---

*Analysis generated on: 2026-04-05T11:57:50.506201*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
