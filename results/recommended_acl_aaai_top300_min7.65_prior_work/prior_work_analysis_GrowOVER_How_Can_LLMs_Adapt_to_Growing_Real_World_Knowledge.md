# Prior Work Analysis Report

## Target Paper

**Title:** GrowOVER: How Can LLMs Adapt to Growing Real-World Knowledge?

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> In the real world, knowledge is constantly evolving, which can render existing knowledge-based datasets outdated.This unreliability highlights the critical need for continuous updates to ensure both accuracy and relevance in knowledgeintensive tasks.To address this, we propose GrowOVER-QA and GrowOVER-Dialogue, dynamic open-domain QA and dialogue benchmarks that undergo a continuous cycle of updates, keeping pace with the rapid evolution of knowledge.Our research indicates that retrieval-augmented language models (RaLMs) struggle with knowledge that has not been trained on or recently updated.Consequently, we introduce a novel retrieval-interactive language model framework, where the language model evaluates and reflects on its answers for further re-retrieval.Our exhaustive experiments demonstrate that our training-free framework significantly improves upon existing methods, performing comparably to or even surpassing continuously trained language models.QA & Dialogue New : D1-Turn1 [153], D1-Turn2 [154] QA1.What is Lionel Messi's all-time rank in goals scored from direct free?Old A.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**TemporalWiki: A Lifelong Benchmark for Training and Evaluating Ever-Evolving Language Models** (2022) [[arXiv](https://arxiv.org/abs/2204.14211)]
- *Authors:* Joel Jang et al.
- *Direct Connection:* TemporalWiki established the paradigm of constructing time-evolving benchmarks from successive Wikipedia snapshots, directly defining the temporal evaluation setting that this paper generalizes to QA and dialogue with maintenance of instances over time.

### 🏷️ Inspiration

**Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection** (2023)
- *Authors:* Akari Asai et al.
- *Direct Connection:* Self-RAG’s idea of using reflection signals to assess relevance/support inspired this paper’s Decision Gate that scores answer reliability, while avoiding LLM finetuning by training only a lightweight certainty classifier.

### 🏷️ Gap Identification

**Carpe Diem: On the Evaluation of World Knowledge in Lifelong Language Models** (2023) [[arXiv](https://arxiv.org/abs/2311.08106)]
- *Authors:* Yujin Kim et al.
- *Direct Connection:* Carpe Diem introduced automatically generated, temporally updated QA from Wikipedia/Wikidata but lacked annotated evidence texts and dataset maintenance, gaps that this paper explicitly addresses in GrowOVER by providing evidence for retriever evaluation and verifying validity across updates.

**Realtime QA: What’s the Answer Right Now?** (2022) [[arXiv](https://arxiv.org/abs/2207.13332)]
- *Authors:* Jungo Kasai et al.
- *Direct Connection:* RealtimeQA showed that even with updated corpora, LMs often answer with outdated knowledge when retrieval fails, directly motivating this paper’s retrieval-interactive loop where the LLM evaluates and guides re-retrieval to avoid stale answers.

### 🏷️ Baseline

**In-Context Retrieval-Augmented Language Models** (2023) [[arXiv](https://arxiv.org/abs/2302.00083)]
- *Authors:* Ori Ram et al.
- *Direct Connection:* This work’s concatenation-based in-context RAG prompting is the primary baseline that the proposed RiLM framework improves upon by gating answer adoption and adaptively re-retrieving without continual pretraining.

### 🏷️ Extension

**Active Retrieval Augmented Generation** (2023)
- *Authors:* Zhengbao Jiang et al.
- *Direct Connection:* Active RAG introduced using the model’s generated continuations to refine retrieval queries, which this paper extends by weighting the influence of generated answers on re-retrieval proportionally to an estimated reliability score.

**REPLUG: Retrieval-Augmented Black-Box Language Models** (2023) [[arXiv](https://arxiv.org/abs/2301.12652)]
- *Authors:* Weijia Shi et al.
- *Direct Connection:* REPLUG’s per-document prompting and selection is directly adopted and extended here by adding a certainty classifier to choose the most reliable document-answer pair and integrating it into an interactive re-retrieval loop.

---

## Synthesis: How Prior Work Led to This Paper

TemporalWiki crystallized the notion that evaluating language models under temporal drift requires benchmarks built from successive knowledge snapshots, setting up a time-aware testing regime. Carpe Diem advanced automatic construction of temporally updated QA from Wikipedia/Wikidata, revealing practical mechanisms for snapshot differencing but omitting evidence passages and ongoing maintenance. RealtimeQA demonstrated that even with fresh corpora, outdated parametric knowledge can leak into answers when retrieval misses, highlighting the need for systems that can detect and correct unreliable retrieval. On the method side, In-Context RAG established a strong, training-free baseline by prompting LLMs with retrieved documents, while REPLUG refined this by prompting per document and aggregating outputs. Self-RAG introduced reflection signals to judge support and completeness, suggesting a self-evaluation step could steer retrieval and generation. Active RAG showed that using generated text to adapt retrieval queries can improve long-form generation, hinting at a feedback loop between generation and retrieval. Collectively, these works surfaced a gap: dynamic, time-sensitive evaluation lacked evidence annotations and maintenance for retriever assessment, and RAG pipelines remained brittle when retrieval failed or model knowledge was stale. The natural next step was to pair a dynamic benchmark that preserves and verifies instances with evidence, and a retrieval-interactive framework that self-assesses answer reliability and uses it to modulate re-retrieval. By integrating per-document prompting with a certainty-based Decision Gate and a reliability-weighted query update, the current work operationalizes reflection without LLM finetuning, improving adaptation to new and changed knowledge while remaining training-light.

---

*Analysis generated on: 2026-04-05T11:55:45.260017*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
