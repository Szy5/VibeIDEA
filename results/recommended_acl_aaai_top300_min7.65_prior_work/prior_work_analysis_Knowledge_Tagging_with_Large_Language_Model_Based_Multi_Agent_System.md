# Prior Work Analysis Report

## Target Paper

**Title:** Knowledge Tagging with Large Language Model Based Multi-Agent System

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Knowledge tagging for questions is vital in modern intelligent educational applications, including learning progress diagnosis, practice question recommendations, and course content organization. Traditionally, these annotations have been performed by pedagogical experts, as the task demands not only a deep semantic understanding of question stems and knowledge definitions but also a strong ability to link problem-solving logic with relevant knowledge concepts. With the advent of advanced natural language processing (NLP) algorithms, such as pre-trained language models and large language models (LLMs), pioneering studies have explored automating the knowledge tagging process using various machine learning models. In this paper, we investigate the use of a multi-agent system to address the limitations of previous algorithms, particularly in handling complex cases involving intricate knowledge definitions and strict numerical constraints. By demonstrating its superior performance on the publicly available math question knowledge tagging dataset, MathKnowCT, we highlight the significant potential of an LLM-based multi-agent system in overcoming the challenges that previous methods have encountered. Finally, through an in-depth discussion of the implications of automating knowledge tagging, we underscore the promising future of deploying LLM-based algorithms in educational contexts.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Inspiration

**Content Knowledge Identification with Multi-Agent Large Language Models (LLMs)** (2024)
- *Authors:* Yang et al.
- *Direct Connection:* By showing that multiple LLM judging agents engaging in group deliberation better align with expert annotations for pedagogical concept identification, this paper directly inspired adopting a multi-agent judging strategy for knowledge tagging.

### 🏷️ Gap Identification

**Evaluating language models for mathematics through interactions** (2024)
- *Authors:* Collins et al.
- *Direct Connection:* This study systematically documented LLMs’ weaknesses on numerical reasoning, directly motivating the introduction of a dedicated numerical judger that verifies constraints via code execution rather than pure text generation.

**PQSCT: Pseudo-Siamese BERT for Concept Tagging With Both Questions and Solutions** (2023)
- *Authors:* Huang et al.
- *Direct Connection:* Although PQSCT improved concept tagging by fusing questions and solutions, its reliance on fixed encoders limited explicit reasoning over strict numerical constraints, a shortcoming addressed here via a numerical judger and task decomposition.

### 🏷️ Baseline

**Knowledge Tagging System on Math Questions via LLMs with Flexible Demonstration Retriever** (2024) [[arXiv](https://arxiv.org/abs/2406.13885)]
- *Authors:* Li et al.
- *Direct Connection:* This work introduced the MathKnowCT dataset and a single-LLM evaluator using CoT/ICL for knowledge tagging, which the current paper directly improves upon by replacing single-agent judging with a decomposed multi-agent pipeline and specialized numerical verification.

**Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks** (2019) [[arXiv](https://arxiv.org/abs/1908.10084)]
- *Authors:* Reimers and Gurevych
- *Direct Connection:* SBERT-style embedding similarity served as a principal non-LLM baseline for tagging, whose limitations in capturing compositional semantics and constraint checking motivated a move to structured, agent-based reasoning.

### 🏷️ Extension

**ToolQA: A dataset for LLM question answering with external tools** (2024)
- *Authors:* Zhuang et al.
- *Direct Connection:* Building on the idea that coupling LLMs with external tool use improves numerically grounded QA, the current work adapts this technique by generating and executing Python programs to evaluate numeric sub-constraints in tagging.

### 🏷️ Related Problem

**EvaAI: A Multi-agent Framework Leveraging Large Language Models for Enhanced Automated Grading** (2024)
- *Authors:* Lagakis and Demetriadis
- *Direct Connection:* Demonstrating that a committee of LLM agents produces more reliable grading than a single model informed the design choice to aggregate multiple specialized judgments to improve robustness in educational labeling.

---

## Synthesis: How Prior Work Led to This Paper

Prior work on automatic knowledge tagging evolved from semantic similarity and fine-tuned encoders to LLM-based evaluators. Sentence-BERT established dense embedding similarity as a practical baseline but struggled to capture compositional semantics and explicit constraints. PQSCT pushed beyond plain encodings by fusing questions and solutions with a pseudo-Siamese BERT, yet its fixed encoder still lacked explicit reasoning about strict numeric conditions. The most relevant advance came from a single-LLM evaluator that used in-context exemplars and chain-of-thought to simulate expert tagging on the MathKnowCT dataset, showing that LLMs can act as taggers with minimal labels. In parallel, multi-agent approaches in education revealed that using multiple LLM judges can improve alignment with expert assessments: multi-agent content knowledge identification demonstrated that deliberative judgment reduces errors, and multi-agent grading showed committees yield more reliable evaluations than single models. Meanwhile, analyses of LLMs’ mathematical abilities underscored persistent failings on numeric reasoning, highlighting the need for tooling. Tool-use research showed that integrating code execution with LLMs improves performance on numerically grounded tasks. Taken together, these strands exposed a clear opportunity: retain the semantic strengths of LLM taggers while mitigating numerical and reliability weaknesses. The natural next step was to decompose knowledge definitions into semantic and numeric sub-constraints handled by specialized agents, pair a planning agent with a question solver, and add a numerical judger that generates and executes Python to enforce strict constraints, aggregating sub-decisions for robust, expert-aligned tagging on MathKnowCT.

---

*Analysis generated on: 2026-04-05T11:59:59.537748*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
