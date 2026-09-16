#!/usr/bin/env python3
"""Sector classification for news items.

Uses the 8-sector map in sector_config.py to tag each item with:
- sector: the primary sector id (or "" if no sector matched)
- sector_hits: list of {sector_id, matched_keywords, score} for all sectors
  that matched, sorted by score desc — the UI can show "also relates to X"

Scoring: per-sector, count keyword hits in title+source+url, weight by
keyword length (longer/more-specific keywords score higher), and add a small
bonus if the hit is in the title vs just the URL/source.
"""

from __future__ import annotations

import re
from typing import Any

from sector_config import SECTOR_ORDER, get_keywords_for, SECTOR_BY_ID


def _haystacks(record: dict[str, Any]) -> tuple[str, str, str]:
    """Return (title_lower, source_lower, url_lower) for matching."""
    title = str(record.get("title") or record.get("title_zh") or record.get("title_en") or "").lower()
    source = str(record.get("source") or record.get("site_name") or "").lower()
    url = str(record.get("url") or "").lower()
    return title, source, url


def _score_sector(sector_id: str, title: str, source: str, url: str,
                  kw_lists: dict[str, list[str]]) -> tuple[float, list[str]]:
    """Return (score, matched_keywords) for one sector."""
    keywords = kw_lists.get(sector_id, [])
    if not keywords:
        return 0.0, []

    # Pre-compile: check each keyword against the three haystacks.
    # Longer keywords are more specific → higher weight.
    matched: list[str] = []
    score = 0.0
    for kw in keywords:
        if len(kw) < 2:
            continue  # skip single-char keywords — too noisy
        hit_title = kw in title
        hit_source = kw in source
        hit_url = kw in url
        if not (hit_title or hit_source or hit_url):
            continue
        matched.append(kw)
        # Weight: title hit = 1.0, source hit = 0.4, url-only hit = 0.2
        if hit_title:
            weight = 1.0
        elif hit_source:
            weight = 0.4
        else:
            weight = 0.2
        # Specificity bonus: longer keywords (company names, tech terms)
        # count more than short generic ones.
        specificity = min(1.0, len(kw) / 8.0)
        score += weight * (0.5 + specificity * 0.5)

    # Require at least 2 keyword hits for a sector to be "assigned"
    # (avoids a single generic word like "agent" matching ai_apps).
    if len(matched) < 2 and score < 1.2:
        return 0.0, matched

    return score, matched


def classify_sectors(record: dict[str, Any]) -> dict[str, Any]:
    """Tag a record with sector classification. Mutates and returns record."""
    title, source, url = _haystacks(record)
    if not title and not source:
        record["sector"] = ""
        record["sector_hits"] = []
        return record

    # Build keyword lists once
    kw_lists = get_keywords_for_all()

    hits: list[dict[str, Any]] = []
    for sector_id in SECTOR_ORDER:
        score, matched = _score_sector(sector_id, title, source, url, kw_lists)
        if score > 0:
            hits.append({
                "sector_id": sector_id,
                "score": round(score, 2),
                "matched_keywords": matched[:12],  # cap display
            })

    hits.sort(key=lambda h: h["score"], reverse=True)
    primary = hits[0]["sector_id"] if hits else ""

    record["sector"] = primary
    record["sector_hits"] = hits

    return record


# Cache keyword lists globally (rebuilt on import)
_KW_CACHE: dict[str, list[str]] | None = None


def get_keywords_for_all() -> dict[str, list[str]]:
    global _KW_CACHE
    if _KW_CACHE is None:
        from sector_config import get_all_keywords
        _KW_CACHE = get_all_keywords()
    return _KW_CACHE


def sector_meta_payload() -> list[dict]:
    """Lightweight sector metadata for UI (id, name, aliases, points)."""
    from sector_config import sector_display_meta
    return sector_display_meta()


def filter_by_sector(items: list[dict[str, Any]], sector_id: str) -> list[dict[str, Any]]:
    """Return items whose primary sector matches, OR whose sector_hits include
    the target sector with a meaningful score (>= 1.0)."""
    out = []
    for item in items:
        if item.get("sector") == sector_id:
            out.append(item)
            continue
        for hit in item.get("sector_hits", []):
            if hit["sector_id"] == sector_id and hit.get("score", 0) >= 1.0:
                out.append(item)
                break
    return out


def sector_stats(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Count items per sector (primary assignment only)."""
    counts: dict[str, int] = {sid: 0 for sid in SECTOR_ORDER}
    for item in items:
        s = item.get("sector") or ""
        if s in counts:
            counts[s] += 1
    out = []
    for sid in SECTOR_ORDER:
        meta = SECTOR_BY_ID.get(sid, {})
        out.append({
            "sector_id": sid,
            "name": meta.get("name", sid),
            "count": counts.get(sid, 0),
        })
    return out
