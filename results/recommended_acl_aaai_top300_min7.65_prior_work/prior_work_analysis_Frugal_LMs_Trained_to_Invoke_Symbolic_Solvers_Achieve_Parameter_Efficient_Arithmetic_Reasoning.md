# Prior Work Analysis Report

## Target Paper

**Title:** Frugal LMs Trained to Invoke Symbolic Solvers Achieve Parameter-Efficient Arithmetic Reasoning

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Large Language Models (LLM) exhibit zero-shot mathematical reasoning capacity as a behavior emergent with scale, commonly manifesting as chain-of-thoughts (CoT) reasoning. However, multiple empirical findings suggest that this prowess is exclusive to LLMs that have exorbitant sizes (beyond 50 billion parameters). Meanwhile, educational neuroscientists suggest that symbolic algebraic manipulation be introduced around the same time as arithmetic word problems so as to modularize language-to-formulation, symbolic manipulation of the formulation, and endgame arithmetic. In this paper, we start with the hypothesis that much smaller LMs, which are weak at multi-step reasoning, can achieve reasonable arithmetic reasoning if arithmetic word problems are posed as a formalize-then-solve task. In our architecture, which we call SyReLM, the LM serves the role of a translator to map natural language arithmetic questions into a formal language (FL) description. A symbolic solver then evaluates the FL expression to obtain the answer. A small frozen LM, equipped with an efficient low-rank adapter, is capable of generating FL expressions that incorporate natural language descriptions of the arithmetic problem (e.g., variable names and their purposes, formal expressions combining variables, etc.). We adopt policy-gradient reinforcement learning to train the adapted LM, informed by the non-differentiable symbolic solver. This marks a sharp departure from the recent development in tool-augmented LLMs, in which the external tools (e.g., calculator, Web search, etc.) are essentially detached from the learning phase of the LM. SyReLM shows massive improvements (e.g., +30.65 absolute point improvement in accuracy on the SVAMP dataset using GPT-J 6B model) over base LMs, while keeping our testbed easy to diagnose and interpret, and within the reach of most researchers.

---

## Key Prior Works (7 papers with direct influence)

### 🏷️ Foundation

**PAL: Program-aided Language Models** (2022) [[arXiv](https://arxiv.org/abs/2211.10435)]
- *Authors:* Liang Gao et al.
- *Direct Connection:* PAL established the paradigm of having an LM generate executable Python as an intermediate representation and delegating computation to a Python interpreter, which SyReLM adopts as its core formalize-then-solve substrate.

**LoRA: Low-Rank Adaptation of Large Language Models** (2021) [[arXiv](https://arxiv.org/abs/2106.09685)]
- *Authors:* Edward J. Hu et al.
- *Direct Connection:* SyReLM relies on LoRA’s parameter-efficient adapters to adapt a frozen small LM for formal-language translation, enabling its frugal training regime without full model fine-tuning.

### 🏷️ Inspiration

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (2022) [[arXiv](https://arxiv.org/abs/2201.11903)]
- *Authors:* Jason Wei et al.
- *Direct Connection:* SyReLM draws directly on Chain-of-Thought’s insight by eliciting explicit stepwise reasoning as comments aligned with the generated code, thereby blending CoT with program-of-thought execution.

### 🏷️ Gap Identification

**ART: Automatic multi-step reasoning and tool-use for large language models** (2023)
- *Authors:* Bhargavi Paranjape et al.
- *Direct Connection:* ART showed multi-step tool orchestration but relied on very large LMs and did not parameter-efficiently adapt smaller models, motivating SyReLM’s focus on frugal LMs with integrated solver feedback during training.

### 🏷️ Baseline

**Toolformer: Language Models Can Teach Themselves to Use Tools** (2023) [[arXiv](https://arxiv.org/abs/2302.04761)]
- *Authors:* Timo Schick et al.
- *Direct Connection:* Toolformer is a primary baseline for learning tool invocation via a halt–compute–resume loop, against which SyReLM contrasts by integrating the external solver into the learning phase rather than only inserting tool outputs as tokens.

### 🏷️ Extension

**Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks** (2022) [[arXiv](https://arxiv.org/abs/2211.12588)]
- *Authors:* Wenhu Chen et al.
- *Direct Connection:* Building on PoT’s use of programs as intermediate reasoning, SyReLM extends the approach by requiring Python (or parsable pseudocode) with inline natural-language comments and training the LM with solver-informed reinforcement to generate such programs.

**Making Language Models Better Tool Learners with Execution Feedback (TRICE)** (2023) [[arXiv](https://arxiv.org/abs/2305.13068)]
- *Authors:* Shuofei Qiao et al.
- *Direct Connection:* SyReLM extends TRICE’s execution-feedback RL idea by defining fine-grained rewards (compilation success, variable/operator alignment, and final answer correctness) to train program generation that invokes a symbolic solver.

---

## Synthesis: How Prior Work Led to This Paper

Program-aided approaches such as PAL demonstrated that numerical reasoning benefits when an LM translates a problem into executable Python and offloads computation to an interpreter, establishing programs as a practical formal language. Program of Thoughts prompting reinforced this by framing programs as the intermediate reasoning substrate for math word problems, separating symbolic computation from language generation. Chain-of-Thought prompting, in turn, showed that eliciting explicit intermediate steps improves reasoning, pointing to the value of human-interpretable traces. Toolformer introduced a halt–compute–resume interaction pattern in which LMs learn to call external tools, providing a concrete mechanism for integrating tool outputs into language generation. TRICE then brought execution feedback into training, using reinforcement signals from tool outcomes to shape tool use policies. Finally, LoRA made it feasible to adapt frozen base models with small parameter-efficient adapters, enabling resource-limited settings to specialize models without full fine-tuning. ART highlighted both the promise of multi-step tool use and the practical limitation that prior methods often presupposed very large models and did not integrate execution into learning for smaller LMs.
Collectively, these works surfaced an opportunity: combine program-based intermediates with explicit reasoning traces, integrate solver execution into the learning loop, and do so with parameter-efficient adaptation so smaller models can reliably invoke tools. SyReLM synthesizes this by training LoRA-augmented, frugal LMs to translate text into Python or parsable pseudocode with CoT-like comments, and by using PPO with solver-informed, fine-grained rewards (compilation, variable/operator alignment, and answer correctness). This unifies CoT and program execution while bringing tool use into training, yielding a practical, interpretable, and effective formalize-then-solve pipeline for arithmetic reasoning.

---

*Analysis generated on: 2026-04-05T12:03:20.086830*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
