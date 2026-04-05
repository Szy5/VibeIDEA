# Prior Work Analysis Report

## Target Paper

**Title:** Knowledge Graph Prompting for Multi-Document Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> The `pre-train, prompt, predict' paradigm of large language models (LLMs) has achieved remarkable success in open-domain question answering (OD-QA). However, few works explore this paradigm in multi-document question answering (MD-QA), a task demanding a thorough understanding of the logical associations among the contents and structures of documents. To fill this crucial gap, we propose a Knowledge Graph Prompting (KGP) method to formulate the right context in prompting LLMs for MD-QA, which consists of a graph construction module and a graph traversal module. For graph construction, we create a knowledge graph (KG) over multiple documents with nodes symbolizing passages or document structures (e.g., pages/tables), and edges denoting the semantic/lexical similarity between passages or document structural relations. For graph traversal, we design an LLM-based graph traversal agent that navigates across nodes and gathers supporting passages assisting LLMs in MD-QA. The constructed graph serves as the global ruler that regulates the transitional space among passages and reduces retrieval latency. Concurrently, the graph traversal agent acts as a local navigator that gathers pertinent context to progressively approach the question and guarantee retrieval quality. Extensive experiments underscore the efficacy of KGP for MD-QA, signifying the potential of leveraging graphs in enhancing the prompt design and retrieval augmented generation for LLMs. Our code: https://github.com/YuWVandy/KG-LLM-MDQA.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Inspiration

**Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions** (2022) [[arXiv](https://arxiv.org/abs/2212.10509)]
- *Authors:* Harsh Trivedi et al.
- *Direct Connection:* KGP’s LLM-based traversal agent that alternates between generating intermediate evidence and selecting the next context node is inspired by IRCoT’s retrieval–reasoning interleaving, but grounds the steps in an explicit document graph to control the search space and latency.

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* KGP leverages the CoT insight that explicit intermediate reasoning improves stepwise problem solving by having the agent generate the “next evidence” at each hop, which then guides graph traversal toward answer-bearing passages.

**Learning to Retrieve Reasoning Paths over Wikipedia Graph for Question Answering** (2019) [[arXiv](https://arxiv.org/abs/1911.10470)]
- *Authors:* Akari Asai et al.
- *Direct Connection:* KGP extends the idea of path-based multi-hop retrieval on a graph by generalizing from Wikipedia hyperlink graphs to a document-derived knowledge graph with lexical/semantic and structural edges and an LLM-guided traversal policy.

### 🏷️ Gap Identification

**Beyond Chain-of-Thought, Effective Graph-of-Thought Reasoning in Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.16582)]
- *Authors:* Yao Yao et al.
- *Direct Connection:* KGP addresses the computational and latency burdens highlighted by Graph-of-Thought methods by replacing unconstrained thought graphs with a document-grounded knowledge graph that constrains expansions and speeds retrieval.

**Dense Passage Retrieval for Open-Domain Question Answering** (2020) [[arXiv](https://arxiv.org/abs/2004.04906)]
- *Authors:* Vlad Karpukhin et al.
- *Direct Connection:* KGP explicitly tackles DPR’s limitation of treating evidence selection as single-hop query–passage matching by modeling and traversing multi-hop logical associations between passages via an explicit graph and step-conditioned selection.

### 🏷️ Extension

**Answering Complex Open-Domain Questions with Multi-hop Dense Retrieval** (2020) [[arXiv](https://arxiv.org/abs/2009.12756)]
- *Authors:* Wenhan Xiong et al.
- *Direct Connection:* KGP directly adopts MDR’s next-supporting-fact prediction objective to (i) train the passage encoder used to build its KNN graph and (ii) instruction-tune its traversal agent, explicitly injecting multi-hop reasoning signals into both graph construction and step selection.

**Knowledge Guided Text Retrieval and Reading for Open Domain Question Answering** (2019) [[arXiv](https://arxiv.org/abs/1911.03868)]
- *Authors:* Sewon Min et al.
- *Direct Connection:* Building on entity-aware retrieval (e.g., TAGME-based linking) from this work, KGP incorporates entity overlap as edges by linking passages that share detected Wikipedia entities to form an entity-informed subgraph for traversal.

---

## Synthesis: How Prior Work Led to This Paper

Multi-hop retrievers demonstrated that predicting the next supporting fact conditions retrieval on previously gathered evidence, with MDR formalizing a sequential training objective that imbues encoders with reasoning signals. Interleaving retrieval with stepwise reasoning, IRCoT showed that LLMs can generate intermediate thoughts to steer evidence acquisition, while Chain-of-Thought revealed that explicit intermediate steps reliably improve reasoning quality. Graph-of-Thought further framed reasoning as structured search over thought states, but also surfaced the cost of unconstrained back-and-forth prompting. Earlier graph-based QA work retrieved paths over a Wikipedia hyperlink graph, proving that graph traversal can expose multi-hop evidence chains. Complementing these ideas, entity-aware retrieval used linkers such as TAGME to connect text via shared entities, furnishing a principled signal for graph connectivity beyond raw lexical overlap. Dense Passage Retrieval, though strong for single-hop matching, highlighted a gap by ignoring the sequential structure of evidence, often failing on tasks that require ordered, multi-document hops.
Taken together, these works suggested a natural next step: constrain stepwise LLM reasoning within a document-grounded graph whose edges encode lexical, semantic, and entity relations, and learn to pick the next hop using a multi-hop objective. The resulting synthesis replaces free-form, costly thought expansion with an LLM traversal agent that generates the next evidence and selects neighbors in a compact knowledge graph, extending MDR’s supervision to both embeddings and traversal while leveraging CoT-style intermediate reasoning and entity signals to efficiently gather high-quality, multi-document context.

---

*Analysis generated on: 2026-04-05T11:39:01.060311*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
