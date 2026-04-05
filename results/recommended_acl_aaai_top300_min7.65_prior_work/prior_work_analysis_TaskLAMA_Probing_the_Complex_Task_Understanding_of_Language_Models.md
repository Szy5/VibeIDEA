# Prior Work Analysis Report

## Target Paper

**Title:** TaskLAMA: Probing the Complex Task Understanding of Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Structured Complex Task Decomposition (SCTD) is the problem of breaking down a complex real-world task (such as planning a wedding) into a directed acyclic graph over individual steps that contribute to achieving the task, with edges specifying temporal dependencies between steps. SCTD is an important component of assistive planning tools, and a challenge for commonsense reasoning systems. We probe how accurately SCTD can be done with the knowledge extracted from pre-trained Large Language Models (LLMs). We introduce a new high-quality human-annotated dataset for this problem and novel metrics to fairly assess performance of LLMs against several baselines. Our experiments reveal that LLMs are able to decompose complex tasks into individual steps effectively, with a relative improvement of 15% to 280% over the best baseline. We also propose a number of approaches to further improve their performance, with a relative improvement of 7% to 37%. However, we find that LLMs still struggle to predict pairwise temporal dependencies, which reveals a gap in their understanding of complex tasks.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Language Models as Knowledge Bases?** (2019) [[arXiv](https://arxiv.org/abs/1909.01066)]
- *Authors:* Fabio Petroni et al.
- *Direct Connection:* Introduced the LAMA probing paradigm for extracting and evaluating latent knowledge in pretrained language models, providing the methodological template that this work extends to structured complex task knowledge.

### 🏷️ Inspiration

**Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents** (2022) [[arXiv](https://arxiv.org/abs/2201.07207)]
- *Authors:* Wenlong Huang et al.
- *Direct Connection:* Showed that LLMs can decompose simple goals into actionable sequences, directly motivating a probe of how far such latent procedural knowledge extends to complex, multi-step task graphs and temporal dependencies.

### 🏷️ Gap Identification

**Learning to Decompose and Organize Complex Tasks** (2021)
- *Authors:* Yiming Zhang et al.
- *Direct Connection:* Proposed a web-summarization approach for SCTD and popularized evaluation via one-to-many matching metrics that are vulnerable to duplicate inflation, a limitation this work explicitly fixes with Hungarian-based one-to-one matching while also drawing task seeds from their MSComplexTasks pool.

**Reasoning about Goals, Steps, and Temporal Ordering with WikiHow** (2020) [[arXiv](https://arxiv.org/abs/2009.07690)]
- *Authors:* Li Zhang et al.
- *Direct Connection:* Constructed procedural goal–step datasets from public web sources (WikiHow), highlighting contamination and coverage issues that this work addresses by collecting human-authored task graphs independent of public websites.

### 🏷️ Baseline

**Supporting Complex Search Tasks** (2014)
- *Authors:* Ahmed Hassan Awadallah et al.
- *Direct Connection:* Pioneered inferring task steps from search query co-occurrence, which is directly instantiated here as the 'Search Query Co-occurrence' baseline against which LLM-based methods are compared.

**Extracting Hierarchies of Search Tasks & Subtasks via a Bayesian Nonparametric Approach** (2017)
- *Authors:* Rishiraj S. Mehrotra and Emine Yilmaz
- *Direct Connection:* Introduced hierarchical clustering of queries to induce task–subtask structure, adopted here as the 'Search Query Hierarchy' baseline to benchmark against LLM-generated decompositions.

### 🏷️ Extension

**The Power of Scale for Parameter-Efficient Prompt Tuning** (2021) [[arXiv](https://arxiv.org/abs/2104.08691)]
- *Authors:* Brian Lester et al.
- *Direct Connection:* Introduced soft prompt tuning, which is adapted here to learn task-specific prompt embeddings for step and edge prediction, yielding the substantial gains reported for temporal dependency classification.

---

## Synthesis: How Prior Work Led to This Paper

Early work established that pretrained language models could be systematically probed for latent knowledge: Petroni et al. introduced LAMA, a template-based framework for extracting and evaluating what models know without task-specific finetuning. In procedural domains, Zhang, Lyu, and Callison-Burch leveraged WikiHow to assemble resources coupling goals, steps, and temporal ordering from public web data, demonstrating feasibility but raising concerns about training contamination and uneven coverage inherent to web extraction. For structured complex task decomposition, Zhang et al. (2021) advanced a summarization-based pipeline that organizes complex tasks into graphs from retrieved web pages and popularized node-evaluation metrics based on one-to-many matching, while the query-centric line of research by Awadallah et al. and Mehrotra and Yilmaz inferred steps and hierarchies from query co-occurrence and clustering to support task planning at web scale. Concurrently, Huang et al. showed that LLMs can function as zero-shot planners for simple goals, suggesting a rich latent procedural prior that could be tapped for more complex settings. Parameter-efficient prompt tuning from Lester et al. offered a way to specialize LLM behavior without full finetuning, a practical lever for improving structured predictions.
Together, these threads revealed an opportunity: probe LLMs directly for complex task graphs using a contamination-resistant, human-authored benchmark; correct metric pathologies from prior SCTD evaluations by enforcing one-to-one matching; and pit LLM-derived decompositions against representative query- and web-based baselines. By uniting LAMA-style probing with robust matching metrics and soft prompt tuning, the present work naturally extends prior insights, showing LLMs’ strength in step generation while exposing a persistent gap in pairwise temporal dependency understanding.

---

*Analysis generated on: 2026-04-05T11:58:42.622619*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
