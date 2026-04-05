# Prior Work Analysis Report

## Target Paper

**Title:** Automated Creation of Reusable and Diverse Toolsets for Enhancing LLM Reasoning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Augmenting large language models (LLMs) with tools significantly enhances their problem-solving potential across multifaceted tasks. However, current tools automatically created by LLMs often serve as a mere summary of specific problems or solutions, which face two main issues: 1) Low reusability: The tools are overly problem-specific and struggle to handle new problems. 2) Limited diversity: The toolsets are too narrow, limiting their application to address a broader range of different problems. In this paper, we propose the Knowledge-grounded Tool Creation with Evolution (KTCE) framework, which aims to craft reusable and comprehensive toolsets for LLMs in a two-stage process. In the first stage (Knowledge-based Tool Creation), we conceptualize tools as a form of executable domain knowledge and propose a problem-knowledge-tool paradigm. Specifically, we leverage LLMs to abstract "knowledge" from "problems" and create a three-layer knowledge tree of topics, concepts, and key points. This hierarchical structure serves as a foundation for inducing atomic "tools" from "knowledge", grounding them in fundamental concepts and enhancing their usability. In the second stage (Tool Evolutionary Search), we evolve the toolsets through several actions including tool selection, mutation, and crossover. This stage mimics the biological evolution process, aiding toolsets in discovering new tools or updating existing ones, thereby increasing the diversity of the toolset. Experiments on challenging mathematical/tabular/scientific reasoning tasks demonstrate that our approach achieves substantial accuracy improvements ranging from 6.23% to 18.49% on average. Moreover, in-depth analyses reveal the superior characteristics of our toolkit, including high reusability, high diversity, and high generalizability on cross-data/LLM performance with low complexity.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Large Language Models as Tool Makers** (2024)
- *Authors:* Tianyi Cai et al.
- *Direct Connection:* By framing LLMs as autonomous tool makers capable of writing Python functions, this work underpins KTCE’s first stage, which extends tool making to be knowledge-grounded rather than problem-summary based.

### 🏷️ Inspiration

**Learning by applying: A general framework for mathematical reasoning via enhancing explicit knowledge learning** (2023)
- *Authors:* Jing Liu et al.
- *Direct Connection:* The paper’s emphasis on explicit, structured domain knowledge and key points for math reasoning directly informs KTCE’s problem–knowledge–tool paradigm and hierarchical knowledge tree for inducing atomic tools.

### 🏷️ Gap Identification

**CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets** (2024)
- *Authors:* Longhui Yuan et al.
- *Direct Connection:* CRAFT’s approach of abstracting tools from individual solutions yields a large but disorganized, low-reusability toolset, a limitation KTCE addresses by inducing atomic tools organized by a topic–concept–key-point knowledge tree.

**CREATOR: Tool Creation for Disentangling Abstract and Concrete Reasoning of Large Language Models** (2023)
- *Authors:* Chong Qian et al.
- *Direct Connection:* CREATOR generates ad-hoc, per-problem temporary Python tools tightly coupled to instances; KTCE directly targets this weakness by abstracting reusable tools from domain knowledge that generalize across problem families.

### 🏷️ Baseline

**TroVE: Inducing Verifiable and Efficient Toolboxes for Solving Programmatic Tasks** (2024)
- *Authors:* Zeyu Wang et al.
- *Direct Connection:* KTCE directly contrasts with TroVE’s iterative sampling-and-selection of small Python toolboxes, overcoming TroVE’s explicitly noted low diversity and <15% MATH coverage by grounding tool creation in a knowledge tree and expanding tools via evolutionary operators.

### 🏷️ Extension

**Genetic programming as a means for programming computers by natural selection** (1994)
- *Authors:* John R. Koza
- *Direct Connection:* KTCE adapts genetic programming’s selection, mutation, and crossover to an LLM-driven, non-gradient evolutionary search that diversifies and refines tools over iterations.

---

## Synthesis: How Prior Work Led to This Paper

Tool creation methods evolved from ad-hoc, per-instance functions toward reusable collections. CREATOR demonstrated that LLMs can synthesize Python tools on the fly, but its per-problem design made tools brittle and non-transferable. CRAFT advanced to forming larger toolsets by abstracting functions from solution traces, yet the resulting repositories were sprawling and unstructured, limiting retrieval and reuse. TroVE curated compact, verifiable toolboxes via iterative sampling-and-selection, improving precision but sacrificing breadth and coverage, especially on challenging math datasets. In parallel, Large Language Models as Tool Makers established that LLMs can autonomously write tools, legitimizing tool creation as a first-class capability rather than mere utilization. On the knowledge side, Learning by Applying highlighted that explicit domain knowledge and key-point structures enhance mathematical reasoning, suggesting that tools should be grounded in knowledge rather than derived from isolated problem summaries. Finally, genetic programming formalized non-gradient evolution through selection, mutation, and crossover, offering a principled way to iteratively refine and diversify programs. Together, these works reveal a gap: existing tool creation is either too problem-specific, too disorganized, or too narrowly curated, and lacks a knowledge-grounded basis and a systematic mechanism for expansion. KTCE synthesizes these insights by first inducing atomic, reusable tools from a hierarchical topic–concept–key-point knowledge structure, then extending the toolbox via an LLM-driven evolutionary search that adapts GP operators to Python functions. This combination naturally addresses reusability and diversity while preserving verifiability and practicality for program-based reasoning.

---

*Analysis generated on: 2026-04-05T11:57:25.952030*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
