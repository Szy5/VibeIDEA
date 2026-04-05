# Prior Work Analysis Report

## Target Paper

**Title:** ANALOGYKB: Unlocking Analogical Reasoning of Language Models with A Million-scale Knowledge Base

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> ANALOGYKB: Unlocking Analogical Reasoning of Language Models with A Million-scale Knowledge Base

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**On Defining Analogy** (1959)
- *Authors:* Mary B. Hesse
- *Direct Connection:* Hesse’s account that analogous relations can be justified by induction to a shared higher-level (meta) relation directly underpins the paper’s Rule 2 filter that accepts a relation pair only if an LLM can summarize them into a common meta relation.

**Analogical reasoning** (2017)
- *Authors:* Dedre Gentner and Francisco Maravilla
- *Direct Connection:* The structural alignment view of analogy articulated by Gentner and Maravilla grounds the paper’s notion of analogous relations (e.g., CEO and head of state) via abstraction to a meta relation like head of organization.

**Wikidata: A free collaborative knowledgebase** (2014)
- *Authors:* Denny Vrandečić and Markus Krötzsch
- *Direct Connection:* Wikidata supplies the large-scale subject–predicate–object triples and pageview signals that the paper directly reorganizes into same-relation analogies and ranks for inclusion in ANALOGYKB.

**ConceptNet 5.5: An Open Multilingual Graph of General Knowledge** (2017) [[arXiv](https://arxiv.org/abs/1612.03975)]
- *Authors:* Robyn Speer et al.
- *Direct Connection:* ConceptNet provides high-quality commonsense relation pairs (filtered by edge weights) that are directly converted into same-relation analogies and used to seed the discovery of analogous relation pairs.

### 🏷️ Inspiration

**Training language models to follow instructions with human feedback** (2022) [[arXiv](https://arxiv.org/abs/2203.02155)]
- *Authors:* Long Ouyang et al.
- *Direct Connection:* The instruction-following capabilities of InstructGPT directly enable the paper’s LLM-driven pipeline for selecting analogous relation candidates and inducing meta relations via in-context prompts with minimal human effort.

### 🏷️ Gap Identification

**Does Wikidata Support Analogical Reasoning?** (2022)
- *Authors:* Filip Ilievski et al.
- *Direct Connection:* By examining analogical structure in Wikidata with relatively small-scale experiments, this paper highlighted both feasibility and limitations, motivating a comprehensive, large-scale analogy resource built from Wikidata.

### 🏷️ Extension

**A Data-Driven Approach for Making Analogies** (2017)
- *Authors:* Mei Si and Craig Carlson
- *Direct Connection:* This work showed how to derive analogies from encyclopedia KG relations, which the current paper generalizes by systematizing relation-pair discovery and scaling to million-level analogies, including analogous-relation cases.

---

## Synthesis: How Prior Work Led to This Paper

Several strands of prior work laid the groundwork for constructing large-scale analogy resources from structured knowledge. Wikidata and ConceptNet established rich repositories of subject–predicate–object triples and commonsense relations; their scope, popularity signals, and edge weights offered immediately usable, high-quality relation–entity pairs suited for forming analogies within the same relation. Theoretical accounts of analogy emphasized structural alignment and abstraction: Hesse’s criterion that two relations are analogous if they can be induced into a shared meta relation, and Gentner and Maravilla’s view of relational mapping, together provided a principled basis for determining when distinct relations should be considered analogous via higher-level schemas (e.g., head of organization). Empirically, Si and Carlson demonstrated that analogies can be constructed from encyclopedia knowledge graphs, while Ilievski and colleagues showed Wikidata contains analogical structure yet prior explorations remained small and limited. Meanwhile, instruction-following language models, exemplified by InstructGPT, showed that LLMs can reliably execute few-shot in-context tasks such as selective matching and abstraction, suggesting a scalable way to automate relation-pair discovery. Collectively, these works exposed an opportunity: KGs make same-relation analogies readily extractable, theory prescribes how to validate analogous relations via meta-abstraction, and LLMs can operationalize this validation at scale. The current paper synthesizes these insights by harvesting same-relation analogies from ConceptNet and Wikidata, then using an instruction-following LLM to propose analogous relation pairs and induce their shared meta relations, with symmetry and meta-relation filters ensuring quality. This combination naturally yields a million-scale, high-quality analogy knowledge base that fills the data scarcity gap and enables both training and prompting for analogical reasoning.

---

*Analysis generated on: 2026-04-05T11:54:52.701382*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
