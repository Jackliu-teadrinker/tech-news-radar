#!/usr/bin/env python3
"""Tech-broad relevance scoring for news records.

This module mirrors the API surface of ``ai_relevance`` so the rest of
update_news.py works unchanged:

- ``TECH_BROAD_RELEVANCE_FLOOR`` — loose gate for the "all" pool.
- ``add_tech_relevance_fields(record)`` — adds ``ai_is_related``/``ai_score``/
  ``ai_label``/... keeping legacy field names (UI reads ``ai_*``).
- ``score_tech_relevance`` — keyword scoring.

Scoring philosophy (per Jack's requirement): keep everything that is
plausibly tech — AI / chips / robots / semis / consumer hardware / software /
SaaS / cloud — in the main pool. The *strong-signal* gate (``ai_is_related``)
still drives the "curated" view, so the UI's curated mode stays high-signal.

Strong signals (bump to curated): AI model/agent news, major chip/semi
announcements (Nvidia/TSMC/Intel), robotics, launch/earnings of major tech
companies.
Weak-but-keep signals: general software, dev tooling, cloud, security,
open source, consumer devices.
Noise: entertainment/celebrity/sports/commerce/food/travel — pushed to the
all-pool floor but not up to curated.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

# ---- keyword sets ---------------------------------------------------------

TECH_CORE_KEYWORDS = [
    # AI / ML
    "ai", "a.i.", "aigc", "llm", "llms", "gpt", "claude", "gemini", "deepseek",
    "openai", "anthropic", "grok", "copilot", "codex", "mcp", "hugging face",
    "huggingface", "transformer", "prompt", "diffusion", "multimodal",
    "语言模型", "大模型", "人工智能", "机器学习", "深度学习", "智能体", "算力",
    "具身智能", "多模态", "推理", "微调", "开源模型",
    # chips / semis
    "nvidia", "tsmc", "intel", "amd", "npu", "gpu", "cuda", "fab",
    "chip", "chips", "semiconductor", "silicon", "asic", "euv", "hbm",
    "芯片", "半导体", "晶圆", "台积电", "英伟达", "英特尔", "黄仁勋", "光刻",
    # robotics
    "robot", "robots", "robotics", "embodied", "humanoid", "quadruped",
    "机器人", "具身", "人形", "四足", "灵巧手", "宇树", "figure",
    # dev / software / SaaS
    "developer", "developers", "sdk", "api", "open source", "open-source",
    "linux", "kernel", "android", "ios", "macos", "windows", "chrome",
    "firefox", "safari", "vulnerability", "exploit", "ransomware",
    "cloud", "kubernetes", "docker", "serverless", "edge computing",
    "database", "frontend", "backend", "fullstack", "low-code",
    "编程", "代码", "软件", "开源", "沙箱", "服务器", "数据库", "漏洞",
    # hardware / devices
    "iphone", "ipad", "macbook", "iphone", "pixel", "galaxy", "playstation",
    "xbox", "switch", "nintendo", "samsung", "apple", "tesla", "robotaxi",
    "autonomous", "self-driving", "drones", "drone", "satellite", "starlink",
    "手机", "平板", "笔记本", "智能眼镜", "可穿戴", "无人机", "卫星",
    "自动驾驶", "robotaxi",
    # cloud / infra / dev-ops
    "aws", "azure", "gcp", "google cloud", "kubernetes", "terraform",
    "ci/cd", "monitoring", "observability", "llmops", "mlops",
    "aws", "微软", "亚马逊", "谷歌", "meta", "字节跳动", "阿里", "百度",
]

STRONG_TECH_SIGNALS = [
    "nvidia", "tsmc", "intel", "semiconductor", "芯片", "半导体", "晶圆",
    "台积电", "英伟达", "光刻", "humanoid", "人形", "机器人", "具身",
    "openai", "anthropic", "deepseek", "gemini", "claude", "gpt",
    "大模型", "人工智能", "llm", "agent", "robotics", "tesla", "自动驾驶",
    "robotaxi", "self-driving", "iphone", "macbook", "pixel", "galaxy",
]

NOISE_KEYWORDS = [
    "娱乐", "明星", "八卦", "足球", "篮球", "彩票", "情感", "旅游", "美食",
    "美食", "综艺", "选秀", "追星", "cosplay",
]

COMMERCE_NOISE_KEYWORDS = [
    "淘宝", "天猫", "京东", "拼多多", "券后", "热销总榜", "促销", "优惠",
    "补贴", "下单", "首发价", "包邮",
]

FINANCE_NOISE_KEYWORDS = [
    "etf", "股票", "etf", "股价", "涨停", "跌停", "a股", "港股通", "北向资金",
]

UNSAFE_HARD_PATTERNS = [
    re.compile(r"\bcreampie\b", re.I),
    re.compile(r"\bblowjob\b", re.I),
    re.compile(r"suck (?:your|my) (?:dick|cock)", re.I),
    re.compile(r"中出|婊子|吸你的鸡鸡|操虚拟女友", re.I),
]

UNSAFE_PROMO_PATTERNS = [
    re.compile(r"\b(?:nsfw|nudes?|porn(?:ography)?)\b", re.I),
    re.compile(r"\buncensored pictures?\b", re.I),
    re.compile(r"未经审查的图片|虚拟女友|色情内容|成人内容", re.I),
]

TECH_BROAD_RELEVANCE_FLOOR = 0.25
TECH_CURATED_THRESHOLD = 0.55

SOURCE_PRIORS = {
    "official_ai": 0.35,
    "curated_media": 0.18,
    "aibase": 0.45,
    "aihot": 0.45,
    "aihubtoday": 0.45,
    "followbuilders": 0.25,
    "opmlrss": 0.15,
    "xapi": 0.15,
    "socialdata_x": 0.15,
    "hackernews": 0.15,
    "techurls": 0.10,
    "buzzing": 0.10,
    "zeli": 0.05,
    "newsnow": 0.05,
    "waytoagi": 0.10,
    "aibreakfast": 0.10,
    "iris": 0.05,
    "bestblogs": 0.10,
}
AI_DEFAULT_SOURCES = {"aibase", "aihot", "aihubtoday"}

LABEL_KEYWORDS = [
    ("ai_model", ["model", "gpt", "claude", "gemini", "deepseek", "llm", "模型", "大模型", "发布", "release", "agent", "智能体"]),
    ("chip_semi", ["chip", "chips", "semiconductor", "gpu", "npu", "cuda", "nvidia", "tsmc", "intel", "fab", "hbm", "芯片", "半导体", "晶圆", "光刻", "台积电", "英伟达"]),
    ("robotics", ["robot", "robotics", "embodied", "humanoid", "quadruped", "机器人", "具身", "人形", "四足", "灵巧手", "宇树", "figure"]),
    ("dev_tool", ["developer", "sdk", "api", "mcp", "copilot", "codex", "cursor", "github", "编程", "代码", "sdk", "api", "开发者", "开源"]),
    ("software_saas", ["software", "saas", "app", "linux", "kernel", "android", "ios", "chrome", "firefox", "vulnerability", "exploit", "cloud", "kubernetes", "docker", "aws", "azure", "gcp", "软件", "漏洞", "数据库", "服务器", "开源"]),
    ("consumer_hw", ["iphone", "ipad", "macbook", "pixel", "galaxy", "playstation", "xbox", "switch", "nintendo", "samsung", "apple", "手机", "平板", "笔记本", "智能眼镜", "可穿戴", "无人机", "卫星", "自动驾驶", "robotaxi"]),
    ("ai_product", ["openai", "anthropic", "google", "meta", "perplexity", "产品", "上线", "更新", "发布"]),
    ("industry_business", ["funding", "acquire", "ipo", "merger", "revenue", "valuation", "融资", "收购", "估值", "营收", "ipo", "公司"]),
    ("infra_compute", ["gpu", "npu", "cuda", "data center", "数据中心", "算力", "推理", "集群", "服务器"]),
]


# ---- helpers -------------------------------------------------------------

def contains_any_keyword(haystack: str, keywords: list[str]) -> bool:
    h = haystack.lower()
    return any(k in h for k in keywords)


def matched_keywords(haystack: str, keywords: list[str]) -> list[str]:
    h = haystack.lower()
    return sorted({k for k in keywords if k in h})


def contains_unsafe_promotional_content(text: str) -> bool:
    if any(p.search(text) for p in UNSAFE_HARD_PATTERNS):
        return True
    return sum(bool(p.search(text)) for p in UNSAFE_PROMO_PATTERNS) >= 2


def _label_for_text(text: str) -> str:
    for label, keywords in LABEL_KEYWORDS:
        if contains_any_keyword(text, keywords):
            return label
    return "tech_general"


def _result(*, is_tech: bool, score: float, label: str, reason: str,
            signals: list[str] | None = None, noise: list[str] | None = None) -> dict[str, Any]:
    return {
        "is_ai_related": bool(is_tech),
        "score": round(max(0.0, min(1.0, score)), 2),
        "label": label,
        "reason": reason,
        "signals": signals or [],
        "noise": noise or [],
    }


def score_tech_relevance(record: dict[str, Any]) -> dict[str, Any]:
    """Tech-broad relevance score. Returns a dict with legacy ``ai_*`` keys
    (``is_ai_related``, ``score``, ``label``) so the rest of the codebase keeps
    working unchanged."""
    site_id = str(record.get("site_id") or "")
    title = str(record.get("title") or "")
    source = str(record.get("source") or "")
    site_name = str(record.get("site_name") or "")
    url = str(record.get("url") or "")
    try:
        url_host = (urlparse(url).netloc or "").lower()
    except Exception:
        url_host = ""
    text = f"{title} {source} {site_name} {url_host}".lower()

    tech_signals = matched_keywords(text, TECH_CORE_KEYWORDS)
    strong_signals = matched_keywords(text, STRONG_TECH_SIGNALS)
    noise = matched_keywords(text, NOISE_KEYWORDS + COMMERCE_NOISE_KEYWORDS + FINANCE_NOISE_KEYWORDS)
    source_prior = SOURCE_PRIORS.get(site_id, 0.0)

    if contains_unsafe_promotional_content(text):
        return _result(is_tech=False, score=0.0, label="unsafe_content",
                       reason="unsafe_promotional_content", signals=[],
                       noise=["unsafe_promotional_content"])

    if site_id in AI_DEFAULT_SOURCES:
        # trusted AI/tech aggregators: keep everything they surface, but the
        # "curated" gate only if we also see a strong tech signal in the title.
        base = 0.55 + source_prior
        is_curated = bool(strong_signals)
        return _result(is_tech=is_curated, score=min(0.95, base),
                       label=_label_for_text(text),
                       reason="trusted_tech_source" + ("+strong" if is_curated else ""),
                       signals=tech_signals[:8], noise=noise)

    has_strong = bool(strong_signals)
    has_tech = bool(tech_signals)

    # Hard drops: noise or commerce without any tech signal.
    if noise and not has_strong and not has_tech:
        return _result(is_tech=False, score=0.15 + source_prior,
                       label="noise_or_commerce",
                       reason="noise_without_tech_signal",
                       signals=[], noise=noise)

    score = source_prior
    if has_strong:
        score += 0.55
    elif has_tech:
        score += 0.35
    score += min(0.15, 0.03 * len(tech_signals))
    score += min(0.10, 0.02 * len(strong_signals))
    if noise:
        score -= min(0.18, 0.04 * len(noise))

    # Floor: any tech signal keeps the item in the all-pool.
    if has_tech or has_strong:
        score = max(score, TECH_BROAD_RELEVANCE_FLOOR)

    # Curated gate: strong tech signal OR very-high score.
    is_curated = has_strong or score >= TECH_CURATED_THRESHOLD

    label = _label_for_text(text) if has_strong or has_tech else "tech_general"
    reason = "matched_strong_tech_signal" if has_strong else (
        "matched_tech_signal" if has_tech else "weak_tech_signal")
    return _result(is_tech=is_curated, score=score, label=label,
                   reason=reason, signals=tech_signals[:10], noise=noise)


def is_tech_related_record(record: dict[str, Any]) -> bool:
    return bool(score_tech_relevance(record)["is_ai_related"])


def is_broadly_tech_related(record: dict[str, Any]) -> bool:
    """Loose gate for the all-pool. Returns True when any tech signal is
    present OR the source prior is high enough (e.g. curated_media with
    AI-specific sources)."""
    score = score_tech_relevance(record)["score"]
    return score >= TECH_BROAD_RELEVANCE_FLOOR


def add_tech_relevance_fields(record: dict[str, Any]) -> dict[str, Any]:
    """Add legacy ``ai_*`` fields populated from the tech-broad scorer.
    Field names stay ``ai_*`` so app.js / persona_score.py /
    backtest_scoring.py keep working without changes."""
    relevance = score_tech_relevance(record)
    out = dict(record)
    out["ai_is_related"] = relevance["is_ai_related"]
    out["ai_score"] = relevance["score"]
    out["ai_label"] = relevance["label"]
    out["ai_relevance_reason"] = relevance["reason"]
    out["ai_signals"] = relevance["signals"]
    out["ai_noise"] = relevance["noise"]
    out["tech_is_related"] = relevance["is_ai_related"]
    out["tech_score"] = relevance["score"]
    out["tech_label"] = relevance["label"]
    return out


# ---- legacy API compatibility --------------------------------------------

# update_news.py imports these names from ai_relevance; we mirror them so
# callers can import from either module without code changes.
AI_BROAD_RELEVANCE_FLOOR = TECH_BROAD_RELEVANCE_FLOOR
add_ai_relevance_fields = add_tech_relevance_fields
is_broadly_ai_related = is_broadly_tech_related
score_ai_relevance = score_tech_relevance
is_ai_related_record = is_tech_related_record
