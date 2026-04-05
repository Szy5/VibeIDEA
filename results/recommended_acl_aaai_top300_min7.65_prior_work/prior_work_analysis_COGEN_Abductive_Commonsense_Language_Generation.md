# Prior Work Analysis Report

## Target Paper

**Title:** COGEN: Abductive Commonsense Language Generation

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Reasoning is one of the most important elements in achieving Artificial General Intelligence (AGI), specifically when it comes to Abductive and counterfactual reasoning. In order to introduce these capabilities of reasoning in Natural Language Processing (NLP) models, there have been recent advances towards training NLP models to better perform on two main tasks - Abductive Natural Language Inference (alphaNLI) and Abductive Natural Language Generation Task (alphaNLG). This paper proposes CoGen, a model for both alphaNLI and alphaNLG tasks that employ a novel approach of combining the temporal commonsense reasoning for each observation (before and after a real hypothesis) from pre-trained models with contextual filtering for training. Additionally, we use state-of-the-art semantic entailment to filter out the contradictory hypothesis during the inference. Our experimental results show that CoGen outperforms current models and set a new state of the art in regards to alphaNLI and alphaNLG tasks. We make the source code of CoGen model publicly available for reproducibility and to facilitate relevant future research.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Back to the Future: Unsupervised Backprop-based Decoding for Counterfactual and Abductive Commonsense Reasoning** (2020) [[arXiv](https://arxiv.org/abs/2010.05906)]
- *Authors:* Lianhui Qin et al.
- *Direct Connection:* This paper formalized abductive generation as generating a hypothesis H that temporally fits between two observations O1 and O2, a formulation COGEN explicitly adopts for both its training and evaluation setup.

**COMET: Commonsense Transformers for Automatic Knowledge Graph Construction** (2019) [[arXiv](https://arxiv.org/abs/1906.05317)]
- *Authors:* Antoine Bosselut et al.
- *Direct Connection:* COGEN uses the COMET model to generate relation-specific commonsense inferences (e.g., xIntent, xEffect) for each observation, providing the before/after knowledge that underpins its temporal augmentation step.

**COMET-ATOMIC 2020: On Symbolic and Neural Commonsense Knowledge Graphs** (2020) [[arXiv](https://arxiv.org/abs/2010.05953)]
- *Authors:* Jena D. Hwang et al.
- *Direct Connection:* ATOMIC2020 supplies the expanded set of before/after relations (e.g., xIntent, xEffect, oEffect) and coverage that COGEN relies on to derive temporal commonsense facts for augmenting the observations.

### 🏷️ Inspiration

**Generating Hypothetical Events for Abductive Inference** (2021) [[arXiv](https://arxiv.org/abs/2106.03973)]
- *Authors:* Debjit Paul et al.
- *Direct Connection:* The strategy of selecting candidate events by how well their consequences match observed outcomes directly inspired COGEN’s contextual filtering that keeps only COMET inferences most similar to the other observation.

**Abductive Reasoning with Temporal Information** (2000) [[arXiv](https://arxiv.org/abs/cs/0011035)]
- *Authors:* Sven Verdoolaege et al.
- *Direct Connection:* This work’s insight that abductive reasoning intrinsically involves temporal cause-and-effect motivated COGEN’s focus on before/after temporal commonsense as the core knowledge to augment observations.

### 🏷️ Baseline

**Abductive Commonsense Reasoning** (2019) [[arXiv](https://arxiv.org/abs/1908.05739)]
- *Authors:* Chandra Bhagavatula et al.
- *Direct Connection:* This work introduced the ART dataset and the αNLI/αNLG tasks and proposed the COMeT-Emb+GPT2 pipeline, which COGEN directly builds upon and surpasses by injecting temporal commonsense and applying contextual and entailment-based filtering.

### 🏷️ Extension

**Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks** (2019) [[arXiv](https://arxiv.org/abs/1908.10084)]
- *Authors:* Nils Reimers et al.
- *Direct Connection:* COGEN repurposes the BERT cross-encoder from this work for two critical filtering stages: selecting the most contextually relevant COMET-generated facts via similarity and removing contradictory hypotheses via entailment checks.

---

## Synthesis: How Prior Work Led to This Paper

Abductive commonsense reasoning was framed concretely by the introduction of the ART benchmark and the αNLI/αNLG tasks, alongside a COMeT-Emb+GPT2 pipeline that demonstrated the feasibility of knowledge-augmented generation yet showed limited plausibility in human judgments (Bhagavatula et al., 2019). The abductive generation problem was further formalized as producing a hypothesis that temporally fits between two observations, emphasizing the infilling nature of the task (Qin et al., 2020). Neural commonsense generation via COMET provided relation-conditional inferences, such as intents and effects, that could be elicited from textual observations (Bosselut et al., 2019). ATOMIC2020 expanded and systematized these relations into before/after categories with broader coverage, enabling richer temporal reasoning (Hwang et al., 2020). For reliably measuring pairwise semantic relations, cross-encoder architectures offered strong similarity and entailment judgments (Reimers and Gurevych, 2019). Complementarily, abductive approaches that select events by their fit to observed outcomes underscored the value of context-sensitive filtering in choosing plausible explanations (Paul and Frank, 2021). Theoretical work had long argued that abduction is tightly coupled to temporal causality, pointing to causes and effects as key targets for reasoning (Verdoolaege et al., 2000). Collectively, these works highlighted a gap: knowledge-augmented generators lacked mechanisms to focus temporal commonsense on what best aligns with both observations and to enforce consistency at inference. The current paper synthesizes these insights by generating before/after commonsense with COMET trained on ATOMIC2020, filtering those inferences by cross-encoder similarity to the other observation, and finally applying entailment-based checks to remove contradictions—yielding a temporally grounded, context-sensitive abductive generator and a stronger inference model.

---

*Analysis generated on: 2026-04-05T12:03:59.027363*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
