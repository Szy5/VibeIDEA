# Prior Work Analysis Report

## Target Paper

**Title:** CK12: A Rounded K12 Knowledge Graph Based Benchmark for Chinese Holistic Cognition Evaluation

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> New NLP benchmarks are urgently needed to align with the rapid development of large language models (LLMs). We present a meticulously designed evaluation benchmark that leverages the knowledge graph. This evaluation comprises 584 level-1 knowledge points and 1,989 level-2 knowledge points, thereby encompassing a comprehensive spectrum of the K12 education domain knowledge. The primary objective is to comprehensively assess the high-level comprehension aptitude and reasoning capabilities of LLMs operating within the Chinese context. Our evaluation incorporates five distinct question types with 39,452 questions. We test the current mainstream LLMs by three distinct modes. Firstly, four prompt evaluation modes were employed to assess the fundamental capacity. Additionally, for choice questions, a result-oriented evaluation approach was designed through data augmentation to assess the model's proficiency in advanced knowledge and reasoning. Moreover, a subset with reasoning process is derived, and the process-oriented testing method is used to test the model's interpretability and higher-order reasoning capacity. We further show models' capability in our knowledge points, and anticipate the evaluation can assist in the assessment of the strengths and deficiencies of LLMs on knowledge points, thus fostering their development within the Chinese context. Our Dataset will be publicly available in https://github.com/tal-tech/chinese-k12-evaluation.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**Training Verifiers to Solve Math Word Problems** (2021) [[arXiv](https://arxiv.org/abs/2110.14168)]
- *Authors:* Karl Cobbe et al.
- *Direct Connection:* GSM8K established the value of math problems with step-by-step solutions for assessing reasoning, which CK12 adopts by creating a large K12 math subset with human-authored analyses for process-oriented evaluation.

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* CK12 directly employs chain-of-thought prompting (e.g., appending “Let’s think step by step”) introduced by Wei et al. to elicit and evaluate interpretable reasoning trajectories in its process-oriented tests.

### 🏷️ Gap Identification

**C-Eval: A Multi-Level Multi-Discipline Chinese Evaluation Suite for Foundation Models** (2023) [[arXiv](https://arxiv.org/abs/2305.08322)]
- *Authors:* Yuzhuo Huang et al.
- *Direct Connection:* C-Eval’s exam-paper-sourced tasks and incomplete coverage of fine-grained knowledge points—sometimes with GPT-4–generated rationales of uneven quality—are explicitly cited as limitations that CK12 overcomes by using a teacher-curated K12 knowledge graph and vetted analyses.

**M3KE: A Massive Multi-Level Multi-Subject Knowledge Evaluation Benchmark for Chinese Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2305.10263)]
- *Authors:* Chang Liu et al.
- *Direct Connection:* M3KE introduces multi-level Chinese evaluation but draws primarily from standardized exams, motivating CK12’s shift to a knowledge-graph organization that guarantees exhaustive K12 level-1/level-2 knowledge-point coverage.

**Xiezhi: An Ever-Updating Benchmark for Holistic Domain Knowledge Evaluation** (2023) [[arXiv](https://arxiv.org/abs/2306.05783)]
- *Authors:* Zhen Gu et al.
- *Direct Connection:* Xiezhi’s large exam-based question set focuses on broad domain knowledge yet lacks comprehensive K12 knowledge-point structuring, directly motivating CK12’s knowledge-graph-based, K12-specific coverage.

### 🏷️ Extension

**ROSCOE: A Suite of Metrics for Scoring Step-by-Step Reasoning** (2022) [[arXiv](https://arxiv.org/abs/2212.07919)]
- *Authors:* Olga Golovneva et al.
- *Direct Connection:* CK12 extends ROSCOE by adopting its faithfulness, source-consistency, alignment, hallucination, and redundancy criteria to systematically score the generated reasoning chains on its math subset.

**Compression, Transduction, and Creation: A Unified Framework for Evaluating Natural Language Generation** (2021) [[arXiv](https://arxiv.org/abs/2109.06379)]
- *Authors:* Mingqi Deng et al.
- *Direct Connection:* CK12 leverages Deng et al.’s alignment-vector framework (with SimCSE embeddings) to operationalize similarity-based components when computing reasoning-step evaluation metrics.

---

## Synthesis: How Prior Work Led to This Paper

Chinese evaluation suites built from exam papers, such as C-Eval, provided a broad, multi-discipline yardstick but often lacked systematic coverage of fine-grained knowledge points and relied on explanations of variable quality. M3KE advanced multi-level and multi-subject testing in Chinese yet still sourced predominantly from standardized exams, leaving gaps in exhaustive knowledge-point coverage. Xiezhi scaled domain knowledge evaluation via an ever-updating, large exam-derived pool but did not structure content to comprehensively reflect the K12 knowledge system. In parallel, GSM8K demonstrated the value of math problems with human-authored, step-by-step solutions to probe reasoning quality, introducing a process-centric paradigm that complements accuracy-only assessments. Chain-of-thought prompting showed that adding explicit reasoning cues (“Let’s think step by step”) can elicit interpretable, multi-step rationales from LLMs, while ROSCOE defined concrete metrics—faithfulness, consistency, alignment, hallucination, redundancy—for scoring the quality of such chains. Deng et al. provided an alignment-vector framework that enables similarity-based scoring components for generated texts.
Against this backdrop, the opportunity emerged to create a Chinese K12 benchmark that is both knowledge-complete and process-aware. CK12 synthesizes these insights by replacing exam-paper sourcing with a teacher-curated, multi-level K12 knowledge graph that guarantees broad and fine-grained coverage, adopting chain-of-thought prompting to elicit rationales, and extending ROSCOE-style metrics—implemented via alignment vectors—to evaluate reasoning quality. It further introduces robust, result-oriented choice evaluations (e.g., shuffling options and adding distractors) to mitigate data contamination and probe deeper knowledge application, naturally unifying knowledge coverage and interpretable reasoning into a single, comprehensive Chinese K12 evaluation.

---

*Analysis generated on: 2026-04-05T12:06:15.525381*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
