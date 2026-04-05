# Prior Work Analysis Report

## Target Paper

**Title:** TARGA: Targeted Synthetic Data Generation for Practical Reasoning over Structured Data

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Semantic parsing, which converts natural language questions into logic forms, plays a crucial role in reasoning within structured environments.However, existing methods encounter two significant challenges: reliance on extensive manually annotated datasets and limited generalization capability to unseen examples.To tackle these issues, we propose Targeted Synthetic Data Generation (TARGA), a practical framework that dynamically generates high-relevance synthetic data without manual annotation.Starting from the pertinent entities and relations of a given question, we probe for the potential relevant queries through layer-wise expansion and cross-layer combination.Then we generate corresponding natural language questions for these constructed queries to jointly serve as the synthetic demonstrations for in-context learning.Experiments on multiple knowledge base question answering (KBQA) datasets demonstrate that TARGA, using only a 7B-parameter model, substantially outperforms existing non-finetuned methods that utilize close-sourced model, achieving notable improvements in F1 scores on GrailQA (+7.7) and KBQA-Agent (+12.2).Furthermore, TARGA also exhibits superior sample efficiency, robustness, and generalization capabilities under non-I.I.D. settings.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Beyond I.I.D.: Three levels of generalization for question answering on knowledge bases** (2021)
- *Authors:* Yu Gu et al.
- *Direct Connection:* GrailQA defined the I.I.D., compositional, and zero-shot generalization splits that frame TARGA’s core goal of improving non-I.I.D. performance without manual annotation.

### 🏷️ Inspiration

**Bring your own KG: Self-supervised program synthesis for zero-shot KGQA** (2024)
- *Authors:* Dhruv Agarwal et al.
- *Direct Connection:* BYOKG demonstrated that executable query programs can be synthesized without manual annotation to supervise KGQA, an idea TARGA adopts but makes question-targeted and online rather than offline and static.

**KQA Pro: A dataset with explicit compositional programs for complex question answering over knowledge base** (2022)
- *Authors:* Shulin Cao et al.
- *Direct Connection:* KQA Pro popularized the pipeline of first sampling structured queries and then verbalizing them, which TARGA leverages while introducing targeted query construction via layer-wise expansion and cross-layer combination.

### 🏷️ Gap Identification

**Few-shot in-context learning on knowledge base question answering** (2023)
- *Authors:* Tianle Li et al.
- *Direct Connection:* KB-Binder’s reliance on retrieving similar annotated examples from a static training set—and its documented performance drop on zero-shot/compositional splits—explicitly motivates TARGA’s online per-question synthesis to avoid distribution bias.

**FlexKBQA: A flexible LLM-powered framework for few-shot knowledge base question answering** (2023) [[arXiv](https://arxiv.org/abs/2308.12060)]
- *Authors:* Zhenyu Li et al.
- *Direct Connection:* FlexKBQA’s template-driven auto-annotation and multi-stage training require a time-consuming offline data collection phase, a limitation TARGA addresses by dynamically synthesizing relevant examples at test time.

### 🏷️ Baseline

**Code-style in-context learning for knowledge-based question answering** (2023) [[arXiv](https://arxiv.org/abs/2309.04695)]
- *Authors:* Zhijie Nie et al.
- *Direct Connection:* KB-Coder provides the primary ICL baseline that retrieves annotated (question, code-style logic form) pairs, which TARGA directly replaces with targeted synthetic (NLQ, Query) pairs to guide generation and improve non-I.I.D. generalization.

### 🏷️ Extension

**MarkQA: A large scale KBQA dataset with numerical reasoning** (2023)
- *Authors:* Xiang Huang et al.
- *Direct Connection:* MarkQA introduced the PyQL program representation and query-to-text generation paradigm that TARGA directly uses and extends with relevance-driven search, textification, and re-ranking for per-question synthesis.

---

## Synthesis: How Prior Work Led to This Paper

Retrieval-driven in-context KBQA methods such as KB-Binder retrieve annotated (question, logic-form) demonstrations from a static training pool, and KB-Coder refines this by using code-style logic forms to better steer generation; however, both methods explicitly report sharp degradations under compositional and zero-shot settings because similar examples are absent from the pre-collected corpus. In parallel, FlexKBQA automates annotation with templates and training phases but requires a costly offline data collection pipeline, and BYOKG shows that one can synthesize executable query programs and verbalize them to supervise KGQA without annotation, although it also assembles a static synthetic set offline. KQA Pro established the practical pipeline of sampling structured queries first and then generating natural language for them, demonstrating the value of program-first supervision. MarkQA operationalized this approach at scale, introducing the PyQL representation and query-to-text generation that make program synthesis and verbalization tractable. Finally, the GrailQA benchmark crystallized the I.I.D., compositional, and zero-shot generalization regimes, exposing the brittleness of static-data approaches. Taken together, these works reveal a gap: retrieval from static annotated or synthetic sets fails on out-of-distribution questions, yet constructing executable programs and verbalizing them can replace manual labels. The natural next step is to synthesize demonstrations online, conditioned on each test question. Building on program-first supervision (KQA Pro, MarkQA) and the feasibility of synthetic programs (BYOKG) while addressing the static-data limitation (KB-Binder, KB-Coder, FlexKBQA), the current paper designs a targeted, question-conditioned query exploration (layer-wise expansion and cross-layer combination), followed by textification and re-ranking, to produce highly relevant (NLQ, Query) pairs for in-context learning without any manual annotation.

---

*Analysis generated on: 2026-04-05T12:06:24.176489*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
