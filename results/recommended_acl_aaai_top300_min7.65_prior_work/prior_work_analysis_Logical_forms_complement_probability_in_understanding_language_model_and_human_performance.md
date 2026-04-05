# Prior Work Analysis Report

## Target Paper

**Title:** Logical forms complement probability in understanding language model (and human) performance

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> With the increasing interest in using large language models (LLMs) for planning in natural language, understanding their behaviors becomes an important research question.This work conducts a systematic investigation of LLMs' ability to perform logical reasoning in natural language.We introduce a controlled dataset of hypothetical and disjunctive syllogisms in propositional and modal logic and use it as the testbed for understanding LLM performance.Our results lead to novel insights in predicting LLM behaviors: in addition to the probability of input (Gonen et al., 2023;McCoy et al., 2024), logical forms should be considered as important factors.In addition, we show similarities and discrepancies between the logical reasoning performances of humans and LLMs by collecting and comparing behavioral data from both.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2210.01273)]
- *Authors:* Abulhair Saparov and He He
- *Direct Connection:* The dataset design adopts Saparov and He’s paradigm of synthesizing natural-language reasoning items from formal logic templates, extending it to controlled hypothetical/disjunctive syllogisms and modal operators.

**Prompting is not a substitute for probability measurements in large language models** (2023)
- *Authors:* Jennifer Hu and Roger Levy
- *Direct Connection:* Following Hu and Levy’s recommendation to evaluate with probabilities rather than greedy outputs, the study uses relative probabilities of 'Yes'/'No' to compute a soft-accuracy metric for logical judgments.

### 🏷️ Inspiration

**Language models, like humans, show content effects on reasoning tasks** (2024)
- *Authors:* Andrew K. Lampinen et al.
- *Direct Connection:* Their demonstration of content effects directly motivated controlling knowledge bias by assigning independent, neutral interpretations to propositional variables in the logic-to-language translation.

### 🏷️ Gap Identification

**Demystifying prompts in language models via perplexity estimation** (2023)
- *Authors:* Hila Gonen et al.
- *Direct Connection:* This work’s claim that perplexity is a strong predictor of LLM performance is directly revisited by showing, on controlled syllogism templates, that logical form (modality and argument pattern) explains additional variance beyond perplexity.

**Embers of autoregression show how large language models are shaped by the problem they are trained to solve** (2024)
- *Authors:* R. Thomas McCoy et al.
- *Direct Connection:* Building on McCoy et al.’s probability–performance correlation, the study demonstrates that this correlation is weak for logical reasoning and must be complemented by explicit logical-form factors.

**Conditional and Modal Reasoning in Large Language Models** (2024)
- *Authors:* Wesley H. Holliday et al.
- *Direct Connection:* This modal-logic case study motivated a broader, controlled benchmark by highlighting modal reasoning in LLMs but lacking systematic controls on knowledge bias and rigorous mixed-effects statistical evaluation.

### 🏷️ Extension

**A systematic comparison of syllogistic reasoning in humans and language models** (2024)
- *Authors:* Tiwalayo Eisape et al.
- *Direct Connection:* Inspired by their human–LLM comparison on categorical syllogisms, the study extends the paradigm by collecting new human data and analyzing hypothetical and disjunctive syllogisms, including modal variants.

---

## Synthesis: How Prior Work Led to This Paper

Template-based logical reasoning benchmarks showed that natural-language questions can be systematically generated from formal logic schemata, enabling targeted evaluations of specific inference patterns. A case study on conditional and modal reasoning highlighted that LLMs do engage with modality, but without stringent controls it is hard to separate logical competence from confounds. Concurrently, methodological work argued that model competence should be assessed via probability measurements rather than greedy decoding, encouraging metrics that reflect token-level confidence. Two influential analyses reported that perplexity or probability often correlates with task success, suggesting input likelihood as a general predictor. However, research on content effects in both humans and LLMs warned that world knowledge and lexical choices can confound logical evaluation unless interpretations are carefully controlled. Parallel comparisons of human and LLM syllogistic reasoning supplied a framework and behavioral baselines for aligning machine patterns with human data.
Together, these strands exposed a gap: perplexity-based predictors alone do not isolate logical reasoning, and existing modal studies lacked controlled, statistically grounded tests disentangled from content effects. The natural next step was to synthesize a controlled benchmark that varies argument forms (disjunctive, modus ponens, modus tollens) and modalities (necessity, possibility) while neutralizing knowledge bias, evaluate with probability-based soft accuracy, and align findings with human behavior. By uniting template-driven data generation, probability-centric evaluation, and human comparison, the study demonstrates that logical form is a crucial complementary factor to probability in predicting LLM (and human) reasoning performance.

---

*Analysis generated on: 2026-04-05T12:06:30.432039*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
