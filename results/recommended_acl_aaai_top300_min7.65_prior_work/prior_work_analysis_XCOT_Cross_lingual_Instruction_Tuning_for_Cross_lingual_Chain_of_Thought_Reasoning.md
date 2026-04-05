# Prior Work Analysis Report

## Target Paper

**Title:** XCOT: Cross-lingual Instruction Tuning for Cross-lingual Chain-of-Thought Reasoning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Chain-of-thought (CoT) has emerged as a powerful technique to elicit reasoning in large language models and improve a variety of downstream tasks. CoT mainly demonstrates excellent performance in English, but its usage in low-resource languages is constrained due to poor language generalization. To bridge the gap among different languages, we propose a cross-lingual instruction fine-tuning framework (xCoT) to transfer knowledge from high-resource languages to low-resource languages. Specifically, the multilingual instruction training data (xCoT-Instruct) is created to encourage the semantic alignment of multiple languages. We introduce cross-lingual in-context few-shot learning (xICL) to accelerate multilingual agreement in instruction tuning, where some fragments of source languages in examples are randomly substituted by their counterpart translations of target languages. During multilingual instruction tuning, we adopt the randomly online CoT strategy to enhance the multilingual reasoning ability of the large language model by first translating the query to another language and then answering in English. To further facilitate the language transfer, we leverage the high-resource CoT to supervise the training of low-resource languages with cross-lingual distillation. Experimental results demonstrate the superior performance of xCoT in reducing the gap among different languages, highlighting its potential to reduce the cross-lingual gap.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Language Models are Multilingual Chain-of-Thought Reasoners** (2023)
- *Authors:* Freda Shi et al.
- *Direct Connection:* This work introduced the MGSM benchmark and showed that translating non-English queries and reasoning in English boosts cross-lingual CoT, establishing the problem setting and core insight that XCOT formalizes and trains for with supervised cross-lingual instruction tuning and “think in English” prompts.

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* This paper established CoT as an effective supervision signal, which XCOT leverages by generating and distilling step-by-step rationales across languages (Random-CoT) to transfer reasoning ability from high- to low-resource languages.

**Training Verifiers to Solve Math Word Problems (GSM8K)** (2021) [[arXiv](https://arxiv.org/abs/2110.14168)]
- *Authors:* Karl Cobbe et al.
- *Direct Connection:* GSM8K provided the high-quality math word problem source that XCOT translated into multiple languages to form xCoT-Instruct while keeping English CoT answers for supervised cross-lingual transfer.

### 🏷️ Inspiration

**ConNER: Consistency Training for Cross-lingual Named Entity Recognition** (2022)
- *Authors:* Rui Zhou et al.
- *Direct Connection:* The consistency-training principle of aligning model outputs on parallel texts inspired XCOT’s cross-lingual distillation that uses token-level KL divergence to align output distributions between high- and low-resource language inputs for the same query.

### 🏷️ Gap Identification

**Cross-lingual Prompting: Improving Zero-shot Chain-of-Thought Reasoning across Languages** (2023)
- *Authors:* Liuqiang Qin et al.
- *Direct Connection:* By showing cross-lingual CoT gains via prompt engineering alone and highlighting limits without fine-tuning, this paper motivated XCOT’s move from prompt-only tricks to supervised cross-lingual instruction tuning with code-switched contexts and Random-CoT.

### 🏷️ Baseline

**Breaking Language Barriers in Multilingual Mathematical Reasoning: Insights and Observations (MathOctopus)** (2023)
- *Authors:* Ningyu Chen et al.
- *Direct Connection:* MathOctopus demonstrated that multilingual instruction data and training substantially improve multilingual math reasoning, serving as the primary multilingual baseline and directly motivating XCOT’s multilingual instruction corpus plus additional alignment mechanisms (xICL and xDistill).

### 🏷️ Extension

**Scaling relationship on learning mathematical reasoning with large language models** (2023) [[arXiv](https://arxiv.org/abs/2308.01825)]
- *Authors:* Zhengyuan Yuan et al.
- *Direct Connection:* XCOT extends RFT’s rejection-sampling idea by multilingual sampling (mSampling) to generate and filter correct reasoning paths in multiple languages, augmenting cross-lingual CoT supervision during instruction tuning.

---

## Synthesis: How Prior Work Led to This Paper

Multilingual chain-of-thought prompting was crystallized by work showing that large language models can benefit from reasoning in English even when queries are non-English, with the MGSM benchmark formalizing this setting and revealing translation-to-English as a strong lever for cross-lingual CoT. Subsequent cross-lingual prompting refined zero-shot techniques to improve multilingual CoT but remained prompt-only and lacked representational alignment from supervised training. In parallel, MathOctopus demonstrated that multilingual instruction datasets and finetuning substantially raise multilingual math reasoning performance, establishing a strong baseline and underscoring the value of multilingual supervision. Chain-of-Thought prompting itself established stepwise rationales as powerful supervision signals. Rejection sampling fine-tuning then showed how to generate multiple CoT paths and select correct ones to strengthen reasoning supervision. Beyond reasoning, cross-lingual consistency training in NER introduced aligning output distributions across parallel inputs via KL, a general idea applicable to multilingual transfer. Finally, GSM8K provided the canonical math word problem corpus from which multilingual instruction data can be derived.
Synthesizing these pieces, the gap emerged: prompt-only cross-lingual CoT helps, but without supervised alignment it plateaus, and prior finetuning lacked explicit multilingual agreement and transfer. XCOT naturally follows by constructing a multilingual instruction set from GSM8K with English CoT answers, injecting code-switched xICL to align representations, using Random-CoT to operationalize “think in English,” leveraging RFT-style multilingual sampling to obtain reliable reasoning paths, and applying cross-lingual KL distillation to transfer high-resource CoT distributions to low-resource inputs—thereby turning scattered insights into a cohesive cross-lingual CoT training framework.

---

*Analysis generated on: 2026-04-05T12:08:14.487997*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
