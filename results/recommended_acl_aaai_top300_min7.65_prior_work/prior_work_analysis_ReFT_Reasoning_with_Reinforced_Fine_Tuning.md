# Prior Work Analysis Report

## Target Paper

**Title:** ReFT: Reasoning with Reinforced Fine-Tuning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> One way to enhance the reasoning capability of Large Language Models (LLMs) is to conduct Supervised Fine-Tuning (SFT) using Chain-of-Thought (CoT) annotations.This approach does not show sufficiently strong generalization ability, however, because the training only relies on the given CoT data.In math problemsolving, for example, there is usually only one annotated reasoning path for each question in the training data.Intuitively, it would be better for the algorithm to learn from multiple annotated reasoning paths given a question.To address this issue, we propose a simple yet effective approach called Reinforced Fine-Tuning (ReFT) to enhance the generalizability of learning LLMs for reasoning, with math problemsolving as an example.ReFT first warmups the model with SFT, and then employs on-line reinforcement learning, specifically the PPO algorithm in this paper, to further fine-tune the model, where an abundance of reasoning paths are automatically sampled given the question and the rewards are naturally derived from the ground-truth answers.Extensive experiments on GSM8K, MathQA, and SVAMP datasets show that ReFT significantly outperforms SFT, and the performance can be potentially further boosted by combining inference-time strategies such as majority voting and re-ranking.Note that ReFT obtains the improvement by learning from the same training questions as SFT, without relying on extra or augmented training questions.This indicates a superior generalization ability for ReFT 1 .* indicates equal contribution, indicates corresponding author 1 Code: https:

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Chain-of-thought prompting elicits reasoning in large language models** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This work established using chain-of-thought (CoT) rationales for supervised fine-tuning, which ReFT explicitly warm-starts from and then surpasses by learning from multiple sampled CoT paths.

**Training verifiers to solve math word problems** (2021) [[arXiv](https://arxiv.org/abs/arXiv:2110.14168)]
- *Authors:* Karl Cobbe et al.
- *Direct Connection:* This paper introduced GSM8K and the practice of extracting and verifying answers from generated solutions, which ReFT directly leverages to define outcome-based rewards from ground-truth answers without a learned reward model.

**PAL: Program-aided Language Models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2211.10435)]
- *Authors:* Luyu Gao et al.
- *Direct Connection:* PAL introduced program-based CoT (Python) with executable reasoning, which ReFT uses to obtain deterministic answer signals and train PPO on both natural-language and program-based CoTs.

### 🏷️ Inspiration

**Self-consistency improves chain of thought reasoning in language models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2203.11171)]
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* By showing that sampling multiple diverse reasoning paths and aggregating improves accuracy, this work inspired ReFT’s core idea to sample many CoTs during training and reinforce those that yield correct answers.

### 🏷️ Gap Identification

**Training language models to follow instructions with human feedback** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2203.02155)]
- *Authors:* Long Ouyang et al.
- *Direct Connection:* This RLHF approach highlighted the reliance on learned reward models and human preference data, a limitation ReFT addresses by using task-inherent, automatic rewards from final-answer correctness instead of a trained reward model.

### 🏷️ Extension

**Fine-Tuning Language Models from Human Preferences** (2019) [[arXiv](https://arxiv.org/abs/arXiv:1909.08593)]
- *Authors:* Daniel M. Ziegler et al.
- *Direct Connection:* ReFT directly adopts the PPO-with-KL framework and value head setup from this work to stabilize online reinforcement learning for language generation after SFT warm-up.

**Seq2SQL: Generating Structured Queries from Natural Language using Reinforcement Learning** (2017) [[arXiv](https://arxiv.org/abs/arXiv:1709.00103)]
- *Authors:* Victor Zhong et al.
- *Direct Connection:* Seq2SQL’s execution-based terminal rewards and partial-credit shaping for numeric outcomes are directly adapted in ReFT to mitigate sparse rewards when using answer correctness as the training signal.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-thought prompting showed that supervising language models on explicit intermediate rationales improves reasoning, but typically relies on a single annotation per problem. GSM8K introduced a math benchmark where solutions can be checked by extracting the final numeric answer, establishing a practical mechanism for validating outputs against ground truth. In parallel, fine-tuning language models from human preferences demonstrated how PPO with a KL penalty and a value head can stabilize on-policy reinforcement learning in text generation. RLHF later scaled this recipe with human preference data and learned reward models, but at significant annotation cost. Program-aided Language Models introduced executable, code-based chains of thought that yield deterministic answers through program execution, offering reliable correctness signals. Self-consistency revealed that sampling and aggregating multiple diverse reasoning paths improves accuracy, indicating the presence of many valid solution trajectories. Earlier, Seq2SQL highlighted how execution-based terminal rewards—and partial-credit shaping for numeric answers—can make reinforcement learning practical for symbolic tasks with sparse signals.
Together these works suggested a path where multiple reasoning paths should be explored and judged by inherent outcome correctness rather than human preferences. The natural verifiability of math answers (and executable code solutions) offers automatic rewards, while the PPO-with-KL machinery provides a stable way to optimize non-differentiable objectives. Building on these insights, the current paper warm-starts from CoT SFT, then performs on-policy PPO that samples many CoTs per question, reinforces those that produce correct answers (with partial rewards to reduce sparsity), and constrains exploration via a KL penalty—thereby transforming the multi-path insight from inference-time heuristics into a training-time principle that improves generalization without extra data.

---

*Analysis generated on: 2026-04-05T11:58:04.251864*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
