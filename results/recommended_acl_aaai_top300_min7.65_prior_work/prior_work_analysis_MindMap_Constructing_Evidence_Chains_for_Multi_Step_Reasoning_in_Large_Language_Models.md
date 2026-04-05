# Prior Work Analysis Report

## Target Paper

**Title:** MindMap: Constructing Evidence Chains for Multi-Step Reasoning in Large Language Models

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large language models (LLMs) have demonstrated remarkable performance in various natural language processing tasks. However, they still face significant challenges in automated reasoning, particularly in scenarios involving multi-step reasoning. In this paper, we focus on the logical reasoning problem. The main task is to answer a question based on a set of available facts and rules. A lot of work has focused on guiding LLMs to think logically by generating reasoning paths, ignoring the structure among available facts. In this paper, we propose a simple approach MindMap by introducing evidence chains for supporting reasoning. An evidence chain refers to a set of facts that involve the same subject. In this way, we can organize related facts together to avoid missing important information. MindMap can be integrated with existing reasoning framework, such as Chain-of-Thought (CoT) and Selection-Inference (SI), by letting the model select relevant evidence chains instead of independent facts. The experimental results on the bAbI and ProofWriterOWA datasets demonstrate the effectiveness of MindMap.It can significantly improve CoT and SI, especially in multi-step reasoning tasks.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks (bAbI)** (2016) [[arXiv](https://arxiv.org/abs/1502.05698)]
- *Authors:* Jason Weston et al.
- *Direct Connection:* bAbI provides the multi-step, temporally ordered fact-based QA setting with annotated supporting facts that MindMap reorganizes into subject-centric chains to better retrieve and integrate the necessary evidence.

**ProofWriter: Generating Implications, Proofs, and Abductive Statements over Natural Language** (2021) [[arXiv](https://arxiv.org/abs/unknown)]
- *Authors:* Oyvind Tafjord et al.
- *Direct Connection:* ProofWriter (including the OWA setting) defines the natural-language facts-and-rules entailment problem with varying proof depths that MindMap adopts, operating by organizing facts into chains to improve multi-step inference fidelity.

### 🏷️ Inspiration

**Unsupervised Learning of Narrative Event Chains** (2008) [[arXiv](https://arxiv.org/abs/unknown)]
- *Authors:* Nate Chambers et al.
- *Direct Connection:* The protagonist-centered narrative event chain concept explicitly inspired MindMap’s core idea of constructing subject-based ‘evidence chains’ by extracting subjects and grouping all associated events/facts around them.

### 🏷️ Gap Identification

**Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought** (2023) [[arXiv](https://arxiv.org/abs/unknown)]
- *Authors:* Amir Saparov et al.
- *Direct Connection:* This analysis shows CoT’s greedy, locally myopic reasoning that can overlook globally relevant evidence, directly motivating MindMap’s grouping of related facts into chains to mitigate missed-information errors across steps.

### 🏷️ Baseline

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* MindMap plugs into CoT by selecting and feeding subject-centric evidence chains rather than isolated facts, directly addressing CoT’s tendency to treat facts independently and miss related information when generating reasoning paths.

### 🏷️ Extension

**Selection-Inference: Exploiting Large Language Models for Interpretable Logical Reasoning** (2023) [[arXiv](https://arxiv.org/abs/unknown)]
- *Authors:* Antonia Creswell et al.
- *Direct Connection:* MindMap directly extends SI by modifying its selection step to choose and iteratively update subject-centric evidence chains instead of individual facts, while retaining SI’s separate inference loop to reduce hallucination and improve coverage.

---

## Synthesis: How Prior Work Led to This Paper

Chain-of-Thought prompting established that prompting models to produce step-by-step rationales can elicit reasoning, but in practice it often treats each fact independently and may miss related information scattered across a context. Selection-Inference then separated selection from inference, iteratively choosing relevant facts and updating the context to curb hallucinations; yet its selection granularity remained at the individual-fact level, which can still lead to omissions when related facts are distributed across a narrative. Earlier work on narrative event chains introduced the idea of organizing events around a protagonist entity, demonstrating that clustering predicate–argument mentions by shared subjects captures coherent event structure. The bAbI tasks defined a controlled, multi-step QA setting with temporally ordered facts and explicit supporting facts, making clear the need to retrieve and integrate multiple, related pieces of evidence. ProofWriter framed natural-language entailment over facts and rules with varying proof depths, including open-world assumptions that demand faithful aggregation of all pertinent premises to justify True, False, or Unknown conclusions. Formal analysis of Chain-of-Thought showed that language models tend to be greedy reasoners, favoring locally plausible steps while overlooking globally pertinent evidence.
Building on these insights, a natural opportunity emerged to change the unit of selection from isolated facts to coherent, subject-centric clusters. By extracting subjects and grouping all associated facts into evidence chains—optionally summarized for compactness—one can feed more complete, organized evidence into reasoning. Integrating this chain selection into CoT and SI leverages their strengths while directly addressing their documented omissions, yielding a straightforward next step toward more faithful multi-step reasoning.

---

*Analysis generated on: 2026-04-05T11:37:54.191952*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
