import numpy as np
from .paper import ArxivPaper
from datetime import datetime
from loguru import logger

def rerank_paper(candidate: list[ArxivPaper], corpus: list[dict], model: str = "avsolatorio/GIST-small-Embedding-v0") -> list[ArxivPaper]:
    try:
        from sentence_transformers import SentenceTransformer
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        encoder = SentenceTransformer(model, device=device)
    except Exception as e:
        logger.warning(f"推荐模型加载失败，将使用原始顺序: {e}")
        for c in candidate:
            if c.score is None:
                c.score = 0.0
        return candidate

    try:
        # sort corpus by date, from newest to oldest
        corpus = sorted(
            corpus,
            key=lambda x: datetime.strptime(x["data"]["dateAdded"], "%Y-%m-%dT%H:%M:%SZ"),
            reverse=True,
        )
        time_decay_weight = 1 / (1 + np.log10(np.arange(len(corpus)) + 1))
        time_decay_weight = time_decay_weight / time_decay_weight.sum()
        corpus_feature = encoder.encode([p["data"]["abstractNote"] for p in corpus])
        candidate_feature = encoder.encode([p.summary for p in candidate])
        sim = encoder.similarity(candidate_feature, corpus_feature)
        scores = (sim * time_decay_weight).sum(axis=1) * 10
        for s, c in zip(scores, candidate):
            c.score = s.item()
        return sorted(candidate, key=lambda x: x.score, reverse=True)
    except Exception as e:
        logger.warning(f"重排序失败，将使用原始顺序: {e}")
        for c in candidate:
            if c.score is None:
                c.score = 0.0
        return candidate