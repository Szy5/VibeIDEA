# prior-work 元信息校准交接文档

## 1. 目标

这部分工作的目标，是对 prior work analysis 结果中的论文标题和 arXiv ID 做二次校准，减少模型抽取造成的标题不规范、ID 缺失或命名不一致问题。

当前实现代码在：

- [backend/enrich_prior_work_analysis.py](/home/sunzongyuan/projects/VibeIDEA/VibeIDEA/backend/enrich_prior_work_analysis.py)

典型输入目录：

- [results/recommended_acl_aaai_top300_min7.65_prior_work](/home/sunzongyuan/projects/VibeIDEA/VibeIDEA/results/recommended_acl_aaai_top300_min7.65_prior_work)

推荐源 JSONL：

- [raw_paper/recommended_acl_aaai_top300_min7.65.jsonl](/home/sunzongyuan/projects/VibeIDEA/VibeIDEA/raw_paper/recommended_acl_aaai_top300_min7.65.jsonl)

## 2. 为什么需要这一步

prior work extraction 阶段输出的 `prior_work_analysis_*.json` 中，存在两类元信息质量问题：

### 2.1 目标论文层

目标论文通常已经有：

- `paper_title`
- `paper_arxiv_id`
- `paper_abstract`

但问题在于：

1. 有些论文不是 arXiv 来源，因此 `paper_arxiv_id = N/A`
2. 标题虽然大致正确，但可能不是 canonical 标题
3. 原始推荐 JSONL 里常常只有 `title / venue / year / url`，未必有 `doi`

### 2.2 prior works 层

`prior_works[*]` 中通常只有：

- `title`
- `authors`
- `year`
- `role`
- `relationship_sentence`
- `arxiv_id`

而这些字段很多是模型生成出来的，不保证与真实论文逐字一致，因此不能只做“精确标题匹配”。

## 3. 当前实现思路

脚本把校准分成两层。

### 3.1 目标论文层

函数：

- `enrich_target_paper()`

逻辑：

1. 先按归一化标题把目标论文映射回推荐源 JSONL
2. 从推荐源拿到 `title/year/authors/doi`
3. 优先尝试：
   - 已有 `paper_arxiv_id` 时直接查 arXiv
   - 有 `doi` 时先查 OpenAlex/Crossref
   - 没有 DOI 时按标题走 OpenAlex / arXiv title search / Crossref
4. 若命中置信度足够高，则：
   - 用 canonical title 覆盖 `paper_title`
   - 若找到了 arXiv ID，则回填 `paper_arxiv_id`

当前推荐 JSONL 中暂时没有 `doi` 字段，所以这一层现在主要依赖标题搜索；但脚本已经支持后续补 DOI。

### 3.2 prior works 层

函数：

- `enrich_prior_work()`

逻辑：

1. 如果 `prior_works[*].arxiv_id` 已存在，则直接查 arXiv，标题以 arXiv canonical title 为准
2. 如果没有 `arxiv_id`，则依次搜索：
   - OpenAlex
   - arXiv 标题搜索
   - Crossref
3. 对候选结果做重排
4. 只有分数超过阈值时才自动写回

## 4. 核心匹配与打分机制

### 4.1 归一化

函数：

- `normalize_title()`

作用：

1. 小写化
2. 去掉大部分标点
3. 合并多余空格

### 4.2 候选源

函数：

- `fetch_arxiv_metadata()`
- `search_arxiv_by_title()`
- `search_openalex()`
- `search_crossref()`
- `fetch_openalex_by_doi()`
- `fetch_crossref_by_doi()`

### 4.3 打分公式

函数：

- `score_candidate()`

当前分数构成为：

- 标题相似度: `0.75`
- 年份匹配: `0.15`
- 第一作者姓氏匹配: `0.10`

也就是：

```text
score = title_similarity * 0.75 + year_score * 0.15 + first_author_score * 0.10
```

其中：

- 年份完全一致记 `1.0`
- 年份相差 1 年记 `0.5`
- 第一作者姓氏一致记 `1.0`

### 4.4 默认阈值

CLI 默认值：

- `--target_threshold 0.78`
- `--prior_threshold 0.82`

解释：

1. 目标论文层输入元信息更干净，所以阈值可略低
2. prior works 层来自模型生成，错配风险更高，所以阈值更保守

## 5. 结构化日志与实时进度

这部分已经做了增强，目的是让后续人工复核更容易。

### 5.1 控制台实时输出

脚本每处理一个文件都会打印：

1. 当前进度 `[i/n]`
2. 当前文件名
3. 本文件总共应用了多少条更新
4. 每条记录的前后对比

示例输出：

```text
[1/2] Done prior_work_analysis_2302_11799.json | applied_updates=6/7 | output=...
  - target_paper: updated | title: 'A' -> 'A' | arxiv: '2302.11799' -> '2302.11799'
  - prior_work: updated | title: 'B' -> 'B canonical' | arxiv: '' -> '1811.00937'
```

### 5.2 JSONL 结构化日志

输出文件：

- `enrichment_log.jsonl`

每条日志包含：

