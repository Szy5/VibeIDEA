# Prior Work Analysis Report

## Target Paper

**Title:** Faithful Question Answering with Monte-Carlo Planning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Although large language models demonstrate remarkable question-answering performances, revealing the intermediate reasoning steps that the models faithfully follow remains challenging. In this paper, we propose FAME (FAithful question answering with MontE-carlo planning) to answer questions based on faithful reasoning steps. The reasoning steps are organized as a structured entailment tree, which shows how premises are used to produce intermediate conclusions that can prove the correctness of the answer. We formulate the task as a discrete decision-making problem and solve it through the interaction of a reasoning environment and a controller. The environment is modular and contains several basic task-oriented modules, while the controller proposes actions to assemble the modules. Since the search space could be large, we introduce a Monte-Carlo planning algorithm to do a look-ahead search and select actions that will eventually lead to high-quality steps. FAME achieves advanced performance on the standard benchmark. It can produce valid and faithful reasoning steps compared with large language models with a much smaller model size.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Explaining Answers with Entailment Trees** (2021)
- *Authors:* Bhavana Dalvi et al.
- *Direct Connection:* This work provides the entailment-tree formulation and evaluation framework (with a fixed fact corpus) that the new method directly adopts as the target structure and reasoning substrate.

**Bandit Based Monte-Carlo Planning** (2006)
- *Authors:* Levente Kocsis and Csaba Szepesvári
- *Direct Connection:* The planning core instantiates UCT, updating action values from simulated successor states and selecting actions via an upper confidence bound exactly as prescribed in this seminal MCTS framework.

### 🏷️ Inspiration

**Mastering the game of Go without human knowledge** (2017)
- *Authors:* David Silver et al.
- *Direct Connection:* The upper confidence bound that blends prior policy scores with value estimates and visit counts, cited in the new method’s selection equation, follows the AlphaGo Zero-style MCTS and inspires its adaptation to language reasoning.

### 🏷️ Gap Identification

**Entailer: Answering Questions with Faithful and Truthful Chains of Reasoning** (2022)
- *Authors:* Oyvind Tafjord et al.
- *Direct Connection:* Entailer’s step-wise overgenerate-and-filter approach based on internal beliefs is explicitly cited as myopic and prone to hallucinated facts, motivating the new method’s grounded retrieval and look-ahead planning to ensure faithfulness.

### 🏷️ Baseline

**Selection-Inference: Exploiting Large Language Models for Interpretable Logical Reasoning** (2022) [[arXiv](https://arxiv.org/abs/abs/2205.09712)]
- *Authors:* Antonia Creswell et al.
- *Direct Connection:* Selection-Inference’s modular, step-wise pipeline with beam search and a halter is the primary baseline that the new method improves upon by replacing local beam decisions with Monte-Carlo planning and by removing the reliance on a complete set of given facts via adaptive retrieval.

### 🏷️ Extension

**MetGen: A Module-Based Entailment Tree Generation Framework for Answer Explanation** (2022)
- *Authors:* Ruixin Hong et al.
- *Direct Connection:* The single-step entailment module directly adopts MetGen’s idea of typed logical operations with prefix prompts to generate intermediate conclusions from multiple premises.

### 🏷️ Related Problem

**Machine Translation Decoding Beyond Beam Search** (2021)
- *Authors:* Rémi Leblond et al.
- *Direct Connection:* By showing MCTS can outperform beam search for text generation decoding, this work directly motivates replacing overgenerate-and-filter/beam strategies with MCTS for action selection in language tasks.

---

## Synthesis: How Prior Work Led to This Paper

EntailmentBank introduced the idea of structuring explanations as entailment trees grounded in a fixed fact corpus, establishing both the target representation for reasoning and the evaluation regime for tree validity. Entailer operationalized faithful QA as step-wise tree construction via overgenerate-and-filter, but relied on internal beliefs that could hallucinate facts and made locally myopic choices. Selection-Inference proposed a modular selection-plus-inference pipeline with a halter and beam search, demonstrating interpretable logical reasoning but assuming a complete set of supporting facts and still making primarily local decisions. Independently, UCT formalized Monte-Carlo tree search as bandit-based planning with action values updated from simulated successors and selection via an upper confidence bound, while AlphaGo Zero popularized a practical UCB rule that blends prior probabilities, value estimates, and visit counts to balance exploration-exploitation. In language generation, MCTS was shown to surpass beam search for decoding, reinforcing that look-ahead search can outperform greedy or beam strategies in sequence decision problems. For generating individual entailment steps, a module-based approach with typed logical operations and prefix prompts was shown to effectively produce intermediate conclusions from premises. Together, these works revealed a gap: faithful QA needs globally foresighted, grounded tree construction rather than local, belief-driven step choices. The natural next step is to treat entailment-tree building as a decision process over modular actions and to guide it with UCT/AlphaGo-style Monte-Carlo planning, while using a typed entailment module for reliable step generation; this synthesis replaces myopic selection with look-ahead action values and grounds reasoning via retrieval, directly addressing faithfulness and search optimality.

---

*Analysis generated on: 2026-04-05T11:54:46.233184*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
