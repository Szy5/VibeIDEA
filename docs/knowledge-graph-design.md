## 科学发现知识图谱技术方案

### 1. 目标与输入

- **目标**: 基于 `results/prior_work_analysis_*.json` 构建可视化的科学发现知识图谱, 支持前端展示单篇论文的本地图谱与全局论文图谱, 并且可随新增 JSON 增量更新。
- **输入**: 每个 JSON 形如:
  - `paper_title`, `paper_arxiv_id`, `paper_abstract`
  - `prior_works`: 其中每项有 `title`, `year`, `role`, `relationship_sentence`, `arxiv_id`, `url`
  - `synthesis_narrative`: 对主论文与前人工作的综合性文字总结
  - `innovation_classification`: 创新模式(tag)

---

### 2. 图谱数据模型

- **节点 (Paper)**  
  - `id`: 论文唯一 ID, 规则:
    - 优先使用 `arxiv_id` (如 `2302.11799`);
    - 若无 `arxiv_id`, 使用 `sha1(f\"{title}-{year}\")[:12]` 等稳定哈希。
  - `title`: 论文标题 (`paper_title` 或 `prior_work.title`)
  - `year`: 年份 (`prior_work.year` 或从外部/文件名补全主论文年份)
  - `authors`: 数组或逗号分隔字符串
  - `arxiv_id`: 可选, 用于跳转 arXiv 页面
  - `source`: `"main"` / `"prior_work"` 用于区分被分析论文与其前人工作
  - `patterns`: 来自 `innovation_classification.primary_pattern_name` 和 `secondary_pattern_names`
  - `narratives`: 数组, 存储该论文相关的所有 `synthesis_narrative` 片段 (通常只对主论文存在, 但允许多版本累积)
  - `degree_in` / `degree_out`: 后处理统计, 便于前端按影响力控制节点大小

- **边 (主论文 → 前人工作)**  
  - `source`: 主论文节点 `id` (`paper_arxiv_id` 对应的 canonical id)
  - `target`: 前人工作节点 `id` (`prior_work.arxiv_id` 或 fallback id)
  - `role`: 原始 `role` 字段 (如 `Baseline`, `Foundation`, `Gap Identification`, `Inspiration` 等)
  - `relation_type`: 将 `role` 归类成少数几种规范化类型, 供前端配色/过滤:
    - `Baseline` → `IMPROVES_OVER`
    - `Foundation` → `BUILDS_ON`
    - `Gap Identification` → `IDENTIFIES_GAP_OF`
    - `Inspiration` → `INSPIRED_BY`
    - dataset/benchmark 类角色 → `EVALUATED_ON` / `USES_DATASET`
    - 未覆盖角色 → `OTHER`
  - `description`: `relationship_sentence`, 为边提供自然语言解释
  - 可选统计: `weight` (基于 role 和时间差启发式赋权), `year_diff` (主论文与前人工作发表年份差)

- **图级结构**  
  输出给前端的标准结构:
  ```jsonc
  {
    "nodes": [
      {
        "id": "2302.11799",
        "title": "FiTs: Fine-grained Two-stage Training ...",
        "year": 2023,
        "authors": ["..."],
        "arxiv_id": "2302.11799",
        "source": "main",
        "patterns": ["Modular Pipeline Composition", "Cross-Domain Synthesis"],
        "narratives": ["GreaseLM established the concrete LM+GNN ..."],
        "degree_in": 12,
        "degree_out": 5
      }
    ],
    "edges": [
      {
        "source": "2302.11799",
        "target": "2201.08860",
        "role": "Baseline",
        "relation_type": "IMPROVES_OVER",
        "description": "GreaseLM is the backbone the paper adopts and improves upon ...",
        "weight": 1.0,
        "year_diff": 1
      }
    ]
  }
  ```

---

### 3. 全量构建流程

以离线脚本 `backend/build_knowledge_graph.py` 为例, 做一次全量构建:

1. **遍历 JSON**  
   - 扫描 `results/prior_work_analysis_*.json`  
   - 对每个文件读取:
     - 主论文信息: `paper_title`, `paper_arxiv_id`, `paper_abstract`
     - `prior_works` 列表
     - `synthesis_narrative`
     - `innovation_classification`

2. **节点去重与合并**  
   - 维护 `nodes_by_id: Dict[str, Node]`
   - 为主论文和每个 `prior_work` 构造 canonical id:
     - 有 `arxiv_id` 时直接使用其标准化字符串;
     - 否则使用 `title+year` 的哈希。
   - 若 `nodes_by_id` 中不存在该 id:
     - 创建节点, 填充 `title/year/authors/arxiv_id/source`;
     - 对主论文还写入 `patterns`。
   - 若节点已存在:
     - 仅补全缺失字段;
     - 对 `patterns/narratives` 做集合并集。

