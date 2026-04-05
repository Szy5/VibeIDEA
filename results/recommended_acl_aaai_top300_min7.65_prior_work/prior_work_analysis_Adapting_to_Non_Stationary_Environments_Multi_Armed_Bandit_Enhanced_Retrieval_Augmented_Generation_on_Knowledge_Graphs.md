# Prior Work Analysis Report

## Target Paper

**Title:** Adapting to Non-Stationary Environments: Multi-Armed Bandit Enhanced Retrieval-Augmented Generation on Knowledge Graphs

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Despite the superior performance of Large language models on many NLP tasks, they still face significant limitations in memorizing extensive world knowledge. Recent studies have demonstrated that leveraging the Retrieval-Augmented Generation (RAG) framework, combined with Knowledge Graphs that encapsulate extensive factual data in a structured format, robustly enhances the reasoning capabilities of LLMs. However, deploying such systems in real-world scenarios presents challenges: the continuous evolution of non-stationary environments may lead to performance degradation and user satisfaction requires a careful balance of performance and responsiveness. To address these challenges, we introduce a Multi-objective Multi-Armed Bandit enhanced RAG framework, supported by multiple retrieval methods with diverse capabilities under rich and evolving retrieval contexts in practice. Within this framework, each retrieval method is treated as a distinct "arm''. The system utilizes real-time user feedback to adapt to dynamic environments, by selecting the appropriate retrieval method based on input queries and the historical multi-objective performance of each arm. Extensive experiments conducted on two benchmark KGQA datasets demonstrate that our method significantly outperforms baseline methods in non-stationary settings while achieving state-of-the-art performance in station environments.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020) [[arXiv](https://arxiv.org/abs/2005.11401)]
- *Authors:* Lewis et al.
- *Direct Connection:* Introduced the RAG paradigm that this work directly builds upon by augmenting LLMs with external retrieval, which is here extended to knowledge-graph retrievers and dynamically selected via bandits.

### 🏷️ Inspiration

**Offline-to-Online Reinforcement Learning via Balanced Replay and Pessimistic Q-Ensemble** (2022)
- *Authors:* Lee et al.
- *Direct Connection:* Motivates the offline-to-online training protocol adopted here, where a selector is pre-trained offline and then adapted online using partial feedback to cope with non-stationary environments.

### 🏷️ Baseline

**ChatKBQA: A Generate-then-Retrieve Framework for Knowledge Base Question Answering with Fine-Tuned Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2310.08975)]
- *Authors:* Luo et al.
- *Direct Connection:* Provides the SPARQL-generation KG retrieval arm with high coverage but high latency that is explicitly included as an arm and whose latency–accuracy trade-off motivated the bandit-based, multi-objective selector.

**Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning** (2023) [[arXiv](https://arxiv.org/abs/2310.01061)]
- *Authors:* Luo et al.
- *Direct Connection:* Supplies the LLM agent-based KG retrieval arm with strong complex reasoning yet slow execution, directly framing the need for an adaptive router that can pick or avoid this arm based on context and multi-objective feedback.

### 🏷️ Extension

**Deep Contextual Multi-Armed Bandits** (2018) [[arXiv](https://arxiv.org/abs/1807.09809)]
- *Authors:* Collier et al.
- *Direct Connection:* Provides the deep contextual bandit formulation that is extended here by using a PLM-based query encoder and by incorporating multi-objective optimization with online updates to handle non-stationarity.

**Multi-Objective Bandits: Optimizing the Generalized Gini Index** (2017)
- *Authors:* Busa-Fekete et al.
- *Direct Connection:* Introduces the use of the Generalized Gini Index in bandit optimization, which is directly adopted to aggregate hit/recall and latency into a single objective guiding arm selection.

### 🏷️ Related Problem

**Bandit Based Optimization of Multiple Objectives on a Music Streaming Platform** (2020)
- *Authors:* Mehrotra et al.
- *Direct Connection:* Demonstrates practical multi-objective contextual bandit optimization (including GGI) to balance user-centric metrics, informing the design choice to balance accuracy, coverage, and delay in online selection.

---

## Synthesis: How Prior Work Led to This Paper

Retrieval-augmented generation established the template for coupling a generator with external knowledge access, enabling factual grounding during generation. Within knowledge graph question answering, two complementary retrieval styles emerged: generate-then-execute SPARQL systems such as ChatKBQA that achieve broad coverage via executable graph queries at the cost of multiple LLM calls and latency, and LLM agent-based graph reasoning, as in Reasoning on Graphs, which excels on complex, multi-hop questions but similarly incurs substantial delays. In parallel, deep contextual bandits showed that non-linear encoders can map rich contexts to arm choices under partial-feedback, addressing scenarios where simple linear models fail to capture complex patterns. For decision-making with multiple competing goals, multi-objective bandits introduced the Generalized Gini Index as a principled scalarization, and platform-scale work demonstrated how contextual bandits with GGI can balance user-facing trade-offs among objectives. Finally, offline-to-online reinforcement learning advanced a practical recipe for pretraining policies offline and adapting them online with streaming feedback to handle distribution shift.
Combining these strands revealed an opportunity: treat heterogeneous KG retrieval methods as arms whose strengths and costs vary by query, learn a deep contextual router that can be pre-trained offline and updated online from user feedback, and use a GGI-based scalarization to balance accuracy, coverage, and latency. This synthesis naturally yields a bandit-enhanced KG-RAG system that adapts to non-stationary demands and backend changes while routing each query to the most suitable retriever under multi-objective constraints.

---

*Analysis generated on: 2026-04-05T11:39:10.114645*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
