# Prior Work Analysis Report

## Target Paper

**Title:** Explore What LLM Does Not Know in Complex Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Complex question answering (QA) is a challenging task in artificial intelligence research which requires reasoning based on related knowledge. The retrieval-augmented generation (RAG) based on large language models (LLMs) have become one promising solution in QA. To facilitate RAG more effectively, the LLM needs to precisely evaluate knowledge required in QA. That is, first, the LLM needs to examine its knowledge boundary (what the LLM does not know) to retrieve external knowledge as supplement. Second, the LLM needs to evaluate the utility of the retrieved knowledge (whether it helps in reasoning) for robust RAG. To this end, in this paper, we propose a novel Question Answering with Knowledge Evaluation (KEQA) framework to promote the effectiveness and efficiency of RAG in QA. First, inspired by quizzes in classroom, we propose a quiz-based method to precisely examine the knowledge state of the uninterpretable LLM for QA. We ask indicative quizzes on each required knowledge, and inspect whether the LLM can consistently answer the quiz to examine its knowledge boundary. Second, we retrieve the unknown knowledge from external source, and evaluate its utility to pick the helpful ones for reasoning. We design a reasoning-based metric to evaluate utility, and construct a demonstration set in training data for reference to guide knowledge picking in inference. We conduct extensive experiments on four widely-used QA datasets, and the results demonstrate the effectiveness of the proposed method.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020) [[arXiv](https://arxiv.org/abs/2005.11401)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* Established the core RAG paradigm of retrieving external passages and conditioning generation on them, which defines the knowledge-augmented QA setting that KEQA seeks to make more accurate and efficient by deciding when and what to retrieve.

### 🏷️ Inspiration

**Least-to-Most Prompting Enables Complex Reasoning in Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2205.10625)]
- *Authors:* Denny Zhou et al.
- *Direct Connection:* Demonstrated decomposing complex questions into simpler sub-questions, directly informing KEQA’s use of decomposition to construct indicative quizzes that isolate single knowledge atoms for evaluation.

### 🏷️ Gap Identification

**Active Retrieval Augmented Generation** (2023)
- *Authors:* Zexuan Jiang et al.
- *Direct Connection:* Introduced probability-based gating to trigger retrieval only when needed, whose reliance on token probabilities and focus on uncertainty rather than specific missing knowledge motivated KEQA’s quiz-based, black-box-compatible knowledge boundary assessment.

**Investigating the Factual Knowledge Boundary of Large Language Models with Retrieval Augmentation** (2023) [[arXiv](https://arxiv.org/abs/2307.11019)]
- *Authors:* Ruiqi Ren et al.
- *Direct Connection:* Showed that LLMs are over-confident and can misclassify unknowns as known even with retrieval, highlighting the need for precise knowledge boundary diagnostics that KEQA addresses via quizzes and consistency.

**Making Retrieval-Augmented Generation Robust to Irrelevant Retrieval Results** (2024)
- *Authors:* Yoran et al.
- *Direct Connection:* Focused on robustness to irrelevant documents mainly via relevancy filtering, underscoring the unmet need to assess utility for reasoning—which KEQA fills by defining a correctness-based utility signal and a demo-guided utility discriminator.

### 🏷️ Baseline

**Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions** (2023)
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* Provided the iterative pipeline that interleaves retrieval with reasoning for multi-step QA, serving as a primary baseline that KEQA improves by retrieving only for unknown sub-knowledge and filtering to helpful documents.

### 🏷️ Extension

**Self-Consistency Improves Chain of Thought Reasoning in Language Models** (2023)
- *Authors:* Xuezhi Wang et al.
- *Direct Connection:* Inspired KEQA’s consistency-based mastery test by extending self-consistency from final-answer voting to semantic-consistency checks across multiple quiz attempts to infer whether the LLM actually knows a required fact.

---

## Synthesis: How Prior Work Led to This Paper

Retrieval-augmented generation established that supplementing generators with external passages can improve knowledge-intensive QA, setting the stage for methods that combine retrieval and reasoning. Building on that paradigm, interleaving approaches for multi-step questions retrieved evidence at intermediate reasoning steps, but generally assumed that more retrieval helps. Active gating methods refined this by triggering retrieval only when generation appeared uncertain based on token probabilities, yet this reliance on model internals and token-level uncertainty left open how to identify exactly which missing facts to fetch, especially for black-box models. Meanwhile, least-to-most prompting showed that decomposing complex questions into simpler sub-questions can isolate the reasoning steps, and self-consistency revealed that aggregating multiple samples provides a robust signal about model beliefs. Complementing these advances, studies on LLM knowledge boundaries documented systematic overconfidence, indicating that self-reported or probability-based judgments can mischaracterize what the model truly knows. Efforts to make RAG robust to irrelevant documents emphasized improving relevancy, but left the deeper question of whether a retrieved item actually increases reasoning correctness largely unaddressed.
Together these threads reveal a gap: precise, black-box-compatible diagnostics of what knowledge is missing, and selection of retrieved items by their causal utility for reasoning rather than mere relevancy. The present work synthesizes decomposition to form single-knowledge quizzes, applies self-consistency as a mastery signal to determine when to retrieve, and operationalizes utility as correctness improvement to pick helpful evidence via demonstration-guided discrimination. This combination naturally advances RAG by retrieving only the unknown and only what helps, yielding both better accuracy and efficiency.

---

*Analysis generated on: 2026-04-05T11:53:17.435150*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
