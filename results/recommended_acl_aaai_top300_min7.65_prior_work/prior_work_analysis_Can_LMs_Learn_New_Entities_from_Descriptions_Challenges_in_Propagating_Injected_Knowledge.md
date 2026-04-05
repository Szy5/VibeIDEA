# Prior Work Analysis Report

## Target Paper

**Title:** Can LMs Learn New Entities from Descriptions? Challenges in Propagating Injected Knowledge

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Pre-trained language models (LMs) are used for knowledge intensive tasks like question answering, but their knowledge gets continuously outdated as the world changes. Prior work has studied targeted updates to LMs, injecting individual facts and evaluating whether the model learns these facts while not changing predictions on other contexts. We take a step forward and study LMs' abilities to make inferences based on injected facts (or propagate those facts): for example, after learning that something is a TV show, does an LM predict that you can watch it? We study this with two cloze-style tasks: an existing dataset of real-world sentences about novel entities (ECBD) as well as a new controlled benchmark with manually designed templates requiring varying levels of inference about injected knowledge. Surprisingly, we find that existing methods for updating knowledge (gradient-based fine-tuning and modifications of this approach) show little propagation of injected knowledge. These methods improve performance on cloze instances only when there is lexical overlap between injected facts and target inferences. Yet, prepending entity definitions in an LM's context improves performance across all settings, suggesting that there is substantial headroom for parameter-updating approaches for knowledge injection.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Modifying Memories in Transformer Models** (2020) [[arXiv](https://arxiv.org/abs/2012.00363)]
- *Authors:* Chen Zhu et al.
- *Direct Connection:* It introduced core model-editing evaluation notions—edit success and locality—that underpin the update-success and specificity metrics used to assess definition-based propagation.

**Entity Cloze By Date: What LMs know about unseen entities** (2022)
- *Authors:* Yasumasa Onoe et al.
- *Direct Connection:* ECBD provides the cloze-by-date setup with unseen entities and paired definition/probe sentences, serving as the principal benchmark repurposed to evaluate whether injected definitions propagate to diverse inferences.

### 🏷️ Inspiration

**Prompt Injection: Parameterization of Fixed Inputs** (2022) [[arXiv](https://arxiv.org/abs/2206.11349)]
- *Authors:* Eunbi Choi et al.
- *Direct Connection:* Their finding that prepending information can outperform fine-tuning directly motivates using in-context definition prepending as a strong baseline and practical upper bound for propagation.

### 🏷️ Gap Identification

**Editing Factual Knowledge in Language Models** (2021) [[arXiv](https://arxiv.org/abs/2104.08164)]
- *Authors:* Nicola De Cao et al.
- *Direct Connection:* This work frames knowledge editing with evaluations focused on paraphrase preservation and locality, a limitation explicitly addressed by shifting evaluation to whether definition-based edits enable downstream inference propagation.

### 🏷️ Baseline

**Fast Model Editing at Scale** (2022) [[arXiv](https://arxiv.org/abs/2110.11309)]
- *Authors:* Eric Mitchell et al.
- *Direct Connection:* MEND’s one-step hypernetwork-based edits are directly used as a primary knowledge-editing baseline to test whether updates from entity definitions can generalize beyond paraphrases to downstream inferences.

**Locating and Editing Factual Associations in GPT** (2022) [[arXiv](https://arxiv.org/abs/2202.05262)]
- *Authors:* Kevin Meng et al.
- *Direct Connection:* ROME’s rank-one rewrites of MLP layers are evaluated as a competing editing method by formatting definition-derived prompts into subject–relation–object edits to assess whether such localized rewrites support propagation for new entities.

### 🏷️ Related Problem

**Probing Factually Grounded Content Transfer with Factual Ablation** (2022)
- *Authors:* Peter West et al.
- *Direct Connection:* By showing that descriptions can drive consistent generation about entities without parameter updates, this work motivates testing whether parameter updates from descriptions yield comparable consistency and propagation.

---

## Synthesis: How Prior Work Led to This Paper

Model editing methods have focused on updating specific facts while preserving unrelated behavior, with evaluation centered on paraphrase generalization and locality. Fast Model Editing at Scale (MEND) introduced a hypernetwork that transforms gradients into one-step parameter edits, demonstrating effective, localized changes and establishing a practical baseline for efficient factual updates. Locating and Editing Factual Associations in GPT (ROME) showed that factual associations can be localized in MLP layers and overwritten via rank-one weight rewrites, enabling targeted subject–relation–object edits. Editing Factual Knowledge in Language Models formalized the task of altering factual knowledge with minimal interference and evaluated on paraphrase variants, while Modifying Memories in Transformer Models codified edit success and locality metrics that became standard for assessing edits. Entity Cloze By Date (ECBD) introduced a cloze benchmark centered on entities unseen at pretraining time, pairing definition sentences with diverse probe sentences to test knowledge of emerging entities in a temporally controlled setting. Concurrently, work on factually grounded content transfer showed that supplying descriptions can induce consistent generations without parameter changes, and findings on prompt injection indicated that prepending information can rival or exceed fine-tuning. Together, these threads revealed a gap: editing methods excel at preserving edited facts and paraphrases but do not test whether knowledge injected from descriptions supports downstream inferences. Building on ECBD’s unseen-entity paradigm, the metrics from early editing work, and strong evidence that descriptions and in-context augmentation can steer models, the present study formulates entity knowledge propagation and introduces a controlled benchmark to isolate inference from exact recall. It systematically evaluates MEND, ROME, and fine-tuning against in-context definition prepending, exposing that current parameter-updating methods yield little propagation beyond lexical overlap and establishing headroom for future editing approaches tailored to definitional knowledge and inference.

---

*Analysis generated on: 2026-04-05T12:00:03.256856*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
