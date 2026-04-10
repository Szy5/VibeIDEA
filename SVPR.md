# Symbolic Verifiable Process Reward (SVPR)

## 1. 基础定义

**定义1（知识图谱）**：知识图谱 $\mathcal{G} = (\mathcal{E}, \mathcal{R}, \mathcal{T})$，其中 $\mathcal{E}$ 为实体集合，$\mathcal{R}$ 为关系集合，$\mathcal{T} \subseteq \mathcal{E} \times \mathcal{R} \times \mathcal{E}$ 为三元组集合。

**定义2（图函数）**：定义七个图操作函数：

$$\mathcal{F} = \{f_{\text{out}},\ f_{\text{in}},\ f_{\text{tail}},\ f_{\text{head}},\ f_{\text{filter}},\ f_{\cap},\ f_{\cup}\}$$

每个函数的类型签名：

| 函数 | 输入 | 输出 | 对应FOL语义 |
|------|------|------|------------|
| $f_{\text{tail}}(e, r)$ | 实体, 关系 | 实体集 | $\{x \mid (e, r, x) \in \mathcal{T}\}$ |
| $f_{\text{head}}(e, r)$ | 实体, 关系 | 实体集 | $\{x \mid (x, r, e) \in \mathcal{T}\}$ |
| $f_{\text{filter}}(S, r, v)$ | 实体集, 关系, 值 | 实体集 | $\{x \in S \mid (x, r, v) \in \mathcal{T}\}$ |
| $f_{\cap}(S_1, ..., S_n)$ | 实体集列表 | 实体集 | $S_1 \cap \cdots \cap S_n$ |
| $f_{\cup}(S_1, ..., S_n)$ | 实体集列表 | 实体集 | $S_1 \cup \cdots \cup S_n$ |

---

## 2. 查询计算树（Query Computation Tree, QCT）

**定义3（QCT）**：给定问题 $Q$，其标注的SPARQL查询 $\psi(Q)$ 可被解析为一棵有根有序树 $\mathcal{C} = (V, E, \ell)$，其中：
- 叶节点为锚实体（topic entity）
- 内部节点为图操作函数 $f \in \mathcal{F}$
- 根节点的输出为答案实体集

**示例**："奥巴马的妻子的母校在哪个国家？"

```
SPARQL: SELECT ?ans WHERE {
  ?wife    :spouse      wd:Q76 .      # Q76 = Obama
  ?school  :educated_at ?wife .
  ?ans     :country     ?school .
}

QCT：
        f_tail(·, country)
               |
        f_head(·, educated_at)
               |
        f_tail(Obama, spouse)
```

对应函数调用序列：
```python
s1 = f_tail('Obama', 'spouse')       # {Michelle Obama}
s2 = f_head(s1, 'educated_at')       # {Princeton, Harvard Law}
s3 = f_tail(s2, 'country')           # {USA}
```

**定义4（调用树）**：将模型生成的函数调用序列解析为树 $\hat{\mathcal{C}} = (\hat{V}, \hat{E}, \hat{\ell})$，构造规则为：若函数 $\hat{f}_i$ 的输入集合来自 $\hat{f}_j$ 的输出，则 $\hat{f}_j$ 是 $\hat{f}_i$ 的子节点。

---

## 3. 三级过程奖励

**定义5（过程奖励函数）**：

$$r_{\text{process}}(\tau, Q, \mathcal{G}) = \lambda_1 \cdot r_{\text{exec}} + \lambda_2 \cdot r_{\text{triple}} + \lambda_3 \cdot r_{\text{struct}}$$

### 第一级：执行合法性奖励 $r_{\text{exec}}$

验证每次函数调用是否在 $\mathcal{G}$ 上返回了非空结果：

$$r_{\text{exec}} = \frac{1}{|\tau|} \sum_{i=1}^{|\tau|} \mathbb{1}[f_i(\cdot) \neq \emptyset]$$

> **直觉**：如果模型调用了 $f_{\text{tail}}(e, r)$ 但 $(e, r, *)$ 在图中根本不存在，说明模型在幻觉——它"凭空"使用了一个不存在的关系。

### 第二级：三元组相关性奖励 $r_{\text{triple}}$

设 $\mathcal{T}^* \subseteq \mathcal{T}$ 为标注的关键三元组集合（数据合成时记录）。设模型推理过程中实际访问的三元组集合为 $\hat{\mathcal{T}}$：