- `level`: `target_paper` 或 `prior_work`
- `before`
- `after`
- `applied`
- `match`
- `file`

因此后续可以直接按这个日志做人工抽查，而不用 diff 整个 JSON 文件。

## 6. 如何运行

### 6.1 输出到新目录，保留原结果

```bash
cd /home/sunzongyuan/projects/VibeIDEA/VibeIDEA

mkdir -p results/recommended_acl_aaai_top300_min7.65_prior_work_enriched

python -u backend/enrich_prior_work_analysis.py \
  --input_dir results/recommended_acl_aaai_top300_min7.65_prior_work \
  --recommendation_jsonl raw_paper/recommended_acl_aaai_top300_min7.65.jsonl \
  --output_dir results/recommended_acl_aaai_top300_min7.65_prior_work_enriched \
  2>&1 | tee results/recommended_acl_aaai_top300_min7.65_prior_work_enriched.run.log
```

### 6.2 原地覆盖

```bash
cd /home/sunzongyuan/projects/VibeIDEA/VibeIDEA

python -u backend/enrich_prior_work_analysis.py \
  --input_dir results/recommended_acl_aaai_top300_min7.65_prior_work \
  --recommendation_jsonl raw_paper/recommended_acl_aaai_top300_min7.65.jsonl \
  --write_inplace \
  2>&1 | tee results/recommended_acl_aaai_top300_min7.65_prior_work_enrich_inplace.run.log
```

### 6.3 只做冒烟测试

```bash
cd /home/sunzongyuan/projects/VibeIDEA/VibeIDEA

python backend/enrich_prior_work_analysis.py \
  --input_dir results/recommended_acl_aaai_top300_min7.65_prior_work \
  --recommendation_jsonl raw_paper/recommended_acl_aaai_top300_min7.65.jsonl \
  --output_dir results/recommended_acl_aaai_top300_min7.65_prior_work_enriched_test \
  --limit 1
```

## 7. 当前验证结果

已经做过多次真实冒烟测试，结论如下：

### 7.1 可用性

脚本可以同时处理：

1. 按标题命名的 prior work JSON
2. 按 arXiv ID 命名的 prior work JSON

因为脚本扫描的是：

- `prior_work_analysis_*.json`

只要 JSON schema 一致，就能一起跑。

### 7.2 实际命中效果

已验证的典型修正包括：

1. 把 prior work 标题修正成更标准的 canonical title
2. 给缺失的 prior work 回填 arXiv ID
3. 对非 arXiv 论文，只修正标题，不乱填 arXiv ID

例如：

- `Think-on-Graph...` 回填为 `2307.07697`
- `G-Retriever...` 回填为 `2402.07630`
- `CommonsenseQA...` 回填为 `1811.00937`

## 8. 当前局限

### 8.1 推荐 JSONL 还没有 DOI

虽然脚本已经实现了 DOI 优先查 OpenAlex/Crossref，但当前输入 JSONL 没有 `doi` 字段，因此目标论文层还未完全发挥出最稳路径。

建议后续如果能从源数据补齐 DOI，目标论文层会更稳。

### 8.2 OpenAlex 可能返回非 arXiv DOI

某些论文能在 OpenAlex/Crossref 中找到标准标题，但没有 arXiv 版本，这时只能修正标题，`arxiv_id` 仍为空。

这属于正常情况，不应强行补 ID。

### 8.3 仍有少量错配风险

尤其是 prior works 层，因为输入本身来自模型生成。当前脚本已经通过阈值尽量保守，但以下情况仍要小心：

1. 标题很短
2. 标题高度通用
3. 作者字段不完整或格式混乱
4. 年份本身被模型抽错

因此建议对 `enrichment_log.jsonl` 做人工 spot check。

## 9. 后续可以继续做什么

### 9.1 把校准结果反写回推荐源 JSONL

当前脚本主要面向 `prior_work_analysis_*.json`。如果后续希望连推荐的 300 篇目标论文原始 JSONL 一并标准化，可以复用同样的匹配逻辑，单独写一个针对推荐源的 enrich 脚本。

### 9.2 给低置信度样本生成待审核清单

当前低于阈值的样本只是 `skipped`。下一步可以把这些样本单独输出为：

- `manual_review_candidates.jsonl`

便于人工检查。

### 9.3 同步更新 Markdown

当前校准脚本只处理 JSON。如果后续希望 Markdown 中展示的标题/arXiv ID 也同步更新，需要：

1. 读取 enrich 后的 JSON
2. 重新渲染 md

这一步当前还没有接入。

## 10. 快速接手建议

新接手的人建议按以下顺序理解：

1. 先看 `MatchResult`
2. 再看 `best_external_match()`
3. 再看 `enrich_target_paper()` 和 `enrich_prior_work()`
4. 最后看 `main()` 中的批量处理和日志输出

如果后续要迭代，最值得优先做的不是继续加更多数据源，而是：

1. 把低置信度样本导出成待审核列表
2. 把 enrich 后的 JSON 再自动同步渲染成 md
3. 如果推荐源补到 DOI，再重新跑一遍目标论文层校准