3. **构建边列表**  
   - 维护 `edges: List[Edge]` (可同时维护 `(source, target, role)` → edge 的索引用于去重)。
   - 对当前 JSON 中每个 `prior_work`:
     - `source = main_paper_id`
     - `target = prior_id`
     - `role = prior_work.role`
     - `relation_type = role_to_relation_type.get(role, \"OTHER\")`
     - `description = prior_work.relationship_sentence`
     - 追加 edge, 或若已存在则视需要合并描述字段。

4. **挂载 synthesis_narrative**  
   - 找到主论文节点 `nodes_by_id[main_paper_id]`:
     - 若无 `narratives` 字段则初始化为 `[]`;
     - 将 `synthesis_narrative` 追加到 `narratives` 中 (可按时间戳排序去重)。
   - 这样, 每篇主论文节点自带一段或多段“高层故事”文本。

5. **计算统计字段**  
   - 初始化所有节点的 `degree_in = 0`, `degree_out = 0`。
   - 遍历 `edges`:
     - `nodes_by_id[source].degree_out += 1`
     - `nodes_by_id[target].degree_in += 1`
     - 若节点具备年份, 同时在 edge 上计算 `year_diff`。
   - 如需 `weight`, 可基于 `role` (Baseline > Foundation > Inspiration) 和 `year_diff` 计算。

6. **导出图数据**  
   - **全局图**: 导出为 `public/graph/papers_kg.json` (包含所有节点与边)。
   - **局部图 (按主论文)**: 为每篇主论文导出一个 `public/graph/<arxiv_id>.json`:
     - 节点: 主论文 + 它所有直接 prior works;
     - 边: 只包含该主论文作为 `source` 的边。

---

### 4. 增量更新策略

考虑到 `results/` 目录会持续新增/更新 JSON, 需要增量构建能力, 而不是每次全量重算。

1. **索引文件**  
   - 在 `public/graph/` 维护一个索引文件 `papers_kg_index.json`, 结构示例:
     ```jsonc
     {
       "version": 1,
       "last_updated": "2026-03-11T10:00:00",
       "papers": {
         "2302.11799": {
           "file": "prior_work_analysis_2302_11799.json",
           "analysis_timestamp": "2026-03-09T00:19:29.944636"
         }
       }
     }
     ```

2. **增量判断规则**  
   - 扫描 `results/prior_work_analysis_*.json`:
     - 若某文件不在索引中 → 视为**新增**;
     - 若 `analysis_timestamp` 比索引记录更新 → 视为**更新版本**。

3. **增量合并逻辑**  
   - 启动时载入现有的 `papers_kg.json` → 恢复 `nodes_by_id` 与 `edges`。
   - 对每个“新增/更新”的 JSON:
     - 若为新主论文:
       - 按“全量流程”增加节点和边。
     - 若为已存在主论文的新版本:
       - 先删除旧版本主论文对应的出边 (可在索引中记录这篇主论文相关的边列表 key)。
       - 再按“全量流程”重新写入该主论文的节点属性、narratives 与出边。
   - 全部增量处理完后重新跑一次统计字段 (度数等)。
   - 更新 `papers_kg.json` 与 `papers_kg_index.json` 中对应记录。

4. **ID 演进与合并**  
   - 若某 prior work 早期没有 `arxiv_id`, 后续新 JSON 中补全了:
     - 可以设计一个 ID 映射表, 在增量脚本中执行“旧 ID → 新 ID”的节点合并与边重定向;
     - 若此类情况少见, 初期可以只在需要时手动清理。

---

### 5. 前端对接与展示设计

1. **全局图视图**  
   - `KnowledgeGraph` 组件新增“从后端加载”模式:
     - `fetch(\"/graph/papers_kg.json\")` → 使用返回的 `nodes/edges` 渲染;
     - 节点颜色可按 `source`/`patterns`/degree 等, 边颜色/线型按 `relation_type` 区分。

2. **单论文局部图视图**  
   - 在 `ArxivDaily` 中为每篇主论文加一个“查看知识图谱”的入口:
     - 点击后跳转到 `/graph?paper=2302.11799`;
     - `KnowledgeGraph` 读取 query 参数, 从 `/graph/2302.11799.json` 加载局部子图。

3. **synthesis_narrative 的前端呈现**  
   - 节点详情面板展示:
     - 标题/年份/作者/模式标签;
     - narrative 列表 (带滚动或“展开更多”按钮)。
   - 可在边 hover 或侧边栏中显示 `description`(relationship_sentence), 形成“节点故事 + 边关系语句”的组合解释。

