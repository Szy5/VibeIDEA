# Prior Work Analysis Report

## Target Paper

**Title:** On the Bias of Next-Token Predictors Toward Systematically Inefficient Reasoning: A Shortest-Path Case Study

**arXiv ID:** [2507.05362](https://arxiv.org/abs/2507.05362)

**Abstract:** 
> Recent advances in natural language processing highlight two key factors for improving reasoning in large language models (LLMs): (i) allocating more test-time compute tends to help on harder problems but often introduces redundancy in the reasoning trace, and (ii) compute is most effective when reasoning is systematic and incremental, forming structured chains of thought (CoTs) akin to human problem-solving. To study these factors in isolation, we introduce a controlled setting based on shortest-path tasks in layered graphs. We train decoder-only transformers on question-trace-answer triples using a custom tokenizer, comparing models trained on optimal bottom-up dynamic programming traces with those trained on longer, valid traces involving backtracking. Surprisingly, with the same training-token budget, models trained on inefficient traces generalize better to unseen graphs. This benefit is not due to length alone-injecting arbitrary redundancy into reasoning traces fails to help and can even hurt performance. Instead, we find that generalization correlates with the model's confidence in next-token prediction, suggesting that long, coherent, and locally incremental traces make the training signal easier to optimize.

**Innovation pattern:** Formal-Experimental Tightening (confidence: high)

Secondary patterns: Data & Evaluation Engineering, Inference-Time Control & Guided Sampling

*Reasoning:* Combines formal/theoretical analysis with controlled synthetic experiments probing next-token training biases; uses supervised intermediate-step datasets (P05) and discusses decoding/population of reasoning trajectories (inference-time control, P09).

---

## Key Prior Works ({len(analysis.prior_works)} papers with direct influence)

### 🏷️ Foundation

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* Introduced the basic idea that providing intermediate, step-by-step reasoning (chain-of-thought) substantially improves LLM problem solving, which motivates the paper’s core methodology of training next-token predictors on explicit algorithmic traces rather than direct question→answer pairs.

**Learning to Execute** (2014) [[arXiv](https://arxiv.org/abs/1410.4615)]
- *Authors:* Marcin Zaremba & Ilya Sutskever
- *Direct Connection:* Introduced the paradigm of training sequence models to imitate algorithmic procedures on synthetic tasks, providing the conceptual and methodological precedent for the controlled layered-graph shortest-path benchmark and for supervising models with full intermediate algorithmic traces.

### 🏷️ Inspiration

**Self-Consistency Improves Chain of Thought Reasoning in Language Models** (2022) [[arXiv](https://arxiv.org/abs/2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* Demonstrated that sampling multiple reasoning trajectories and aggregating them improves final performance and exposed the importance of trace diversity and decoding dynamics, directly inspiring the present paper’s investigation of how trace structure, length and sampling temperature affect next-token learning and generalization.

### 🏷️ Extension

**Chain of thought empowers transformers to solve inherently serial problems** (2024)
- *Authors:* Zhiyuan Li, Hong Liu, Denny Zhou, Tengyu Ma
- *Direct Connection:* Provided theoretical and empirical evidence that supplying intermediate computation steps expands what transformers can represent and learn on serial algorithmic tasks, a technical premise this paper extends by dissecting which kinds of algorithmic traces (optimal vs. backtracking/inefficient) align with next-token predictors’ inductive biases.

### 🏷️ Related Problem

**Neural execution of graph algorithms** (2021)
- *Authors:* Petar Veličković et al.
- *Direct Connection:* Showed how neural models can be trained to reproduce intermediate steps of classical graph algorithms and highlighted layered/graph algorithm tasks as a diagnostic playground, directly informing the choice of shortest-path layered graphs and the decision to supervise with intermediate solver traces.

---

## Synthesis: How Prior Work Led to This Paper

Work on chain-of-thought (CoT) prompting established that exposing intermediate reasoning steps improves LLM performance (Wei et al. 2022), and follow-up empirical techniques such as self-consistency showed that the population and decoding of multiple reasoning trajectories matter for final answers (Wang et al. 2022). More recent theoretical/empirical analyses formalized how supplying computation steps expands transformers’ expressive power on serial algorithmic problems (Li et al., 2024), giving a direct technical foundation for studying which kinds of intermediate computations are learnable. Separately, the sequence-model–as–algorithmic-executor paradigm (Zaremba & Sutskever, 2014) set the methodological precedent of using synthetic algorithmic tasks and supervising every intermediate step, while work on neural execution of graph algorithms (Veličković et al.) demonstrated that graph algorithm traces are a practical diagnostic for structured reasoning. Together these strands make a tight intellectual lineage: CoT shows the value of intermediate steps; self-consistency and sampling expose the role of trajectory diversity and decoding; theoretical work explains why serial traces change learnability; and algorithmic/graph execution papers provide the controlled benchmarks and supervision format. The combination naturally leads to the present question—given the same token budget, which trace structures (globally optimal versus longer, locally incremental/backtracking traces) best align with next-token predictors—and motivates the paper’s controlled shortest-path experiments and the use of next-token confidence to explain why systematic inefficiency can paradoxically improve generalization.

---

*Analysis generated on: 2026-03-09T00:05:28.610091*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*

*Token usage (Qwen tokenizer): input=15369, output=1029*
