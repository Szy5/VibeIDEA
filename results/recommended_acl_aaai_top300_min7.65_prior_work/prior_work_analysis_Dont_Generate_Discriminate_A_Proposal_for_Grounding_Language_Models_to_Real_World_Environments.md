# Prior Work Analysis Report

## Target Paper

**Title:** Don’t Generate, Discriminate: A Proposal for Grounding Language Models to Real-World Environments

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> A key missing capacity of current language models (LMs) is grounding to real-world environments. Most existing work for grounded language understanding uses LMs to directly generate plans that can be executed in the environment to achieve the desired effects. It thereby casts the burden of ensuring grammaticality, faithfulness, and controllability all on the LMs. We propose Pangu, a generic framework for grounded language understanding that capitalizes on the discriminative ability of LMs instead of their generative ability. Pangu consists of a symbolic agent and a neural LM working in a concerted fashion: The agent explores the environment to incrementally construct valid plans, and the LM evaluates the plausibility of the candidate plans to guide the search process. A case study on the challenging problem of knowledge base question answering (KBQA), which features a massive environment, demonstrates the remarkable effectiveness and flexibility of Pangu: A BERT-base LM is sufficient for setting a new record on standard KBQA datasets, and larger LMs further bring substantial gains.Pangu also enables, for the first time, effective few-shot in-context learning for KBQA with large LMs such as Codex.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Semantic Parsing via Staged Query Graph Generation** (2015)
- *Authors:* Wen-tau Yih et al.
- *Direct Connection:* The staged enumerate-and-rank paradigm for KBQA—first generating valid query graph candidates from the KB and then ranking them—provides the foundational insight that Pangu extends with incremental environment-guided expansion and LM-based scoring.

### 🏷️ Inspiration

**Do as I Can, Not as I Say: Grounding Language in Robotic Affordances** (2022) [[arXiv](https://arxiv.org/abs/2204.01691)]
- *Authors:* Michael Ahn et al.
- *Direct Connection:* This work demonstrated using an LLM to score agent-proposed, affordance-valid actions, directly inspiring Pangu’s core design of leveraging an LM as a discriminator to guide symbolic search over candidate plans rather than generating them.

### 🏷️ Gap Identification

**Beyond I.I.D.: Three Levels of Generalization for Question Answering on Knowledge Bases** (2021)
- *Authors:* Yu Gu et al.
- *Direct Connection:* By establishing GRAILQA’s non-i.i.d. splits and showing that direct program generation struggles on large KBs, this work identified the generalization gap that Pangu targets by avoiding reliance on LMs to generate executable programs.

### 🏷️ Baseline

**ArcaneQA** (2022)
- *Authors:* Yu Gu and Yu Su
- *Direct Connection:* ArcaneQA’s constrained decoding over S-expressions ensured program validity in autoregressive KBQA, and Pangu directly addresses its remaining limitation by replacing token-level generation with plan-level discrimination while reusing the compact S-expression formalism.

**UnifiedSKG: Unifying and Multi-Tasking Structured Knowledge Grounding with Text-to-Text Transformers** (2022)
- *Authors:* Tianbao Xie et al.
- *Direct Connection:* UnifiedSKG exemplified input-augmented autoregressive plan generation across structured grounding tasks, whose lack of grammaticality/faithfulness guarantees motivated Pangu’s decoupling of validity (handled by a symbolic agent) from LM modeling (used only for scoring).

**RnG-KBQA: Retrieve-and-Generate for Knowledge Base Question Answering** (2022)
- *Authors:* Sitao Ye et al.
- *Direct Connection:* RnG-KBQA combined retrieval with generation and up-front candidate enumeration, highlighting both the utility of ranking and the limitations of exhaustive enumeration that Pangu overcomes with LM-guided incremental expansion in the environment.

### 🏷️ Extension

**SmBoP: Semi-autoregressive Bottom-up Semantic Parsing** (2021)
- *Authors:* Ohad Rubin et al.
- *Direct Connection:* SmBoP’s idea of incrementally constructing complex programs from subplans with bottom-up teacher forcing directly informed Pangu’s incremental search and training strategy, which it generalizes by discovering missing “ingredients” via environment exploration and using an LM solely to score (sub)plans.

---

## Synthesis: How Prior Work Led to This Paper

Bottom-up program construction proved effective in SmBoP, which incrementally built complex logical forms from subplans using bottom-up teacher forcing, showing that compositional assembly can reduce search complexity if good subplan scores are available. Earlier KBQA systems like Semantic Parsing via Staged Query Graph Generation established an enumerate-and-rank paradigm: generate valid query graphs from the KB and then rank them, but practical systems often enumerated up front, limiting program complexity. In robotics, Do as I Can, Not as I Say demonstrated a different leverage point for language models: use them to score affordance-valid actions proposed by an agent, indicating that LMs can act as powerful discriminators to steer decision making without owning low-level validity. Autoregressive KBQA advances such as ArcaneQA ensured grammaticality via constrained decoding over compact S-expressions yet still required token-level generation, while UnifiedSKG relied on input augmentation to prompt LMs to produce plans without strong guarantees. Retrieve-and-generate approaches like RnG-KBQA reinforced the benefit of ranking but also exposed the inefficiency and depth limits of exhaustive candidate enumeration. Concurrently, the GRAILQA benchmark showed that direct generation struggles in massive KBs and under non-i.i.d. generalization.
Together, these threads highlighted a natural opportunity: separate validity from language modeling by having a symbolic agent propose only valid candidates and let an LM do what it is best at—discriminate. Building on bottom-up construction, staged ranking, and action-scoring insights, the current work synthesizes a search agent that incrementally explores the environment to assemble executable plans while an LM scores (sub)plans to guide expansion and termination. This resolves the core limitations of autoregressive generation—faithfulness, grammaticality, and controllability—while retaining the flexibility and sample efficiency needed for robust generalization and few-shot adaptation.

---

*Analysis generated on: 2026-04-05T11:56:29.873441*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
