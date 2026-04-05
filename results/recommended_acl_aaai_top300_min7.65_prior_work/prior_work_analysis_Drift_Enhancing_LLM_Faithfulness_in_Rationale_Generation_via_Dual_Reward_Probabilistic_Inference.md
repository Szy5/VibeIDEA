# Prior Work Analysis Report

## Target Paper

**Title:** Drift: Enhancing LLM Faithfulness in Rationale Generation via Dual-Reward Probabilistic Inference

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> As Large Language Models (LLMs) are increasingly applied to complex reasoning tasks, achieving both accurate task performance and faithful explanations becomes crucial.However, LLMs often generate unfaithful explanations, partly because they do not consistently adhere closely to the provided context.Existing approaches to this problem either rely on superficial calibration methods, such as decomposed Chain-of-Thought prompting, or require costly retraining to improve model faithfulness.In this work, we propose a probabilistic inference paradigm that leverages taskspecific and lookahead rewards to ensure that LLM-generated rationales are more faithful to model decisions and align better with input context.These rewards are derived from a domainspecific proposal distribution, allowing for optimized sequential Monte Carlo approximations.Our evaluations across three different reasoning tasks show that this method, which allows for controllable generation during inference, improves both accuracy and faithfulness of LLMs.This method offers a promising path towards making LLMs more reliable for reasoning tasks without sacrificing performance.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Sequential Monte Carlo Steering of Large Language Models using Probabilistic Programs** (2023) [[arXiv](https://arxiv.org/abs/2306.03081)]
- *Authors:* Alexander K. Lew et al.
- *Direct Connection:* It provides the Feynman–Kac/SMC steering framework that Drift instantiates by defining potential functions—here, task-specific and lookahead rationale rewards—to reweight and select high-probability decoding trajectories.

**Feynman-Kac Formulae: Genealogical and Interacting Particle Systems with Applications** (2004)
- *Authors:* Pierre Del Moral
- *Direct Connection:* This monograph supplies the Feynman–Kac formalism underlying Drift’s sequential Monte Carlo inference, enabling path-weighting via potential functions during generation.

### 🏷️ Inspiration

**FUDGE: Controlled Text Generation with Future Discriminators** (2021)
- *Authors:* Kevin Yang and Dan Klein
- *Direct Connection:* FUDGE’s idea of future-aware control—scoring continuations with a ‘future’ model—directly inspires Drift’s use of a generative expert as a lookahead reward, but without training discriminators and embedded within a probabilistic inference procedure.

### 🏷️ Gap Identification

**Measuring Faithfulness in Chain-of-Thought Reasoning** (2023) [[arXiv](https://arxiv.org/abs/2307.13702)]
- *Authors:* Tamera Lanham et al.
- *Direct Connection:* This paper documents that CoT explanations often fail to reflect input perturbations, defining the faithfulness gap Drift targets by making rationales responsive to domain-relevant changes.

**Question Decomposition Improves the Faithfulness of Model-Generated Reasoning** (2023) [[arXiv](https://arxiv.org/abs/2307.11768)]
- *Authors:* Ansh Radhakrishnan et al.
- *Direct Connection:* While showing decomposition can improve faithfulness, it relies on structured prompting and auxiliary verification, motivating Drift’s alternative inference-time control that avoids retraining and heavy post-hoc tooling.

### 🏷️ Baseline

**Tuning Language Models by Proxy** (2024)
- *Authors:* Alisa Liu et al.
- *Direct Connection:* Its token-local logit fusion approach for decoding-time control is implemented as a baseline that Drift explicitly surpasses by introducing lookahead, sequence-level rewards instead of local logit interpolation.

### 🏷️ Extension

**Faithful Question Answering with Monte-Carlo Planning** (2023)
- *Authors:* Ruixin Hong et al.
- *Direct Connection:* This work introduced a faithfulness-seeking reward used during Monte-Carlo search for QA, which is directly adapted by replacing MCTS/training with inference-time dual rewards (task and generative lookahead) in a probabilistic decoding scheme.

---

## Synthesis: How Prior Work Led to This Paper

Monte-Carlo planning for faithful question answering demonstrated that a faithfulness-seeking reward can steer search toward faithful responses, but used MCTS and training to operationalize the idea. Sequential Monte Carlo steering of LLMs showed how Feynman–Kac potentials can reweight trajectories during decoding, offering a probabilistic alternative to rollout-heavy search. The Feynman–Kac formalism itself provides the mathematical basis for path-weighting via potential functions, enabling efficient approximation of target distributions over sequences. In contrast, token-local decoding-time control, such as logit fusion in tuning-by-proxy, fuses logits stepwise but lacks lookahead needed to enforce attributes spanning longer text segments. Earlier controlled generation with future discriminators (FUDGE) introduced future-aware control by scoring candidate continuations, though it required training discriminators. Meanwhile, faithfulness studies on chain-of-thought reasoning revealed that generated rationales often fail to reflect input perturbations, and question decomposition approaches improved faithfulness but demanded structure and auxiliary verification.
Taken together, these works suggest a gap: training- or rollout-heavy methods can enforce faithfulness with lookahead, while token-local constraints are efficient but insufficient for long-range attributes. A natural next step is to combine the probabilistic SMC steering paradigm with future-aware scoring, but without training, by using domain-specific generative models as lookahead evaluators. Adding a lightweight task-specific constraint at the answer step from a strong classifier aligns label prediction, while trajectory weights from the generative expert encourage context-sensitive, faithful spans. This synthesis yields an inference-time, dual-reward probabilistic decoding that advances both accuracy and rationale faithfulness.

---

*Analysis generated on: 2026-04-05T11:54:36.578549*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
