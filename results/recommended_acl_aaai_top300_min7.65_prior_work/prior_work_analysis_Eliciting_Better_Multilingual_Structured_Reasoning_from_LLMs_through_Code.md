# Prior Work Analysis Report

## Target Paper

**Title:** Eliciting Better Multilingual Structured Reasoning from LLMs through Code

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> The development of large language models (LLM) has shown progress on reasoning, though studies have largely considered either English or simple reasoning tasks.To address this, we introduce a multilingual structured reasoning and explanation dataset, termed xSTREET, that covers four tasks across six languages.xSTREET exposes a gap in base LLM performance between English and non-English reasoning tasks. 1 We then propose two methods to remedy this gap, building on the insight that LLMs trained on code are better reasoners.First, at training time, we augment a code dataset with multilingual comments using machine translation while keeping program code as-is.Second, at inference time, we bridge the gap between training and inference by employing a prompt structure that incorporates step-by-step code primitives to derive new facts and find a solution.Our methods show improved multilingual performance on xSTREET, most notably on the scientific commonsense reasoning subtask.Furthermore, the models show no regression on non-reasoning tasks, thus demonstrating our techniques maintain general-purpose abilities.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**STREET: A Multi-task Structured Reasoning and Explanation Benchmark** (2022)
- *Authors:* Danilo Neves Ribeiro et al.
- *Direct Connection:* Introduced the structured reasoning graph formulation and linearized prompts that are directly translated and used as the target structure and baseline format for the multilingual xSTREET benchmark.

**The Stack: 3 TB of permissively licensed source code** (2022) [[arXiv](https://arxiv.org/abs/2211.15533)]
- *Authors:* Denis Kocetkov et al.
- *Direct Connection:* Provided the large-scale code-with-comments corpus that was directly augmented by translating comments to create the multilingual TCC fine-tuning data central to the training-time method.

### 🏷️ Inspiration

**Language Models of Code are Few-Shot Commonsense Learners** (2022)
- *Authors:* Aman Madaan et al.
- *Direct Connection:* Demonstrated that reformulating natural language commonsense problems as code prompts markedly improves reasoning with code-trained LMs, directly inspiring the paper’s code-like prompting strategy.

**Holistic Evaluation of Language Models** (2023)
- *Authors:* Percy Liang et al.
- *Direct Connection:* Reported that code-trained models consistently outperform text-only models on reasoning-heavy scenarios, motivating both the training-time code-centric augmentation and the inference-time alignment via code-like prompts.

### 🏷️ Gap Identification

**Language models are multilingual chain-of-thought reasoners** (2022)
- *Authors:* Freda Shi et al.
- *Direct Connection:* Revealed a multilingual reasoning gap and showed English chain-of-thought often outperforms native-language CoT, motivating a multilingual evaluation setting and techniques that bridge training–inference across languages.

### 🏷️ Extension

**Selection-Inference: Exploiting Large Language Models for Interpretable Logical Reasoning** (2023)
- *Authors:* Antonia Creswell et al.
- *Direct Connection:* Provided the select–infer loop that is adapted into single-prompt functions (select_facts and infer_new_fact) in the SIM prompting format to structure multi-step reasoning.

**Causal reasoning of entities and events in procedural texts** (2023)
- *Authors:* Li Zhang et al.
- *Direct Connection:* Inspired annotating function calls with inline comments specifying return values, a design adopted to make code prompts self-explanatory and align with the model’s code-trained representations.

---

## Synthesis: How Prior Work Led to This Paper

Structured reasoning graphs and their linearized instantiation were established by STREET, which curated expert multi-premise explanations and a graph-based, stepwise proof format for tasks like ARC science questions and GSM8K arithmetic. Multilingual chain-of-thought work showed that step-by-step prompting generalizes across languages but also uncovered a striking gap: English chain-of-thought often beats native-language prompting, pointing to a fundamental limitation in multilingual reasoning. In parallel, code-centric prompting demonstrated that casting natural language reasoning as code—especially for commonsense problems—improves performance with code-trained models, suggesting that code structures naturally scaffold multi-step inference. The Selection-Inference framework contributed a simple yet powerful select–infer loop for interpretable logical reasoning, while procedural text prompting work refined code prompt design by annotating function calls with inline comments and explicit return values to make prompts self-descriptive. Broader evaluations reported that models trained on code consistently outperform text-only models on reasoning-intensive tasks, strengthening the case for code as indirect supervision. Finally, The Stack offered a permissively licensed code corpus with rich comments to manipulate at scale.

Together, these works surfaced a clear opportunity: there was no multilingual benchmark with structured reasoning graphs, code-trained models benefited from code-aligned inputs, and multilingual prompting lagged English. The current paper synthesizes these insights by extending STREET into a six-language benchmark, designing a single-prompt Selection-Inference-inspired code format with inline return annotations to bridge training–inference representations, and augmenting a real code corpus by translating comments to create multilingual supervision without altering code. This combination naturally follows from prior findings and directly targets the multilingual reasoning gap while leveraging the demonstrated strengths of code-based reasoning.

---

*Analysis generated on: 2026-04-05T11:53:05.244935*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
