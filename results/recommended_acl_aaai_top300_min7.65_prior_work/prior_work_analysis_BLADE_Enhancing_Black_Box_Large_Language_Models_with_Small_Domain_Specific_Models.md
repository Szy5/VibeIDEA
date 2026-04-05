# Prior Work Analysis Report

## Target Paper

**Title:** BLADE: Enhancing Black-Box Large Language Models with Small Domain-Specific Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLMs) like ChatGPT and GPT-4 are versatile and capable of addressing open-domain question-answering(QA) tasks effectively. However, general LLMs, which are developed on open-domain data, may lack the domain-specific knowledge essential for tasks in vertical domains, such as legal, medical, etc. To address this issue, previous approaches either conduct continuous pre-training with domain-specific data or employ retrieval augmentation to support general LLMs in handling QA tasks. Unfortunately, these strategies are either cost-intensive or unreliable in practical applications. To this end, we present a novel framework named BLADE, which enhances Black-box LArge language models with small Domain-spEcific models. BLADE consists of a black-box LLM and a small domain-specific LM. The small LM preserves domain-specific knowledge and offers specialized insights, while the general LLM contributes robust language comprehension and reasoning capabilities. Specifically, our method involves three steps: 1) pre-training the small LM with domain-specific data, 2) fine-tuning this model using knowledge instruction data, and 3) joint Bayesian optimization of the general LLM and the small LM. In our experiments, we verify the effectiveness of BLADE on diverse LLMs and datasets across different domains. This shows the potential of BLADE as an effective and cost-efficient solution in adapting general LLMs for vertical domains.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020) [[arXiv](https://arxiv.org/abs/2005.11401)]
- *Authors:* Patrick Lewis et al.
- *Direct Connection:* This work established the core paradigm of concatenating retrieved passages with inputs to improve knowledge-intensive tasks, which BLADE rethinks by supplying generated domain knowledge in place of retrieval.

### 🏷️ Inspiration

**Generate rather than retrieve: Large language models are strong context generators** (2022) [[arXiv](https://arxiv.org/abs/2209.10063)]
- *Authors:* Wenhao Yu et al.
- *Direct Connection:* This paper showed that LLM-generated contextual passages can substitute retrieval, directly inspiring BLADE’s use of a generator to provide task-specific context for a downstream black-box LLM.

### 🏷️ Baseline

**Replug: Retrieval-augmented black-box language models** (2023) [[arXiv](https://arxiv.org/abs/2301.12652)]
- *Authors:* Wenda Shi et al.
- *Direct Connection:* RePlug treated the LLM as a black box enhanced by a retriever; BLADE adopts the same black-box setting but replaces the retriever with a small, domain-pretrained generator to overcome reliance on semantic retrieval.

### 🏷️ Extension

**Black-box tuning for language-model-as-a-service** (2022)
- *Authors:* Tianxiang Sun et al.
- *Direct Connection:* BBT introduced low-dimensional, derivative-free optimization of soft prompts via random projections and CMA-ES, which BLADE’s Bayesian Prompted Optimization adopts and tailors to tune the small LM’s soft embeddings to maximize black-box LLM performance.

**InstructZero: Efficient Instruction Optimization for Black-Box Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2306.03082)]
- *Authors:* Linjie Chen et al.
- *Direct Connection:* InstructZero’s GP-based Bayesian optimization for black-box prompt search motivates BLADE’s EI-guided optimization loop to iteratively select soft prompts that best improve a black-box LLM’s task metric via the small LM.

**Promptagator: Few-shot dense retrieval from 8 examples** (2022) [[arXiv](https://arxiv.org/abs/2209.11755)]
- *Authors:* Zhuyun Dai et al.
- *Direct Connection:* Promptagator’s consistency-based filtering of synthetic data inspired BLADE’s Knowledge Instruction Tuning to retain only generated knowledge that causes the black-box LLM to answer correctly.

### 🏷️ Related Problem

**Recitation-augmented language models** (2022) [[arXiv](https://arxiv.org/abs/2210.01296)]
- *Authors:* Zihan Sun et al.
- *Direct Connection:* By demonstrating that prompting an LM to recite relevant facts improves QA, this work informed BLADE’s strategy of producing targeted knowledge before answer synthesis.

---

## Synthesis: How Prior Work Led to This Paper

Retrieval-Augmented Generation (RAG) formalized enhancing language models by concatenating retrieved passages with the input to tackle knowledge-intensive tasks, providing a clear template for injecting external knowledge. Building on this, RePlug showed how to treat the language model strictly as a black box augmented by a retriever, but also exposed brittleness due to retrievers’ dependence on exact or semantic matches. In parallel, work on generated contexts demonstrated that large language models can synthesize contextual passages to replace retrieval, while recitation-augmented models showed that prompting a model to produce relevant facts prior to answering can measurably improve QA. On the optimization front, Black-Box Tuning (BBT) introduced low-dimensional, derivative-free optimization of soft prompts via random projections and CMA-ES for models accessible only through APIs, and InstructZero brought GP-based Bayesian optimization to efficiently search instruction prompts for black-box LLMs. For data quality, Promptagator’s consistency filtering ensured that only synthetic items that led to correct outcomes were kept, providing a practical mechanism to curate self-generated supervision.
Collectively, these works revealed both the promise and the limitations of retrieval augmentation, suggested replacing retrieval with generated knowledge, and supplied practical black-box optimization and filtering tools. The natural next step was to pair a small, domain-pretrained generator with a general black-box LLM, instruction-tune the generator using consistency-filtered knowledge, and then optimize its soft prompts via a BO-guided, low-dimensional derivative-free search so that the generated knowledge maximally boosts the black-box LLM’s task performance—precisely the synthesis realized in BLADE.

---

*Analysis generated on: 2026-04-05T11:59:12.773393*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
