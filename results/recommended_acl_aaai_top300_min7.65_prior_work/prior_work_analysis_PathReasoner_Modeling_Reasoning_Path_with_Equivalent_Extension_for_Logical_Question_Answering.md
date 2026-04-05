# Prior Work Analysis Report

## Target Paper

**Title:** PathReasoner: Modeling Reasoning Path with Equivalent Extension for Logical Question Answering

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Logical reasoning task has attracted great interest since it was proposed.Faced with such a task, current competitive models, even large language models (e.g., ChatGPT and PaLM 2), still perform badly.Previous promising LMs struggle in logical consistency modeling and logical structure perception.To this end, we model the logical reasoning task by transforming each logical sample into reasoning paths and propose an architecture PathReasoner.It addresses the task from the views of both data and model.To expand the diversity of the logical samples, we propose an atom extension strategy supported by equivalent logical formulas, to form new reasoning paths.From the model perspective, we design a stack of transformer-style blocks.In particular, we propose a path-attention module to joint model in-atom and cross-atom relations with the highorder diffusion strategy.Experiments show that PathReasoner achieves competitive performances on two logical reasoning benchmarks and great generalization abilities.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**ReClor: A Reading Comprehension Dataset Requiring Logical Reasoning** (2019) [[arXiv](https://arxiv.org/abs/2002.04326)]
- *Authors:* Weihao Yu et al.
- *Direct Connection:* ReClor established the logical MRC problem setting and benchmark that this work targets, defining the task formulation and evaluation protocol used to assess logical reasoning over text.

**Incorporating Context Graph with Logical Reasoning for Inductive Relation Prediction** (2022)
- *Authors:* Qika Lin et al.
- *Direct Connection:* The formalization of inputs as logical rules composed of function symbols and variables follows and adapts Lin et al.’s logical rule framework, enabling representation of rule bodies and heads that underpin reasoning paths.

### 🏷️ Inspiration

**Logic-driven Context Extension and Data Augmentation for Logical Reasoning of Text** (2022)
- *Authors:* Siyuan Wang et al.
- *Direct Connection:* The Equivalent Path Extension directly builds on LReasoner’s idea of logic-driven augmentation by using external logical equivalences to create semantically preserved variants, but shifts the augmentation to an atom/rule level rather than raw text.

### 🏷️ Gap Identification

**MERIt: Meta-path Guided Contrastive Learning for Logical Reasoning** (2022)
- *Authors:* Fangkai Jiao et al.
- *Direct Connection:* MERIt showed the value of path-based data signals via meta-path guided contrastive pretraining yet lacked explicit modeling of relations between logical units, motivating a design that couples augmentation with structured relation modeling.

**DAGN: Discourse-aware Graph Network for Logical Reasoning** (2021)
- *Authors:* Yinya Huang et al.
- *Direct Connection:* DAGN’s discourse-unit graph underscored the importance of explicit logical relation modeling but its chain-like graph constrained complex interactions, prompting a move to capture such relations without heavy graph construction.

### 🏷️ Baseline

**Logiformer: A Two-branch Graph Transformer Network for Interpretable Logical Reasoning** (2022)
- *Authors:* Fangzhi Xu et al.
- *Direct Connection:* As the strongest prior baseline modeling logic and syntax via explicit text graphs, Logiformer motivates replacing costly graph construction with a scalable attention mechanism that still preserves interpretable logical cues.

### 🏷️ Extension

**Adaptive Diffusion in Graph Neural Networks** (2021)
- *Authors:* Jialin Zhao et al.
- *Direct Connection:* The high-order diffusion used here extends Zhao et al.’s adaptive diffusion idea by applying power-series aggregation to attention score matrices, allowing information to propagate across distant in-atom and cross-atom interactions.

---

## Synthesis: How Prior Work Led to This Paper

ReClor framed logical machine reading comprehension as a multiple-choice reasoning problem and supplied a rigorous benchmark that crystallized the community’s focus on logic-sensitive understanding. LReasoner demonstrated that injecting logical equivalences into training data can improve robustness, introducing logic-driven augmentation as a practical tool, albeit applied at the raw text level. MERIt advanced the idea of path-like supervision via meta-path guided contrastive learning and extra data, but stopped short of explicit modeling of relations among logical units within a sample. On the modeling side, DAGN established the value of representing discourse units and their logical links in a graph, though its chain-like topology limited expressivity for complex interactions. Logiformer pursued interpretable logic and syntax modeling through two-branch graph transformers, but required heavy text graph construction that can be costly and less scalable. In parallel, Lin et al. provided a logical rule perspective—representing inputs as rule bodies/heads composed of function symbols and variables—that offers a compact, compositional handle on textual logic. Zhao et al. introduced adaptive diffusion as a principled way to capture high-order dependencies beyond first-order neighborhoods.
Together, these works exposed a gap: data sparsity and inconsistent logic sensitivity demand augmentation grounded in equivalence, while graph-heavy solutions strain scalability and still struggle to model both local (within-unit) and global (across-unit) logical interactions. A natural next step is to adopt the logical rule formalism to unify sentences as atoms, perform equivalence-driven augmentation at the rule level to diversify training without altering semantics, and replace explicit graphs with a path-attention mechanism that jointly models in-atom and cross-atom relations enhanced by diffusion-inspired high-order propagation—thereby combining augmentation, structured logical perception, and scalability for strong performance on benchmarks like ReClor.

---

*Analysis generated on: 2026-04-05T12:02:48.450841*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
