# 科研日报 (Research Daily)

基于个人 Zotero 文献库与 arXiv 订阅的每日论文推荐系统：后端生成推荐并写入 JSON，前端展示「每日 ArXiv 推荐」与「科学发现图谱」。

## 目录结构

```
├── backend/           # 后端：推荐流水线（Python）
│   ├── main.py        # CLI 入口
│   ├── paper.py       # 论文模型
│   ├── recommender.py # 重排序
│   ├── llm.py         # LLM 封装
│   └── construct_*.py # 邮件/微信/飞书渲染与发送
├── public/            # 静态资源与推荐数据
│   └── recommendations/  # latest.json, papers_YYYY-MM-DD.json
├── src/               # 前端（React + Vite）
│   ├── constants/    # 接口等常量
│   ├── components/   # 可复用组件
│   ├── pages/        # 页面
│   ├── theme.js      # 设计令牌
│   ├── App.jsx
│   └── Layout.jsx
├── docs/              # 需求与技术设计
├── index.html
├── package.json
├── requirements.txt   # Python 依赖
└── .env / .env.example
```

## 环境要求

- **Node.js** 18+（前端）
- **Python** 3.10+（后端）
- 配置 `.env`（可复制 `.env.example` 后修改）

## 快速开始

### 1. 安装依赖

```bash
# 前端
npm install

# 后端（建议使用虚拟环境；若运行时报 ModuleNotFoundError 请先执行）
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录创建 `.env`，参考 `.env.example` 配置至少：

- `ZOTERO_ID`、`ZOTERO_KEY`（必填）
- 启用邮件时：`SENDER`、`RECEIVER`、`SENDER_PASSWORD`
- 使用 OpenAI 生成 TLDR 时：`OPENAI_API_KEY`

### 3. 运行后端（生成推荐数据）

在**项目根目录**执行：

```bash
python -m backend.main
```

可选参数示例：

- `--debug`：调试模式（取 50 篇论文、不按日期过滤）
- `--max_paper_num 5`：仅保留前 5 篇
- `--enable_email false`：关闭邮件推送

推荐数据会写入 `public/recommendations/latest.json` 与按日期的 `papers_YYYY-MM-DD.json`。

### 4. 运行前端

```bash
npm run dev
```

浏览器访问提示的地址（如 http://localhost:5173），即可查看：

- **每日 ArXiv 推荐**：从 `latest.json` 拉取并展示，支持搜索过滤。
- **科学发现图谱**：D3 力导向图（当前为静态示例数据）。

### 5. 生产构建

```bash
npm run build
npm run preview   # 本地预览构建结果
```

## 知识图谱构建 (offline)

基于 `results/prior_work_analysis_*.json` 可离线构建「主论文–前人工作」科学发现知识图谱，支持 FAISS 标题相似度融合（GPU + 代理）。

**推荐在 conda 环境 `research` 下运行**，并在 `.env` 中配置 `HTTP_PROXY` / `HTTPS_PROXY`，以便首次下载 allenai-specter 模型。详细步骤、参数与常见问题见 **[知识图谱 - 使用说明](docs/知识图谱-使用说明.md)**。

```bash
conda activate research
# 全量重建（推荐首次执行；启用 FAISS 时需代理下载模型）
python -m backend.build_knowledge_graph --full

# 增量更新
python -m backend.build_knowledge_graph
```

生成结果: `public/graph/papers_kg.json`、`papers_kg_index.json`，以及（启用 FAISS 时）`papers_kg_faiss.index`、`papers_kg_faiss_ids.json`。前端从 `papers_kg.json` 读取图数据展示（schema 见 `docs/knowledge-graph-design.md`）。

## 数据流说明

1. 后端 `backend/main.py`：拉取 Zotero 文献 → 拉取 arXiv 新论文 → 重排序 → 可选 LLM 生成 TLDR → 写入 `public/recommendations/` → 可选邮件/微信/飞书推送。
2. 前端从 `/recommendations/latest.json` 读取静态 JSON 展示，无需常驻后端服务。

## 文档

- [需求设计](docs/requirements.md)
- [技术方案](docs/technical-design.md)

## 许可与致谢

仅供学习与个人使用。推荐逻辑依赖 Zotero、arXiv、sentence-transformers 与可选 OpenAI/本地 LLM。
