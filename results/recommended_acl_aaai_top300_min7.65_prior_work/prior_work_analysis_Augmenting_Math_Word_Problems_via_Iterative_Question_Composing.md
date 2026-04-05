# Prior Work Analysis Report

## Target Paper

**Title:** Augmenting Math Word Problems via Iterative Question Composing

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Despite the advancements in large language models (LLMs) for mathematical reasoning, solving competition-level math problems remains a significant challenge, especially for open-source LLMs without external tools. We introduce the MMIQC dataset, comprising a mixture of processed web data and synthetic question-response pairs, aimed at enhancing the mathematical reasoning capabilities of base language models. Models fine-tuned on MMIQC consistently surpass their counterparts in performance on the MATH benchmark across various model sizes. Notably, Qwen-72B-MMIQC achieves a 45.0% accuracy, exceeding the previous open-source state-of-the-art by 8.2% and outperforming the initial version GPT-4 released in 2023. Extensive evaluation results on Hungarian high school finals suggest that such improvement can generalize to unseen data. Our ablation study on MMIQC reveals that a large part of the improvement can be attributed to our novel augmentation method, Iterative Question Composing (IQC), which involves iteratively composing new questions from seed problems using an LLM and applying rejection sampling through another LLM.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Measuring Mathematical Problem Solving With the MATH Dataset** (2021) [[arXiv](https://arxiv.org/abs/2103.03874)]
- *Authors:* D. Hendrycks et al.
- *Direct Connection:* The MATH dataset supplies both the core competition-level benchmark and the seed problems from its training split that IQC iteratively composes into more complex question-answer pairs.

### 🏷️ Inspiration

**OpenWebMath: An Open Dataset of High-Quality Mathematical Web Text** (2023)
- *Authors:* K. Paster et al.
- *Direct Connection:* By evidencing the high quality and competition alignment of Mathematics Stack Exchange content, OpenWebMath motivated extracting and preprocessing Math StackExchange pages into question–response pairs included in MMIQC.

### 🏷️ Baseline

**MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models** (2023) [[arXiv](https://arxiv.org/abs/2309.12284)]
- *Authors:* L. Yu et al.
- *Direct Connection:* The paper directly integrates MetaMath’s question-bootstrapping prompts and filtered MetaMathQA samples as part of its data, and positions IQC to address MetaMath’s limitation of producing near-duplicate variants by composing multi-step extensions that increase diversity.

### 🏷️ Extension

**TinyGSM: achieving >80% on GSM8k with small language models** (2023) [[arXiv](https://arxiv.org/abs/2312.09241)]
- *Authors:* B. Liu et al.
- *Direct Connection:* The authors modify TinyGSM’s prompt for generating similar problems to produce brief-solution, single-box answer variants, using it as a complementary augmentation module alongside IQC.

**Scaling relationship on learning mathematical reasoning with large language models** (2023) [[arXiv](https://arxiv.org/abs/2308.01825)]
- *Authors:* Z. Yuan et al.
- *Direct Connection:* Building on Yuan et al.’s use of rejection sampling to filter model-generated solutions, this work extends the technique by employing a separate LLM as a verifier to accept only IQC-composed questions whose answers match the verifier’s output.

### 🏷️ Related Problem

**Llemma: An open language model for mathematics** (2023) [[arXiv](https://arxiv.org/abs/2310.10631)]
- *Authors:* Z. Azerbayev et al.
- *Direct Connection:* Llemma demonstrated the benefits of math-specific web corpora (e.g., StackExchange/ArXiv) via continual pretraining, informing this work’s choice to reuse high-quality pretraining math web data during fine-tuning and its contamination-checking methodology.

---

## Synthesis: How Prior Work Led to This Paper

MetaMath introduced question bootstrapping that generates new math problems from seed items, operationalized through MetaMathQA, but its strategies often create near-duplicate variants rather than genuinely richer tasks. TinyGSM provided an effective prompt design for producing similar problems with concise, single-box answers, furnishing a practical recipe for reliable, verifier-friendly question–solution pairs. Yuan et al. showed that rejection sampling can filter noisy model generations by discarding samples whose answers fail a secondary check, highlighting a simple, scalable mechanism for quality control without human labels. The MATH dataset established a large, competition-level benchmark and a rich pool of seed problems that reflect diverse math subfields. OpenWebMath demonstrated that Mathematics Stack Exchange contains high-quality, competition-relevant math text, spotlighting it as a strong source for mined question–answer material. Llemma, through math-specific continual pretraining on curated web corpora, underscored that injecting math-focused web data improves reasoning, and it disseminated contamination-checking practices used widely in math-LM work. Together, these works revealed a gap: existing augmentation pipelines could expand data volume but struggled to increase structural complexity and diversity without sacrificing correctness. This motivated composing new questions that scaffold additional reasoning steps atop seed problems while automatically filtering errors. The current paper synthesizes bootstrapping (MetaMath) and similar-problem prompting (TinyGSM) with verifier-based rejection sampling (Yuan) and high-quality web QA mining (inspired by OpenWebMath and Llemma), all anchored to MATH seeds, and advances the field by introducing an iterative composing procedure that systematically builds complexity and diversity while maintaining answer validity.

---

*Analysis generated on: 2026-04-05T12:03:44.781184*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
