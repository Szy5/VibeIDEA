# Prior Work Analysis Report

## Target Paper

**Title:** Journey to the Center of the Knowledge Neurons: Discoveries of Language-Independent Knowledge Neurons and Degenerate Knowledge Neurons

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Pre-trained language models (PLMs) contain vast amounts of factual knowledge, but how the knowledge is stored in the parameters remains unclear. This paper delves into the complex task of understanding how factual knowledge is stored in multilingual PLMs, and introduces the Architecture-adapted Multilingual Integrated Gradients method, which successfully localizes knowledge neurons more precisely compared to current methods, and is more universal across various architectures and languages. Moreover, we conduct an in-depth exploration on knowledge neurons, leading to the following two important discoveries: (1) The discovery of Language-Independent Knowledge Neurons, which store factual knowledge in a form that transcends language. We design cross-lingual knowledge editing experiments, demonstrating that the PLMs can accomplish this task based on language-independent neurons; (2) The discovery of Degenerate Knowledge Neurons, a novel type of neuron showing that different knowledge neurons can store the same fact. Its property of functional overlap endows the PLMs with a robust mastery of factual knowledge. We design fact-checking experiments, proving that the degenerate knowledge neurons can help the PLMs to detect wrong facts. Experiments corroborate these findings, shedding light on the mechanisms of factual knowledge storage in multilingual PLMs, and contribute valuable insights to the field. The code is available at https://github.com/heng840/AMIG.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Axiomatic Attribution for Deep Networks** (2017) [[arXiv](https://arxiv.org/abs/1703.01365)]
- *Authors:* Mukund Sundararajan et al.
- *Direct Connection:* AMIG is built directly on Integrated Gradients’ axiomatic framework to compute neuron-level attribution, then adapts the baseline choice to suit differing PLM architectures.

**Language Models as Knowledge Bases?** (2019) [[arXiv](https://arxiv.org/abs/1909.01066)]
- *Authors:* Fabio Petroni et al.
- *Direct Connection:* The cloze-style factual probing setup and criterion for a model ‘knowing’ a fact define the localization objective and evaluation protocol that AMIG adopts for neuron-level knowledge attribution.

**Multilingual LAMA: Investigating Knowledge in Multilingual Pretrained Language Models** (2021) [[arXiv](https://arxiv.org/abs/2102.00894)]
- *Authors:* Nora Kassner et al.
- *Direct Connection:* mLAMA provides the multilingual factual triples and probing framework that directly enable the identification of language-independent knowledge neurons and cross-lingual editing evaluations.

### 🏷️ Gap Identification

**The Effective coalitions of Shapley value For Integrated Gradients** (2022)
- *Authors:* Shu Liu et al.
- *Direct Connection:* Because prior IG practice commonly used zero-vector baselines, this work highlights a limitation that AMIG addresses by designing architecture-specific baseline vectors rather than relying on the zero-baseline assumption.

### 🏷️ Baseline

**Knowledge Neurons in Pretrained Transformers** (2022) [[arXiv](https://arxiv.org/abs/2104.08696)]
- *Authors:* Deren Lei Dai et al.
- *Direct Connection:* This paper introduced the notion of “knowledge neurons” and an IG-based neuron attribution pipeline that serves as the primary localization baseline that AMIG generalizes and improves across architectures and languages.

### 🏷️ Extension

**A rigorous study of integrated gradients method and extensions to internal neuron attributions** (2022)
- *Authors:* Daniel D. Lundstrom et al.
- *Direct Connection:* AMIG extends the internal-neuron IG formulation by introducing architecture-adapted baseline vectors that enable accurate attribution of internal activations in both auto-encoding and auto-regressive PLMs.

**Sequential Integrated Gradients: a simple but effective method for explaining language models** (2023) [[arXiv](https://arxiv.org/abs/2305.15853)]
- *Authors:* Julien Enguehard
- *Direct Connection:* Following Sequential IG’s word-wise decomposition, AMIG constructs low-information, word-conditioned baselines and then adapts them to different architectures to improve neuron localization fidelity.

---

## Synthesis: How Prior Work Led to This Paper

Knowledge neuron localization was first concretized by Dai et al., who defined “knowledge neurons” and used Integrated Gradients (IG) to attribute internal activations to factual predictions. IG itself, introduced by Sundararajan et al., provided the axiomatic basis—Sensitivity and Implementation Invariance—for reliable attribution, later extended by Lundstrom et al. to internal neuron attributions within deep networks. Enguehard’s Sequential IG contributed a practical technique for word-wise decomposition to build low-information, stepwise baselines tailored to language inputs. Meanwhile, common IG practice of using a zero-vector baseline, underscored by Liu et al., exposed a mismatch between baseline selection and the dynamics of different PLM architectures. For factual probing, Petroni et al. established the cloze-style evaluation that operationalizes whether a model “knows” a fact, and Kassner et al. extended this to multilingual probing via mLAMA, surfacing the cross-lingual dimension of stored knowledge.
Together these works highlighted two core opportunities: first, to reconcile IG-based neuron attribution with architectural diversity by replacing naive baselines with architecture-adapted, word-conditioned baselines; second, to probe multilingual models under a principled, cross-lingual regime. Building on IG’s neuron-level attributions, internal attribution extensions, and sequential baseline construction, the current work designs Architecture-adapted Multilingual Integrated Gradients to reliably localize knowledge neurons across BERT- and GPT-style models. Leveraging multilingual probing, it isolates intersections across languages to reveal language-independent knowledge neurons, and uses precise neuron-level attribution to discover degenerate knowledge neurons—overlapping neuron sets that redundantly encode the same facts—thereby enabling robust cross-lingual editing and internal fact-checking without external data.

---

*Analysis generated on: 2026-04-05T12:02:26.711982*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
