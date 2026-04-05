# Prior Work Analysis Report

## Target Paper

**Title:** Capture the Key in Reasoning to Enhance CoT Distillation Generalization

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> As Large Language Models (LLMs) scale up and gain powerful Chain-of-Thoughts (CoTs) reasoning abilities, practical resource constraints drive efforts to distill these capabilities into more compact Smaller Language Models (SLMs).We find that CoTs consist mainly of simple reasoning forms, with a small proportion ( 4.7%) of key reasoning steps that truly impact conclusions.However, previous distillation methods typically involve supervised fine-tuning student SLMs only on correct CoTs data produced by teacher LLMs, resulting in students struggling to learn the key, instead imitating the teacher's reasoning forms and making errors or omissions in reasoning.To address these issues, drawing an analogy to human learning, where analyzing mistakes according to correct solutions often reveals the crucial steps leading to successes or failures, we propose mistakE-Driven key reasonIng step distillaTion (EDIT), a novel method that further aids SLMs learning key reasoning steps rather than mere simple fine-tuning.Firstly, to expose the crucial steps in CoTs, we carefully design specific prompts to generate dual CoTs data with similar reasoning paths but divergent conclusions.Then, we apply the minimum edit distance algorithm on the dual CoTs data to locate these key steps and optimize the likelihood on these tokens.Extensive experiments and analysis validate the effectiveness of EDIT across both in-domain(IND) and out-ofdomain(OOD) benchmark reasoning datasets 1 .* Kun Li is the corresponding author. 1 Code can be found at https://github.com/ C-W-D/EDIT On the floor, I see two magenta scrunchiephone chargers, one gold fidget spinner, three gold booklets, three silver scrunchiephone chargers, two silver booklets, and two magenta booklets.If I remove all the magenta items from the floor, how many scrunchiephone chargers remain on it?Op ons: (A) zero (B) one (C) two (D) three (E) four (F) five (G) six According to this ques on, there are two magenta scrunchiephone chargers and three silver scrunchiephone chargers on the floor.If we remove all the magenta items from the floor, we are le with 2 silver scrunchiephone chargers.Therefore, the answer is (C).According to this ques on, there are two magenta scrunchiephone chargers and three silver scrunchiephone chargers on the floor.If we remove all the magenta items, we are le with only the silver scrunchiephone chargers.Therefore, the number of scrunchiephone chargers that remain on the floor is three.Therefore, the answer is (D).Teacher Ques on Unthinking Student On the floor, I see two magenta scrunchiephone chargers, one gold fidget spinner...According to this ques on, there are two magenta scrunchiephone chargers and three silver scrunchiephone chargers on the floor.If we remove all the magenta items from the floor, we are le with 2 silver scrunchiephone chargers.Therefore, the answer is (C).According to this ques on, there are a total of 5 scrunchiephone chargers on the floor: 2 magentascrunchiephone chargers and 3 silver scrunchiephone chargers.If we remove all the magenta items from the floor, we remove the 2 magenta scrunchiephone chargers.Therefore, the number of scrunchiephone chargers remaining on the floor is 3. Therefore, the answer is (D).

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Inspiration

**SCOTT: Self-Consistent Chain-of-Thought Distillation** (2023)
- *Authors:* Peifeng Wang et al.
- *Direct Connection:* SCOTT’s use of counterfactual/coherent CoT data to promote faithful reasoning directly inspired EDIT’s construction of dual CoT pairs with divergent conclusions, from which EDIT then mines decisive tokens.

**Beyond Imitation: Leveraging Fine-Grained Quality Signals for Alignment** (2024) [[arXiv](https://arxiv.org/abs/2311.04072)]
- *Authors:* Geyang Guo et al.
- *Direct Connection:* EDIT borrows the insight of using fine-grained (token-level) quality signals and adapts it to reasoning by weighting tokens identified as key steps via edit distance to guide positive and negative likelihood training.

### 🏷️ Gap Identification

**Learning from Mistakes Makes LLM Better Reasoner (LEMA)** (2023) [[arXiv](https://arxiv.org/abs/2310.20689)]
- *Authors:* Shengnan An et al.
- *Direct Connection:* LEMA showed that training on corrected mistakes improves reasoning but primarily targeted large models, highlighting a gap that EDIT fills by leveraging teacher mistakes for SLM distillation and explicitly isolating key reasoning steps.

### 🏷️ Baseline

**Teaching Small Language Models to Reason** (2023)
- *Authors:* Lucie Charlotte Magister et al.
- *Direct Connection:* This work established the standard CoT distillation paradigm—supervised fine-tuning on correct teacher rationales—which EDIT explicitly augments by incorporating teacher mistakes and focusing training on key reasoning steps to avoid mere style imitation.

### 🏷️ Extension

**STAR: Bootstrapping Reasoning with Reasoning (Rationalization)** (2022)
- *Authors:* Eric Zelikman et al.
- *Direct Connection:* EDIT extends STAR’s answer-hint rationalization by using an answer-hint prompt to rectify teacher-wrong CoTs into correct ones with similar reasoning paths, enabling formation of dual CoTs for key-step identification.

### 🏷️ Related Problem

**Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes** (2023)
- *Authors:* Cheng-Yu Hsieh et al.
- *Direct Connection:* By separating rationale and answer distillation within a supervised framework, this work exemplifies correct-CoT-only training whose limitations (overfitting to reasoning form rather than key steps) motivated EDIT’s mistake-driven, key-step-focused distillation.

---

## Synthesis: How Prior Work Led to This Paper

Standard chain-of-thought (CoT) distillation showed that small models can inherit reasoning by supervised fine-tuning on correct teacher rationales, but it largely mirrors surface forms (Magister et al., 2023). A related line separated rationale and answer supervision to better structure learning, yet still trained only on correct CoTs, risking form imitation instead of acquiring decisive reasoning moves (Hsieh et al., 2023). Another thread introduced counterfactual data to encourage faithful reasoning, suggesting that contrasting explanations can reveal crucial decision points (Wang et al., 2023a). In parallel, rationalization with answer hints demonstrated that providing the correct answer can steer models to produce aligned rationales, offering a practical way to generate corrected explanations that are structurally similar to mistaken ones (Zelikman et al., 2022). From the alignment perspective, weighting fine-grained (token-level) quality signals proved effective for guiding learning beyond coarse labels (Guo et al., 2024). Complementing these, mistake-centric training indicated that corrected errors can sharpen reasoning, though prior efforts focused on larger models and did not pinpoint which parts of the rationale were most decisive (An et al., 2023). Taken together, these works reveal an opportunity: construct paired (dual) rationales that differ in conclusion yet share path structure, then emphasize the exact tokens that flip outcomes. Building on this, the current paper generates dual CoTs by rectifying and corrupting teacher explanations, localizes key steps via edit distance, and applies token-weighted objectives to promote correct decisive moves and suppress erroneous ones—naturally extending CoT distillation from form imitation to key-step learning and improving generalization.

---

*Analysis generated on: 2026-04-05T12:03:39.934231*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
