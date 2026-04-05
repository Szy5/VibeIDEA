# Prior Work Analysis Report

## Target Paper

**Title:** IRIS: Interactive Research Ideation System for Accelerating Scientific Discovery

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> The rapid advancement in capabilities of large language models (LLMs) raises a pivotal question: How can LLMs accelerate scientific discovery?This work tackles the crucial first stage of research, generating novel hypotheses.While recent work on automated hypothesis generation focuses on multi-agent frameworks and extending test-time compute, none of the approaches effectively incorporate transparency and steerability through a synergistic Human-in-the-loop (HITL) approach.To address this gap, we introduce IRIS for interactive hypothesis generationm, an open-source platform designed for researchers to leverage LLM-assisted scientific ideation.IRIS incorporates innovative features to enhance ideation, including adaptive test-time compute expansion via Monte Carlo Tree Search (MCTS), fine-grained feedback mechanism, and querybased literature synthesis.Designed to empower researchers with greater control and insight throughout the ideation process.We additionally conduct a user study with researchers across diverse disciplines, validating the effectiveness of our system in enhancing ideation.We open-source our code here.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Bandit Based Monte-Carlo Planning** (2006)
- *Authors:* Levente Kocsis and Csaba Szepesvári
- *Direct Connection:* This paper introduces the UCT variant of Monte Carlo Tree Search that is directly instantiated and adapted to subjective, LLM-based rewards for traversing and refining the research-idea space.

### 🏷️ Inspiration

**IdeaSynth: Iterative Research Idea Development through Evolving and Composing Idea Facets with Literature-Grounded Feedback** (2024) [[arXiv](https://arxiv.org/abs/2410.04025)]
- *Authors:* Kevin Pu et al.
- *Direct Connection:* Its iterative, literature-grounded facet-based development of ideas directly inspires a researcher-in-the-loop workflow, which is expanded with finer-grained critiques and a broader action space for controllable refinement.

### 🏷️ Gap Identification

**Can LLMs generate novel research ideas? A large-scale human study with 100+ NLP researchers** (2024) [[arXiv](https://arxiv.org/abs/2409.04109)]
- *Authors:* Chenglei Si et al.
- *Direct Connection:* This work’s single-pass, fully automated idea generation and simplistic retrieval augmentation are cited as core limitations that the current system overcomes via iterative, human-steerable refinement and richer, targeted literature synthesis.

**ResearchAgent: Iterative Research Idea Generation over Scientific Literature with Large Language Models** (2025) [[arXiv](https://arxiv.org/abs/2404.07738)]
- *Authors:* Jinheon Baek et al.
- *Direct Connection:* By relying on coarse criteria (e.g., novelty/rigor) and recursive LLM-as-a-judge loops, this system exhibits ‘reward hacking’ behaviors, directly motivating the introduction of fine-grained, segment-level feedback with human verification to guide refinement.

**Nova: An Iterative Planning and Search Approach to Enhance Novelty and Diversity of LLM Generated Ideas** (2024) [[arXiv](https://arxiv.org/abs/2410.14255)]
- *Authors:* Xiang Hu et al.
- *Direct Connection:* Nova emphasizes exploration through planning and search but lacks systematic refinement of promising directions, motivating an alternating exploration–exploitation search via MCTS for idea development.

### 🏷️ Baseline

**SciMON: Scientific Inspiration Machines Optimized for Novelty** (2024)
- *Authors:* Qingyun Wang et al.
- *Direct Connection:* As a primary automated baseline that optimizes for novelty with coarse scoring and simplistic retrieval (e.g., appending abstracts/keywords), it sets the comparison point for adding structured search and query-based literature synthesis.

### 🏷️ Extension

**AI2 Scholar QA: Organized Literature Synthesis with Attribution** (2025) [[arXiv](https://arxiv.org/abs/2504.10861)]
- *Authors:* Amanpreet Singh et al.
- *Direct Connection:* The system adopts and extends ScholarQA’s two-stage retrieval plus three-stage attributed synthesis pipeline to produce clustered, cited, query-focused literature reports that ground and refine hypotheses.

---

## Synthesis: How Prior Work Led to This Paper

Recent automated ideation systems exposed key bottlenecks that shaped this work’s direction. Si et al. demonstrated that large language models can propose research ideas but typically in a single pass with simplistic context augmentation, limiting iterative refinement and steerability. ResearchAgent by Baek et al. introduced iterative literature-grounded generation but optimized against coarse criteria with recursive LLM-as-a-judge loops, revealing reward gaming and misalignment risks. Nova (Hu et al.) advanced exploration of diverse ideas via planning, yet offered little mechanism for systematic exploitation and subsequent refinement of promising threads. SciMON (Wang et al.) optimized for novelty using coarse scoring and naive retrieval (e.g., appending abstracts/keywords), becoming a de facto baseline for novelty-centric, exploitation-heavy pipelines. In parallel, Kocsis and Szepesvári’s UCT provided a principled algorithm for alternating exploration and exploitation via Monte Carlo Tree Search, while ScholarQA (Singh et al.) introduced a query-focused, two-stage retrieval and three-stage, attributed synthesis pipeline for organizing multi-document scientific evidence. IdeaSynth (Pu et al.) showed the promise of iterative, literature-grounded, interactive idea development through composable facets. Together these works revealed a gap: automated systems lacked transparent, controllable, and literature-grounded iterative development, with structured search and precise feedback. The current system synthesizes these insights by adapting UCT-style MCTS to subjective, LLM-mediated rewards for idea quality; inserting query-based, attributed literature synthesis to ground revisions; and replacing coarse, global critiques with fine-grained, segment-level feedback that users can verify—yielding a human-steerable, exploration–exploitation framework for research ideation.

---

*Analysis generated on: 2026-04-05T11:58:23.880014*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
