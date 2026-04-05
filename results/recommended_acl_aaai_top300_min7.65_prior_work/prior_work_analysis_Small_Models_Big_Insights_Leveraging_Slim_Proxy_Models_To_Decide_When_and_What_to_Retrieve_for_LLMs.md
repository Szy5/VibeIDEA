# Prior Work Analysis Report

## Target Paper

**Title:** Small Models, Big Insights: Leveraging Slim Proxy Models To Decide When and What to Retrieve for LLMs

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> The integration of large language models (LLMs) and search engines represents a significant evolution in knowledge acquisition methodologies.However, determining the knowledge that an LLM already possesses and the knowledge that requires the help of a search engine remains an unresolved issue.Most existing methods solve this problem through the results of preliminary answers or reasoning done by the LLM itself, but this incurs excessively high computational costs.This paper introduces a novel collaborative approach, namely SlimPLM, that detects missing knowledge in LLMs with a slim proxy model, to enhance the LLM's knowledge acquisition process.We employ a proxy model which has far fewer parameters, and take its answers as heuristic answers.Heuristic answers are then utilized to predict the knowledge required to answer the user question, as well as the known and unknown knowledge within the LLM.We only conduct retrieval for the missing knowledge in questions that the LLM does not know.Extensive experimental results on five datasets with two LLMs demonstrate a notable improvement in the end-to-end performance of LLMs in question-answering tasks, achieving or surpassing current state-of-the-art models with lower LLM inference costs.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories** (2023)
- *Authors:* Alex Mallen et al.
- *Direct Connection:* Findings that retrieval can degrade performance when unnecessary foreground the core problem of retrieval necessity prediction that SlimPLM tackles using a proxy-generated heuristic answer.

### 🏷️ Inspiration

**ReAct: Synergizing Reasoning and Acting in Language Models** (2023)
- *Authors:* Shunyu Yao et al.
- *Direct Connection:* ReAct’s practice of turning intermediate generated thoughts into search queries directly inspires SlimPLM’s conversion of a generated heuristic answer into aspect-specific retrieval queries.

**Query Rewriting for Retrieval-Augmented Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.14283)]
- *Authors:* Xinbei Ma et al.
- *Direct Connection:* Evidence that specialized query rewriting improves RAG informs SlimPLM’s dedicated rewrite module, which uniquely conditions rewriting on the proxy model’s heuristic answer rather than the raw user query.

**FactScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation** (2023)
- *Authors:* Sewon Min et al.
- *Direct Connection:* SlimPLM adapts FactScore’s claim decomposition idea by breaking the heuristic answer into atomic claims to drive fine-grained query generation and claim-level retrieval filtering.

### 🏷️ Gap Identification

**Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection** (2023) [[arXiv](https://arxiv.org/abs/2310.11511)]
- *Authors:* Akari Asai et al.
- *Direct Connection:* Self-RAG shows retrieval control via model-internal signals but requires fine-tuning the main LLM, a computational and forgetting risk that SlimPLM addresses by offloading retrieval decisions to a small proxy without tuning the target LLM.

### 🏷️ Baseline

**Active Retrieval Augmented Generation** (2023)
- *Authors:* Zhengbao Jiang et al.
- *Direct Connection:* FLARE’s strategy of triggering retrieval when generation logits are low and using masked sentences as queries is directly supplanted by SlimPLM’s use of a proxy model’s heuristic answer to both decide retrieval necessity and derive targeted, claim-level queries with fewer main-LLM passes.

**Language Models (Mostly) Know What They Know** (2022) [[arXiv](https://arxiv.org/abs/2207.05221)]
- *Authors:* Saurav Kadavath et al.
- *Direct Connection:* The self-evaluation idea that LMs can judge when they know an answer motivates SlimPLM’s retrieval decision, but SlimPLM replaces costly self-judgment by the target LLM with a slim proxy plus a fine-tuned judgment model to cut inference cost.

---

## Synthesis: How Prior Work Led to This Paper

Work on active retrieval augmented generation demonstrated that retrieval need not be static: FLARE showed how low generation logits can trigger retrieval and how masked text can serve as retrieval queries, linking generation-time signals to both when and what to retrieve. Complementing this, evidence that language models can assess what they know introduced self-evaluation as a practical basis for retrieval decisions, albeit at the cost of additional main-model inference. Self-RAG then formalized retrieval control via reflection tokens, but required fine-tuning the large model, raising efficiency and forgetting concerns. Parallel advances showed that generated intermediate content can be repurposed as search queries—as in ReAct’s thought-action loops—while dedicated query rewriting, rather than raw questions, consistently improves retrieval quality. Finally, claim decomposition methods such as FactScore established that complex answers can be broken into atomic statements, offering a natural unit for fine-grained evaluation and targeting. Empirical analyses also showed that retrieval can harm when unnecessary, highlighting the need for accurate retrieval necessity prediction.
Taken together, these works revealed two intertwined opportunities: decide retrieval without repeatedly invoking or fine-tuning the main LLM, and formulate sharper, aspect-specific queries grounded in the model’s reasoning. SlimPLM synthesizes these insights by delegating decision and query planning to a slim proxy: it uses a proxy-generated heuristic answer to train a lightweight judgment model for when retrieval is needed, decomposes that answer into claims to determine what to retrieve, and filters at the claim level—achieving state-of-the-art effectiveness while reducing target LLM compute.

---

*Analysis generated on: 2026-04-05T11:53:04.589941*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
