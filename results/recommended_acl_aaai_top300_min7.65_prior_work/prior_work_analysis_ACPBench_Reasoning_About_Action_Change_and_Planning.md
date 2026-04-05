# Prior Work Analysis Report

## Target Paper

**Title:** ACPBench: Reasoning About Action, Change, and Planning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> There is an increasing body of work using Large Language Models (LLMs) as agents for orchestrating workflows and making decisions in domains that require planning and multistep reasoning. As a result, it is imperative to evaluate LLMs on core skills required for planning. In this work, we present ACPBench, a benchmark for evaluating the reasoning tasks in the field of planning. The benchmark consists of 7 reasoning tasks over 13 planning domains. The collection is constructed from planning domains described in a formal language. This allows us to synthesize problems with provably correct solutions across many tasks and domains. Further, it allows us the luxury of scale without additional human effort, i.e., many] additional problems can be created automatically. Our extensive evaluation of 21 LLMs and OpenAI o1 reasoning models highlight the significant gap in the reasoning capability of the LLMs. Our findings with OpenAI o1, a multi-turn reasoning model, reveal significant gains in performance on multiple-choice questions, yet surprisingly, no notable progress is made on boolean questions.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**The 1998 AI Planning Systems Competition** (2000)
- *Authors:* Drew McDermott
- *Direct Connection:* PDDL, established and popularized within the planning community, provides the formal action/state semantics ACPBench relies on to synthesize large-scale problems and guarantee correctness of answers.

### 🏷️ Inspiration

**AutoPlanBench: Automatically generating benchmarks for LLM planners from PDDL** (2024) [[arXiv](https://arxiv.org/abs/2311.09830)]
- *Authors:* Kilian Stein et al.
- *Direct Connection:* AutoPlanBench showed how to scale PDDL-to-NL benchmarks and provided a domain set that ACPBench adopts and expands upon, while addressing AutoPlanBench’s focus on only plan generation by adding diverse reasoning tasks.

**Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them** (2023) [[arXiv](https://arxiv.org/abs/2210.09261)]
- *Authors:* Mert Yuksekgonul Suzgun et al.
- *Direct Connection:* The BigBench Hard shuffle task’s focus on tracking changes inspired ACPBench’s emphasis on progression/effects and directly motivated creation of the new Swap domain.

### 🏷️ Gap Identification

**PlanBench: An Extensible Benchmark for Evaluating Large Language Models on Planning and Reasoning about Change** (2023)
- *Authors:* Karthik Valmeekam et al.
- *Direct Connection:* PlanBench’s PDDL-derived benchmark highlighted that LLM planning evaluation was confined to a small set of domains and task types, directly motivating ACPBench’s broader, multi-task design across many domains with provable labels.

**ActionReasoningBench: Reasoning about Actions with and without Ramification Constraints** (2024) [[arXiv](https://arxiv.org/abs/2406.04046)]
- *Authors:* Dhruv Handa et al.
- *Direct Connection:* ActionReasoningBench covered a subset of action reasoning tasks but lacked key capabilities like reachability, validation, justification, and landmarks, gaps ACPBench explicitly fills with dedicated tasks and provable labels.

### 🏷️ Extension

**Landmarks Revisited** (2008)
- *Authors:* Silvia Richter, Malte Helmert, and Matthias Westphal
- *Direct Connection:* ACPBench’s Landmark task uses the RHW method to extract a sound subset of landmarks, directly enabling automatic labeling of necessary subgoals across domains.

**RIFO Revisited: Detecting Relaxed Irrelevance** (2001)
- *Authors:* Jörg Hoffmann and Bernhard Nebel
- *Direct Connection:* Delete-relaxed reachability from this work underpins ACPBench’s construction of guaranteed-unreachable facts for negative examples in the Reachability and Action Reachability tasks.

---

## Synthesis: How Prior Work Led to This Paper

PlanBench established that LLM planning evaluation can be grounded in PDDL, but revealed practical limits: it concentrated on a small set of domains and tasks while using templates to pose planning questions. AutoPlanBench demonstrated how to scale PDDL-to-natural-language generation across many domains and automated template creation, though it restricted evaluation to plan generation. In parallel, ActionReasoningBench expanded action-centric testing (e.g., executability and effects), yet omitted crucial planning competencies such as reachability, validation, justification, and landmarks that are necessary for reliable planning workflows. At the core of these efforts lies PDDL’s formal specification of states, actions, and goals, which enables synthesizing questions with provable correctness. For specific capability labels, the RHW landmark extraction method offers a principled way to derive necessary subgoals, and delete-relaxed reachability provides a polynomial-time filter for constructing guaranteed-unreachable targets—both critical for automated, large-scale labeling. Complementing this, the BigBench Hard shuffle task exposed LLM weaknesses in tracking change, suggesting the need for focused evaluation of progression effects.
Collectively, these works pointed to a gap: existing PDDL-derived benchmarks either emphasized a narrow slice of planning (plan generation) or lacked key skills assessments, and they did not fully exploit formal methods to guarantee correctness across many domains. ACPBench naturally emerges by synthesizing these insights—leveraging PDDL semantics and landmark and reachability machinery to produce provably labeled datasets—and broadening scope to seven core tasks (applicability, progression, reachability, action reachability, validation, justification, and landmarks), with a new shuffle-inspired Swap domain to stress test change tracking at scale.

---

*Analysis generated on: 2026-04-05T11:56:24.225906*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
