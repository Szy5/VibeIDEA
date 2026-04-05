# Prior Work Analysis Report

## Target Paper

**Title:** Walk Wisely on Graph: Knowledge Graph Reasoning with Dual Agents via Efficient Guidance-Exploration

**arXiv ID:** [N/A](https://arxiv.org/abs/N/A)

**Abstract:** 
> Recent years, multi-hop reasoning has been widely studied for knowledge graph (KG) reasoning due to its efficacy and interpretability. However, previous multi-hop reasoning approaches are subject to two primary shortcomings. First, agents struggle to learn effective and robust policies at the early phase due to sparse rewards. Second, these approaches often falter on specific datasets like sparse knowledge graphs, where agents are required to traverse lengthy reasoning paths. To address these problems, we propose a multi-hop reasoning model with dual agents based on hierarchical reinforcement learning (HRL), which is named FULORA. FULORA tackles the above reasoning challenges by eFficient GUidance-ExpLORAtion between dual agents. The high-level agent walks on the simplified knowledge graph to provide stage-wise hints for the low-level agent walking on the original knowledge graph. In this framework, the low-level agent optimizes a value function that balances two objectives: (1) maximizing return, and (2) integrating efficient guidance from the high-level agent. Experiments conducted on three real-word knowledge graph datasets demonstrate that FULORA outperforms RL-based baselines, especially in the case of long-distance reasoning.

---

## Key Prior Works (6 papers with direct influence)

### 🏷️ Foundation

**Go for a Walk and Arrive at the Answer: Reasoning Over Paths in Knowledge Bases using Reinforcement Learning** (2018)
- *Authors:* Rajarshi Das et al.
- *Direct Connection:* MINERVA established the target-agnostic RL path-walking formulation for multi-hop KG query answering that FULORA adopts at the entity level and augments with hierarchical guidance from a high-level agent.

**Expressing Arbitrary Reward Functions as Potential-Based Advice** (2015)
- *Authors:* Armen Harutyunyan et al.
- *Direct Connection:* FULORA’s dynamic path feedback is a potential-based reward shaping scheme grounded in this work’s theory to provide dense intermediate rewards to the high-level agent while preserving optimal-policy invariance.

### 🏷️ Inspiration

**Maximum a Posteriori Policy Optimisation** (2018)
- *Authors:* Abbas Abdolmaleki et al.
- *Direct Connection:* FULORA follows the Lagrangian multiplier–based policy optimization template from MPO to balance return and a similarity-based guidance constraint, learning a state-dependent weight λ to trade off exploration versus guidance.

### 🏷️ Baseline

**Learning to Walk with Dual Agents for Knowledge Graph Reasoning** (2022)
- *Authors:* Denghui Zhang et al.
- *Direct Connection:* CURL provides the dual-agent GIANT–DWARF framework and cluster-level guidance that FULORA retains, but FULORA replaces CURL’s mutual reinforcement rewards with a guidance–exploration trade-off and reward shaping to prevent policy coupling and improve long-distance reasoning.

### 🏷️ Extension

**Incorporating Graph Attention Mechanism into Knowledge Graph Reasoning Based on Deep Reinforcement Learning** (2019)
- *Authors:* Haoyu Wang et al.
- *Direct Connection:* FULORA directly imports AttnPath’s graph-attention neighbor weighting to compute the attention vector for the low-level agent, focusing exploration on query-relevant edges within the original KG.

### 🏷️ Related Problem

**DeepPath: A Reinforcement Learning Method for Knowledge Graph Reasoning** (2017)
- *Authors:* Wenhan Xiong et al.
- *Direct Connection:* DeepPath pioneered framing KG reasoning as sequential decision-making with RL and informed the path-search and evaluation setup that FULORA builds upon in a hierarchical setting.

---

## Synthesis: How Prior Work Led to This Paper

MINERVA showed that multi-hop KG reasoning could be cast as a target-agnostic RL path-walking problem, defining the core states, actions, and sparse terminal rewards that make path-based inference both effective and interpretable. DeepPath earlier framed KG inference as sequential decision-making with RL, catalyzing the path-search paradigm that shaped later evaluations and training setups. AttnPath demonstrated that injecting graph attention into the RL agent’s decision process effectively biases exploration toward query-relevant neighbors, mitigating local branching. CURL then introduced a dual-agent architecture in which a high-level agent walks a clustered, simplified KG to give stage-wise hints to a low-level agent on the original KG, improving long-distance reasoning but coupling policies via mutual reinforcement rewards and suffering near-random behavior early due to extreme reward sparsity. From the RL theory side, Harutyunyan et al. established potential-based reward shaping as a policy-invariant way to deliver dense intermediate feedback, while Abdolmaleki et al. popularized Lagrangian-multiplier policy objectives for balancing multiple criteria during optimization. Taken together, these works illuminated a path: leverage cluster-level guidance to shrink search, use attention to sharpen local choices, but avoid brittle policy coupling and sparse-reward stagnation. FULORA synthesizes these insights by keeping CURL’s cluster-level guidance yet decoupling it via a learnable Lagrangian trade-off between return and state-similarity guidance, and by shaping the high-level agent’s reward with potential-based dynamic path feedback to accelerate learning; combined with AttnPath-style attention for the low-level agent, this yields robust long-distance reasoning in sparse KGs.

---

*Analysis generated on: 2026-04-05T12:07:56.225253*

*Pipeline: Prior Work Extraction v2.0 (Direct Lineage Focus)*
