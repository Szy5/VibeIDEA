# Prior Work Analysis Report

## Target Paper

**Title:** Fact-Driven Logical Reasoning for Machine Reading Comprehension

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent years have witnessed an increasing interest in training machines with reasoning ability, which deeply relies on accurately and clearly presented clue forms. The clues are usually modeled as entity-aware knowledge in existing studies. However, those entity-aware clues are primarily focused on commonsense, making them insufficient for tasks that require knowledge of temporary facts or events, particularly in logical reasoning for reading comprehension. To address this challenge, we are motivated to cover both commonsense and temporary knowledge clues hierarchically. Specifically, we propose a general formalism of knowledge units by extracting backbone constituents of the sentence, such as the subject-verb-object formed ``facts''. We then construct a supergraph on top of the fact units, allowing for the benefit of sentence-level (relations among fact groups) and entity-level interactions (concepts or actions inside a fact). Experimental results on logical reasoning benchmarks and dialogue modeling datasets show that our approach improves the baselines substantially, and it is general across backbone models. Code is available at https://github.com/ozyyshr/FocalReasoner.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**ReClor: A Reading Comprehension Dataset Requiring Logical Reasoning** (2020) [[arXiv](https://arxiv.org/abs/2002.04326)]
- *Authors:* Wenpeng Yu et al.
- *Direct Connection:* This work defines the exam-style logical reasoning MRC setting that foregrounds hypothetical and temporary facts, providing the primary benchmark on which the fact-driven supergraph approach is evaluated and motivated.

**LogiQA: A Challenge Dataset for Machine Reading Comprehension with Logical Reasoning** (2020)
- *Authors:* Jian Liu et al.
- *Direct Connection:* This dataset further formalizes logical reasoning in MRC with LSAT/GMAT-style questions, serving as a second foundational benchmark exposing the need to capture sentence-level relations and transient facts.

### 🏷️ Gap Identification

**MERIt: Meta-Path Guided Contrastive Learning for Logical Reasoning** (2022) [[arXiv](https://arxiv.org/abs/2203.00357)]
- *Authors:* Fangzhou Jiao et al.
- *Direct Connection:* By focusing on entity/phrase-level meta-paths without explicit sentence-level relations, MERIt highlights the gap our method fills by connecting fact units across sentences to capture broader logical structures and temporary facts.

### 🏷️ Baseline

**DAGN: Discourse-Aware Graph Network for Logical Reasoning** (2021)
- *Authors:* Yutao Huang et al.
- *Direct Connection:* DAGN’s use of discourse (EDU) graphs for sentence-level reasoning is the main prior system our method surpasses, and its limitation of lacking entity-level interactions directly motivates our hierarchical fact-unit supergraph.

### 🏷️ Extension

**Modeling Hierarchical Reasoning Chains by Linking Discourse Units and Key Phrases for Reading Comprehension** (2022)
- *Authors:* Jian Chen et al.
- *Direct Connection:* This work’s idea of jointly modeling inter- and intra-sentence interactions inspires our extension to a hierarchical design where discourse units/phrases are replaced by subject–verb–object fact units linked in a supergraph.

**Translating Embeddings for Modeling Multi-relational Data** (2013)
- *Authors:* Antoine Bordes et al.
- *Direct Connection:* The TransE translation principle directly informs our logical fact regularization v_subject + v_predicate ≈ v_object, used to enforce factual coherence of extracted SVO fact units in representation space.

**Encoding Sentences with Graph Convolutional Networks for Semantic Role Labeling** (2017)
- *Authors:* Diego Marcheggiani and Ivan Titov
- *Direct Connection:* Their Levi-graph-style node treatment and edge-typed GCN (default/reverse/self) are directly adapted and extended by us to direction-sensitive edge types inside each fact unit’s inner graph.

---

## Synthesis: How Prior Work Led to This Paper

Exam-style logical reasoning tasks were crystallized by ReClor and LogiQA, where questions from GMAT/LSAT stress evaluating arguments that hinge on relationships among facts and often involve hypothetical or transient events. DAGN established discourse-aware reasoning by building graphs over elementary discourse units to capture sentence-level relations, but it did not explicitly model entity-level interactions within those units. Building on this trend, HGN introduced a hierarchical design linking discourse units with key phrases to capture both inter- and intra-sentence interactions, signaling the utility of hierarchical structures for reasoning. MERIt advanced entity-centric modeling via meta-paths among logical variables (entities and phrases) using contrastive learning, yet left sentence-level relational structures implicit and did not target temporary facts. At the representation level, Marcheggiani and Titov’s use of Levi-graph-style node conversions and edge-typed GCNs provided a practical template for encoding relation-labeled structures, while TransE’s translational triple constraint delivered a simple but powerful way to regularize (head, relation, tail) coherence in embedding space. Together these works showed that reasoning benefits from structured units and relational propagation but also revealed a gap: discourse- and entity-focused methods separately miss a unified carrier for both commonsense and transient knowledge. The natural next step was to formalize subject–verb–object fact units as general knowledge carriers, encode each as a Levi-form inner graph with enriched edge types, and integrate them hierarchically via a supergraph that links units across sentences (including coreference and identical mentions), with a TransE-inspired regularizer ensuring factual consistency—thereby jointly capturing entity- and sentence-level logical interactions essential for exam-style reasoning.

---

*Analysis generated on: 2026-04-05T12:00:13.336695*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
