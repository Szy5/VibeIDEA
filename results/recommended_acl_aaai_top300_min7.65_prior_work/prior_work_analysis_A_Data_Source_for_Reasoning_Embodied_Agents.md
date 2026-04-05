# Prior Work Analysis Report

## Target Paper

**Title:** A Data Source for Reasoning Embodied Agents

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent progress in using machine learning models for reasoning tasks has been driven by novel model architectures, large-scale pre-training protocols, and dedicated reasoning datasets for fine-tuning. In this work, to further pursue these advances, we introduce a new data generator for machine reasoning that integrates with an embodied agent. The generated data consists of templated text queries and answers, matched with world-states encoded into a database. The world-states are a result of both world dynamics and the actions of the agent. We show the results of several baseline models on instantiations of train sets. These include pre-trained language models fine-tuned on a text-formatted representation of the database, and graph-structured Transformers operating on a knowledge-graph representation of the database. We find that these models can answer some questions about the world-state, but struggle with others. These results hint at new research directions in designing neural reasoning models and database representations. Code to generate the data and train the models will be released at github.com/facebookresearch/neuralmemory

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**droidlet: modular, heterogenous, multi-modal agents** (2021)
- *Authors:* Pratik et al.
- *Direct Connection:* This work provides the 3D agent environment, object-centered key–value memory with memids/triples, and scripted task executor that are directly used to generate the world states and agent actions underpinning our context–query–answer triples.

**Embodied Question Answering** (2018)
- *Authors:* Abhishek Das et al.
- *Direct Connection:* By formulating QA in an embodied setting and tying questions to an agent’s environment, it established the embodied QA paradigm that we adopt while abstracting perception to focus on memory and reasoning.

### 🏷️ Inspiration

**CLEVR: A Diagnostic Dataset for Compositional Language and Elementary Visual Reasoning** (2017)
- *Authors:* Justin Johnson et al.
- *Direct Connection:* Its programmatic, template-based question generation over fully known scenes directly inspired our approach of templated queries grounded in a structured scene representation.

**CLEVRER: CoLlision Events for Video REpresentation and Reasoning** (2020) [[arXiv](https://arxiv.org/abs/1910.01442)]
- *Authors:* Kexin Yi et al.
- *Direct Connection:* Its emphasis on reasoning over temporal events motivated our inclusion of multi-snapshot contexts and temporal query types (e.g., who moved farthest, location at time).

**Database Reasoning Over Text** (2021) [[arXiv](https://arxiv.org/abs/2106.01074)]
- *Authors:* James Thorne et al.
- *Direct Connection:* It demonstrated that textifying database contents and leveraging pretrained LMs can execute queries, directly informing our choice to provide a textual dump of the agent memory and a language-model baseline.

### 🏷️ Gap Identification

**PIGLET: Language grounding through neuro-symbolic interaction in a 3D world** (2021) [[arXiv](https://arxiv.org/abs/2106.00188)]
- *Authors:* Rowan Zellers et al.
- *Direct Connection:* While introducing a 3D neuro-symbolic grounding environment, it provided only a few labeled QA examples and relied on unsupervised transitions, highlighting the need for a generator that yields large numbers of labeled QA grounded in agent-alterable worlds.

### 🏷️ Extension

**CraftAssist instruction parsing: Semantic parsing for a voxel-world assistant** (2020)
- *Authors:* Kavya Srinet et al.
- *Direct Connection:* We reuse and adapt its voxel-world grammar to programmatically produce our templated query texts and logical forms that operate over the agent’s memory.

---

## Synthesis: How Prior Work Led to This Paper

A line of work established that synthetic, programmatically generated questions can precisely probe compositional reasoning over fully specified scenes; CLEVR introduced template-based question generation against structured scene graphs, while CLEVRER extended this idea to temporal events that unfold over time, emphasizing dynamics-aware reasoning. In parallel, embodied QA framed question answering within interactive environments, embedding queries in the context of an agent’s world and actions. Neuro-symbolic efforts like PIGLET grounded language in a 3D world with structured state representations and dynamics, but provided few labeled QA examples, focusing instead on leveraging unsupervised transitions. On the systems side, droidlet offered a practical 3D agent platform with an object-centered key–value memory (memids and triples) and scripted executors, enabling reliable manipulation and recording of agent-affected world states. CraftAssist’s instruction-parsing grammar for a voxel world supplied a concrete mechanism for generating well-formed, grounded language utterances over such memories. Concurrently, database reasoning over text showed that flattening structured stores into textual form allows pretrained language models to serve as neural query executors.
These threads jointly revealed an opportunity: create a scalable source of labeled QA grounded in dynamic, agent-alterable worlds, while abstracting perception to focus on memory and reasoning, and support both textualized and structured representations. Building atop droidlet’s memory and executors and CraftAssist’s grammar, and drawing from CLEVR/CLEVRER’s templated diagnostics and EmbodiedQA’s embodied framing, the current work synthesizes a data generator that emits context–query–answer triples over multi-snapshot worlds, enabling direct comparison of LM-based textified reasoning and relational-structured transformers, and systematically exposing gaps in spatial and temporal reasoning for embodied agents.

---

*Analysis generated on: 2026-04-05T11:54:30.705058*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
