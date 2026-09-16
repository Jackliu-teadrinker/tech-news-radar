#!/usr/bin/env python3
"""Direction + company classification for news items.

Each item is tagged with:
- direction: primary direction id (one of the 10) or "" if no match
- direction_hits: all matched directions [{direction_id, score, matched_keywords}]
- companies: list of matched company names (dedup, display casing)

Scoring: per direction, count keyword hits weighted by haystack (title > source > url)
and keyword specificity. Companies are matched by lower-cased substring in
title/source/url — a company hit also counts as a +1 toward its parent direction's
score (so a "寒武纪" item lands in compute_dc reliably).
"""

from __future__ import annotations

from typing import Any

from sector_config import (
    DIRECTION_ORDER,
    DIRECTION_BY_ID,
    get_company_keywords,
    get_direction_keywords,
)


def _haystacks(record: dict[str, Any]) -> tuple[str, str, str]:
    title = str(record.get("title") or record.get("title_zh") or record.get("title_en") or "").lower()
    source = str(record.get("source") or record.get("site_name") or "").lower()
    url = str(record.get("url") or "").lower()
    return title, source, url


_KW_CACHE: dict[str, list[str]] | None = None
_COMPANY_CACHE: dict[str, list[str]] | None = None


def _kw() -> dict[str, list[str]]:
    global _KW_CACHE
    if _KW_CACHE is None:
        _KW_CACHE = get_direction_keywords()
    return _KW_CACHE


def _companies() -> dict[str, list[str]]:
    global _COMPANY_CACHE
    if _COMPANY_CACHE is None:
        _COMPANY_CACHE = get_company_keywords()
    return _COMPANY_CACHE


def _score_direction(direction_id: str, title: str, source: str, url: str,
                     kw_lists: dict[str, list[str]]) -> tuple[float, list[str]]:
    keywords = kw_lists.get(direction_id, [])
    if not keywords:
        return 0.0, []

    matched: list[str] = []
    score = 0.0
    for kw in keywords:
        if len(kw) < 2:
            continue
        hit_title = kw in title
        hit_source = kw in source
        hit_url = kw in url
        if not (hit_title or hit_source or hit_url):
            continue
        matched.append(kw)
        if hit_title:
            weight = 1.0
        elif hit_source:
            weight = 0.4
        else:
            weight = 0.2
        specificity = min(1.0, len(kw) / 8.0)
        score += weight * (0.5 + specificity * 0.5)

    # Require at least 2 keyword hits, OR a very strong single title hit.
    if len(matched) < 2 and score < 1.2:
        return 0.0, matched

    return score, matched


def _match_companies(title: str, source: str, url: str) -> list[str]:
    """Return matched company display names (deduped, original casing)."""
    com = _companies()
    haystack = f"{title} {source} {url}"
    found: list[str] = []
    seen: set[str] = set()
    for lc_key in sorted(com.keys(), key=len, reverse=True):
        if lc_key not in haystack:
            continue
        display = com[lc_key][0]
        # Skip if a longer matched company already contains this one.
        if any(display.lower() in existing.lower() for existing in found if existing.lower() != display.lower()):
            continue
        if display.lower() not in seen:
            seen.add(display.lower())
            found.append(display)
    return found


def classify_directions(record: dict[str, Any]) -> dict[str, Any]:
    """Tag a record with direction + companies classification. Mutates record.

    Scoring model (v2):
    - Each direction scores on its own keyword list only.
    - A company hit boosts ONLY the directions whose own company list
      contains that company (a company's news belongs to its home directions).
    - This prevents "宁德时代" from leaking into compute_dc / autonomous_vehicle.
    """
    title, source, url = _haystacks(record)
    if not title and not source:
        record["direction"] = ""
        record["direction_hits"] = []
        record["companies"] = []
        return record

    kw_lists = _kw()
    company_hits = _match_companies(title, source, url)

    hits: list[dict[str, Any]] = []
    for direction_id in DIRECTION_ORDER:
        score, matched = _score_direction(direction_id, title, source, url, kw_lists)
        # Only count companies that belong to THIS direction's company list.
        direction_companies = [
            c.lower() for c in DIRECTION_BY_ID.get(direction_id, {}).get("companies", [])
        ]
        direction_company_hits = [c for c in company_hits if c.lower() in direction_companies]
        if direction_company_hits:
            score += 0.6 + 0.15 * min(len(direction_company_hits), 3)
            matched = matched + [c.lower() for c in direction_company_hits]
        elif not matched and company_hits:
            # Pure company-only item with no keyword match in this direction:
            # don't grant a baseline here — the company's own directions will
            # pick it up with the 0.6 boost. Avoids cross-direction leakage.
            pass

        if score > 0:
            hits.append({
                "direction_id": direction_id,
                "score": round(min(score, 5.0), 2),
                "matched_keywords": matched[:12],
                "companies": direction_company_hits[:8],
            })

    hits.sort(key=lambda h: h["score"], reverse=True)
    primary = hits[0]["direction_id"] if hits else ""

    record["direction"] = primary
    record["direction_hits"] = hits
    record["companies"] = company_hits

    return record


# Back-compat aliases (older code / tests import these names)
classify_sectors = classify_directions


def direction_stats(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Count items per direction (primary assignment only)."""
    counts: dict[str, int] = {did: 0 for did in DIRECTION_ORDER}
    for item in items:
        d = item.get("direction") or ""
        if d in counts:
            counts[d] += 1
    out = []
    from sector_config import DIRECTION_BY_ID
    for did in DIRECTION_ORDER:
        meta = DIRECTION_BY_ID.get(did, {})
        out.append({
            "direction_id": did,
            "name": meta.get("name", did),
            "count": counts.get(did, 0),
        })
    return out


def filter_by_direction(items: list[dict[str, Any]], direction_id: str) -> list[dict[str, Any]]:
    out = []
    for item in items:
        if item.get("direction") == direction_id:
            out.append(item)
            continue
        for hit in item.get("direction_hits", []):
            if hit["direction_id"] == direction_id and hit.get("score", 0) >= 1.0:
                out.append(item)
                break
    return out


def filter_by_company(items: list[dict[str, Any]], company: str) -> list[dict[str, Any]]:
    lc = company.lower()
    out = []
    for item in items:
        for c in item.get("companies", []):
            if c.lower() == lc or lc in c.lower():
                out.append(item)
                break
    return out


def direction_meta_payload() -> list[dict]:
    from sector_config import direction_meta_payload as _f
    return _f()


def framework_layers_payload() -> list[dict]:
    from sector_config import framework_layers_payload as _f
    return _f()
