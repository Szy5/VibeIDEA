# 技术方案设计

## 1. 目录结构（重构后）

```
2-front/
├── backend/                    # 后端：推荐流水线（Python）
│   ├── __init__.py
│   ├── main.py                 # CLI 入口
│   ├── paper.py                # ArxivPaper 模型
│   ├── recommender.py          # 重排序
│   ├── llm.py                  # LLM 封装
│   ├── construct_email.py
│   ├── construct_wechat.py
│   ├── construct_feishu.py
│   └── ...
├── public/                     # 静态资源 + 推荐数据输出目录
│   └── recommendations/        # latest.json, papers_YYYY-MM-DD.json
├── src/                        # 前端（React + Vite）
│   ├── main.jsx
│   ├── App.jsx
│   ├── Layout.jsx
│   ├── theme.js
│   ├── constants/
│   │   └── api.js              # 接口/静态资源 URL 等常量
│   ├── components/
│   │   └── PaperCard.jsx       # 论文卡片
│   └── pages/
│       ├── ArxivDaily.jsx
│       └── KnowledgeGraph.jsx
├── index.html
├── package.json
├── vite.config.js
├── requirements.txt            # Python 依赖（根目录，便于一键安装）
├── .env / .env.example
├── docs/
│   ├── requirements.md
│   └── technical-design.md
└── README.md
```

---

## 2. 后端技术方案

### 2.1 运行方式

- **工作目录**：在**项目根目录**执行 `python -m backend.main`，或进入 `backend` 后执行 `python main.py`（见 README 约定）。
- **输出路径**：推荐 JSON 写入 `public/recommendations/`（相对 backend 为 `../public/recommendations`），由 `main.py` 根据 `__file__` 解析项目根目录后拼接路径，保证无论从根目录还是 backend 目录运行都能写对位置。

### 2.2 模块职责

| 模块 | 职责 |
|------|------|
| `main.py` | 参数解析、流程编排：Zotero → arXiv → Rerank → 写 JSON → 邮件/微信/飞书 |
| `paper.py` | `ArxivPaper` 及 `to_web_dict()`，与前端 JSON 契约一致 |
| `recommender.py` | 基于 sentence-transformers 与时间衰减的 rerank |
| `llm.py` | 全局 LLM（OpenAI / 本地），供 TLDR 等调用 |
| `construct_*.py` | 各渠道的渲染与发送（文件/网络） |

### 2.3 路径与配置

- `RECOMMENDATIONS_DIR`：`os.path.join(os.path.dirname(__file__), "..", "public", "recommendations")`（当 `__file__` 在 `backend/main.py` 时指向项目根下 `public/recommendations`）；若从项目根 `python -m backend.main` 运行，则 `__file__` 为 `backend/main.py`，同样正确。
- 飞书消息等输出文件路径可继续写当前工作目录或显式指定到项目根，在 README 中说明即可。

---

## 3. 前端技术方案

### 3.1 技术栈

- React 18 + Vite 5，react-router-dom 7，D3 7。
- 无全局状态库，页面级 `useState`/`useEffect` 即可。

### 3.2 结构约定

- **常量**：`src/constants/api.js` 统一存放 `RECOMMENDATIONS_URL` 等，便于后续改为环境变量或代理。
- **组件**：可复用 UI 放入 `src/components/`，如 `PaperCard.jsx`；页面级组件放在 `src/pages/`（ArxivDaily、KnowledgeGraph）。
- **主题**：仅使用 `src/theme.js` 的 `theme` 与 `fontImports`，不在页面内重复写字体 `@import`。

### 3.3 数据流

- 每日推荐：`fetch(RECOMMENDATIONS_URL)` → `latest.json` → 列表 + 搜索过滤。
- 图谱：仍使用页面内静态数据（或后续扩展为从 JSON/API 加载），本次仅做路径与引用整理。

### 3.4 路由

- `/` → ArxivDaily  
- `/graph` → KnowledgeGraph（embedded）

---

## 4. 前后端协作契约

- **推荐列表 JSON**（`public/recommendations/latest.json`）格式：

```json
{
  "date": "YYYY-MM-DD",
  "count": 15,
  "papers": [
    {
      "id": "2302.11799",
      "arxivId": "2302.11799",
      "title": "...",
      "abstract": "...",
      "tldr": "...",
      "authors": [],
      "category": "cs.AI",
      "categories": ["cs.AI", "cs.LG"],
      "date": "2026-03-11",
      "link": "https://arxiv.org/abs/2302.11799",
      "pdf_url": "...",
      "code_url": null
    }
  ]
}
```

- 前端使用字段：`id`/`arxivId`、`title`、`abstract`、`tldr`、`category`/`categories`、`date`、`link` 等，与 `paper.to_web_dict()` 保持一致。

---

## 5. 重构实施要点

1. **后端**：新建 `backend/`，将现有根目录 Python 文件迁入；统一使用「相对 backend 的上一级」解析 `public/recommendations`；保持 `requirements.txt` 在根目录。
2. **前端**：新增 `constants/api.js`、`components/PaperCard.jsx`；将 `KnowledgeGraph.jsx` 移入 `pages/` 并删除其内重复的 font 引用；ArxivDaily 引用 `PaperCard` 与 `RECOMMENDATIONS_URL`。
3. **入口**：README 中明确 `npm run dev` / `npm run build` 与 `python -m backend.main`（或 `cd backend && python main.py`）及 `.env` 配置。
4. **验证**：重构后执行一次后端流水线（可用 `--debug` 减少数据量）并确认 `public/recommendations/latest.json` 更新；再执行 `npm run build` 与 `npm run preview` 检查前端展示与请求是否正常。