$$r_{\text{triple}} = \frac{|\hat{\mathcal{T}} \cap \mathcal{T}^*|}{|\mathcal{T}^*|}$$

> **直觉**：如果模型最终答对了，但访问的是无关三元组，说明答案来自参数知识而非图推理。

### 第三级：结构一致性奖励 $r_{\text{struct}}$

比较模型的调用树 $\hat{\mathcal{C}}$ 与标注QCT $\mathcal{C}^*$ 的结构相似度：

$$r_{\text{struct}} = \text{TreeEditSim}(\hat{\mathcal{C}},\ \mathcal{C}^*)$$

其中 $\text{TreeEditSim}$ 基于树编辑距离（Tree Edit Distance）定义：

$$\text{TreeEditSim}(\hat{\mathcal{C}}, \mathcal{C}^*) = 1 - \frac{\text{TED}(\hat{\mathcal{C}}, \mathcal{C}^*)}{|V^*|}$$

节点匹配规则：当且仅当两节点的函数类型相同（如同为 $f_{\text{tail}}$）且关系参数相同时，视为匹配。

> **直觉**：这一项强制模型不仅找到正确答案，还要用正确的逻辑结构找到它。

---

## 4. 完整奖励函数

$$r_{\text{total}} = \underbrace{r_{\text{format}}}_{\text{格式奖励}} + \underbrace{\lambda_1 r_{\text{exec}} + \lambda_2 r_{\text{triple}} + \lambda_3 r_{\text{struct}}}_{\text{过程奖励}\ r_{\text{process}}} + \underbrace{r_{\text{outcome}}}_{\text{结果奖励}}$$

其中结果奖励（允许集合部分匹配）：

$$r_{\text{outcome}} = \mathbb{1}[\hat{A} \cap A^* \neq \emptyset]$$

$\hat{A}$ 为模型预测的答案集，$A^*$ 为标注答案集。

---

## 5. 核心命题

**命题1（忠实性充分条件）**：若模型轨迹 $\tau$ 满足：
1. $r_{\text{exec}} = 1$（所有调用返回非空）
2. $r_{\text{struct}} = 1$（调用树与QCT完全同构）

则 $\tau$ 在 $\mathcal{G}$ 上是**可验证忠实**的，即答案 $\hat{A}$ 是由 $\mathcal{G}$ 中存在的三元组链推导得出，而非模型参数知识。

**证明思路**：由 $r_{\text{struct}} = 1$，调用树与QCT同构，说明执行的逻辑结构与问题的FOL公式一致。由 $r_{\text{exec}} = 1$，每步函数调用都在 $\mathcal{G}$ 上有实际返回，说明推理路径是图中真实存在的路径。两者合取，答案只能来自图中路径，不可能依赖参数知识。$\square$

---

## 6. 忠实性评估协议

| 指标 | 形式化定义 | 测量方式 |
|------|------------|----------|
| **PA**（参数准确率, Parametric Accuracy） | $\Pr[\hat{A} \cap A^* \neq \emptyset \mid \text{无图访问}]$ | 禁用所有图函数调用，模型纯参数回答 |
| **GA**（图接地准确率, Grounded Accuracy） | $\Pr[\hat{A} \cap A^* \neq \emptyset \mid \text{正常推理}]$ | 正常Agentic推理 |
| **SA**（虚假准确率, Spurious Accuracy） | $\Pr[\hat{A} \cap A^* \neq \emptyset \mid \mathcal{G}' = \mathcal{G} \setminus \mathcal{T}^*]$ | 删除关键三元组后推理，答对则说明靠参数知识 |
| **FS**（忠实性得分, Faithfulness Score） | $\text{GA} - \text{SA}$ | 越高越好 |

> **说明**：若 $\text{PA} \approx \text{GA}$，说明模型根本没在利用图结构，需重点排查。

---

## 7. 待讨论问题

- **$r_{\text{struct}}$ 的严格性**：树编辑距离可能对等价调用顺序惩罚过重（例如先求交集还是先过滤，逻辑等价但树结构不同）。可考虑改为更宽松的**图同构匹配**或引入语义等价规则。
- **$\lambda$ 系数调优**：$\lambda_1, \lambda_2, \lambda_3$ 的比例需消融实验确定。
- **$\mathcal{T}^*$ 的完备性**：数据合成时需确保关键三元组标注不遗漏，否则 $r_{\text{triple}}$ 会低估忠实度。
