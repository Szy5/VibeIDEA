# Prior Work Analysis Report

## Target Paper

**Title:** Union Is Strength! Unite the Power of LLMs and MLLMs for Chart Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Chart Question Answering (CQA) requires models to perform chart perception and reasoning. Recent studies driven by Large Language Models (LLMs) have dominated CQA. These include employing more cognitively capable LLMs for indirectly reasoning over transformed charts, i.e., tables, and directly perceiving charts utilizing Multimodal Large Language Models (MLLMs) with a wider perceptual range. Yet, they often encounter bottlenecks due to the limitation of the receptive field of LLMs and the fragility of the complex reasoning of some MLLMs. To unite the strengths of LLMs and MLLMs to complement each other's limitations, we propose Synergy, a framework that unites the power of both models for CQA. Synergy first unites the chart with a table as the augmented perceptual signal. Next, it unites LLMs and MLLMs, scheduling the former to decompose a question into subquestions and the latter to answer these by perceiving the chart. Lastly, it operates LLMs to summarize the subquestion-answer pairs to refine the final answer. Extensive experimental results on popular CharQA and PlotQA benchmarks reveal that, with the power of union, Synergy outperforms strong competitors and achieves superior boosts over naive MLLMs by uniting them with a smaller LLM.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**DePlot: One-shot Visual Language Reasoning by Plot-to-Table Translation** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2212.10505)]
- *Authors:* F. Liu et al.
- *Direct Connection:* Synergy directly uses DePlot as its chart2table module to extract accurate numerical tables and builds on DePlot’s chart-to-table paradigm by augmenting MLLM inputs with both the chart image and DePlot’s JSON table.

**ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning** (2022) [[arXiv](https://arxiv.org/abs/arXiv:2203.10244)]
- *Authors:* A. Masry et al.
- *Direct Connection:* ChartQA defined the CQA task with human and augmented splits requiring combined visual perception and numerical/logical reasoning, providing the core problem setting and evaluation bed for Synergy.

**PlotQA: Reasoning over Scientific Plots** (2020)
- *Authors:* N. Methani et al.
- *Direct Connection:* PlotQA introduced large-scale plot understanding with fine-grained numerical questions, forming the numerical reasoning benchmark (via PlotQA-sub) that Synergy targets to demonstrate its perception–reasoning integration.

### 🏷️ Gap Identification

**Do LLMs Work on Charts? Designing Few-Shot Prompts for Chart Question Answering and Summarization (PROMPTCHART)** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2312.10610)]
- *Authors:* X. L. Do et al.
- *Direct Connection:* PROMPTCHART exposed information loss in chart-to-table conversion and attempted to add textual visual cues, directly motivating Synergy’s solution of feeding MLLMs the original chart alongside the table to recover color and spatial cues.

**CogVLM: Visual Expert for Pretrained Language Models** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2311.03079)]
- *Authors:* W. Wang et al.
- *Direct Connection:* CogVLM showed that aligning LLMs with multimodal data weakens their pure-text reasoning, underpinning Synergy’s design choice to delegate cognition-heavy steps (decomposition and verification) to a native LLM while reserving perception for an MLLM.

**MME: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models** (2024) [[arXiv](https://arxiv.org/abs/arXiv:2306.13394)]
- *Authors:* C. Fu et al.
- *Direct Connection:* MME documented fragile and inconsistent reasoning chains in MLLMs, directly motivating Synergy’s final LLM-based summary-verification stage over subquestion-answer pairs.

### 🏷️ Extension

**DOMINO: A Dual-System for Multi-step Visual Language Reasoning** (2023) [[arXiv](https://arxiv.org/abs/arXiv:2310.02804)]
- *Authors:* P. Wang et al.
- *Direct Connection:* Synergy extends DOMINO’s dual-system pipeline—LLM-based question decomposition with a separate answering agent—by replacing DEPLOT-only answering with an MLLM that cross-perceives chart+table and adding an LLM verifier to refine the final answer without any fine-tuning.

---

## Synthesis: How Prior Work Led to This Paper

DePlot established the plot-to-table translation paradigm that enabled language models to reason over charts in textual form, providing accurate numerical extraction but inherently discarding visual cues. PROMPTCHART highlighted this information-loss problem and attempted to mitigate it by injecting textual surrogates for visual attributes (e.g., color), underscoring that table-only representations miss critical spatial and stylistic signals. DOMINO introduced a dual-system pipeline in which an LLM decomposes a complex question and a specialized answering module resolves subqueries on tabular inputs, demonstrating that decomposition can unlock multi-step visual-language reasoning but still relying on table-only perception and supervised fine-tuning. In parallel, CogVLM showed that multimodal alignment can erode the underlying LLM’s textual reasoning, revealing a tension between perception and cognition capacities in MLLMs. Complementing this, the MME benchmark documented brittle and inconsistent reasoning chains in MLLMs, pointing to the need for external verification to ensure reliable conclusions. ChartQA and PlotQA formalized chart QA as a combined perception–numerical reasoning problem, with human-authored and numerically intensive splits, respectively, that stress both visual fidelity and multi-step arithmetic. Together, these works indicated an opportunity: retain the strong textual cognition of LLMs, leverage MLLMs’ broader perception without losing visual cues, and add a mechanism to check fragile chains. Synergy naturally emerges by augmenting MLLM perception with both chart images and extracted tables, using an LLM to decompose questions into chart-grounded subqueries, delegating subquery answering to the MLLM, and finally employing an LLM verifier to summarize and correct subquestion-answer paths into a robust final answer.

---

*Analysis generated on: 2026-04-05T12:05:47.756028*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
