# Prior Work Analysis Report

## Target Paper

**Title:** Evaluating LLM Reasoning in the Operations Research Domain with ORQA

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> In this paper, we introduce and apply Operations Research Question Answering (ORQA), a new benchmark, to assess the generalization capabilities of Large Language Models (LLMs) in the specialized technical domain of Operations Research (OR). This benchmark is designed to evaluate whether LLMs can emulate the knowledge and reasoning skills of OR experts when given diverse and complex optimization problems. The dataset, crafted by OR experts, presents real-world optimization problems that require multistep reasoning to build their mathematical models. Our evaluations of various open-source LLMs, such as LLaMA 3.1, DeepSeek, and Mixtral reveal their modest performance, indicating a gap in their aptitude to generalize to specialized technical domains. This work contributes to the ongoing discourse on LLMs’ generalization capabilities, providing insights for future research in this area. The dataset and evaluation code are publicly available.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**NL4OPT competition: Formulating optimization problems based on their natural language descriptions** (2022)
- *Authors:* R. Ramamonjison et al.
- *Direct Connection:* NL4OPT introduced the concrete task of mapping natural-language problem descriptions to optimization models, which ORQA directly adopts but reframes as multiple-choice identification of model components to enable fine-grained, solver-free evaluation.

**Modelling in Mathematical Programming** (2021)
- *Authors:* J. M. G. Sánchez et al.
- *Direct Connection:* ORQA’s question taxonomy and annotations directly instantiate Sánchez et al.’s decomposition of optimization models into elements, decision activities, data attributes, objectives, and specifications.

### 🏷️ Inspiration

**Leveraging large language models for multiple choice question answering** (2023)
- *Authors:* J. Robinson et al.
- *Direct Connection:* ORQA’s evaluation harness borrows Robinson and Wingate’s symbol-binding MCQ protocol (binding options to A–D and appending a standardized 'Therefore...' cue) to robustly parse model outputs.

### 🏷️ Gap Identification

**OptiMUS: Scalable Optimization Modeling with (MI)LP Solvers and Large Language Models** (2024)
- *Authors:* A. AhmadiTeshnizi et al.
- *Direct Connection:* By showing that solver-based, end-to-end evaluations confound modeling with code-generation errors (21–31%), OptiMUS/NLP4LP directly motivated ORQA’s design as a multiple-choice benchmark that isolates modeling comprehension from coding and solving.

**Chain-of-Experts: When LLMs Meet Complex Operations Research Problems** (2023)
- *Authors:* Z. Xiao et al.
- *Direct Connection:* ComplexOR’s small size (37 problems), narrow domain coverage, and frequent naming of canonical problems highlighted the need for a larger, context-rich, jargon-free OR benchmark that ORQA addresses.

**PlanBench: An Extensible Benchmark for Evaluating Large Language Models on Planning and Reasoning about Change** (2023)
- *Authors:* K. Valmeekam et al.
- *Direct Connection:* The critique that existing reasoning benchmarks are overly simplistic and the call for more challenging, structured tasks directly motivated ORQA’s expert-crafted, multi-step reasoning questions in a technical domain.

**Optimization modeling and verification from problem specifications using a multi-agent multi-stage LLM framework** (2024)
- *Authors:* M. Mostajabdaveh et al.
- *Direct Connection:* Empirically finding that SOTA LLMs achieved only modest performance on optimization modeling in a practical pipeline exposed evaluation blind spots and directly prompted the creation of ORQA as a diagnostic benchmark focused on the modeling step.

---

## Synthesis: How Prior Work Led to This Paper

Work on natural language to optimization modeling first coalesced around NL4OPT, which formalized converting textual problem descriptions into mathematical models, establishing the concrete mapping that subsequent efforts explored. Sánchez and colleagues provided a practitioner-grounded decomposition of optimization models—elements, decision activities, data attributes, objectives, and specifications—that offered an actionable schema for breaking down modeling tasks. As researchers pushed LLMs into OR, the NLP4LP/OptiMUS effort revealed that end-to-end evaluation—requiring code generation and solving—entangled modeling ability with implementation errors, even quantifying substantial coding failure rates. ComplexOR demonstrated a more realistic direction by pairing natural language with models, but its limited size, narrow domain coverage, and frequent explicit naming of canonical problems underscored scale and contamination issues. In parallel, the LLM evaluation community showed that MCQ protocols can be made parse-robust via simple output-format cues and answer-symbol binding, as exemplified by Robinson and Wingate. At the same time, benchmarking studies like PlanBench argued that many reasoning datasets were too simple and called for more challenging, structured reasoning tasks.
Collectively, these insights exposed a gap: a large, expert-curated, context-rich OR benchmark that tests multi-step modeling reasoning without confounding code or solvers, grounded in a principled component taxonomy and supported by robust MCQ evaluation. ORQA synthesizes these threads by adopting NL4OPT’s problem formulation, instantiating Sánchez et al.’s component schema as question types, addressing OptiMUS and ComplexOR’s dataset and evaluation limitations, and operationalizing a reliable MCQ protocol inspired by Robinson and Wingate to deliver a challenging, domain-specific reasoning benchmark.

---

*Analysis generated on: 2026-04-05T12:02:07.880827*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
